"""MCP entry point: provide __file__ and explicitly run build_all via __main__."""
from pathlib import Path
p=Path('/root/Blender/DELL-C6420/v001/scripts/build_c6420.py')
namespace={'__name__':'__main__','__file__':str(p)}
exec(compile(p.read_text(),str(p),'exec'),namespace)
