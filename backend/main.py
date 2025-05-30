import json
import websockets
from fastapi.responses import FileResponse
from fastapi import WebSocket, WebSocketDisconnect, FastAPI
from fastapi.middleware.cors import CORSMiddleware

import binance_pb2
from lib import config, auth, utils

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,       
    allow_credentials=True,
    allow_methods=["*"],          
    allow_headers=["*"],         
)

@app.websocket("/binance-api/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token or not auth.verify_auth(token):
        await websocket.close(code=1008) 
        return

    await websocket.accept()
    
    try:
        data = await websocket.receive_bytes()
        request = binance_pb2.SubscriptionRequest()
        request.ParseFromString(data)

        async with websockets.connect(utils.get_binance_url(request)) as binance_ws:
            while True:
                response = await binance_ws.recv()
                json_data = json.loads(response)
                model = utils.binance_response_to_model(json_data)

                await websocket.send_bytes(model.SerializeToString())

    except WebSocketDisconnect:
        print("Disconnected")
    except Exception as e:
        print("Error:", e)


@app.get("/binance-api/binance.proto")
async def get_proto_file():
    return FileResponse("binance.proto", media_type="text/plain")