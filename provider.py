#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import re
import sys
from urllib.request import urlopen

SOURCE_URL = "https://raw.githubusercontent.com/sm-monirulislam/Upcoming-and-Live-Sports-Data/main/Sports_data.m3u"
OUTPUT_FILE = "stv12.m3u"
LOG_FILE = "stv12.log"


def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


def clean_m3u(content):
    lines = content.splitlines()

    filtered = []
    for line in lines:
        s = line.strip()

        # Remove developer/header attributes
        if (
            s.startswith("#=================================")
            or s.startswith("#  Developed by:")
            or s.startswith("# Developed by:")
            or s.startswith("#  Telegram:")
            or s.startswith("# Telegram:")
            or s.startswith("#  Telegram channel")
            or s.startswith("# Telegram channel")
            or s.startswith("#  Last Updated:")
            or s.startswith("# Last Updated:")
            or s.startswith("#  Live Channels Count:")
            or s.startswith("# Live Channels Count:")
        ):
            continue

        filtered.append(line)

    return "\n".join(filtered) + "\n"


def download_m3u():
    logging.info("Downloading playlist: %s", SOURCE_URL)

    with urlopen(SOURCE_URL, timeout=60) as response:
        content = response.read().decode("utf-8", errors="ignore")

    content = clean_m3u(content)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    logging.info("Saved cleaned playlist to %s", OUTPUT_FILE)
    print(f"Saved: {OUTPUT_FILE}")
    print(f"Log  : {LOG_FILE}")


def main():
    setup_logging()

    try:
        download_m3u()
    except Exception as e:
        logging.exception("Failed")
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
