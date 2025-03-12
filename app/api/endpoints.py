import os
import json
import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import FileResponse, JSONResponse
from utils.generate_architecture import generate_architecture_diagram
from utils.llm import get_response_from_llm

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/generate/terraform")
async def generate_terraform(request: QueryRequest):
    return {"terraform_code": f"Generated Terraform for: {request.query}"}

@router.post("/generate/overview")
async def generate_description(request: QueryRequest):
    try:
        data = request.model_dump()
        user_query = data.get("query", "")
        if not user_query:
            return JSONResponse(content={"fail": "User Query not found"}, status_code=400)

        return JSONResponse(content={"success": "Cool"}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"fail": "Something went wrong"}, status_code=400)


@router.post("/generate/pros_cons")
async def generate_pros_cons(request: QueryRequest):
    return {"pros_cons": f"Pros and Cons for: {request.query}"}



@router.post("/generate-architecture/")
async def generate_architecture(request: QueryRequest):
    """Receives user query, processes it with LLM, and generates an architecture diagram."""
    
    data = request.model_dump()
    user_query = data.get("query", "")
    if not user_query:
        return JSONResponse(content={"fail": "User Query not found"}, status_code=200)


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
