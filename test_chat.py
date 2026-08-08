"""Small helper script to test Backboard conversation threads.

This script creates or loads the ReliefLink assistant, creates one fresh thread,
sends a single message, and prints only the assistant reply. It does not modify
the Streamlit UI, implement memory, or persist thread IDs.
"""

from services.backboard_client import create_or_load_assistant, create_thread, send_message


def main() -> None:
    """Send a basic test message through a fresh ReliefLink thread."""
    assistant = create_or_load_assistant()
    thread = create_thread(assistant)
    reply = send_message(thread, "Hello!")

    print(reply)


if __name__ == "__main__":
    main()
