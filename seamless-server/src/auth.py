from src.logging import initialize_logger
import requests

logger = initialize_logger(__name__)


def google_auth_check(token):
    try:
        response = requests.get(
            "https://www.googleapis.com/oauth2/v3/tokeninfo",
            params={"access_token": token},
        )
        if response.status_code == 200:
            token_info = response.json()
            return token_info
        else:
            return None
    except Exception as e:
        logger.info(e)
        return None
