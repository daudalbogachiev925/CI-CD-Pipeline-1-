import subprocess
from pathlib import Path
from datetime import datetime

def find_platform(version="8.3"):
    for c in Path("C:/Program Files/1cv8").glob(f"{version}*"):
        exe = c / "bin" / "1cv8.exe"
        if exe.exists():
            return str(exe)
    raise FileNotFoundError("1cv8.exe not found")

def deploy_cf(cf_path, env):
    platform = env.get("platform") or find_platform()
    cmd = [
        platform, "DESIGNER",
        "/S", f"{env['server']}/{env['cluster']}",
        "/N", env["user"],
        "/P", env["password"],
        "/UpdateCfg", cf_path,
        "/UpdateDBCfg",
        "/Out", "deploy.log",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    log = Path("deploy.log").read_text(encoding="utf-8", errors="ignore")
    if result.returncode != 0 or "Ошибка" in log:
        raise RuntimeError(f"Deploy failed: {log[:500]}")
    return {"deployed_at": datetime.utcnow().isoformat(),
            "env": env["name"], "cf": cf_path}

def deploy_extension(epf_path, env, extension_name):
    platform = env.get("platform") or find_platform()
    cmd = [
        platform, "DESIGNER",
        "/S", f"{env['server']}/{env['cluster']}",
        "/N", env["user"], "/P", env["password"],
        "/LoadExternalDataProcessorOrReportFromFile", epf_path,
        "/UpdateDBCfg",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
    return {"deployed_at": datetime.utcnow().isoformat(),
            "extension": extension_name}
