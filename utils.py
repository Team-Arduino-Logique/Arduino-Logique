import os


def resource_path(relative_path: str) -> str:
    new_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
    print("new_path:", new_path)
    return new_path
