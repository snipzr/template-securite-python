import requests
from src.tp3.utils.config import logger
from src.tp3.utils.captcha import Captcha

class Session:
    """
    Class representing a session to solve a captcha and submit a flag.
    """

    def __init__(self, url):
        self.url = url
        self.captcha_value = ""
        self.flag_guess = 1000
        self.final_flag_buffer = ""
        self.response_bucket = ""
        
        self.http_sess = requests.Session()

    def prepare_request(self):
        """
        Prepares the request for sending by capturing and solving the captcha.
        """
        captcha = Captcha(self.url, self.http_sess)
        captcha.capture()
        captcha.solve()

        self.captcha_value = captcha.get_value()
        logger.info(f"captcha lu : {self.captcha_value} | flag tester : {self.flag_guess}")

    def submit_request(self):
        """
        Sends the flag and captcha.
        """
        current_try_payload = {
            "flag": str(self.flag_guess),
            "captcha": self.captcha_value,
            "submit": "Envoyer",
        }

        resp = self.http_sess.post(self.url, data=current_try_payload)
        self.response_bucket = resp.text

    def process_response(self):
        """
        Processes the response.
        """

    def get_flag(self):
        """
        Returns the valid flag.

        Returns:
            str: The valid flag.
        """
        return self.valid_flag
