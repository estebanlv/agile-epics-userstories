from fastapi import APIRouter, Request, Form, HTTPException, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from src.services.story_generator import generate_user_stories
from src.services.story_extender import extend_user_story
from src.schemas.user_story import UserStorySchema
from src.schemas.extended_user_story import ExtendedUserStorySchema
from src.schemas.extend_request import ExtendRequest
from typing import List, Dict

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def post_generate(request: Request, epic: str = Form(...)):
    # Input validation
    if len(epic.strip()) < 20:
        raise HTTPException(status_code=400, detail="Epic is too short. Please provide a more detailed epic.")
    if len(epic.strip()) > 1000:
        raise HTTPException(status_code=400, detail="Epic is too long. Please provide a shorter epic.")

    user_stories = await generate_user_stories(epic)
    return templates.TemplateResponse("result.html", {"request": request, "user_stories": user_stories})

@router.post("/extend", response_class=JSONResponse)
async def extend_user_story_endpoint(request: Request, extend_request: ExtendRequest = Body(...)):
    description = extend_request.description
    if not description.strip():
        return JSONResponse(status_code=400, content={"error": "Description cannot be empty."})
    
    extended_story = await extend_user_story(description)
    if not extended_story:
        return JSONResponse(status_code=400, content={"error": "Failed to extend user story. Please try again."})
    return JSONResponse(content=extended_story)
