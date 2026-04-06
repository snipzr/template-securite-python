import os
from tp2.utils.config import logger, LLM_MODEL, LLM_MAX_INSTRUCTIONS

def get_llm_analysis(asm_list: list[str], emu_report: str | None = None) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    if not asm_list:
        return "Aucune instruction valide a analyser."

    safe_slice = asm_list[:LLM_MAX_INSTRUCTIONS]
    str_payload = "\n".join(safe_slice)

    if len(asm_list) > LLM_MAX_INSTRUCTIONS:
        str_payload += f"\n... [Tronqué : {len(asm_list) - LLM_MAX_INSTRUCTIONS} instructions passées sous silence]"

    context_prompt = (
        "Vous agissez en tant qu'Analyste Malware et Expert en rétro-ingénierie. "
        "Exécutez une analyse forensique de ce dump d'instructions.\n"
        "Restituez un rapport francophone très concis structuré en 4 points :\n"
        "1) Catégorie du code (ex: Downloader, Reverse Shell...)\n"
        "2) Déroulement pas-à-pas de l'attaque\n"
        "3) Appels systèmes ou comportements furtifs repérés\n"
        "4) Score de sévérité ciblé\n\n"
        f"--- VECTEUR ASSEMBLEUR ---\n{str_payload}\n"
    )

    if emu_report and "Aucun appel" not in emu_report:
        context_prompt += f"\n--- TRACE D'EXECUTION (SANDBOX) ---\n{emu_report}\n"

    try:
        from openai import OpenAI
        bot = OpenAI(api_key=api_key)

        chat_completion = bot.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "Tu es un assistant de cybersécurité offensif expert en shellcodes."},
                {"role": "user", "content": context_prompt}
            ]
        )

        insight = chat_completion.choices[0].message.content
        return insight if insight else "Echec de generation de la reponse cote modele."

    except Exception as llm_fault:
        return f"Erreur de communication IA : {llm_fault}"
