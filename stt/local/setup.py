import os
import sys
import wget
from zipfile import ZipFile
import logging

from stt.local.model_path import en_model_path, fr_model_path


def download_en_model():
    MODEL_EN_VERSION = os.environ.get('MODEL_EN_VERSION', '0.22')
    url = f"http://alphacephei.com/kaldi/models/vosk-model-en-us-{MODEL_EN_VERSION}.zip"
    filename = wget.download(url)

    with ZipFile(filename, 'r') as zipObj:
        zipObj.extractall(en_model_path())
        logging.info("EN model file has been downloaded !")
    os.unlink(filename)


def download_fr_model():
    MODEL_FR_VERSION = os.environ.get('MODEL_FR_VERSION', '0.6')
    LINTO_FR_VERSION = os.environ.get('LINTO_FR_VERSION', '2.2.0')
    url = f"https://alphacephei.com/vosk/models/vosk-model-fr-${MODEL_FR_VERSION}-linto-${LINTO_FR_VERSION}.zip "
    filename = wget.download(url)

    with ZipFile(filename, 'r') as zipObj:
        zipObj.extractall(fr_model_path())
        logging.info("Fr model file has been downloaded !")
    os.unlink(filename)


def setup():
    if len(sys.argv) > 1:
        model = sys.argv[1]
        if model in ['fr', 'french']:
            download_fr_model()
        elif model in ['en', 'english']:
            download_en_model()
        else:
            logging.exception(
                "Model provided as argument is invalid, fr and en are only supported"
            )
            sys.exit(1)
    else:
        logging.exception("there no model provided as argument")
        sys.exit(1)


if __name__ == '__main__':
    setup()
