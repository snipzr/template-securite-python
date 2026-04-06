import re
from tp2.utils.config import logger, MIN_STRING_LEN

def get_shellcode_strings(target_buffer: bytes, threshold: int = MIN_STRING_LEN) -> list[str]:
    decoded_layer = target_buffer.decode("ascii", errors="replace")
    
    ascii_regex = r'[\x20-\x7E]{' + str(threshold) + r',}'
    discovered_artifacts = re.findall(ascii_regex, decoded_layer)

    if discovered_artifacts:
        logger.info(f"Artefacts ASCII extraits : {len(discovered_artifacts)} item(s)")
        for artifact in discovered_artifacts:
            logger.debug(f"  --> {artifact}")
    else:
        logger.info("Aucune signature lisible intercepter")

    return discovered_artifacts
