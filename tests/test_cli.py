import sys

sys.path.insert(0, "../")

import supermark
from supermark import Core, build, info
from click.testing import CliRunner
from pathlib import Path


def test_cli():
    # core = Core()
    # print(core)
    # core.info()

    runner = CliRunner()
    result = runner.invoke(info, ["info"])
    print(result)

    result = runner.invoke(build, ["--template", Path("~")])
    print(result)
    # assert result.exit_code == 0
    # assert result.output == "Hello Peter!\n"
