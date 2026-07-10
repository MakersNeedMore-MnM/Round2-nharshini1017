import os
import subprocess
import time
import sys   # <-- ADD THIS

INPUT_VIDEO = "INPUT_VIDEO.mp4"

os.makedirs("outputs", exist_ok=True)

print("\n🚦 Running all violation modules separately...\n")

python_exe = sys.executable   # <-- THIS IS THE FIX

scripts = [
    ("Helmetless Riding", [python_exe, "helmetless_violation.py"]),
    ("Triple Riding", [python_exe, "triple_riding.py", "--input", INPUT_VIDEO, "--output", "outputs/triple_riding_output.mp4"]),
    ("Wrong Way", [python_exe, "wrong_way.py"]),
    ("Mobile Usage", [python_exe, "mobile_usage.py"])
]

for name, cmd in scripts:
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"▶ Running: {name}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    start = time.time()
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Completed {name} in {round(time.time() - start, 2)} sec")
    except subprocess.CalledProcessError:
        print(f"❌ Error while running {name}")

print("\n✅ DONE ✅ All outputs are generated inside outputs/ and logs/")
print("📌 logs/violations.csv will be used for dashboard")