from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.services.story_generator import generate_user_stories
from src.schemas.user_story import UserStorySchema
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("/index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def post_generate(request: Request, epic: str = Form(...)):
    user_stories = await generate_user_stories(epic)
    return templates.TemplateResponse("/result.html", {"request": request, "user_stories": user_stories})
