# Doc_ai

## Doc AI
* Ultra Doc AI is a document intelligence API designed to process logistics documents such as rate confirmations and bills of lading. The system allows users to upload documents, ask natural language questions about them, and extract structured shipment data.

This project demonstrates how retrieval augmented generation and rule based extraction can be combined to build a practical AI system for real world logistics workflows.

The goal of this assignment was to show the ability to design a clean backend system, integrate embeddings and vector search, and handle semi structured business documents.

## Project Overview
* Logistics documents often contain critical shipment information but in different layouts and formats. This project solves that problem by:

Allowing document upload
Converting documents into searchable text
Creating embeddings for semantic search
Answering user questions using retrieval
Extracting structured shipment data into JSON

The system is built as a FastAPI service and can be tested easily using Swagger UI.

## Technology Stack
* FastAPI for building the API
Sentence Transformers for embeddings
FAISS for vector search
LangChain text splitters for chunking
Regex based extraction for structured fields
Python multipart for file uploads
PDF parsing using pypdf

These tools were selected because they are lightweight, reliable, and widely used in production AI systems.

## Python Environment
* This project was developed using a dedicated Python virtual environment.

A separate environment was used to avoid dependency conflicts and to ensure reproducibility. Document AI systems often require specific versions of libraries, especially for embeddings and vector search.

Python version used
Python 3.10

Reason for choosing this version
Stable support across FastAPI, FAISS, and Sentence Transformers
Compatible with most AI libraries
Avoids breaking changes from very new Python versions

## How the System Works
* Step 1 Document Upload
The user uploads a PDF document through the upload endpoint. The file is saved locally and parsed into raw text.

Step 2 Text Processing
The text is split into smaller chunks. This improves embedding quality and retrieval accuracy.

Step 3 Embedding Generation
Each chunk is converted into a vector embedding using a Sentence Transformer model.

Step 4 Vector Storage
Embeddings are stored in a FAISS index. This allows fast similarity search.

Step 5 Question Answering
When a question is asked, the system embeds the query and retrieves the most similar chunks. The answer is generated from those retrieved sections.

Step 6 Structured Extraction
A separate endpoint extracts shipment details such as shipper, consignee, rate, and dates using pattern matching.

## Errors Faced and How They Were Fixed
* During development several real world issues occurred.

JSON serialization error
The system initially returned numpy float values from FAISS. FastAPI cannot serialize numpy types into JSON.
Solution
Converted numpy floats into native Python floats before returning responses.

LangChain import error
The text splitter module had moved to a separate package.
Solution
Installed langchain text splitters package and updated imports.

Internal server error on ask endpoint
This happened when asking questions before uploading a document.
Solution
Added safety checks and user friendly messages when no index exists.

Extraction returning null values
Some logistics documents use inconsistent formatting.
Solution
Improved regex patterns to handle variations.

These issues reflect realistic development challenges and demonstrate debugging skills.

## API Endpoints
* Upload endpoint
Accepts a PDF file and processes it into embeddings.

Ask endpoint
Accepts a natural language question and returns an answer, confidence score, and sources.

Extract endpoint
Accepts a PDF and returns structured shipment data in JSON.

## How to Run the Project
* Install dependencies
pip install requirements.txt

Start the server
uvicorn app.main:app reload

Open Swagger UI
http://127.0.0.1:8000/docs

Upload a document first before asking questions.

## Why This Approach

Retrieval augmented generation is well suited for logistics because documents contain precise business data that must not be hallucinated.

Vector search ensures answers come from actual document content.
Rule based extraction ensures consistent JSON output for downstream systems.

This combination balances intelligence and reliability.

## Why This Approach

Retrieval augmented generation is well suited for logistics because documents contain precise business data that must not be hallucinated.

Vector search ensures answers come from actual document content.
Rule based extraction ensures consistent JSON output for downstream systems.

This combination balances intelligence and reliability.

## Final Thoughts

This project demonstrates practical AI engineering skills including:

API design
Vector databases
Embedding models
Information retrieval
Data extraction
Debugging and problem solving

The system is simple but realistic and can be extended into a production grade document intelligence platform