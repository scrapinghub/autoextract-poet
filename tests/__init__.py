import json
import os


def load_fixture(name):
    path = os.path.join(
        os.path.dirname(__file__),
        f"fixtures/{name}"
    )
    with open(path, 'r') as f:
        return json.loads(f.read())
