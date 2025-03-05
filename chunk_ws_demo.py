from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse
import asyncio
from typing import AsyncGenerator

app = FastAPI()


text = "今朝は少し早く起きて、近くの公園を散歩しました。空は晴れていて、涼しい風が心地よく吹いていました。公園では、犬を散歩させている人やジョギングをしている人たちが見られ、平和な雰囲気が広がっていました。ベンチに座ってコーヒーを飲みながら、鳥のさえずりを聞くのはとてもリラックスできました。\n"


# CHUNKED TRANSFER ENCODING DEMO
async def chunked_text_stream() -> AsyncGenerator[bytes, None]:

    text_chunks = [char.encode('utf-8') for char in text]
    for chunk in text_chunks:
        yield chunk
        await asyncio.sleep(0.1)  # Simulate delay


# progressively growing stream
async def chunked_text_stream_progressive() -> AsyncGenerator[bytes, None]:

    text_chunks = [char for char in text]
    message = ''

    for chunk in text_chunks:
        message += str(chunk)
        yield f"{message}\n".encode('utf-8')
        await asyncio.sleep(0.1)  # Simulate delay


@app.get("/chunked")
async def chunked_response():
    return StreamingResponse(chunked_text_stream_progressive(), media_type="text/plain")


# WEBSOCKET DEMO
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    text_chunks = [char for char in text]
    message = ''

    for i in range(len(text_chunks)):
        message += str(text_chunks[i])
        await websocket.send_text(f"{message}")
        await asyncio.sleep(0.1)  # Simulate delay
    await websocket.close()

# To run: uvicorn filename:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
