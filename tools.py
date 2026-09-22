import ast
import operator as op

from config import COURSE_FEES


def get_course_fee(course_code):
    return COURSE_FEES.get(course_code.upper())


# Safe calculator
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
}


def calculator(expression):
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.BinOp):
            operator = ALLOWED_OPERATORS.get(type(node.op))

            if operator is None:
                raise ValueError("Operator not allowed")

            return operator(
                evaluate(node.left),
                evaluate(node.right)
            )

        raise ValueError("Expression not allowed")

    return evaluate(tree)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Get the fee for a course code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string"
                    }
                },
                "required": ["course_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a basic arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


TOOL_FUNCTIONS = {
    "get_course_fee": get_course_fee,
    "calculator": calculator,
}


if __name__ == "__main__":
    print("get_course_fee('ai202') ->", get_course_fee("ai202"))
    print("calculator('(12000 + 18000) * 0.9') ->",
          calculator("(12000 + 18000) * 0.9"))
    print("calculator('15000 - 12000') ->",
          calculator("15000 - 12000"))