# Fetch a cursed OIDC token from extremely-dangerous-public-oidc-beacon
#
# This script exists for a few reasons:
# * Multiple sigstore-related projects need a non-expired OIDC token for testing
#   (and GitHub Actions tokens are not available in PRs for good reasons)
# * extremely-dangerous-public-oidc-beacon project produces a token every few minutes but
#   the tokens are short-lived: this means any fetching method with caching or latency
#   of minutes will not work (this covers Github Pages and https://raw.githubusercontent.com/)
# * There are still times when there is no valid token available for a while because GitHub
#   schedule triggers are best-effort
# * Accessing the tokens published as GitHub artifacts requires a GitHub token: this is
#   inconvenient
#
# To counter all of these issues:
# * use git to fetch token from "current-token" branch
# * parse jwt just enough to check token validity
# * retry a bit later if it is expired (or will soon expire)
#
# The token can alternatively be fetched from the GCS bucket by setting
# OIDC_TOKEN_SOURCE=google. Note that the bucket serves a different identity
# (a Google service account token) than the "current-token" branch (a GitHub
# Actions token), so this is opt-in to avoid breaking existing consumers.

from base64 import b64decode
from datetime import datetime, timedelta
from urllib.request import urlopen
import json
import sys
from tempfile import TemporaryDirectory
import logging
import os
import subprocess
import time

MIN_VALIDITY = timedelta(seconds=10)
MAX_RETRY_TIME = timedelta(minutes=5)
RETRY_SLEEP_SECS = 30
GIT_URL = "https://github.com/sigstore-conformance/extremely-dangerous-public-oidc-beacon.git"
GCS_URL = "https://storage.googleapis.com/sigstore-conformance-testing-token/untrusted-testing-token.txt"

# "github" (default) clones the current-token git branch and yields a GitHub
# Actions identity token; "google" fetches from the GCS bucket and yields a
# Google service account identity token.
SOURCE = os.environ.get("OIDC_TOKEN_SOURCE", "github")

logger = logging.getLogger(__name__)


def git_clone(url: str, dir: str) -> None:
    base_cmd = ["git", "clone", "--quiet", "--branch", "current-token", "--depth", "1"]
    subprocess.run(base_cmd + [url, dir], check=True)


def fetch_from_branch() -> str:
    with TemporaryDirectory() as tempdir:
        git_clone(GIT_URL, tempdir)
        with open(os.path.join(tempdir, "oidc-token.txt")) as f:
            return f.read().rstrip()


def fetch_from_gcs() -> str:
    with urlopen(GCS_URL) as response:
        return response.read().decode().strip()


def fetch_token() -> str:
    if SOURCE == "google":
        return fetch_from_gcs()
    if SOURCE == "github":
        return fetch_from_branch()
    sys.exit(f"Unknown OIDC_TOKEN_SOURCE {SOURCE!r}: expected 'github' or 'google'")


def is_valid_at(token: str, reference_time: datetime) -> bool:
    # b64 decode (with padding) the payload, parse as json, validate expiry
    payload = token.split(".")[1]
    payload += "=" * (4 - len(payload) % 4)
    payload_json = json.loads(b64decode(payload))

    expiry = datetime.fromtimestamp(payload_json["exp"])
    valid = reference_time < expiry
    logger.debug(
        "token is %s (ref time: %s, expiry: %s)",
        "valid" if valid else "expired",
        reference_time,
        expiry,
    )
    return valid


start_time = datetime.now()
while True:
    token = fetch_token()

    if is_valid_at(token, datetime.now() + MIN_VALIDITY):
        with open("./oidc-token.txt", "w") as f:
            f.write(token)
        print("Downloaded valid token to ./oidc-token.txt")
        break

    if datetime.now() > start_time + MAX_RETRY_TIME:
        sys.exit(f"Failed to find a valid token in {MAX_RETRY_TIME}")

    print(f"Current token expires too early, retrying in {RETRY_SLEEP_SECS} seconds.")
    time.sleep(RETRY_SLEEP_SECS)
