from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_MODE_64
from tp2.utils.config import logger, MAX_DISASM_LINES

def get_capstone_analysis(binary_payload: bytes, arch: int = 32) -> list[str]:
    cpu_mode = CS_MODE_64 if arch == 64 else CS_MODE_32
    reverse_engine = Cs(CS_ARCH_X86, cpu_mode)
    
    asm_instructions = []
    
    for operation in reverse_engine.disasm(binary_payload, 0x00000000):
        if len(asm_instructions) >= MAX_DISASM_LINES:
            break
            
        formatted_op = f"[{operation.address:#06x}]  {operation.mnemonic:<7} {operation.op_str}"
        asm_instructions.append(formatted_op)

    return asm_instructions
