import asyncio 

import logging 
import uvicorn
import secrets 
from fastapi.middleware.cors import CORSMiddleware

import uuid 
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRelay
from fastapi import FastAPI, Request
from fastapi.openapi.docs import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from MediaTrack import AudioTransformTrack

security = HTTPBasic()
app = FastAPI()

origins = ["http://localhost:5000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pcs = set()
dcs = set()

relay = MediaRelay()

@app.post("/api/offer")
async def offer(request:Request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    # pc_id = "PeerConnection(%s)"% uuid.uuid4()
    pcs.add(pc)


    recorder = MediaBlackhole()

    @pc.on("datachannel")
    def on_datachannel(channel):
        dcs.add(channel)

        @channel.on("message")
        def on_message(message):
            if isinstance(message, str) and message.startswith("ping"):
                channel.send("pong"+message[4:])
    

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        if pc.connectionState=="failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        if track.kind == "audio":
            pc.addTrack(AudioTransformTrack(relay.subscribe(track)))

            pass


        for participant in pcs:
            if participant != pc:  # Не отправляем трек самому себе
                participant.addTrack(track)

        @track.on("ended")
        async def on_ended():
            await recorder.stop()

    await pc.setRemoteDescription(offer)
    await recorder.start()

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return JSONResponse(
        {"sdp":pc.localDescription.sdp, "type":pc.localDescription.type},
    )

@app.post("/message", include_in_schema=False)
async def message(request: Request):
    params = await request.json()
    message = params["message"]

    # Отправляем сообщение всем участникам
    for participant in pcs:
        for channel in participant.dataChannels:
            channel.send(message)

    return JSONResponse({"status": "Message sent"})