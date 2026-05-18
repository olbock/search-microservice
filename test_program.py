"""Test program for the Search Microservice.

This program does not directly call the microservice. It only writes a request
text file and reads the response text file.
"""

from pathlib import Path
import time

REQUEST_FILE = Path("requests/search_request.txt")
RESPONSE_FILE = Path("responses/search_response.txt")


def main() -> None:
    REQUEST_FILE.parent.mkdir(exist_ok=True)
    RESPONSE_FILE.parent.mkdir(exist_ok=True)

    if RESPONSE_FILE.exists():
        RESPONSE_FILE.unlink()

    print("Writing search request...")
    REQUEST_FILE.write_text(
        "query=calculus homework\n"
        "category=assignments\n"
        "limit=1\n",
        encoding="utf-8",
    )

    print("Waiting for response...")
    while not RESPONSE_FILE.exists():
        time.sleep(1)

    response = RESPONSE_FILE.read_text(encoding="utf-8")
    print("Response received:")
    print(response)


if __name__ == "__main__":
    main()
