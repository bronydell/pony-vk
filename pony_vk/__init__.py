import requests
import logging
import pony_vk.errors as errors

logger = logging.getLogger("pony-vk-client")

"""
Request class stores information about request,
including client object, method name and arguments
This idea is based on: https://github.com/python273/vk_api
"""


class Request(object):
    __slots__ = ('_api', '_method_name', '_method_args')

    def __init__(self, api, method_name):
        self._api = api
        self._method_name = method_name
        self._method_args = {}

    def __getattr__(self, method_name):
        return Request(self._api, self._method_name + '.' + method_name)

    def __call__(self, **method_args):
        method_args['access_token'] = self._api.access_token
        self._method_args = method_args

        return self._api.method(self)

"""
Class Client is our API, we are using it to call API methods.
There is 2 options how to make client:
* Using login and password, this method is default! It uses Android version of VK, so you can use
things like audio VK
* Using access token, this method allowing you use community tokens
You can use your own app id
"""


class Client(object):
    auth_url = "https://oauth.vk.com/token"
    request_template_url = "https://api.vk.com/method/"
    id = -1

    def __getattr__(self, method_name):
        return Request(self, method_name)

    def __call__(self, method_name, **method_kwargs):
        return getattr(self, method_name)(**method_kwargs)

    def __init__(self, login="",
                 password="",
                 access_token=None,
                 **method_kwargs):
        self.session = requests.session()
        if access_token:
            self.access_token = access_token
        else:
            self.auth_params = {
                "scope": method_kwargs.get("scope", "all"),
                "client_id": method_kwargs.get("client_id", "2274003"),
                "client_secret": method_kwargs.get("client_secret", "hHbZxrka2uZ6jB1inYsH"),
                "2fa_supported": 1,
                "lang": method_kwargs.get("lang", "ru"),
                "device_id": method_kwargs.get("device_id", ""),
                "grant_type": method_kwargs.get("grant_type", "password"),
                "username": login,
                "password": password,
                "libverify_support": "1",
                "code": method_kwargs.get("code", None),
                "v": method_kwargs.get("v", "5.67")
            }
            self.session.headers['User-Agent'] = 'VKAndroidApp/4.9-1118 (Android 5.1; SDK 22; armeabi-v7a; UMI IRON; ru'
            resp = self.session.post(self.auth_url, data=self.auth_params).json()
            logger.debug(resp)
            self.error_process(resp)
            if 'access_token' in resp:
                self.access_token = resp['access_token']
                self.v = method_kwargs.get("v", "5.67")
            else:
                raise errors.AuthError(resp)
            self.info = self.users.get()

    def method(self, request):
        params = request._method_args
        params['access_token'] = self.access_token
        params['v'] = self.v
        resp = self.session.post(url=self.request_template_url + request._method_name, data=params).json()
        self.error_process(resp)
        return resp['response']

    @staticmethod
    def error_process(json):
        if 'error' in json:
            error_code = json['error']
            if type(error_code) is not str:
                error_code = error_code.get('error_code', -1)
            if error_code == "need_validation":
                raise errors.CodeRequiredError(json)
            elif error_code == 1:
                raise errors.UnknownError(json)
            elif error_code == 2:
                raise errors.ApplicationDisabledError(json)
            elif error_code == 3:
                raise errors.UnknownMethodError(json)
            elif error_code == 4:
                raise errors.IncorrectSignError(json)
            elif error_code == 5:
                raise errors.AuthError(json)
            elif error_code == 6:
                raise errors.TooManyRequestsError(json)
            elif error_code == 7:
                raise errors.PermissionDeniedError(json)
            elif error_code == 8:
                raise errors.InvalidRequestError(json)
            elif error_code == 9:
                raise errors.FloodControlError(json)
            elif error_code == 10:
                raise errors.ServerError(json)
            elif error_code == 11:
                raise errors.AppInTestModeError(json)
            elif error_code == 14:
                raise errors.CaptchaError(json)
            elif error_code == 15:
                raise errors.AccessDeniedError(json)
            elif error_code == 16:
                raise errors.HTTPAuthFailedError(json)
            elif error_code == 17:
                raise errors.ValidationRequiredError(json)
            elif error_code == 18:
                raise errors.UserBannedError(json)
            elif error_code == 20:
                raise errors.StandaloneOnlyError(json)
            elif error_code == 21:
                raise errors.StandaloneAndOpenAPIOnlyError(json)
            elif error_code == 23:
                raise errors.MethodDisabledError(json)
            elif error_code == 24:
                raise errors.ConfirmationRequiredError(json)
            elif error_code == 27:
                raise errors.GroupAuthFailedError(json)
            elif error_code == 28:
                raise errors.AppAuthFailedError(json)
            elif error_code == 100:
                raise errors.BadRequestError(json)
            elif error_code == 101:
                raise errors.InvalidAppIDError(json)
            elif error_code == 113:
                raise errors.InvalidUserIDError(json)
            elif error_code == 150:
                raise errors.InvalidTimestampError(json)
            elif error_code == 200:
                raise errors.AccessToAlbumDeniedError(json)
            elif error_code == 201:
                raise errors.AccessToAudioDeniedError(json)
            elif error_code == 203:
                raise errors.AccessToGroupDeniedError(json)
            elif error_code == 300:
                raise errors.AlbumFullError(json)
            elif error_code == 500:
                raise errors.AppPermissionDeniedError(json)
            elif error_code == 600:
                raise errors.PermissionDeniedWithObjectsError(json)
            elif error_code == 603:
                raise errors.AdsError(json)
            else:
                raise errors.VKError(json)
