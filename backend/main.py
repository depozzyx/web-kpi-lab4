from fastapi.responses import FileResponse
from fastapi import WebSocket, WebSocketDisconnect, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import verify_auth
import binance_pb2
import websockets
import json
import time

app = FastAPI()

origins = [
    "http://localhost:5050",
    "http://127.0.0.1:5050"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["*"],          
    allow_headers=["*"],         
)

@app.websocket("/binance-api/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("allooo")

    token = websocket.query_params.get("token")
    if not token or not verify_auth(token):
        await websocket.close(code=1008) 
        return

    await websocket.accept()
    
    try:
        data = await websocket.receive_bytes()
        request = binance_pb2.SubscriptionRequest()
        request.ParseFromString(data)
        symbols = [s.lower() + "@ticker" for s in request.symbols]

        url = f"wss://stream.binance.com:9443/stream?streams={'/'.join(symbols)}"
        async with websockets.connect(url) as binance_ws:
            while True:
                response = await binance_ws.recv()
                json_data = json.loads(response)
                symbol = json_data['data']['s']
                price = json_data['data']['c']
                ts = int(time.time() * 1000)

                msg = binance_pb2.TickerData(symbol=symbol, price=price, timestamp=ts)
                await websocket.send_bytes(msg.SerializeToString())

    except WebSocketDisconnect:
        print("Disconnected")
    except Exception as e:
        print("Error:", e)


@app.get("/binance-api/binance.proto")
async def get_proto_file():
    return FileResponse("binance.proto", media_type="text/plain")