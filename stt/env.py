import os


def fr_server_port():
    return int(os.environ.get('STT_SERVER_PORT', 2782))


def en_server_port():
    return int(os.environ.get('STT_SERVER_PORT', 2781))


def server_interface():
    return os.environ.get('SERVER_INTERFACE', '0.0.0.0')
