# encoding:utf-8
from phoneco.logger import logger
from phoneco.models import State, Phone, Cli, Params
import paho.mqtt.client as mqtt
from time import sleep
from phoneco.params_parser import load_params
import bluetooth


# instanciation du singleton de params
print(Params(load_params()).phones)


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
        sleep(15)


def connexion():
    """
    Réalise la connection, et renvoie le client
    :return:
    """
    cur_cli = Params().client
    logger.info(f"starting on client data: {cur_cli}")
    client = mqtt.Client(cur_cli.name)
    client.tls_set(cur_cli.certificate_file)
    client.username_pw_set(cur_cli.username, cur_cli.password)
    logger.debug(f"starting client connexion...")
    client.connect(cur_cli.mqtt_broker, cur_cli.port)
    logger.debug(f"Connexion established.")
    client.loop_start()
    logger.debug("client loop thread started")
    return client


def main():
    while True:
        try:
            client = connexion()
            status_control(client)
        except Exception as e:
            logger.exception(f"A non planned error occured")
            logger.info(f"instead of error, the script will continue indefinitely.")


if __name__ == '__main__':
    main()
