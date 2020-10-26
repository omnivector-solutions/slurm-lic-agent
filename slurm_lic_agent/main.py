#!/usr/bin/env python3
import os
import pwd


def main():
    uid = os.geteuid()
    username = pwd.getpwuid(uid).pw_name
    print(f"{username} ({uid})\n")


if __name__ == "__main__":
    main()
