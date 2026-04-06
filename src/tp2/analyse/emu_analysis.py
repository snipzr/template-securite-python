from tp2.utils.config import logger

try:
    from pylibemu import Emulator
    HAS_PYLIB = True
except ImportError:
    HAS_PYLIB = False

def get_pylibemu_analysis(malicious_buffer: bytes) -> str | None:
    if not HAS_PYLIB:
        return None

    execution_trace = None
    try:
        sandbox_env = Emulator()
        sandbox_env.run(malicious_buffer)

        intercepted_calls = sandbox_env.emu_profile_output

        if not intercepted_calls:
            execution_trace = "Aucun appel api win32 detecté par l'émulateur"
        else:
            if isinstance(intercepted_calls, bytes):
                execution_trace = intercepted_calls.decode("utf-8", errors="ignore")
            else:
                execution_trace = intercepted_calls

        sandbox_env.free()
        
    except Exception as emu_crash:
        execution_trace = f"Erreur critique de la sandbox : {emu_crash}"

    return execution_trace
