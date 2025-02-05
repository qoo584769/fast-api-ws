import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.controllers.websocket_controller import WebSocketManager
from app.models.websocket_message import WebSocketMessage

router = APIRouter()
websocket_manager = WebSocketManager()


@router.websocket('/{room_id}')
async def websocket_endpoint(websocket: WebSocket, room_id: str):
	await websocket_manager.connect_websocket(websocket, room_id)
	try:
		while True:
			data = await websocket.receive_text()
			message = WebSocketMessage(**json.loads(data))
			print(message)
			await websocket_manager.handle_message(websocket, message, room_id)
	except WebSocketDisconnect:
		await websocket_manager.disconnect_websocket(room_id, message.user_email)


@router.websocket('/ws')
async def websocket_endpoint2(websocket: WebSocket):
	await websocket.accept()
	while True:
		data = await websocket.receive_text()
		await websocket.send_text(f'Message text was: {data}')
