from httpx import Client
from config import settings
from clients.event_hooks import curl_event_hook


def get_public_http_builder() -> Client:
    """
    Функция создаёт экземпляр httpx.Client с базовыми настройками.
    :return: Готовый к использованию объект httpx.Client.
    """
    return Client(timeout=settings.http_client.timeout, base_url=settings.http_client.client_url, event_hooks={"request": [curl_event_hook]})