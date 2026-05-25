from click.testing import CliRunner

from sardine.__main__ import main


def test_web_command_hint_when_sardine_web_is_missing():
    result = CliRunner().invoke(main, ["web"])

    assert result.exit_code != 0
    assert "sardine-web" in result.output
    assert "python -m pip install sardine-web" in result.output
