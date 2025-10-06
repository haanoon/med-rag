"""
FastAPI application for Medical RAG System
Provides REST API endpoints for medical Q&A
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from config.settings import settings
from src.rag import rag
from src.vdb import vdb
from src.kg import kg
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="Medical RAG System API for intelligent medical question answering"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class QuestionRequest(BaseModel):
    """Request model for asking a question"""
    question: str = Field(..., description="The medical question to answer", min_length=1)
    top_k: Optional[int] = Field(None, description="Number of documents to retrieve", ge=1, le=20)
    use_kg: Optional[bool] = Field(True, description="Whether to use knowledge graph expansion")


class Source(BaseModel):
    """Source document model"""
    id: int
    text: str
    score: float
    metadata: Dict[str, Any]


class AnswerResponse(BaseModel):
    """Response model for answers"""
    answer: str
    sources: List[Source]
    confidence: float
    query: str
    expanded_query: Optional[str]
    retrieved_docs: int
    model: Optional[str]
    note: Optional[str]
    error: Optional[str]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    vdb_status: Dict[str, Any]
    kg_status: Dict[str, Any]
    rag_initialized: bool


# API Endpoints

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "Medical RAG API",
        "version": settings.api_version,
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    Returns status of all system components
    """
    return HealthResponse(
        status="healthy",
        vdb_status=vdb.get_statistics(),
        kg_status=kg.get_statistics(),
        rag_initialized=rag.initialized
    )


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Answer a medical question using RAG
    
    Args:
        request: Question request with query and optional parameters
    
    Returns:
        Answer with sources and metadata
    """
    try:
        logger.info(f"Received question: {request.question}")
        
        # Process question using RAG system
        result = rag.answer_question(
            query=request.question,
            use_kg=request.use_kg,
            top_k=request.top_k
        )
        
        # Format sources for response
        sources = [
            Source(
                id=doc["id"],
                text=doc["text"],
                score=doc.get("score", 0.0),
                metadata=doc.get("metadata", {})
            )
            for doc in result["sources"]
        ]
        
        return AnswerResponse(
            answer=result["answer"],
            sources=sources,
            confidence=result["confidence"],
            query=result["query"],
            expanded_query=result.get("expanded_query"),
            retrieved_docs=result["retrieved_docs"],
            model=result.get("model"),
            note=result.get("note"),
            error=result.get("error")
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search", response_model=List[Source])
async def search_documents(query: str, k: int = 5):
    """
    Search for relevant documents
    
    Args:
        query: Search query
        k: Number of results to return
    
    Returns:
        List of relevant documents
    """
    try:
        results = vdb.search(query, k=k)
        
        return [
            Source(
                id=doc["id"],
                text=doc["text"],
                score=doc.get("score", 0.0),
                metadata=doc.get("metadata", {})
            )
            for doc in results
        ]
        
    except Exception as e:
        logger.error(f"Error searching documents: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/kg/search")
async def search_kg_entities(query: str, limit: int = 10):
    """
    Search for entities in the knowledge graph
    
    Args:
        query: Search query
        limit: Maximum number of results
    
    Returns:
        List of matching entities
    """
    try:
        if not kg.connected:
            raise HTTPException(status_code=503, detail="Knowledge graph not available")
        
        results = kg.search_entities(query, limit=limit)
        return {"entities": results}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching KG: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/kg/entity/{entity_id}")
async def get_related_entities(entity_id: str, entity_type: str = "Disease", max_hops: int = 1):
    """
    Get entities related to a specific entity
    
    Args:
        entity_id: ID of the entity
        entity_type: Type of the entity
        max_hops: Maximum relationship hops
    
    Returns:
        List of related entities
    """
    try:
        if not kg.connected:
            raise HTTPException(status_code=503, detail="Knowledge graph not available")
        
        results = kg.query_related_entities(entity_id, entity_type, max_hops)
        return {"related_entities": results}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error querying related entities: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_statistics():
    """
    Get system statistics
    
    Returns:
        Statistics for all components
    """
    return {
        "vector_db": vdb.get_statistics(),
        "knowledge_graph": kg.get_statistics(),
        "rag_initialized": rag.initialized,
        "api_version": settings.api_version
    }


# Startup and shutdown events

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    logger.info("=" * 60)
    logger.info("Starting Medical RAG API")
    logger.info("=" * 60)
    logger.info(f"VDB Status: {vdb.get_statistics()}")
    logger.info(f"KG Status: {kg.get_statistics()}")
    logger.info(f"RAG Initialized: {rag.initialized}")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Medical RAG API")
    if kg.connected:
        kg.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
