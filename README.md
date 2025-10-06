# Medical RAG System - MVP

A foundational MVP implementation of an Intelligent Medical Retrieval-Augmented Generation (RAG) system with Knowledge Graph, Vector Database, and Q&A capabilities.

## 🚀 Overview

This system combines three powerful technologies to provide accurate medical information:

1. **Knowledge Graph (Neo4j)** - Stores medical entities (diseases, drugs, symptoms) and their relationships
2. **Vector Database (FAISS)** - Enables semantic search over medical documents
3. **RAG System (Gemini)** - Generates accurate answers with source citations

## ✨ Features

- **Intelligent Q&A**: Ask medical questions and get accurate, sourced answers
- **Semantic Search**: Find relevant medical information using natural language
- **Knowledge Graph**: Navigate relationships between medical concepts
- **Source Citations**: Every answer includes references to source documents
- **Confidence Scores**: Understand how confident the system is in its answers
- **Modern UI**: Clean, responsive React interface

## 📋 Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **Docker & Docker Compose** (optional, for easy setup)
- **Google Gemini API Key** (for answer generation)

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/haanoon/med-rag.git
cd med-rag
```

2. **Set up environment variables:**
```bash
# Create .env file in backend directory
cp backend/.env.example backend/.env

# Edit backend/.env and add your Gemini API key
# GEMINI_API_KEY=your_api_key_here
```

3. **Start all services:**
```bash
docker-compose up
```

4. **Initialize data (in a new terminal):**
```bash
docker exec -it medrag-backend python src/utils/init_data.py
```

5. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Neo4j Browser: http://localhost:7474 (user: neo4j, password: medical123)

### Option 2: Manual Setup

#### Backend Setup

1. **Install Python dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Set up environment:**
```bash
cp .env.example .env
# Edit .env and configure settings
```

3. **Start Neo4j (optional):**
```bash
docker run -d \
  --name neo4j-medical \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/medical123 \
  neo4j:5.13
```

4. **Initialize data:**
```bash
python src/utils/init_data.py
```

5. **Start the backend:**
```bash
python main.py
```

#### Frontend Setup

1. **Install Node dependencies:**
```bash
cd ..  # Back to project root
npm install
```

2. **Start the frontend:**
```bash
npm run dev
```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 📖 Usage

### Asking Questions

Simply type your medical question in the chat interface. Examples:

- "What is diabetes?"
- "What are the symptoms of hypertension?"
- "What is aspirin used for?"
- "How is Type 2 diabetes treated?"
- "What are the side effects of ibuprofen?"

### Viewing Sources

Click "Show sources" on any bot response to see:
- Source documents used to generate the answer
- Relevance scores for each source
- Document metadata (category, source type)

### Understanding Confidence

Each answer includes a confidence score indicating how reliable the system believes its answer to be based on the retrieved documents.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   React Frontend                     │
│           (Medical Q&A Chat Interface)               │
└────────────────────┬────────────────────────────────┘
                     │ HTTP/REST
                     ▼
┌─────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)             │
├─────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────┐   │
│  │           RAG System (Core Logic)            │   │
│  │  • Query Processing                          │   │
│  │  • Context Retrieval                         │   │
│  │  • Answer Generation                         │   │
│  └──────┬───────────────────────────────┬───────┘   │
│         │                               │           │
│  ┌──────▼────────┐            ┌─────────▼────────┐  │
│  │  Vector DB    │            │  Knowledge Graph │  │
│  │   (FAISS)     │            │     (Neo4j)      │  │
│  │               │            │                  │  │
│  │ • Embeddings  │            │ • Entities       │  │
│  │ • Similarity  │            │ • Relationships  │  │
│  │   Search      │            │ • Query Expand   │  │
│  └───────────────┘            └──────────────────┘  │
└─────────────────────────────────────────────────────┘
                     │
                     ▼
         ┌──────────────────────┐
         │   Google Gemini API   │
         │  (Answer Generation)  │
         └──────────────────────┘
```

## 📊 Current Data

The MVP includes sample medical data:

- **15 Medical Q&A pairs** covering:
  - Diseases (diabetes, hypertension, pneumonia, asthma)
  - Drugs (aspirin, ibuprofen, metformin, insulin)
  - Symptoms and diagnosis
  - Treatments and procedures

- **12 Medical Entities** in Knowledge Graph:
  - 4 Diseases
  - 4 Drugs
  - 4 Symptoms

- **8 Relationships** in Knowledge Graph:
  - TREATS (drug → disease/symptom)
  - HAS_SYMPTOM (disease → symptom)

## 🔌 API Endpoints

### Main Endpoints

- `POST /ask` - Ask a medical question
- `GET /search` - Search for documents
- `GET /health` - System health check
- `GET /stats` - System statistics

### Knowledge Graph Endpoints

- `GET /kg/search` - Search entities
- `GET /kg/entity/{id}` - Get related entities

Full API documentation: http://localhost:8000/docs

## 🛠️ Development

### Project Structure

```
med-rag/
├── backend/                 # Python backend
│   ├── config/             # Configuration
│   ├── src/
│   │   ├── kg/            # Knowledge Graph module
│   │   ├── vdb/           # Vector Database module
│   │   ├── rag/           # RAG System module
│   │   └── utils/         # Utilities & sample data
│   ├── data/              # Data storage
│   ├── main.py            # FastAPI app
│   └── requirements.txt   # Python dependencies
├── src/                    # React frontend
│   ├── components/        # UI components
│   └── App.tsx           # Main app component
├── docker-compose.yml     # Docker setup
└── package.json          # Node dependencies
```

### Adding Your Own Data

See the [Backend README](backend/README.md) for detailed instructions on:
- Adding documents to the vector database
- Creating knowledge graph entities and relationships
- Integrating with real data sources (PubMed, MedQuAD, UMLS)

### Running Tests

```bash
# Backend tests (when available)
cd backend
pytest tests/

# Frontend tests (when available)
npm test
```

## 🔐 Security Note

- Store your Gemini API key securely in `.env` files
- Never commit `.env` files to version control
- The system includes medical disclaimers on all answers
- This is for educational purposes only - not for medical diagnosis

## 📝 Medical Disclaimer

⚠️ **Important**: This system is for educational and informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare professionals with any questions you may have regarding medical conditions.

## 🗺️ Future Enhancements

- [ ] Integration with PubMed API for real medical literature
- [ ] Support for MedQuAD dataset
- [ ] UMLS integration for medical terminology
- [ ] Advanced query expansion using knowledge graph
- [ ] Multi-hop reasoning in knowledge graph
- [ ] Answer verification and fact-checking
- [ ] User feedback mechanism
- [ ] Caching for improved performance
- [ ] Medical entity extraction from queries
- [ ] Support for multiple languages

## 📄 For More Information

See the complete [Project Plan](./MEDICAL_RAG_PROJECT_PLAN.txt) for detailed technical specifications and 6-phase implementation roadmap.

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check the [Backend README](backend/README.md) for detailed documentation

## 🙏 Acknowledgments

- Built with FastAPI, React, Neo4j, FAISS, and Google Gemini
- UI components from shadcn/ui
- Sample medical data compiled from various educational sources

---

**Happy coding! 🚀**