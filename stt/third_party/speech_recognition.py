import asyncio
from datetime import datetime
import logging
import os
import sys
import speech_recognition as sr
import websockets
import concurrent.futures
import json
from io import BytesIO


from env import server_interface, third_party_server_port


gr = sr.Recognizer()


def process_chunk(message, sample_rate):
    global lang
    global wit_en_key
    global wit_fr_key

    file_like = BytesIO(message)
    with sr.AudioFile(file_like) as source:
        audio_data = gr.record(source)
        if lang.startswith('en') and wit_en_key != None:
            logging.info('Recognize wit.ai, English Lang')
            text = gr.recognize_wit(
                audio_data, key=wit_en_key, show_all=False
            )
        elif lang.startswith('fr') and wit_fr_key != None:
            logging.info('Recognize wit.ai, French Lang')
            text = gr.recognize_wit(
                audio_data, key=wit_fr_key, show_all=False
            )
        else:
            logging.info('recognize google')
            text = gr.recognize_google(
                audio_data, language=lang, show_all=False
            )
        return json.JSONEncoder().encode({"text": text}), True


async def recognize(websocket):
    global loop
    global pool
    global lang

    sample_rate = None

    lang = None

    while True:
        message = await websocket.recv()

        logging.info('Connection from %s', websocket.remote_address)

        if isinstance(message, str) and 'config' in message:
            jobj = json.loads(message)['config']
            logging.info("Config %s", jobj)
            if 'sample_rate' in jobj:
                sample_rate = float(jobj['sample_rate'])
            if 'language' in jobj:
                lang = str(jobj['language'])
            continue

        if lang == None:
            message = "No speech language has been provided"
            logging.warning(message)
            await websocket.send(json.JSONEncoder().encode({"error": message}))
            break

        response, stop = await loop.run_in_executor(pool, process_chunk, message, sample_rate)
        await websocket.send(response)
        if stop:
            break


def start():
    global loop
    global pool
    global wit_en_key
    global wit_fr_key

    args = type('', (), {})()

    logging.basicConfig(level=logging.INFO)

    args.interface = server_interface()
    args.port = third_party_server_port()
    wit_en_key = os.environ.get('WIT_EN_API_KEY')
    wit_fr_key = os.environ.get('WIT_FR_API_KEY')

    pool = concurrent.futures.ThreadPoolExecutor((os.cpu_count() or 1))
    loop = asyncio.get_event_loop()

    start_server = websockets.serve(
        recognize, args.interface, args.port)

    logging.info("Listening on %s:%d", args.interface, args.port)
    loop.run_until_complete(start_server)
    loop.run_forever()
