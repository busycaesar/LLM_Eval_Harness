"""Package installation utilities."""
import subprocess
import sys


def install_if_missing(package: str) -> None:
    """pip-install the given package if it isn't already installed."""
    show = subprocess.run(
        [sys.executable, "-m", "pip", "show", package],
        capture_output=True,
    )
    if show.returncode != 0:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            check=True,
        )
