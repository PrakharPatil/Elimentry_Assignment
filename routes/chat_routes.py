from fastapi import APIRouter, Depends, Query, HTTPException
from utils.auth_utils import get_current_user, check_access
from utils.gemini_llm import call_llm_gemini
import pandas as pd
import logging, os

router = APIRouter(prefix="/chat", tags=["Chatbot"])

os.makedirs("app/logs", exist_ok=True)
logging.basicConfig(filename="app/logs/chat_logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

@router.get("/")
def chat(query: str = Query(..., description="User question"), user: dict = Depends(get_current_user)):
    check_access(user, ["analyst", "cro"])

    df = pd.read_csv("app/data/ecl_segment_data.csv")
    if user["role"] == "analyst":
        df = df[df["segment"].isin(["EDUCATION", "HOMEIMPROVEMENT"])]

    if df.empty:
        raise HTTPException(status_code=404, detail="No data available")

    context = df.to_string(index=False)
    instruction = (
        "You are an analyst assistant. Provide detailed segment-level insights."
        if user["role"] == "analyst"
        else "You are a CRO assistant. Provide high-level strategic recommendations."
    )

    prompt = f"""
    {instruction}

    Context:
    {context}

    Question:
    {query}
    """

    response = call_llm_gemini(prompt)
    logging.info(f"User: {user['username']} | Role: {user['role']} | Query: {query} | Response: {response}")

    return {"role": user["role"], "query": query, "response": response}
