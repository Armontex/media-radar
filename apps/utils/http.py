import requests
from urllib.parse import urljoin
from enum import Enum
from ..core.logger import logger


class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"


class HTTPClient:

    DEFAULT_TIMEOUT = 5  # Seconds

    def __init__(self, base_url: str) -> None:
        self._session = requests.Session()
        self._base_url = base_url

    @property
    def base_url(self) -> str:
        return self._base_url

    def _request(self,
                 method: RequestMethod,
                 path: str = "",
                 **kwargs) -> requests.Response:
        url = urljoin(self._base_url, path)
        kwargs.setdefault("timeout", self.DEFAULT_TIMEOUT)

        logger.info("Выполняется запрос",
                    extra={
                        "method": method.value,
                        "url": url
                    })

        response = self._session.request(method.value, url, **kwargs)
        try:
            response.raise_for_status()
            return response
        except requests.HTTPError:
            logger.error(
                "HTTP ошибка",
                extra={
                    "method": method.value,
                    "url": url,
                    "status": response.status_code,
                    "body": response.text,
                },
            )
            raise

        except requests.RequestException as e:
            logger.error(
                "Ошибка запроса",
                extra={
                    "method": method.value,
                    "url": url,
                    "error": str(e),
                },
            )
            raise

    def get(self, path: str = "", **kwargs) -> requests.Response:
        return self._request(RequestMethod.GET, path, **kwargs)

    def post(self, path: str = "", **kwargs) -> requests.Response:
        return self._request(RequestMethod.POST, path, **kwargs)

    def close(self):
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


__all__ = ["HTTPClient"]