"""Проверка доступности Docker daemon для целей Makefile `db-*`."""

from __future__ import annotations

import subprocess
import sys


def main() -> None:
    r = subprocess.run(
        ["docker", "info"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if r.returncode != 0:
        print(
            "Docker daemon недоступен (например `failed to connect to the docker API`). "
            "На Windows запустите Docker Desktop и дождитесь готовности движка, "
            "затем повторите команду.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
