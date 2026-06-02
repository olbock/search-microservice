"""Search Microservice for CS361.

Communication pipe: text files.
The microservice reads requests/search_request.txt and writes responses/search_response.txt.
Run this file in one terminal, then run test_program.py in another terminal.
"""

from pathlib import Path
from difflib import SequenceMatcher
import time

REQUEST_FILE = Path("requests/search_request.txt")
RESPONSE_FILE = Path("responses/search_response.txt")

# Sample data for the Assignment Tracker main program.
# You can add or change these items later.
DATABASE = [
    {"name": "Calculus Homework 5", "category": "assignments"},
    {"name": "Biology Exam", "category": "exams"},
    {"name": "Chemistry Lab Report", "category": "assignments"},
    {"name": "Discussion Post", "category": "assignments"},
    {"name": "Physics Quiz", "category": "quizzes"},
]


def parse_request(text: str) -> dict[str, str]:
    """Parse key=value lines from the request file."""
    request_data: dict[str, str] = {}
    for line in text.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            request_data[key.strip()] = value.strip()
    return request_data


def get_similarity_score(first: str, second: str) -> float:
    """Return a similarity score between 0 and 1."""
    return SequenceMatcher(None, first.lower(), second.lower()).ratio()


def find_closest_match(query, category):
    """Find the closest matching item from the database."""
    possible_items = DATABASE
    if category:
        possible_items = [item for item in DATABASE if item["category"].lower() == category.lower()]

    if not possible_items:
        return False, "No Match Found", 0.0

    best_item = max(possible_items, key=lambda item: get_similarity_score(query, item["name"]))
    score = similarity(query, best_item["name"])

    # This threshold prevents a random weak match from being returned.
    if score < 0.35:
        return False, "No Match Found", score

    return True, best_item["name"], score


def write_response(match_found: bool, closest_match: str, confidence_score: float) -> None:
    """Write the response file for the requesting program."""
    RESPONSE_FILE.parent.mkdir(exist_ok=True)
    RESPONSE_FILE.write_text(
        f"match_found={str(match_found).lower()}\n"
        f"closest_match={closest_match}\n"
        f"confidence_score={confidence_score:.2f}\n",
        encoding="utf-8",
    )


def handle_request() -> None:
    """Read the request file, process the search, and write the response."""
    request_text = REQUEST_FILE.read_text(encoding="utf-8")
    request_data = parse_request(request_text)

    query = request_data.get("query", "")
    category = request_data.get("category")

    if not query:
        write_response(False, "No query provided", 0.0)
    else:
        match_found, closest_match, confidence_score = find_closest_match(query, category)
        write_response(match_found, closest_match, confidence_score)

    # Remove the request so the same request is not processed repeatedly.
    REQUEST_FILE.unlink()


def main() -> None:
    print("Search Microservice is running...")
    print("Waiting for requests/search_request.txt")

    while True:
        if REQUEST_FILE.exists():
            print("Request received. Processing search...")
            handle_request()
            print("Response written to responses/search_response.txt")
        time.sleep(1)


if __name__ == "__main__":
    main()
