from typing import Dict, List

from fastapi import WebSocket

from app.models.websocket_message import WebSocketMessage


# user_id = None
# user_email = None
class WebSocketManager:
	def __init__(self):
		self.connected_clients: Dict[str, WebSocket] = {}
		self.rooms: Dict[str, List[WebSocket]] = {}

	async def connect_websocket(self, websocket: WebSocket, room_id: str):
		await websocket.accept()
		if room_id not in self.rooms:
			self.rooms[room_id] = []
		self.rooms[room_id].append(websocket)

	async def disconnect_websocket(self, room_id: str, user_email: str):
		websocket = self.connected_clients.pop(user_email, None)
		if websocket and room_id in self.rooms:
			self.rooms[room_id].remove(websocket)
			if not self.rooms[room_id]:
				del self.rooms[room_id]

	async def broadcast_message(self, message: str, room_id: str):
		for websocket in self.rooms[room_id]:
			await websocket.send_text(message)

	async def handle_message(
		self, websocket: WebSocket, message: WebSocketMessage, room_id: str
	):
		user_email = message.user_email
		self.connected_clients[user_email] = websocket
		# 處理不同類型的訊息
		if message.type == 'chat':
			await self.broadcast_message(
				f'Chat from {message.content["user"]}: {message.content["message"]}', room_id
			)
		elif message.type == 'notification':
			await self.broadcast_message(f'Notification: {message.content}')
		else:
			await websocket.send_text('Unsupported message type')
