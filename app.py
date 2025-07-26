from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

from src.chatbot import Chatbot


app = FastAPI()
chatbot = Chatbot()
chat_sessions = {}


@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_id = body.get("user_id")
    user_question = body.get("user_question")
    chat_history = chat_sessions.get(user_id, [])

    def stream():
        chunks = chatbot.response(user_question, chat_history)
        response = ""
        for chunk in chunks:
            response += chunk
            yield chunk

        chat_history.append({"role": "user", "content": user_question})
        chat_history.append({"role": "assistant", "content": response})
        chat_sessions[user_id] = chat_history

    return StreamingResponse(stream(), media_type="text/plain")