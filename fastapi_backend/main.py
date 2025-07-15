#import pyodbc
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow cross-origin requests from the Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your fine-tuned model and tokenizer
MODEL_PATH = "./finetuned-t5-text2sql"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)

class QueryRequest(BaseModel):
    question: str

# Database connection
#server = 'your_server'
#database = 'your_database'
#username = 'your_username'
#password = 'your_password'
#connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Create a connection
#conn = pyodbc.connect(connection_string)

# Create a cursor
#cursor = conn.cursor()

@app.post("/chat")
async def chat(request: QueryRequest):
    inputs = tokenizer(request.question, return_tensors="pt", truncation=True, padding=True)
    outputs = model.generate(**inputs, max_length=256)
    sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"sql": sql, "response": sql, "type": "sql"}