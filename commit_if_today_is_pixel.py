# commit_if_today_is_pixel.py
import json
import os
import subprocess
from datetime import datetime

TODAY = datetime.today().strftime("%Y-%m-%d")

# Load pixel days
if not os.path.exists("pixel_days.json"):
    print("❌ Run generate_future_pixel_days.py first!")
    exit(1)

with open("pixel_days.json") as f:
    pixel_days = set(json.load(f))

if TODAY not in pixel_days:
    print(f"📅 {TODAY} is not a 'LOVE MENTEE' day. Skipping.")
    exit(0)

print(f"🎉 {TODAY} is a LOVE MENTEE pixel day! Making 12 commits...")

# Initialize repo if needed
if not os.path.exists(".git"):
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "config", "user.name", "SyabAhmad"], check=True)
    subprocess.run(["git", "config", "user.email", "syabblogger@gmail.com"], check=True)
    with open("README.md", "w") as f:
        f.write("# LOVE MENTEE ❤️\nFuture contribution art.\n")
    subprocess.run(["git", "add", "README.md"], check=True)
    subprocess.run(["git", "commit", "-m", "Initial"], check=True)

# ML methods
methods = [
    "Linear Regression", "Random Forest", "XGBoost", "SVM", "KNN", "Naive Bayes",
    "Neural Network", "CNN", "RNN", "Transformer", "BERT", "GAN"
]

# Make 12 commits
for i, method in enumerate(methods, 1):
    with open("ml_methods.txt", "a") as f:
        f.write(f"{method} ({TODAY})\n")
    subprocess.run(["git", "add", "ml_methods.txt"], check=True)
    subprocess.run(["git", "commit", "-m", f"Add: {method}"], check=True)

# Optional: Auto-push (if remote is set)
# subprocess.run(["git", "push"], check=False)

print(f"✅ Done! 12 commits for {TODAY}")