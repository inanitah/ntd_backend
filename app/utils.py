import requests


def perform_operation(operation_type: str) -> str:
    if operation_type == "addition":
        return str(1 + 1)
    elif operation_type == "subtraction":
        return str(1 - 1)
    elif operation_type == "multiplication":
        return str(1 * 1)
    elif operation_type == "division":
        return str(1 / 1)
    elif operation_type == "square_root":
        return str(1 ** 0.5)
    elif operation_type == "random_string":
        response = requests.get(
            "https://www.random.org/strings/?num=1&len=8&digits=on&upperalpha=on"
            "&loweralpha=on&unique=on&format=plain&rnd=new"
        )
        return response.text.strip()
    else:
        raise ValueError("Invalid operation type")
