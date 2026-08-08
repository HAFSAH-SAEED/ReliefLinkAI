"""Backboard memory verification script for ReliefLink AI.

This script tests whether facts shared in one fresh thread can be remembered in
another fresh thread that uses the same persisted ReliefLink assistant.
"""

from services.backboard_client import create_or_load_assistant, create_thread, send_message


EXPECTED_MEMORY_TERMS = ("hafsa", "swat", "5", "five")


def main() -> None:
    """Run a two-thread memory test and print the assistant's final reply."""
    assistant = create_or_load_assistant()

    first_thread = create_thread(assistant)
    send_message(first_thread, "My name is Hafsa.")
    send_message(first_thread, "My city is Swat.")
    send_message(first_thread, "My family has 5 members.")

    second_thread = create_thread(assistant)
    reply = send_message(second_thread, "What do you remember about me?")

    print(reply)

    normalized_reply = reply.lower()
    remembered_name = "hafsa" in normalized_reply
    remembered_city = "swat" in normalized_reply
    remembered_family_size = "5" in normalized_reply or "five" in normalized_reply

    if remembered_name and remembered_city and remembered_family_size:
        print("Memory test passed.")
    else:
        print("Memory test failed.")


if __name__ == "__main__":
    main()
