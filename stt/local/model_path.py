import os


def fr_model_path() -> str:
    return os.environ.get('VOSK_FR_MODEL_PATH', 'stt/local/model/fr')


def en_model_path() -> str:
    return os.environ.get('VOSK_EN_MODEL_PATH', 'stt/local/model/en')
