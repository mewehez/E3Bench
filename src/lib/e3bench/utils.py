from pathlib import Path
import shutil

THIS_DIR = Path(__file__).parent.resolve()
PROFILERS_DIR = THIS_DIR / "profilers"


def profiler_path_from_name(profiler_name: str) -> Path:
    valid = ["tegrastats", "smiprof", "inaprof"]
    if not any(profiler_name.startswith(v) for v in valid) :
        raise ValueError(f"Invalid option {profiler_name}. Use one of {valid}")
    
    if profiler_name == "tegrastats":
        # Check that the tegrastats command is available
        if shutil.which("tegrastats") is None:
            raise FileNotFoundError("The 'tegrastats' command was not found in PATH.")
        path = PROFILERS_DIR / "tegrastats/profiler.sh"
    elif profiler_name == "smiprof":
        # Check that nvidia-smi is available
        if shutil.which("nvidia-smi") is None:
            raise FileNotFoundError("The 'nvidia-smi' command was not found in PATH.")
        path = PROFILERS_DIR / "smiprof/profiler.sh"
    else:
        # Expect pattern like "inaprof-<rail>"
        parts = profiler_name.split("-", 1)
        if len(parts) != 2 or not parts[1]:
            raise ValueError("For 'inaprof', specify a rail name, e.g. 'inaprof-VDD_IN'")
        rail_name = parts[1]
        path = PROFILERS_DIR / f"inaprof/bin/{rail_name}"

    if not path.exists():
        raise FileNotFoundError(f"Profiler program {path} not found.")
    
    return path
    

__all__ = ["profiler_path_from_name"]
