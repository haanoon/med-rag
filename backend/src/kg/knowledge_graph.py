"""
Knowledge Graph module using Neo4j
Manages medical entities and relationships
"""
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class KnowledgeGraph:
    """
    Knowledge Graph interface using Neo4j
    Stores medical entities (diseases, symptoms, drugs) and their relationships
    """
    
    def __init__(self):
        """Initialize Neo4j connection"""
        self.driver = None
        self.connected = False
        try:
            self.driver = GraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password)
            )
            self.driver.verify_connectivity()
            self.connected = True
            logger.info("Successfully connected to Neo4j")
        except Exception as e:
            logger.warning(f"Could not connect to Neo4j: {e}. KG features will be disabled.")
    
    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
    
    def create_constraints(self):
        """Create database constraints for entity uniqueness"""
        if not self.connected:
            return
        
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Disease) REQUIRE d.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Symptom) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (dr:Drug) REQUIRE dr.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Procedure) REQUIRE p.id IS UNIQUE"
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    logger.debug(f"Constraint creation note: {e}")
    
    def add_entity(self, entity_type: str, entity_id: str, name: str, properties: Dict[str, Any] = None):
        """
        Add a medical entity to the knowledge graph
        
        Args:
            entity_type: Type of entity (Disease, Symptom, Drug, Procedure)
            entity_id: Unique identifier for the entity
            name: Human-readable name
            properties: Additional properties as dict
        """
        if not self.connected:
            return
        
        props = properties or {}
        props.update({"id": entity_id, "name": name})
        
        query = f"""
        MERGE (e:{entity_type} {{id: $entity_id}})
        SET e += $properties
        RETURN e
        """
        
        with self.driver.session() as session:
            session.run(query, entity_id=entity_id, properties=props)
    
    def add_relationship(self, from_id: str, to_id: str, relationship_type: str, 
                        from_type: str, to_type: str, properties: Dict[str, Any] = None):
        """
        Add a relationship between two entities
        
        Args:
            from_id: ID of the source entity
            to_id: ID of the target entity
            relationship_type: Type of relationship (TREATS, CAUSES, etc.)
            from_type: Entity type of source
            to_type: Entity type of target
            properties: Additional relationship properties
        """
        if not self.connected:
            return
        
        props = properties or {}
        
        query = f"""
        MATCH (a:{from_type} {{id: $from_id}})
        MATCH (b:{to_type} {{id: $to_id}})
        MERGE (a)-[r:{relationship_type}]->(b)
        SET r += $properties
        RETURN r
        """
        
        with self.driver.session() as session:
            session.run(query, from_id=from_id, to_id=to_id, properties=props)
    
    def query_related_entities(self, entity_id: str, entity_type: str, 
                               max_hops: int = 1) -> List[Dict[str, Any]]:
        """
        Query entities related to a given entity
        
        Args:
            entity_id: ID of the entity to start from
            entity_type: Type of the starting entity
            max_hops: Maximum number of relationship hops (default: 1)
        
        Returns:
            List of related entities with their relationships
        """
        if not self.connected:
            return []
        
        query = f"""
        MATCH (start:{entity_type} {{id: $entity_id}})
        MATCH path = (start)-[r*1..{max_hops}]-(related)
        RETURN related, labels(related) as types, r, length(path) as distance
        LIMIT 50
        """
        
        results = []
        with self.driver.session() as session:
            result = session.run(query, entity_id=entity_id)
            for record in result:
                node = record["related"]
                results.append({
                    "id": node.get("id"),
                    "name": node.get("name"),
                    "types": record["types"],
                    "distance": record["distance"]
                })
        
        return results
    
    def search_entities(self, query: str, entity_types: Optional[List[str]] = None, 
                       limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for entities by name
        
        Args:
            query: Search query string
            entity_types: Optional list of entity types to filter
            limit: Maximum number of results
        
        Returns:
            List of matching entities
        """
        if not self.connected:
            return []
        
        type_filter = ""
        if entity_types:
            type_labels = "|".join(entity_types)
            type_filter = f":{type_labels}"
        
        cypher_query = f"""
        MATCH (e{type_filter})
        WHERE toLower(e.name) CONTAINS toLower($query)
        RETURN e, labels(e) as types
        LIMIT $limit
        """
        
        results = []
        with self.driver.session() as session:
            result = session.run(cypher_query, query=query, limit=limit)
            for record in result:
                node = record["e"]
                results.append({
                    "id": node.get("id"),
                    "name": node.get("name"),
                    "types": record["types"],
                    "properties": dict(node)
                })
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge graph statistics"""
        if not self.connected:
            return {"error": "Not connected to Neo4j"}
        
        query = """
        MATCH (n)
        RETURN labels(n) as label, count(n) as count
        """
        
        stats = {"node_counts": {}, "connected": True}
        
        with self.driver.session() as session:
            result = session.run(query)
            for record in result:
                label = record["label"][0] if record["label"] else "Unknown"
                stats["node_counts"][label] = record["count"]
            
            # Get relationship count
            rel_result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            stats["relationship_count"] = rel_result.single()["count"]
        
        return stats


# Global KG instance
kg = KnowledgeGraph()
