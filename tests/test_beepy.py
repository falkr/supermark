from beepy import beep
from time import sleep

# for sound in range(8):
#    beep(sound=sound)
#    sleep(1)

beep(sound=5)

import click

click.clear()

from rich.console import Console

console = Console()

test_data = [
    {
        "jsonrpc": "2.0",
        "method": "sum",
        "params": [None, 1, 2, 4, False, True],
        "id": "1",
    },
    {"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},
    {"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": "2"},
]


def test_log():
    enabled = False
    context = {
        "foo": "bar",
    }
    movies = ["Deadpool", "Rise of the Skywalker"]
    console.log("Hello from", console, "!")
    console.log(test_data, log_locals=True)


test_log()

console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")