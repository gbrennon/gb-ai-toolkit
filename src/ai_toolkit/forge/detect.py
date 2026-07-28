import json
import sys

from ai_toolkit.forge.api import (
    detect_forge,
    get_main_remote,
    get_remote_url,
)


def main() -> int:
    forge = detect_forge()
    if forge is None:
        print("No git remote found", file=sys.stderr)
        return 1

    remote = get_main_remote()
    url = get_remote_url()

    if "--json" in sys.argv:
        print(
            json.dumps(
                {
                    "forge": forge,
                    "remote": remote,
                    "url": url,
                }
            )
        )
    else:
        print(forge)

    return 0


if __name__ == "__main__":
    sys.exit(main())
