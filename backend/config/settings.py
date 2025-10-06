"""
Configuration settings for the Medical RAG system
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    api_title: str = "Medical RAG API"
    api_version: str = "0.1.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Neo4j Settings
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "medical123"
    
    # Vector DB Settings
    faiss_index_path: str = "./data/indices/faiss.index"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    
    # Gemini API Settings
    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-1.5-flash"
    
    # RAG Settings
    top_k_retrieval: int = 5
    max_answer_length: int = 500
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
