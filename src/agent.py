import json
import time
from llm import llm


def audit(event):
    with open("audit.jsonl", "a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {"t": time.time(), **event}
            ) + "\n"
        )


def route(q):
    label = llm(
        "Classify the student message. Reply with exactly one word:\n"
        "info (asks for facts from university documents)\n"
        "service (asks you to write or prepare a request, email or form)\n"
        "out_of_scope (anything else)\n\n"
        "Message: " + q,
        fast=True
    ).strip().lower()

    return label if label in (
        "info",
        "service",
        "out_of_scope"
    ) else "info"


def draft_email(q):
    return llm(
        "Draft a short, polite email to the university office "
        "for this request. "
        "Do not invent dates, names or policies; "
        "use [placeholders] instead.\n\n"
        "Request: " + q
    )