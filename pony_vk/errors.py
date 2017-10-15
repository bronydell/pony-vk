"""
This module provides almost every VK Error.

Every error is child of VKError, which contains description, details and json.
Description is full name of error
Details is description how to fix this error
json is answer from server
"""


class VKError(Exception):
    description = "Unknown VK Error"
    details = "???"

    def __init__(self, json):
        self.json = json
        super(VKError, self).__init__(json)


# It doesn't have any code
class CodeRequiredError(VKError):
    description = "Code is required"
    details = "Code was sent with sms(by default) or with another method. Recreate Client with code param"
    pass


# Code 1
class UnknownError(VKError):
    description = "Unknown error"
    details = "Try again later."
    pass


# Code 2
class ApplicationDisabledError(VKError):
    description = "Application is disabled. Enable your application or use test mode"
    details = "You need to switch on the app in Settings (https://vk.com/editapp?id={Your API_ID} " \
              "or use the test mode (test_mode=1)."
    pass


# Code 3
class UnknownMethodError(VKError):
    description = "Unknown method passed"
    details = "Check the method name: http://vk.com/dev/methods ."
    pass


# Code 4
class IncorrectSignError(VKError):
    description = "Incorrect signature"
    details = "Check if the signature has been formed correctly: https://vk.com/dev/api_nohttps."
    pass


# Code 5
class AuthError(VKError):
    description = "User authorization failed"
    details = "Make sure that you use a correct authorization type(https://vk.com/dev/access_token)"
    pass


# Code 6
class TooManyRequestsError(VKError):
    description = "Too many requests per second"
    details = "Decrease the request frequency or use the execute(https://vk.com/dev/execute) method.\n" \
              "More details on frequency limits here: http://vk.com/dev/api_requests."
    pass


# Code 7
class PermissionDeniedError(VKError):
    description = "Permission to perform this action is denied"
    details = "Make sure that your have received required permissions(https://vk.com/dev/permissions)" \
              " during the authorization. You can do it with the " \
              "account.getAppPermissions(https://vk.com/dev/account.getAppPermissions) method."
    pass


# Code 8
class InvalidRequestError(VKError):
    description = "Invalid request "
    details = "Check the request syntax(https://vk.com/dev/api_requests) and used" \
              " parameters list (it can be found on a method description page) ."
    pass


# Code 9
class FloodControlError(VKError):
    description = "Invalid request "
    details = "You need to decrease the count of identical requests." \
              "For more efficient work you may use execute(https://vk.com/dev/execute)" \
              " or JSONP(https://vk.com/dev/jsonp)."
    pass


# Code 10
class ServerError(VKError):
    description = "Internal server error"
    details = "Try again later."
    pass


# Code 11
class AppInTestModeError(VKError):
    description = "In test mode application should be disabled or user should be authorized"
    details = "Switch the app off in Settings: https://vk.com/editapp?id={Your API_ID}."
    pass


# Code 14
class CaptchaError(VKError):
    description = "Captcha needed"
    details = "Work with this error is explained in detail on the separate page(https://vk.com/dev/captcha_error)"
    pass


# Code 15
class AccessDeniedError(VKError):
    description = "Access denied"
    details = "Make sure that you use correct identifiers and the content is" \
              " available for the user in the full version of the site."
    pass


# Code 16
class HTTPAuthFailedError(VKError):
    description = "HTTP authorization failed "
    details = "To avoid this error check if a user has the 'Use secure connection'" \
              "option enabled with the account.getInfo(https://vk.com/dev/account.getInfo) method."
    pass


# Code 17
class ValidationRequiredError(VKError):
    description = "Validation required"
    details = "Make sure that you don't use a token received with http://vk.com/dev/auth_mobile for a request" \
              " from the server. It's restricted. The validation process is described on the separate page."
    pass


# Code 18
class UserBannedError(VKError):
    description = "User was deleted or banned"
    details = "User was deleted or banned ¯\_(ツ)_/¯"
    pass


# Code 20
class StandaloneOnlyError(VKError):
    description = "Permission to perform this action is denied for non-standalone applications"
    details = "If you see this error despite your app has the Standalone type, make sure that you use " \
              "redirect_uri=https://oauth.vk.com/blank.html. Details here: http://vk.com/dev/auth_mobile."
    pass


# Code 21
class StandaloneAndOpenAPIOnlyError(VKError):
    description = "Permission to perform this action is allowed only for Standalone and OpenAPI applications"
    details = "Permission to perform this action is allowed only for Standalone and OpenAPI applications."
    pass


# Code 23
class MethodDisabledError(VKError):
    description = "This method was disabled"
    details = "All the methods available now are listed here: http://vk.com/dev/methods."
    pass


# Code 24
class ConfirmationRequiredError(VKError):
    description = "Confirmation required "
    details = "Confirmation process is described on the separate page(https://vk.com/dev/need_confirmation)."
    pass


# Code 27
class GroupAuthFailedError(VKError):
    description = "Group authorization failed"
    details = "Group authorization failed"
    pass


# Code 28
class AppAuthFailedError(VKError):
    description = "Application authorization failed"
    details = "Application authorization failed"
    pass


# Code 100
class BadRequestError(VKError):
    description = "One of the parameters specified was missing or invalid "
    details = "Check the reqired parameters list and their format on a method description page."
    pass


# Code 101
class InvalidAppIDError(VKError):
    description = "Invalid application API ID "
    details = "Find the app in the administrated list in settings: http://vk.com/apps?act=settings" \
              " And set the correct API_ID in the request."
    pass


# Code 113
class InvalidUserIDError(VKError):
    description = "Invalid user id"
    details = "Make sure that you use a correct id. You can get an id using a screen name with the" \
              " utils.resolveScreenName(https://vk.com/dev/utils.resolveScreenName) method"
    pass


# Code 150
class InvalidTimestampError(VKError):
    description = "Invalid timestamp"
    details = "You may get a correct value with the " \
              "utils.getServerTime(https://vk.com/dev/utils.getServerTime) method."
    pass


# Code 200
class AccessToAlbumDeniedError(VKError):
    description = "Access to album denied"
    details = "Make sure you use correct ids (owner_id is always positive for users, negative for communities) " \
              "and the current user has access to the requested content in the full version of the site."
    pass


# Code 201
class AccessToAudioDeniedError(VKError):
    description = "Access to audio denied"
    details = "Make sure you use correct ids (owner_id is always positive for users, negative for communities) " \
              "and the current user has access to the requested content in the full version of the site."
    pass


# Code 203
class AccessToGroupDeniedError(VKError):
    description = "Access to group denied"
    details = "Make sure that the current user is a member or admin of the " \
              "community (for closed and private groups and events)"
    pass


# Code 300
class AlbumFullError(VKError):
    description = "This album is full"
    details = "You need to delete the odd objects from the album or use another album."
    pass


# Code 500
class AppPermissionDeniedError(VKError):
    description = "Permission denied. You must enable votes processing in application settings"
    details = "Check the app settings: http://vk.com/editapp?id={Your API_ID}&section=payments"
    pass


# Code 600
class PermissionDeniedWithObjectsError(VKError):
    description = "Permission denied. You have no access to operations specified with given object(s)"
    details = "Permission denied. You have no access to operations specified with given object(s)"
    pass


# Code 603
class AdsError(VKError):
    description = "Some ads error occurred"
    details = "Some ads error occured"
    pass
