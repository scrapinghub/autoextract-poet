import contextlib
import json
import os
import random


def load_fixture(name):
    path = os.path.join(
        os.path.dirname(__file__),
        f"fixtures/{name}"
    )
    with open(path, 'r') as f:
        return json.loads(f.read())


@contextlib.contextmanager
def temp_seed(seed):
    state = random.getstate()
    random.seed(seed)
    try:
        yield
    finally:
        random.setstate(state)


def crazy_monkey_nullify(data, drop_prob=0.5):
    if isinstance(data, list):
        return [crazy_monkey_nullify(value, drop_prob) for value in data]
    elif isinstance(data, dict):
        return {k: (None if drop_prob <= random.random()
                    else crazy_monkey_nullify(v, drop_prob))
                for k, v in data.items()}
    else:
        return data
