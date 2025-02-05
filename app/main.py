from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.views import item_view, websocket_view

app = FastAPI()

origins = ['*']

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*'],
)

app.include_router(item_view.router)
app.include_router(websocket_view.router)
