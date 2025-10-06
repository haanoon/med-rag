# Medical RAG MVP - Getting Started Guide

Welcome to the Medical RAG System! This guide will help you get the system up and running quickly.

## 🎯 What You're Building

A complete Medical Question-Answering system with:
- **Backend**: FastAPI server with RAG capabilities
- **Knowledge Graph**: Neo4j database for medical entities
- **Vector Database**: FAISS for semantic search
- **LLM Integration**: Google Gemini for answer generation
- **Frontend**: React chat interface

## 📋 Prerequisites Checklist

Before you start, make sure you have:

- [ ] **Python 3.9+** installed (`python3 --version`)
- [ ] **Node.js 18+** installed (`node --version`)
- [ ] **Google Gemini API Key** (Get one at: https://makersuite.google.com/app/apikey)
- [ ] **Docker** (optional, for Neo4j): https://docs.docker.com/get-docker/

## 🚀 Quick Start (5 Minutes)

### Method 1: Automated Setup (Easiest)

```bash
# 1. Clone the repository
git clone https://github.com/haanoon/med-rag.git
cd med-rag

# 2. Run the quick start script
./quick-start.sh

# 3. Add your Gemini API key
# Edit backend/.env and add: GEMINI_API_KEY=your_key_here

# 4. Start the backend
cd backend && python3 main.py

# 5. In a new terminal, start the frontend
cd med-rag  # go back to root
npm run dev
```

### Method 2: Manual Setup (Step by Step)

#### Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 4. (Optional) Start Neo4j with Docker
docker run -d \
  --name neo4j-medical \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/medical123 \
  neo4j:5.13

# 5. Initialize sample data
python3 src/utils/init_data.py

# 6. Start the backend server
python3 main.py
```

The backend will be running at: http://localhost:8000

#### Frontend Setup

```bash
# 1. Go back to project root
cd ..

# 2. Install Node.js dependencies
npm install

# 3. Start the frontend
npm run dev
```

The frontend will be running at: http://localhost:3000

### Method 3: Using Docker Compose (Most Complete)

```bash
# 1. Set up environment
cp backend/.env.example backend/.env
# Edit backend/.env and add your GEMINI_API_KEY

# 2. Start all services
docker-compose up

# 3. In a new terminal, initialize data
docker exec -it medrag-backend python src/utils/init_data.py
```

Access the services:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Neo4j: http://localhost:7474 (user: neo4j, pass: medical123)

## 🧪 Testing the System

### 1. Test the Backend API

Open your browser to http://localhost:8000/docs

Try the `/ask` endpoint with this request:
```json
{
  "question": "What is diabetes?",
  "top_k": 5,
  "use_kg": true
}
```

### 2. Test the Frontend

Open http://localhost:3000 and try these questions:

- "What is diabetes?"
- "What are the symptoms of hypertension?"
- "What is aspirin used for?"
- "How is Type 2 diabetes treated?"
- "What are the side effects of ibuprofen?"

### 3. Verify the Knowledge Graph

If you're using Neo4j, open http://localhost:7474

Run this query to see the data:
```cypher
MATCH (n) RETURN n LIMIT 25
```

## 🎨 Using the Interface

### Chat Interface

1. **Ask Questions**: Type your medical question in the input box
2. **View Answers**: The bot will respond with an answer based on medical knowledge
3. **Check Sources**: Click "Show sources" to see which documents were used
4. **View Confidence**: Each answer has a confidence score (0-100%)

### Understanding the Response

Each bot response includes:
- **Answer**: The generated answer with medical disclaimer
- **Sources**: The relevant documents used (click to expand)
- **Confidence Score**: How confident the system is (higher is better)
- **Source Relevance**: Individual scores for each source document

## 📊 Sample Questions

The system comes with 15 sample medical Q&A pairs. Try these categories:

### Diseases
- "What is diabetes?"
- "What causes pneumonia?"
- "What is asthma?"

### Drugs
- "What is aspirin used for?"
- "What are the side effects of ibuprofen?"
- "What are antibiotics?"

### Symptoms & Diagnosis
- "What are the symptoms of hypertension?"
- "How to diagnose high cholesterol?"

### Treatment
- "How is Type 2 diabetes treated?"
- "What is the flu vaccine?"

## 🔧 Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError`
- **Solution**: Install dependencies: `pip install -r backend/requirements.txt`

**Error**: `Connection refused to Neo4j`
- **Solution**: Neo4j is optional. The system will work without it.
- Or start Neo4j: `docker run -d --name neo4j-medical -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/medical123 neo4j:5.13`

**Error**: `No Gemini API key`
- **Solution**: Add your key to `backend/.env`: `GEMINI_API_KEY=your_key_here`
- The system can work without Gemini (using retrieval only)

### Frontend shows connection error

**Error**: "I'm having trouble connecting to my knowledge base"
- **Solution**: Make sure the backend is running at http://localhost:8000
- Check the backend terminal for errors
- Verify the API URL in the browser console

### Data not initialized

**Error**: No results when searching
- **Solution**: Run the data initialization: `cd backend && python3 src/utils/init_data.py`

### Port already in use

**Error**: `Address already in use`
- **Solution**: Change the port in `backend/config/settings.py` or `.env`
- Or stop the process using the port: `lsof -ti:8000 | xargs kill -9`

## 🎓 Next Steps

### 1. Add Your Own Data

See `backend/README.md` for instructions on:
- Adding documents to the vector database
- Creating knowledge graph entities
- Integrating with external data sources

### 2. Customize the System

- Modify `backend/config/settings.py` for configuration
- Edit `src/App.tsx` for frontend customization
- Add new API endpoints in `backend/main.py`

### 3. Deploy to Production

- Use Docker Compose for deployment
- Set up environment variables securely
- Configure CORS for your domain
- Add authentication if needed

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Backend README**: [backend/README.md](backend/README.md)
- **Project Plan**: [MEDICAL_RAG_PROJECT_PLAN.txt](MEDICAL_RAG_PROJECT_PLAN.txt)
- **Main README**: [README.md](README.md)

## 🆘 Getting Help

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review the error messages in the terminal
3. Check the backend logs for detailed errors
4. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - System information (OS, Python version, Node version)

## 🎉 Success!

If you can:
- ✅ Open the frontend at http://localhost:3000
- ✅ Ask a question and get an answer
- ✅ See sources and confidence scores
- ✅ Access the API docs at http://localhost:8000/docs

**Congratulations! Your Medical RAG MVP is working! 🚀**

## 📝 Important Notes

### Medical Disclaimer
⚠️ This system is for **educational purposes only**. It is NOT intended for:
- Medical diagnosis
- Treatment decisions
- Emergency medical situations
- Replacing professional medical advice

Always consult qualified healthcare professionals for medical concerns.

### API Key Security
- Never commit your `.env` file
- Keep your Gemini API key secure
- Use environment variables in production
- Monitor your API usage

### Data Privacy
- Sample data is public medical information
- Don't store sensitive patient data
- Follow HIPAA guidelines if handling real medical data
- Implement proper authentication for production use

---

**Happy Learning! 🏥✨**

For more information, visit the main [README.md](README.md) or open an issue on GitHub.
