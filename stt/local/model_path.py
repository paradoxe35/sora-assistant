import os


def fr_model_path() -> str:
    return os.environ.get('VOSK_MODEL_PATH', 'stt/local/model/fr')


def en_model_path() -> str:
    return os.environ.get('VOSK_MODEL_PATH', 'stt/local/model/en')
