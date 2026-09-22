import re

from config import COURSE_FEES


def workflow(text):
    text_lower = text.lower()

    # Find course codes mentioned in the question
    courses = []

    for code in COURSE_FEES:
        if code.lower() in text_lower:
            courses.append(code)

    # Fee question
    if len(courses) == 1 and "fee" in text_lower:
        return f"{courses[0]} fee is Rs. {COURSE_FEES[courses[0]]}"

    # Scholarship total
    if len(courses) >= 2 and "scholarship" in text_lower:
        match = re.search(r"(\d+)\s*%", text_lower)

        if match:
            scholarship = int(match.group(1))
            total = sum(COURSE_FEES[c] for c in courses)
            final_amount = total * (100 - scholarship) / 100

            return f"Total after {scholarship}% scholarship: Rs. {final_amount:.0f}"

    return "No rule matched."
    

QUESTIONS = [
    "What is the fee for AI202?",
    "What is the total fee for CS101 and AI202 after a 10% scholarship?",
    "Is DS303 more expensive than CS101, and by how much?",
    "Write a two-line welcome message for new AI students.",
]


for question in QUESTIONS:
    print("Q:", question)
    print("A:", workflow(question))
    print()