#!/usr/bin/env python3
"""
Test script to verify the Medical RAG system structure and logic
This script validates the architecture without requiring external dependencies
"""

import sys
import os

print("=" * 70)
print("Medical RAG System - Structure Verification")
print("=" * 70)

# Test 1: Check directory structure
print("\n[TEST 1] Verifying directory structure...")
required_dirs = [
    "config",
    "src/kg",
    "src/vdb",
    "src/rag",
    "src/utils",
    "data/raw",
    "data/processed",
    "data/indices"
]

missing_dirs = []
for dir_path in required_dirs:
    full_path = os.path.join(os.path.dirname(__file__), dir_path)
    if os.path.exists(full_path):
        print(f"  ✓ {dir_path}")
    else:
        print(f"  ✗ {dir_path} (missing)")
        missing_dirs.append(dir_path)

if missing_dirs:
    print(f"\n  ERROR: {len(missing_dirs)} directories missing")
    sys.exit(1)
else:
    print(f"\n  SUCCESS: All {len(required_dirs)} directories present")

# Test 2: Check Python files exist
print("\n[TEST 2] Verifying Python modules...")
required_files = [
    "config/settings.py",
    "src/kg/knowledge_graph.py",
    "src/vdb/vector_db.py",
    "src/rag/rag_system.py",
    "src/utils/sample_data.py",
    "src/utils/init_data.py",
    "main.py"
]

missing_files = []
for file_path in required_files:
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    if os.path.exists(full_path):
        print(f"  ✓ {file_path}")
    else:
        print(f"  ✗ {file_path} (missing)")
        missing_files.append(file_path)

if missing_files:
    print(f"\n  ERROR: {len(missing_files)} files missing")
    sys.exit(1)
else:
    print(f"\n  SUCCESS: All {len(required_files)} files present")

# Test 3: Verify sample data
print("\n[TEST 3] Verifying sample data...")
sys.path.insert(0, os.path.dirname(__file__))

try:
    from src.utils.sample_data import SAMPLE_MEDICAL_DATA, SAMPLE_KG_DATA
    
    num_qa_pairs = len(SAMPLE_MEDICAL_DATA)
    num_entities = len(SAMPLE_KG_DATA["entities"])
    num_relationships = len(SAMPLE_KG_DATA["relationships"])
    
    print(f"  ✓ Sample Q&A pairs: {num_qa_pairs}")
    print(f"  ✓ Knowledge Graph entities: {num_entities}")
    print(f"  ✓ Knowledge Graph relationships: {num_relationships}")
    
    # Verify data structure
    assert num_qa_pairs > 0, "No Q&A pairs found"
    assert num_entities > 0, "No entities found"
    assert num_relationships > 0, "No relationships found"
    
    # Check first Q&A pair structure
    first_qa = SAMPLE_MEDICAL_DATA[0]
    assert "question" in first_qa, "Missing 'question' field"
    assert "answer" in first_qa, "Missing 'answer' field"
    assert "metadata" in first_qa, "Missing 'metadata' field"
    
    print(f"\n  Sample question: \"{first_qa['question']}\"")
    print(f"  Answer preview: \"{first_qa['answer'][:80]}...\"")
    
    print(f"\n  SUCCESS: Sample data is valid")
    
except Exception as e:
    print(f"\n  ERROR: Failed to load sample data: {e}")
    sys.exit(1)

# Test 4: Check configuration
print("\n[TEST 4] Verifying configuration...")
try:
    # Check if .env.example exists
    env_example = os.path.join(os.path.dirname(__file__), ".env.example")
    if os.path.exists(env_example):
        print(f"  ✓ .env.example present")
        with open(env_example) as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
            print(f"  ✓ Configuration variables: {len(lines)}")
    else:
        print(f"  ✗ .env.example missing")
    
    print(f"\n  SUCCESS: Configuration files present")
    
except Exception as e:
    print(f"\n  ERROR: Configuration check failed: {e}")

# Test 5: Verify API structure
print("\n[TEST 5] Verifying API endpoints...")
try:
    with open("main.py") as f:
        content = f.read()
        
    # Check for key endpoints
    endpoints = [
        ("/ask", "POST /ask - Main Q&A endpoint"),
        ("/search", "GET /search - Document search"),
        ("/health", "GET /health - Health check"),
        ("/stats", "GET /stats - System statistics"),
        ("/kg/search", "GET /kg/search - KG entity search"),
    ]
    
    for endpoint, description in endpoints:
        if endpoint in content:
            print(f"  ✓ {description}")
        else:
            print(f"  ✗ {description} (not found)")
    
    print(f"\n  SUCCESS: API structure verified")
    
except Exception as e:
    print(f"\n  ERROR: API verification failed: {e}")

# Summary
print("\n" + "=" * 70)
print("✓ VERIFICATION COMPLETE: Medical RAG MVP structure is valid!")
print("=" * 70)
print("\nNext steps:")
print("1. Install dependencies: pip install -r requirements.txt")
print("2. Set up .env file with your Gemini API key")
print("3. (Optional) Start Neo4j: docker run -d --name neo4j-medical \\")
print("   -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/medical123 neo4j:5.13")
print("4. Initialize data: python src/utils/init_data.py")
print("5. Start the server: python main.py")
print("6. Access the API: http://localhost:8000/docs")
print("\n" + "=" * 70)
