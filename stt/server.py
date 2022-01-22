from local.asr_server_en import start as start_en_server
from local.asr_server_fr import start as start_fr_server
import sys
import logging


if __name__ == '__main__':
    if len(sys.argv) > 1:
        executor = sys.argv[1]
        if executor == 'local-en':
            start_en_server()
        elif executor == 'local-fr':
            start_fr_server()
        else:
            logging.warning('unknown server argument')
    else:
        logging.warning("server argument is required")
