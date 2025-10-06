"""
Data initialization script
Loads sample medical data into the vector database and knowledge graph
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.vdb import vdb
from src.kg import kg
from src.utils.sample_data import SAMPLE_MEDICAL_DATA, SAMPLE_KG_DATA
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_vector_db():
    """Load sample documents into vector database"""
    logger.info("Initializing vector database with sample data...")
    
    texts = [item["answer"] for item in SAMPLE_MEDICAL_DATA]
    metadata = [
        {
            "question": item["question"],
            **item["metadata"]
        }
        for item in SAMPLE_MEDICAL_DATA
    ]
    
    vdb.add_documents(texts, metadata)
    vdb.save_index()
    
    logger.info(f"✓ Loaded {len(texts)} documents into vector database")


def initialize_knowledge_graph():
    """Load sample entities and relationships into knowledge graph"""
    if not kg.connected:
        logger.warning("Neo4j not connected. Skipping knowledge graph initialization.")
        return
    
    logger.info("Initializing knowledge graph with sample data...")
    
    # Create constraints
    kg.create_constraints()
    
    # Add entities
    for entity in SAMPLE_KG_DATA["entities"]:
        kg.add_entity(
            entity_type=entity["type"],
            entity_id=entity["id"],
            name=entity["name"],
            properties={"description": entity.get("description", "")}
        )
    
    logger.info(f"✓ Added {len(SAMPLE_KG_DATA['entities'])} entities")
    
    # Add relationships
    for rel in SAMPLE_KG_DATA["relationships"]:
        kg.add_relationship(
            from_id=rel["from"],
            to_id=rel["to"],
            relationship_type=rel["type"],
            from_type=rel["from_type"],
            to_type=rel["to_type"]
        )
    
    logger.info(f"✓ Added {len(SAMPLE_KG_DATA['relationships'])} relationships")
    
    # Print stats
    stats = kg.get_statistics()
    logger.info(f"Knowledge Graph Stats: {stats}")


def main():
    """Main initialization function"""
    logger.info("=" * 60)
    logger.info("Medical RAG System - Data Initialization")
    logger.info("=" * 60)
    
    try:
        # Initialize vector database
        initialize_vector_db()
        
        # Initialize knowledge graph
        initialize_knowledge_graph()
        
        logger.info("=" * 60)
        logger.info("✓ Data initialization complete!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Error during initialization: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # Cleanup
        if kg.connected:
            kg.close()


if __name__ == "__main__":
    main()
