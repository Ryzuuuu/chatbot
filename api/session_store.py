from core.chain import ChatbotChain

sessions = {}

def get_session(session_id: str) -> ChatbotChain:
    if session_id not in sessions:
        sessions[session_id] = ChatbotChain(memory_type="summary_buffer")
    return sessions[session_id]

def delete_session(session_id: str):
    if session_id in sessions:
        sessions[session_id].clear()
        del sessions[session_id]