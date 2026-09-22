from config import client, MODEL, QUESTIONS, banner

banner("Plain LLM Chatbot")

for question in QUESTIONS:
    print("Q:", question)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful college assistant."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    print("A:", response.choices[0].message.content)
    print()