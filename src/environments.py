import yaml
from pathlib import Path

def load_environment(name, folder="configs"):
    path = Path(folder) / f"{name}.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

def list_environments(folder="configs"):
    return [p.stem for p in Path(folder).glob("*.yaml")]

def validate_env(env):
    required = ["name", "platform", "ib_path", "server", "user", "cluster"]
    missing = [k for k in required if k not in env]
    if missing:
        raise ValueError(f"Missing fields: {missing}")
    return True
