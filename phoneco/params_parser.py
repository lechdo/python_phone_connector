from json import loads
from json.decoder import JSONDecodeError
from phoneco.logger import logger


def load_params():
    try:
        with open("params.json", "r", encoding="utf-8") as file:
            content = loads(file.read())
        return content
    except IOError as e:
        logger.exception("An error occ")
        raise
    except JSONDecodeError as e:
        logger.exception(e)
        raise
