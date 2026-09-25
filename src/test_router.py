from agent import route


tests = [
    ("What is the last date for fee payment?", "info"),
    ("What is the tuition fee for B.Tech?", "info"),
    ("When does the academic session begin?", "info"),
    ("What is the last date to apply for KIITEE?", "info"),
    ("What documents are required for admission?", "info"),
    ("When are the semester examinations scheduled?", "info"),
    ("What is the attendance requirement?", "info"),
    ("What is the hostel fee?", "info"),

    ("Write an email asking for a fee extension.", "service"),
    ("Draft a request to the examination office.", "service"),
    ("Prepare an email requesting my internship certificate.", "service"),
    ("Write a formal request for a duplicate ID card.", "service"),
    ("Draft an email asking about my scholarship status.", "service"),
    ("Prepare a request to correct my name in the records.", "service"),

    ("What's the weather today?", "out_of_scope"),
    ("Write me a poem about friendship.", "out_of_scope"),
    ("Who won yesterday's cricket match?", "out_of_scope"),
    ("Tell me a joke.", "out_of_scope"),
]


ok = 0

for q, expected in tests:
    predicted = route(q)

    print()
    print("Question :", q)
    print("Expected :", expected)
    print("Predicted:", predicted)

    if predicted == expected:
        ok += 1


print()
print(f"router accuracy: {ok}/{len(tests)}")