from abc import ABCMeta

from fisher.config import ConfigurationManager

_config = ConfigurationManager()

class MessageConnector(metaclass=ABCMeta):
    def send(self, target: str, message: str):
        raise NotImplementedError("This is an abstract method!")


class TwilioConnector(MessageConnector):
    def __init__(self, account_sid=_config.twilio_sid, auth_token=_config.twilio_token, source=_config.twilio_source):
        super().__init__()
        from twilio.rest import Client
        self._client = Client(password=auth_token, username=account_sid)
        self._source = source
        super().__init__()

    def send(self, target: str, message: str):
        self._client.api.account.messages.create(to=target, from_=self._source, body=message)


class LinuxNotifyConnector(MessageConnector):
    def __init__(self):
        super().__init__(self)          #just a warning message
        import platform
        if "Linux" not in platform:
            print("Warning! Your OS has not reported itself as Linux. This notification Connector may fail.")

    def send(self, target: str, message: str):
        from subprocess import call
        call(["notify-send", message])


_service_table = {
    "desktop": LinuxNotifyConnector,
    "sms": TwilioConnector
}