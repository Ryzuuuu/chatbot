import json
import httpx
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        await self.accept()
    # removed greeting here — chat.html already shows it as static HTML

    async def disconnect(self, code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_msg = data.get("message", "").strip()
        if not user_msg:
            return

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    "http://localhost:8000/chat",
                    json={
                        "session_id": self.session_id,
                        "message": user_msg,
                        "memory_type": "summary_buffer"
                    }
                )
                result = response.json()

            await self.send(text_data=json.dumps({
                "reply": result["reply"],
                "turn_count": result["turn_count"]
            }))

        except Exception as e:
            await self.send(text_data=json.dumps({
                "reply": f"Error reaching AI backend: {str(e)}",
                "turn_count": 0
            }))