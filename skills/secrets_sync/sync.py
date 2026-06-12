#!/usr/bin/env python3
"""Keychain -> Secret Manager push. See SKILL.md."""
import os
import subprocess
import sys

PROJECT = os.environ.get("FRIDAY_BQ_PROJECT", "friday-prod-7401")


def read_keychain(service: str, account: str = "jarvis") -> str:
    out = subprocess.run(
        ["security", "find-generic-password", "-s", service, "-a", account, "-w"],
        capture_output=True, text=True)
    if out.returncode != 0:
        raise KeyError(f"keychain item not found: service={service} account={account}")
    return out.stdout.strip()


def push(keychain_service: str, sm_name: str, account: str = "jarvis") -> str:
    from google.cloud import secretmanager
    value = read_keychain(keychain_service, account)
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{PROJECT}"
    try:
        client.create_secret(request={"parent": parent, "secret_id": sm_name,
                                      "secret": {"replication": {"automatic": {}}}})
    except Exception:
        pass  # already exists
    version = client.add_secret_version(request={
        "parent": f"{parent}/secrets/{sm_name}",
        "payload": {"data": value.encode()}})
    return version.name


if __name__ == "__main__":
    print(push(sys.argv[1], sys.argv[2]))
