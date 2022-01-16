import sys

sys.path.insert(0, "../")
from pathlib import Path

from supermark.command import build

from click.testing import CliRunner


def test_continuous():
    print("bbi")
    runner = CliRunner(echo_stdin=True)
    input_path = Path("/Users/kraemer/Dropbox/Teaching/TTM4115/website/pages")
    template_path = Path(
        "/Users/kraemer/Dropbox/Teaching/TTM4115/website/templates/page.html"
    )
    output_path = Path("/Users/kraemer/Dropbox/Teaching/TTM4115/website")

    if True:
        result = runner.invoke(
            build,
            [
                "-c",
                "-i",
                str(input_path),
                "-o",
                str(output_path),
                "-t",
                str(template_path),
            ],
        )
        print(result)
    # assert result.exit_code == 0
    # assert result.output == 'Hello Peter!\n'

    else:
        run(
            False,
            False,
            False,
            True,
            input=input_path,
            output=output_path,
            template=template_path,
        )


test_continuous()