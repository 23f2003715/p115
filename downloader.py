import os
import requests

def download_file(url):
    os.makedirs("temp", exist_ok=True)

    filename = url.split("/")[-1].split("?")[0]

    if filename == "":
        filename = "data.csv"

    filepath = os.path.join("temp", filename)

    r = requests.get(url, timeout=60)
    r.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(r.content)

    return filepath