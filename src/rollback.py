import json
from pathlib import Path
from datetime import datetime

ROLLBACK_LOG = "rollback_history.json"

def record_release(env_name, version, cf_path):
    history = load_history()
    history.append({
        "env": env_name,
        "version": version,
        "cf": cf_path,
        "deployed_at": datetime.utcnow().isoformat(),
        "action": "deploy",
    })
    save_history(history)

def load_history():
    p = Path(ROLLBACK_LOG)
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))

def save_history(history):
    Path(ROLLBACK_LOG).write_text(
        json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")

def previous_version(env_name):
    history = [h for h in load_history() if h["env"] == env_name and h["action"] == "deploy"]
    if len(history) < 2:
        return None
    return history[-2]

def rollback(env_name, deploy_fn):
    prev = previous_version(env_name)
    if not prev:
        raise RuntimeError("No previous version to rollback")
    result = deploy_fn(prev["cf"])
    history = load_history()
    history.append({
        "env": env_name,
        "version": prev["version"],
        "cf": prev["cf"],
        "deployed_at": datetime.utcnow().isoformat(),
        "action": "rollback",
    })
    save_history(history)
    return result
