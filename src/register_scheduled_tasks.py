import subprocess
from pathlib import Path

bat_path = Path(__file__).resolve().parent.parent / "actualizar_dashboard.bat"
assert bat_path.exists(), f"Batch script not found: {bat_path}"

tasks = [
    ("QaliKay_Sync_Dashboard_0730", "07:30"),
    ("QaliKay_Sync_Dashboard_1530", "15:30")
]

for name, time_str in tasks:
    cmd = [
        "schtasks.exe", "/create",
        "/tn", name,
        "/tr", f'"{str(bat_path)}"',
        "/sc", "daily",
        "/st", time_str,
        "/f"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Task {name} [{time_str}]: Exit Code = {res.returncode}")
    if res.stdout:
        print("   STDOUT:", res.stdout.strip())
    if res.stderr:
        print("   STDERR:", res.stderr.strip())

print("\nVerificando tareas registradas en Windows:")
verify_res = subprocess.run(["schtasks.exe", "/query", "/tn", "QaliKay_Sync_Dashboard_0730", "/fo", "LIST"], capture_output=True, text=True)
print(verify_res.stdout.strip())
