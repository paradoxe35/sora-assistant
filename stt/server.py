from local.asr_server_en import start as start_en_server
from local.asr_server_fr import start as start_fr_server
from third_party.speech_recognition import start as start_sr
import sys
import logging
from env import fr_server_port, en_server_port


if __name__ == '__main__':
    if len(sys.argv) > 1:
        executor = sys.argv[1]
        if executor == 'local-en':
            start_en_server()
        elif executor == 'local-fr':
            start_fr_server()
        elif executor == 'sr-fr':
            start_sr('fr-FR', fr_server_port())
        elif executor == 'sr-en':
            start_sr('en-US', en_server_port())
        else:
            logging.warning('unknown server argument')
    else:
        logging.warning("server argument is required")
