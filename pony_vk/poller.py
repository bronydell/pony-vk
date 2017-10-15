import logging
import time
import threading
import requests
from enum import Enum

logger = logging.getLogger("pony-vk-poller")


class LongPool(object):
    def __init__(self, url, key, ts):
        self.url = url
        self.key = key
        self.ts = ts

    def get_poll_url(self):
        return 'https://{url}?act=a_check&key={key}&ts={ts}&wait=25&mode=2&version=1'.format(url=self.url,
                                                                                             key=self.key,
                                                                                             ts=self.ts)

    def pool(self):
        session = requests.session()
        answer = session.get(self.get_poll_url(), timeout=27.0)
        if answer.status_code == 200:
            if 'ts' in answer.json():
                self.ts = answer.json()['ts']
            return answer.json()
        else:
            raise Exception(
                'Error with get request {url}. Answers contains code: {code}'.format(url=answer.url,
                                                                                 code=answer.status_code))


def get_long_pool_server(client):
    try:
        answ = client.messages.getLongPollServer()
        server = LongPool(answ['server'], answ['key'], answ['ts'])
    except:
        return get_long_pool_server(client)
    return server


class Errors(Enum):
    HISTORY_FAILED = 1
    KEY_IS_NOT_VALID = 2
    USER_INFO_LOST = 3
    VERSION_IS_NOT_VALID = 4


class Codes(Enum):
    FLAG_CHANGED = 1
    FLAG_SETUPED = 2
    FLAG_RESETED = 3
    FLAG_CHANGED_COMMUNITY = 11
    FLAG_SETUPED_COMMUNITY = 12
    FLAG_RESETED_COMMUNITY = 10
    NEW_MESSAGE = 4
    READ_INCOMING_MESSAGES = 6
    READ_OUTCOMING_MESSAGES = 7
    USER_ONLINE = 8
    USER_GONE_OFFLINE = 9
    CHAT_NAME_CHANGED = 51
    USER_TYPING_PRIVATE = 61
    USER_TYPING_CHAT = 62
    USER_CALLS = 70
    UNREAD_MESSAGES_COUNTER_UPDATE = 80
    NOTIFICATIONS_SETTINGS_UPDATE = 114


class VKPooler(object):
    def __init__(self):
        self.functions = {}

    def addHandler(self, code, function):
        if code.value in self.functions:
            self.functions[code.value].append(function)
        else:
            self.functions[code.value] = [function]

    errors = {Errors.HISTORY_FAILED: 'Error with history ot ts event',
              Errors.KEY_IS_NOT_VALID: 'Key is not valid. Relogin pls',
              Errors.USER_INFO_LOST: 'Restart it with new key',
              Errors.VERSION_IS_NOT_VALID: 'Minimal(ot maximal) version is wrong'}

    def start_polling(self, client):
        threading.Thread(target=self.poll, args=(client,)).start()

    def poll(self, client):
        server = get_long_pool_server(client)
        while True:
            try:
                answ = server.pool()
                if 'error' in answ:
                    for error in Errors:
                        if error.value == answ['error']:
                            logging.error(Errors[error.value])
                            time.sleep(1)
                            server = get_long_pool_server(client)
                else:
                    for update in answ['updates']:
                        for code in Codes:
                            if update[0] == code.value:
                                if code.value in self.functions:
                                    for function in self.functions[code.value]:
                                        function(client, update)
            except Exception as ex:
                print(ex)
                time.sleep(1)
                server = get_long_pool_server(client)
