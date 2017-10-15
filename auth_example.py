import pony_vk
import logging
from pony_vk import errors as error

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

email = input("Input number or e-mail: ")
password = input("Input password: ")

try:
    client = pony_vk.Client(login=email, password=password)
    print(client.id)
except error.VKError as exception:
    print(exception.description)
    print(exception.details)



