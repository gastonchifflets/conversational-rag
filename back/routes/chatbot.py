from fastapi import APIRouter, Request
from back.services.chatbot import makeIaCall


router = APIRouter()

@router.post("/")
async def index(request: Request):
    data = await request.json()
    input = data["input"]
    if (input == ""):
        return "You must insert something as input to get a response."
    return makeIaCall(input)