import io
from urllib.parse import urljoin
from PIL import Image
from src.tp3.utils.config import logger

class Captcha:
    def __init__(self, url, http_session=None):
        self.url = url
        self.http = http_session
        self.image = None
        self.value = ""

    def solve(self):
        """
        Fonction permettant la résolution du captcha.
        """
        self.value = "FIXME"

    def capture(self):
        """
        Stocke l'image captcha envoyée pour cette session en mémoire RAM.
        """
        captcha_endpoint = urljoin(self.url, "../captcha.php")
        logger.debug(f"dl depuis {captcha_endpoint}")

        res = self.http.get(captcha_endpoint)
        if res.status_code == 200:
            captcha_snapshot = io.BytesIO(res.content)
            self.image = Image.open(captcha_snapshot)
        else:
            logger.error(f"erreur lors du download du captcha : {res.status_code}")

    def get_value(self):
        """
        Fonction retournant la valeur du captcha
        """
        return self.value
