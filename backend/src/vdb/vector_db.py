"""
Vector Database module using FAISS
Manages document embeddings for semantic search
"""
import os
import pickle
import numpy as np
import faiss
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class VectorDatabase:
    """
    Vector Database using FAISS for semantic search
    Stores document embeddings and enables similarity search
    """
    
    def __init__(self):
        """Initialize the vector database"""
        self.model = None
        self.index = None
        self.documents = []  # Store original documents with metadata
        self.initialized = False
        
        try:
            # Load embedding model
            logger.info(f"Loading embedding model: {settings.embedding_model}")
            self.model = SentenceTransformer(settings.embedding_model)
            
            # Initialize or load FAISS index
            if os.path.exists(settings.faiss_index_path):
                self.load_index()
            else:
                self.initialize_index()
                
            self.initialized = True
            logger.info("Vector database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize vector database: {e}")
    
    def initialize_index(self):
        """Initialize a new FAISS index"""
        self.index = faiss.IndexFlatL2(settings.embedding_dimension)
        self.documents = []
        logger.info("Created new FAISS index")
    
    def add_documents(self, texts: List[str], metadata: List[Dict[str, Any]] = None):
        """
        Add documents to the vector database
        
        Args:
            texts: List of text documents to add
            metadata: Optional list of metadata dicts for each document
        """
        if not self.initialized:
            logger.warning("Vector database not initialized")
            return
        
        if not texts:
            return
        
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(texts)} documents")
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        
        # Normalize embeddings for cosine similarity (optional but recommended)
        embeddings = embeddings.astype('float32')
        faiss.normalize_L2(embeddings)
        
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Store documents with metadata
        if metadata is None:
            metadata = [{} for _ in texts]
        
        for i, text in enumerate(texts):
            self.documents.append({
                "id": len(self.documents),
                "text": text,
                "metadata": metadata[i]
            })
        
        logger.info(f"Added {len(texts)} documents. Total: {len(self.documents)}")
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents using semantic similarity
        
        Args:
            query: Query text
            k: Number of results to return
        
        Returns:
            List of documents with similarity scores
        """
        if not self.initialized or self.index.ntotal == 0:
            logger.warning("No documents in vector database")
            return []
        
        # Generate query embedding
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        query_embedding = query_embedding.astype('float32')
        faiss.normalize_L2(query_embedding)
        
        # Search
        k = min(k, self.index.ntotal)  # Don't search for more than we have
        distances, indices = self.index.search(query_embedding, k)
        
        # Format results
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.documents):
                doc = self.documents[idx].copy()
                # Convert L2 distance to similarity score (0-1, higher is better)
                doc["score"] = float(1 / (1 + dist))
                doc["rank"] = i + 1
                results.append(doc)
        
        return results
    
    def save_index(self, path: str = None):
        """
        Save the FAISS index and documents to disk
        
        Args:
            path: Optional custom path (uses settings.faiss_index_path by default)
        """
        if not self.initialized:
            logger.warning("Cannot save uninitialized index")
            return
        
        path = path or settings.faiss_index_path
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, path)
        
        # Save documents metadata
        docs_path = path.replace('.index', '_docs.pkl')
        with open(docs_path, 'wb') as f:
            pickle.dump(self.documents, f)
        
        logger.info(f"Saved index to {path}")
    
    def load_index(self, path: str = None):
        """
        Load the FAISS index and documents from disk
        
        Args:
            path: Optional custom path (uses settings.faiss_index_path by default)
        """
        path = path or settings.faiss_index_path
        
        if not os.path.exists(path):
            logger.warning(f"Index file not found: {path}")
            self.initialize_index()
            return
        
        # Load FAISS index
        self.index = faiss.read_index(path)
        
        # Load documents metadata
        docs_path = path.replace('.index', '_docs.pkl')
        if os.path.exists(docs_path):
            with open(docs_path, 'rb') as f:
                self.documents = pickle.load(f)
        else:
            logger.warning(f"Documents file not found: {docs_path}")
            self.documents = []
        
        logger.info(f"Loaded index with {self.index.ntotal} vectors and {len(self.documents)} documents")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get vector database statistics"""
        return {
            "initialized": self.initialized,
            "total_documents": len(self.documents),
            "index_size": self.index.ntotal if self.index else 0,
            "embedding_dimension": settings.embedding_dimension,
            "model": settings.embedding_model
        }


# Global VDB instance
vdb = VectorDatabase()
