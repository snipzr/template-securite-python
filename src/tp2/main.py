import os
from tp2.utils.config import logger, INFECTED_SAMPLES, hex_to_bytes, print_report_block
from tp2.analyse.strings_extract import get_shellcode_strings
from tp2.analyse.emu_analysis import get_pylibemu_analysis
from tp2.analyse.disasm_analysis import get_capstone_analysis
from tp2.analyse.llm_analysis import get_llm_analysis

def main():
    logger.info("*" * 65)
    logger.info("TP2 --> analyse de shellcode")
    logger.info("*" * 65)

    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("Attention : clé OpenAI manquante, le rapport IA sera ignorer")

    for threat_name, hex_signature in INFECTED_SAMPLES.items():
        logger.info(f"\n Traitement de la signature : {threat_name}")
        
        malicious_bytes = hex_to_bytes(hex_signature)

        trace_dyn = get_pylibemu_analysis(malicious_bytes)
        print_report_block("EMULATION DYNAMIQUE (PYLIBEMU)", trace_dyn)

        ascii_arts = get_shellcode_strings(malicious_bytes)
        print_report_block("EXTRACTION DE CHAINES (STRINGS)", ascii_arts)

        opcode_dump = get_capstone_analysis(malicious_bytes, arch=32)
        print_report_block("RETRO-INGENIERIE STATIQUE (CAPSTONE)", opcode_dump)

        ai_insight = get_llm_analysis(opcode_dump, emu_report=trace_dyn)
        print_report_block("EXPERT IA (RAPPORTEUR OPENAI)", ai_insight)

    logger.info("*" * 65)
    logger.info("Investigation terminer pour tous les échantillons")
    logger.info("*" * 65)

if __name__ == "__main__":
    main()
