import os


def fr_server_port():
    return int(os.environ.get('STT_FR_LOCAL_SERVER_PORT', 2782))


def en_server_port():
    return int(os.environ.get('STT_EN_LOCAL_SERVER_PORT', 2781))


def third_party_server_port():
    return int(os.environ.get('STT_THIRD_PARTY_SERVER_PORT', 2790))


def server_interface():
    return os.environ.get('STT_SERVER_INTERFACE', '0.0.0.0')
