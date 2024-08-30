#!/usr/bin/env python
"""
Collect stats about inotify instances and watches per process.

Inspired by and based on 
- https://unix.stackexchange.com/questions/15509/whos-consuming-my-inotify-resources
- https://github.com/fatso83/dotfiles/blob/master/utils/scripts/inotify-consumers
"""

import re
import collections
from pathlib import Path
import sys


def main():
    watch_regex = re.compile(r"^inotify\s", flags=re.MULTILINE)
    instances_per_pid = collections.Counter()
    watches_per_pid = collections.Counter()
    for fdinfo in Path("/proc").glob("*/fdinfo/*"):
        try:
            watches = len(watch_regex.findall(fdinfo.read_text()))
        except Exception as e:
            print(e, file=sys.stderr)
        if watches:
            pid = int(fdinfo.parts[-3])
            instances_per_pid[pid] += 1
            watches_per_pid[pid] += watches

    print("    PID Instances  Watches Command")
    for pid, watches in watches_per_pid.most_common(n=None):
        cmd = Path(f"/proc/{pid}/cmdline").read_text().split()[0][:60]
        print(f"{pid:8} {instances_per_pid[pid]:8} {watches:8} {cmd}")
    print(
        f"   Total {sum(instances_per_pid.values()):8} {sum(watches_per_pid.values()):8}"
    )


if __name__ == "__main__":
    main()
