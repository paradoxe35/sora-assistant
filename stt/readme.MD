## End to end speech recognition system

- **English Local Server port:** 2781
- **French Local Server port:** 2782s
- **English and French Server port by third party (Gooogle, Wit.ai)** 2790

## Docker compose Setup

For a quick setup, you can use docker compose by running the following command:

```bash
docker-compose -f ./stt/kaldi-docker/docker-compose.yml up -d
```

You can specify a service instead of run all services

```bash
docker-compose -f ./stt/kaldi-docker/docker-compose.yml up [service](stt-en_us | stt-fr_fr) -d
```

## Alternative Setup

Here are list of proccess need to be setup on this section:

- Install all dependencies which are list in **requirements.txt** - run:

```bash
pip install -r requirements.txt
```

- Download French vosk speech recognition model - run:

```bash
python stt/local/setup.py fr
```

- Download English vosk speech recognition model - run:

```bash
python stt/local/setup.py en
```

### Server

There are two options to run speech recognition server:

- From local (Using our own speech recognition models)

- Using third party services for speech recognition like (Google speech recognition, Wit.ai speech)

To run server from local, use commands below:

- French local speech recognition - run:

```bash
python ./stt/server.py local-fr
```

- English local speech recognition - run:

```bash
python ./stt/server.py local-en
```

To run server using third party services, use commands below:

- French and English both are supported in third party speech recognition - run:

```bash
python ./stt/server.py third-party
```

## Environment variables

For local speech recognizer

- `VOSK_SPK_MODEL_PATH` vosk spk model path. No default value
- `VOSK_SAMPLE_RATE` vosk sample rate for audio wave format. Default value: _8000_
- `VOSK_ALTERNATIVES` vosk alteranatives. Default value: _0_
- `VOSK_SHOW_WORDS` vosk show words. Default value: _True_
- `VOSK_FR_MODEL_PATH` vosk path for french model. Default value: _stt/local/model/fr_
- `VOSK_EN_MODEL_PATH` vosk path for english model. Default value: _stt/local/model/en_

For local speech recognition server

- `STT_EN_LOCAL_SERVER_PORT` English speech recognition server port. Default value: _2781_
- `STT_FR_LOCAL_SERVER_PORT` French speech recognition server port. Default value: _2782_
- `STT_THIRD_PARTY_SERVER_PORT` English speech recognition server port. Default value: _2790_
- `STT_SERVER_INTERFACE` Server interface. Default value: _0.0.0.0_

For third party speech recognizer with wit.ai, those variables below are required to the service.

- `WIT_EN_API_KEY` wit.ai app server key with English as language
- `WIT_FR_API_KEY` wit.ai app server key with French as language

Here you'll need to create two applications on [wit.io](), so one with french language and another one with English language

### Models

Our speech recognition local Models versions files.
**French**:

- `MODEL_FR_VERSION` default value: _0.6_
- `LINTO_FR_VERSION` default value: _2.2.0_

**English**:

- `MODEL_EN_VERSION` default value: _0.22_

For informations, check out all supported [models](https://alphacephei.com/vosk/models) by vosk.
