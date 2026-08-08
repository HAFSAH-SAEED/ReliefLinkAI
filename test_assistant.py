"""Small helper script to verify ReliefLink assistant creation and reuse.

Run this script after setting BACKBOARD_API_KEY. It does not create threads,
send chat messages, or enable memory; it only tests assistant persistence.
"""

from services.backboard_client import create_or_load_assistant


def main() -> None:
    """Create or load the ReliefLink assistant and print the result."""
    result = create_or_load_assistant()
    status = "newly created" if result.was_created else "loaded from reliefLink.json"

    print(f"Assistant ID: {result.assistant_id}")
    print(f"Status: {status}")


if __name__ == "__main__":
    main()
