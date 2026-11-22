"""
Index a text file through the running app.

Usage: python index_file.py <path-to-text-file> <index-name> [app-url]
Example: python index_file.py sample_data/universal_declaration_of_human_rights.txt first-index
"""

import json
import sys
import urllib.request


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    path, index_name = sys.argv[1], sys.argv[2]
    app_url = sys.argv[3] if len(sys.argv) > 3 else "http://localhost:8081"

    with open(path, encoding="utf-8") as f:
        text = f.read()

    payload = json.dumps({"text": text, "index_name": index_name}).encode("utf-8")
    request = urllib.request.Request(
        app_url.rstrip("/") + "/api/index/",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        print(response.read().decode("utf-8"))


if __name__ == "__main__":
    main()
