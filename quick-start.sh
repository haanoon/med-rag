#!/bin/bash

# Medical RAG System - Quick Start Script
# This script helps set up and run the system

set -e

echo "=========================================="
echo "Medical RAG System - Quick Start"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running in the correct directory
if [ ! -f "backend/main.py" ]; then
    echo -e "${RED}Error: Please run this script from the project root directory${NC}"
    exit 1
fi

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Step 1: Check prerequisites
echo -e "\n${YELLOW}[Step 1]${NC} Checking prerequisites..."

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_status "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 not found. Please install Python 3.9 or higher"
    exit 1
fi

if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_status "Node.js found: $NODE_VERSION"
else
    print_warning "Node.js not found. Frontend won't be available"
fi

if command -v docker &> /dev/null; then
    print_status "Docker found"
    HAS_DOCKER=true
else
    print_warning "Docker not found. Neo4j KG features will be disabled"
    HAS_DOCKER=false
fi

# Step 2: Set up backend
echo -e "\n${YELLOW}[Step 2]${NC} Setting up backend..."

cd backend

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file from template"
    cp .env.example .env
    print_warning "Please edit backend/.env and add your GEMINI_API_KEY"
else
    print_status ".env file already exists"
fi

# Install Python dependencies
echo "Installing Python dependencies (this may take a few minutes)..."
if pip install -q -r requirements.txt; then
    print_status "Python dependencies installed"
else
    print_warning "Some dependencies may have failed to install"
    print_warning "You can try installing them manually: pip install -r requirements.txt"
fi

cd ..

# Step 3: Start Neo4j (optional)
if [ "$HAS_DOCKER" = true ]; then
    echo -e "\n${YELLOW}[Step 3]${NC} Setting up Neo4j..."
    
    # Check if Neo4j container already exists
    if docker ps -a --format '{{.Names}}' | grep -q "^neo4j-medical$"; then
        if docker ps --format '{{.Names}}' | grep -q "^neo4j-medical$"; then
            print_status "Neo4j container already running"
        else
            echo "Starting existing Neo4j container..."
            docker start neo4j-medical
            print_status "Neo4j container started"
        fi
    else
        echo "Creating and starting Neo4j container..."
        docker run -d \
            --name neo4j-medical \
            -p 7474:7474 -p 7687:7687 \
            -e NEO4J_AUTH=neo4j/medical123 \
            neo4j:5.13
        print_status "Neo4j container created and started"
        echo "   - Neo4j Browser: http://localhost:7474"
        echo "   - Username: neo4j"
        echo "   - Password: medical123"
    fi
else
    echo -e "\n${YELLOW}[Step 3]${NC} Skipping Neo4j setup (Docker not available)"
fi

# Step 4: Initialize data
echo -e "\n${YELLOW}[Step 4]${NC} Initializing sample data..."
cd backend
if python3 src/utils/init_data.py; then
    print_status "Sample data initialized"
else
    print_warning "Data initialization may have had issues"
fi
cd ..

# Step 5: Install frontend dependencies
if command -v npm &> /dev/null; then
    echo -e "\n${YELLOW}[Step 5]${NC} Setting up frontend..."
    
    if [ ! -d "node_modules" ]; then
        echo "Installing Node.js dependencies..."
        npm install
        print_status "Frontend dependencies installed"
    else
        print_status "Frontend dependencies already installed"
    fi
fi

# Final instructions
echo -e "\n=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "To start the system:"
echo ""
echo "1. Start the backend (in one terminal):"
echo "   cd backend && python3 main.py"
echo ""
echo "2. Start the frontend (in another terminal):"
echo "   npm run dev"
echo ""
echo "3. Access the application:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
if [ "$HAS_DOCKER" = true ]; then
    echo "   - Neo4j Browser: http://localhost:7474"
fi
echo ""
echo "Or use Docker Compose to run everything:"
echo "   docker-compose up"
echo ""
echo "=========================================="
