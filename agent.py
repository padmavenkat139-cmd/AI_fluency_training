import json

from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = """
You are a helpful college assistant.

Important:
- Never guess course fees.
- Use get_course_fee when you need a course fee.
- Use calculator for arithmetic.
- Answer the user clearly and briefly.
"""


def agent(question):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for _ in range(5):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        messages.append(message)

        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            function = TOOL_FUNCTIONS[function_name]
            result = function(**arguments)

            print(
                f"Tool: {function_name}({arguments}) -> {result}"
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )

    return "Agent stopped after too many tool calls."


if __name__ == "__main__":
    banner("Tool-Using Agent")

    for question in QUESTIONS:
        print("Q:", question)
        print("A:", agent(question))
        print()