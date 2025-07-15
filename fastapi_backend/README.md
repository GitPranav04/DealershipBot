# TVS DMS Chatbot Backend (FastAPI)

## Features
- Uses Salesforce t5 text-to-sql model from Hugging Face
- `/chat` endpoint: Converts natural language to SQL
- Ready for fine-tuning on your own DMS schema dataset (`text2sql_dataset.jsonl`)

## Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Start the server:
   ```
   uvicorn main:app --reload
   ```
3. (Optional) Fine-tune the model:
   ```
   python train_model.py
   ```

## Connect with Angular Frontend
- POST user questions to `http://localhost:8000/chat`
- Response will contain generated SQL

---

**Place your `text2sql_dataset.jsonl` in this folder for training.**
