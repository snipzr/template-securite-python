import io
from urllib.parse import urljoin
import pytesseract
from PIL import Image, ImageFilter
from src.tp3.utils.config import logger

class Captcha:
    def __init__(self, url, http_session=None):
        self.url = url
        self.http = http_session
        self.image = None
        self.value = ""

    def solve(self):
        """
        Traitement d'image pour aider l'OCR, puis extraction textuelle.
        """
        if self.image is None:
            logger.warning("pas d'image a resoudre")
            self.value = ""
            return

        img_processed = self.image.convert("L") 
        
        limit_seuil = 128
        img_processed = img_processed.point(lambda px: 255 if px > limit_seuil else 0)
        
        img_processed = img_processed.filter(ImageFilter.SHARPEN)
        
        config_ocr = "--psm 7 -c tessedit_char_whitelist=0123456789"
        raw_text = pytesseract.image_to_string(img_processed, config=config_ocr)

        self.value = raw_text.strip()
        logger.debug(f"captcha resolu : '{self.value}'")

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
