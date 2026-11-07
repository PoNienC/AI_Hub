"""Offline gh executable used only by release integration tests."""

import json
import os
import shutil
import sys
from pathlib import Path

root = Path(os.environ["FAKE_GH_ROOT"])
args = sys.argv[1:]
with (root / "commands.jsonl").open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(args) + "\n")
mode = json.loads((root / "mode.json").read_text(encoding="utf-8"))
operation = args[1]
remote = root / "remote"
if mode.get("error"):
    sys.stderr.write(mode["error"])
    sys.exit(1)
if operation == "view":
    if not (root / "exists").exists():
        sys.stderr.write("release not found\n")
        sys.exit(1)
    if mode.get("invalid_metadata"):
        print('{"assets": null}')
    else:
        print(json.dumps({"assets": [
            {"name": path.name, "size": path.stat().st_size + mode.get("size_delta", 0)}
            for path in remote.iterdir() if path.is_file()
        ]}))
elif operation == "create":
    (root / "exists").touch()
elif operation == "download":
    target = Path(args[args.index("--dir") + 1])
    for name in ("gateway.sqlite", "evidence.jsonl"):
        if (remote / name).exists():
            shutil.copyfile(remote / name, target / name)
    if mode.get("download_fail"):
        sys.exit(1)
elif operation == "upload":
    if mode.get("upload_fail"):
        sys.exit(1)
    for value in args[3:-1]:
        path = Path(value)
        shutil.copyfile(path, remote / path.name)
else:
    sys.exit(2)
