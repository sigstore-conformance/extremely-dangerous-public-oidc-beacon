# Fetch a cursed OIDC token from extremely-dangerous-public-oidc-beacon git
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
# * use pyjwt to check if token is invalid
# * retry a bit later if it is expired (or will soon expire)

from datetime import datetime, timedelta
import sys
from tempfile import TemporaryDirectory
import logging
import os
import subprocess
import shutil
import time

import jwt

MIN_VALIDITY = timedelta(seconds=10)
MAX_RETRY_TIME = timedelta(minutes=5)
RETRY_SLEEP_SECS = 30
GIT_URL = "https://github.com/sigstore-conformance/extremely-dangerous-public-oidc-beacon.git"

logger = logging.getLogger(__name__)


def git_clone(url: str, dir: str) -> None:
    base_cmd = ["git", "clone", "--quiet", "--branch", "current-token", "--depth", "1"]
    subprocess.run(base_cmd + [url, dir])


def is_valid_at(token_path: str, reference_time: datetime):
    with open(token_path) as f:
        token = jwt.decode(f.read().rstrip(), options={"verify_signature": False})
    expiry = datetime.fromtimestamp(token["exp"])
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
    with TemporaryDirectory() as tempdir:
        git_clone(GIT_URL, tempdir)

        token_path = os.path.join(tempdir, "oidc-token.txt")
        if is_valid_at(token_path, datetime.now() + MIN_VALIDITY):
            shutil.copyfile(token_path, "./oidc-token.txt")
            print("Downloaded valid token to ./oidc-token.txt")
            break

    if datetime.now() > start_time + MAX_RETRY_TIME:
        sys.exit(f"Failed to find a valid token in {MAX_RETRY_TIME}")

    print(f"Current token expires too early, retrying in {RETRY_SLEEP_SECS} seconds.")
    time.sleep(RETRY_SLEEP_SECS)
