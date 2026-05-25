from django.shortcuts import render
import uuid


def chat_view(request):
    session_id = request.session.get("chat_session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session["chat_session_id"] = session_id
    return render(request, "chatui/chat.html", {"session_id": session_id})


def clear_chat(request):
    if "chat_session_id" in request.session:
        del request.session["chat_session_id"]
    new_session_id = str(uuid.uuid4())
    request.session["chat_session_id"] = new_session_id
    return render(request, "chatui/chat.html", {"session_id": new_session_id})