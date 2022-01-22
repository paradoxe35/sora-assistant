import asyncio
import logging
import os
import sys
import speech_recognition as sr
import websockets
import concurrent.futures
import json

from env import server_interface


gr = sr.Recognizer()


def process_chunk(message, sample_rate):
    global lang
    with sr.AudioData(message, sample_rate=sample_rate, sample_width=1) as source:
        audio_data = gr.record(source)
        text = gr.recognize_wit(audio_data, language=lang)
        print(f'text {text}')
        return {'text': text}, True


async def recognize(websocket):
    global loop
    global pool
    global lang

    sample_rate = None

    while True:
        message = await websocket.recv()

        logging.info('Connection from %s', websocket.remote_address)

        if isinstance(message, str) and 'config' in message:
            jobj = json.loads(message)['config']
            logging.info("Config %s", jobj)
            if 'sample_rate' in jobj:
                sample_rate = float(jobj['sample_rate'])
            continue

        response, stop = await loop.run_in_executor(pool, process_chunk, message, sample_rate)
        await websocket.send(response)
        if stop:
            break


def start(language: str, port: int):
    global loop
    global pool
    global lang

    lang = language

    args = type('', (), {})()

    logging.basicConfig(level=logging.INFO)

    args.interface = server_interface()
    args.port = port

    pool = concurrent.futures.ThreadPoolExecutor((os.cpu_count() or 1))
    loop = asyncio.get_event_loop()

    start_server = websockets.serve(
        recognize, args.interface, args.port)

    logging.info("Listening on %s:%d", args.interface, args.port)
    loop.run_until_complete(start_server)
    loop.run_forever()
