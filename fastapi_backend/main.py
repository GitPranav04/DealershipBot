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

import pyodbc

# Database connection strings
DMSConnection = "Driver={ODBC Driver 17 for SQL Server};Server=10.42.57.36; Initial Catalog=OnlineDMS_Staging; User Id=dmsuser; Password=Dms2023#; Pooling=True;Max Pool Size=2500;Connect Timeout=200;Application Name=PerformTest"
DMSConnReport = "Driver={ODBC Driver 17 for SQL Server};Server=10.42.57.36; Initial Catalog=OnlineDMS_Staging; User Id=dmsuser; Password=Dms2023#; ApplicationIntent=ReadOnly;MultiSubnetFailover=True; Pooling=True;Max Pool Size=2500;Connect Timeout=200;"

# Create a connection using DMSConnection
conn = pyodbc.connect(DMSConnection)

# Create a cursor
cursor = conn.cursor()

@app.post("/chat")
async def chat(request: QueryRequest):
    inputs = tokenizer(request.question, return_tensors="pt", truncation=True, padding=True)
    outputs = model.generate(**inputs, max_length=256)
    sql = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Execute the generated SQL query
    try:
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        results = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in results]
        response = {"sql": sql, "response": data, "type": "data"}
    except Exception as e:
        response = {"sql": sql, "response": str(e), "type": "error"}

    return response