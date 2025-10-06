# Medical RAG System - Backend

A foundational MVP implementation of a Medical Retrieval-Augmented Generation (RAG) system with Knowledge Graph, Vector Database, and Q&A capabilities.

## Features

### Core Components

1. **Knowledge Graph (Neo4j)**
   - Stores medical entities (diseases, drugs, symptoms, procedures)
   - Manages relationships between entities (TREATS, HAS_SYMPTOM, etc.)
   - Enables query expansion with related medical concepts

2. **Vector Database (FAISS)**
   - Semantic search using sentence embeddings
   - Fast similarity search for relevant documents
   - Supports document metadata and retrieval

3. **RAG System (Gemini)**
   - Retrieves relevant context from vector database
   - Generates accurate answers using Google Gemini API
   - Includes source citations and confidence scores

### API Endpoints

- `POST /ask` - Ask a medical question (main RAG endpoint)
- `GET /search` - Search for relevant documents
- `GET /health` - System health check
- `GET /stats` - System statistics
- `GET /kg/search` - Search knowledge graph entities
- `GET /kg/entity/{id}` - Get related entities

## Quick Start

### Prerequisites

- Python 3.9+
- Neo4j (optional, via Docker)
- Google Gemini API key

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

3. **Initialize with sample data:**
```bash
python src/utils/init_data.py
```

4. **Start the API server:**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Using Docker

Run the entire stack (backend, Neo4j, frontend):

```bash
# From the project root
docker-compose up
```

## Usage Examples

### Ask a Question

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the symptoms of diabetes?",
    "top_k": 5,
    "use_kg": true
  }'
```

### Search Documents

```bash
curl "http://localhost:8000/search?query=hypertension&k=5"
```

### Search Knowledge Graph

```bash
curl "http://localhost:8000/kg/search?query=aspirin&limit=10"
```

## Data Initialization

The system includes sample medical data for demonstration:

- 15 medical Q&A pairs covering various topics
- 12 medical entities (diseases, drugs, symptoms)
- 8 relationships between entities

To load your own data:

```python
from src.vdb import vdb
from src.kg import kg

# Add documents to vector database
vdb.add_documents(texts, metadata)
vdb.save_index()

# Add entities to knowledge graph
kg.add_entity("Disease", "entity_id", "Entity Name", properties)
kg.add_relationship("from_id", "to_id", "RELATIONSHIP_TYPE", "FromType", "ToType")
```

## Configuration

Edit `config/settings.py` or use environment variables:

- `API_HOST` - API host (default: 0.0.0.0)
- `API_PORT` - API port (default: 8000)
- `NEO4J_URI` - Neo4j connection URI
- `NEO4J_USER` - Neo4j username
- `NEO4J_PASSWORD` - Neo4j password
- `GEMINI_API_KEY` - Google Gemini API key
- `FAISS_INDEX_PATH` - Path to FAISS index file
- `EMBEDDING_MODEL` - Sentence transformer model name
- `TOP_K_RETRIEVAL` - Number of documents to retrieve
- `MAX_ANSWER_LENGTH` - Maximum answer length

## System Architecture

```
┌─────────────┐
│   Frontend  │
│   (React)   │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────────────────────────────┐
│         FastAPI Backend             │
├─────────────────────────────────────┤
│  ┌───────────┐  ┌──────────────┐   │
│  │    RAG    │  │   API Routes │   │
│  │  System   │  │              │   │
│  └─────┬─────┘  └──────────────┘   │
│        │                            │
│  ┌─────▼─────┐  ┌──────────────┐   │
│  │  Vector   │  │  Knowledge   │   │
│  │ Database  │  │    Graph     │   │
│  │  (FAISS)  │  │   (Neo4j)    │   │
│  └───────────┘  └──────────────┘   │
└─────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│   Gemini    │
│     API     │
└─────────────┘
```

## Development

### Project Structure

```
backend/
├── config/               # Configuration files
│   └── settings.py      # Application settings
├── src/
│   ├── api/             # API routes (future expansion)
│   ├── kg/              # Knowledge Graph module
│   │   └── knowledge_graph.py
│   ├── vdb/             # Vector Database module
│   │   └── vector_db.py
│   ├── rag/             # RAG System module
│   │   └── rag_system.py
│   └── utils/           # Utilities
│       ├── sample_data.py
│       └── init_data.py
├── data/                # Data storage
│   ├── raw/            # Raw data files
│   ├── processed/      # Processed data
│   └── indices/        # FAISS indices
├── tests/               # Test files
├── main.py             # FastAPI application
├── requirements.txt    # Python dependencies
└── Dockerfile          # Docker configuration
```

### Running Tests

```bash
pytest tests/
```

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Data Sources

The MVP is designed to work with:

- **PubMed**: Medical literature and research papers
- **MedQuAD**: Medical question-answer pairs
- **UMLS**: Unified Medical Language System

For the MVP, sample data is included for demonstration. Integration with real data sources can be added by:

1. Implementing data ingestion scripts in `src/utils/`
2. Processing and chunking documents
3. Adding to vector database with `vdb.add_documents()`
4. Adding entities/relationships to KG with `kg.add_entity()` and `kg.add_relationship()`

## Limitations & Future Work

### Current MVP Limitations

- Sample data only (15 Q&A pairs)
- Neo4j is optional (system works without it)
- Basic confidence scoring
- No user authentication

### Planned Enhancements

- [ ] Integration with real medical datasets (PubMed, MedQuAD)
- [ ] Advanced query expansion strategies
- [ ] Multi-hop reasoning in knowledge graph
- [ ] Answer verification and fact-checking
- [ ] User feedback and learning mechanisms
- [ ] Medical entity extraction from queries
- [ ] Caching for improved performance
- [ ] User authentication and rate limiting

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For questions or issues, please open an issue on GitHub.
