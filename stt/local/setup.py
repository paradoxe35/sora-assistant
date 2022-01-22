import os
import shutil
import sys
import wget
from zipfile import ZipFile
import logging

from model_path import en_model_path, fr_model_path


def download_model(model: str, url: str, path: str):
    print(f'Download {model} vosk model...')
    filename = wget.download(url)
    with ZipFile(filename, 'r') as zipObj:
        # extract model file from zip
        zipObj.extractall(path)
        # move files from unzip model folder to model folder
        source_dir = path + '/' + filename.split('.zip')[0]
        target_dir = path
        # move all file
        file_names = os.listdir(source_dir)
        for file_name in file_names:
            shutil.move(os.path.join(source_dir, file_name), target_dir)
        logging.info(f"{model} model file has been downloaded !")
    # remove origin zip file
    os.remove(filename)


def setup():
    if len(sys.argv) > 1:
        model = sys.argv[1]
        if model in ['fr', 'french']:
            MODEL_FR_VERSION = os.environ.get('MODEL_FR_VERSION', '0.6')
            LINTO_FR_VERSION = os.environ.get('LINTO_FR_VERSION', '2.2.0')
            url = f"https://alphacephei.com/vosk/models/vosk-model-fr-{MODEL_FR_VERSION}-linto-{LINTO_FR_VERSION}.zip"
            download_model('French', url, fr_model_path())

        elif model in ['en', 'english']:
            MODEL_EN_VERSION = os.environ.get('MODEL_EN_VERSION', '0.22')
            url = f"http://alphacephei.com/kaldi/models/vosk-model-en-us-{MODEL_EN_VERSION}.zip"
            download_model('English', url, en_model_path())

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
