from fastapi import APIRouter
from pydantic import BaseModel

import os
import json
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from utils.generate_architecture import generate_architecture_diagram
from utils.llm import get_response_from_llm

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/generate/terraform")
async def generate_terraform(request: QueryRequest):
    return {"terraform_code": f"Generated Terraform for: {request.query}"}

@router.post("/generate/description")
async def generate_description(request: QueryRequest):
    return {"description": f"Description for: {request.query}"}

@router.post("/generate/pros_cons")
async def generate_pros_cons(request: QueryRequest):
    return {"pros_cons": f"Pros and Cons for: {request.query}"}



@router.post("/generate-architecture/")
async def generate_architecture(request: Request):
    """Receives user query, processes it with LLM, and generates an architecture diagram."""
    data = await request.json()
    user_query = data.get("query", "")

    # Unique ID per session/user
    user_id = str(uuid.uuid4())  # Generates unique session ID for each user

    # filename = f"{CACHE_DIR}/arch_{user_id}.png"
    
    # Call LLM 
    llm_response = get_response_from_llm(user_query)

    llm_response = json.loads(llm_response) or ''
    created = generate_architecture_diagram(llm_response)
    if not created:
        return JSONResponse(content={"fail": "Something went wrong"}, status_code=200)

    return JSONResponse(content={"image_url": f"/get-architecture/{user_id}"}, status_code=200)
