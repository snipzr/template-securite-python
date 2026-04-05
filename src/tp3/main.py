from src.tp3.utils.config import logger
from src.tp3.utils.session import Session

def main():
    logger.info("Debut TP3 - Brute force Captcha")

    ip_target = "31.220.95.27:9002"
    challenge_list = {"1": f"http://{ip_target}/captcha1/"}



    for idx in challenge_list:
        target_url = challenge_list[idx]
        logger.info(f"--> Target {idx} : {target_url}")
        sess = Session(target_url)
        sess.prepare_request()
        sess.submit_request()

        while not sess.process_response():
            sess.prepare_request()
            sess.submit_request()

        logger.info("Smell good !")
        logger.info(f"Le flag de {target_url} est : {sess.get_flag()}")

if __name__ == "__main__":
    main()
