"""
RAG (Retrieval-Augmented Generation) module
Combines retrieval with LLM generation for medical Q&A
"""
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from config.settings import settings
from src.vdb import vdb
from src.kg import kg
import logging

logger = logging.getLogger(__name__)


class RAGSystem:
    """
    RAG System for medical question answering
    Retrieves relevant context and generates answers using Gemini
    """
    
    def __init__(self):
        """Initialize the RAG system"""
        self.initialized = False
        
        # Configure Gemini
        if settings.gemini_api_key:
            try:
                genai.configure(api_key=settings.gemini_api_key)
                self.model = genai.GenerativeModel(settings.gemini_model)
                self.initialized = True
                logger.info("RAG system initialized with Gemini")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
        else:
            logger.warning("No Gemini API key provided. RAG system will use retrieval only.")
    
    def retrieve_context(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context for a query
        
        Args:
            query: User's question
            top_k: Number of documents to retrieve
        
        Returns:
            List of relevant documents with scores
        """
        top_k = top_k or settings.top_k_retrieval
        
        # Search vector database
        results = vdb.search(query, k=top_k)
        
        logger.info(f"Retrieved {len(results)} documents for query: {query[:50]}...")
        return results
    
    def expand_query_with_kg(self, query: str) -> str:
        """
        Expand query using knowledge graph entities
        
        Args:
            query: Original query
        
        Returns:
            Expanded query with related entities
        """
        # Search for entities mentioned in the query
        entities = kg.search_entities(query, limit=5)
        
        if not entities:
            return query
        
        # Add related entity names to expand the query
        related_terms = [e["name"] for e in entities[:3]]
        expanded = query
        
        if related_terms:
            expanded += " " + " ".join(related_terms)
            logger.info(f"Expanded query with KG entities: {related_terms}")
        
        return expanded
    
    def generate_answer(self, query: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate an answer using retrieved context and Gemini
        
        Args:
            query: User's question
            context_docs: Retrieved context documents
        
        Returns:
            Dictionary with answer and metadata
        """
        if not context_docs:
            return {
                "answer": "I couldn't find relevant information to answer your question. Please try rephrasing or ask a different medical question.",
                "sources": [],
                "confidence": 0.0
            }
        
        # Build context from retrieved documents
        context_text = "\n\n".join([
            f"Source {i+1}: {doc['text']}"
            for i, doc in enumerate(context_docs[:5])
        ])
        
        # If Gemini is not available, return a simple answer
        if not self.initialized:
            return {
                "answer": f"Based on the retrieved information:\n\n{context_docs[0]['text'][:300]}...",
                "sources": context_docs,
                "confidence": 0.5,
                "note": "Using retrieval only (no LLM generation)"
            }
        
        # Create prompt for Gemini
        prompt = f"""You are a helpful medical information assistant. Based on the provided medical context, answer the user's question.

Important guidelines:
- ONLY use information from the provided context
- Cite sources using [Source X] notation
- If information is insufficient, say so clearly
- Include medical disclaimers when appropriate
- Be precise and factual

Context:
{context_text}

Question: {query}

Answer (be concise and cite sources):"""
        
        try:
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=settings.max_answer_length,
                )
            )
            
            answer = response.text
            
            # Add medical disclaimer
            disclaimer = "\n\n⚠️ Medical Disclaimer: This information is for educational purposes only. Always consult healthcare professionals for medical advice."
            
            return {
                "answer": answer + disclaimer,
                "sources": context_docs,
                "confidence": self._calculate_confidence(context_docs),
                "model": settings.gemini_model
            }
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return {
                "answer": f"Error generating answer. Based on retrieved context: {context_docs[0]['text'][:200]}...",
                "sources": context_docs,
                "confidence": 0.3,
                "error": str(e)
            }
    
    def _calculate_confidence(self, context_docs: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence score based on retrieval quality
        
        Args:
            context_docs: Retrieved documents
        
        Returns:
            Confidence score between 0 and 1
        """
        if not context_docs:
            return 0.0
        
        # Use average score of top documents
        scores = [doc.get("score", 0.5) for doc in context_docs[:3]]
        avg_score = sum(scores) / len(scores) if scores else 0.5
        
        # Adjust based on number of documents
        doc_factor = min(len(context_docs) / settings.top_k_retrieval, 1.0)
        
        confidence = avg_score * 0.7 + doc_factor * 0.3
        return round(confidence, 2)
    
    def answer_question(self, query: str, use_kg: bool = True, top_k: int = None) -> Dict[str, Any]:
        """
        Main method to answer a medical question using RAG
        
        Args:
            query: User's question
            use_kg: Whether to use knowledge graph for query expansion
            top_k: Number of documents to retrieve
        
        Returns:
            Complete answer with sources and metadata
        """
        logger.info(f"Processing question: {query}")
        
        # Optionally expand query with KG
        search_query = query
        if use_kg and kg.connected:
            search_query = self.expand_query_with_kg(query)
        
        # Retrieve relevant context
        context_docs = self.retrieve_context(search_query, top_k)
        
        # Generate answer
        result = self.generate_answer(query, context_docs)
        
        # Add processing metadata
        result["query"] = query
        result["expanded_query"] = search_query if search_query != query else None
        result["retrieved_docs"] = len(context_docs)
        
        return result


# Global RAG instance
rag = RAGSystem()
