import requests
from rest_framework.status import HTTP_408_REQUEST_TIMEOUT, HTTP_429_TOO_MANY_REQUESTS

UNKNOWN_STATUS = -1


class FbRQ:
    def __init__(self, token, protocol=None, domain=None, version=None):
        if protocol is None:
            protocol = 'https'
        if domain is None:
            domain = "probe.fbrq.cloud"
        if version is None:
            version = 1

        self.__token = token
        self.base_url = f"{protocol}://{domain}/v{version}"

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.__token}"}

    def send_message(self, id: int, phone: int, text: str) -> int:
        try:
            response = requests.post(
                url=f"{self.base_url}/send/{id}",
                json={
                  "id": id,
                  "phone": phone,
                  "text": text
                },
                headers=self.headers
            )
        except requests.exceptions.Timeout:
            return HTTP_408_REQUEST_TIMEOUT
        except requests.exceptions.TooManyRedirects:
            return HTTP_429_TOO_MANY_REQUESTS
        except requests.exceptions.RequestException:
            return UNKNOWN_STATUS

        return response.status_code

