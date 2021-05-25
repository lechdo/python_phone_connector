# encoding:utf-8
from .logger import logger
from .models import State, Phone, Params
import paho.mqtt.client as mqtt
from time import sleep
from .params_parser import load_params
import bluetooth

# instanciation du singleton de params
print(Params(load_params()))


def status_control(client):
    """
    Réalise dans la boucle le métier. Reprend le statut de connexion du telephone et agit en conséquence.
    Agit selon le client fourni.
    :param client:
    :return:
    """
    phones = [Phone(name=ele.name, mac=ele.mac) for ele in Params().phones]
    while True:
        for phone in phones:
            logger.debug(f"checking status for {phone.name}'s phone")
            key = "bluetooth/presence/" + phone.name
            result = bluetooth.lookup_name(phone.mac, timeout=3)
            detected_state = State.HOME if result else State.NOT_HOME
            logger.debug(f"current state status : {repr(detected_state)}")
            if phone.status != detected_state:
                phone.status = detected_state
                logger.info(f"Changed phone status : phone {phone.name}, status {repr(phone.status)}")
                client.publish(key, detected_state, retain=False)
        logger.info("Status control, pending 15 seconds...")
        sleep(15)


def connexion():
    """
    Réalise la connection, et renvoie le client
    :return:
    """
    cli = Params().client
    logger.info(f"starting on client data: {cli}")
    client = mqtt.Client(cli.name)
    client.username_pw_set(cli.username, cli.password)
    logger.debug(f"starting client connexion...")
    client.connect(cli.mqtt_broker, cli.port)
    logger.debug(f"Connexion established.")
    client.loop_start()
    logger.debug("client loop thread started")
    return client


def main():
    while True:
        try:
            client = connexion()
            status_control(client)
        except FileNotFoundError as e:
            logger.exception("The param json file cannot be found !")
            raise
        except Exception as e:
            logger.exception(f"A non planned error occured")
            logger.warning(f"instead of any error, the script will continue indefinitely. Be careful !")


if __name__ == '__main__':
    main()
