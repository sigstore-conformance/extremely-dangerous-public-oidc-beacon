# extremely-dangerous-public-oidc-beacon

This repository publishes an OIDC identity token for testing purposes.
This OIDC token should not be trusted, but it can be useful for testing
Sigstore keyless signing and verification, see e.g. [conformance testing].

## Usage

The repository includes an action that will download the current token into
working directory (`./oidc-token.txt`):

    - uses: sigstore-conformance/extremely-dangerous-public-oidc-beacon@main

## Details

The workflow `trigger-extremely-dangerous-oidc-beacon.yml` dispatches
`extremely-dnagerous-oidc-beacon.yml` on a schedule. The latter *intentionally*
leaks an OIDC identity token corresponding to its workflow identity. The token is
made available in the workflow artifacts and also in an ephemeral (force-pushed)
git branch
[current-token](https://github.com/sigstore-conformance/extremely-dangerous-public-oidc-beacon/tree/current-token).

The workflows are intentionally isolated in their own repository, within
an otherwise unused GitHub organization, to minimize the possibility
that users will incorrectly trust these identity tokens. The workflow
names also include `extremely-dangerous` to emphasize that identity tokens
originating from them must not be trusted for anything except testing purposes.

Because GitHub workflow scheduling is best-effort, the published token may sometimes
be expired for a while. Users may want to retry a little later in these cases like
the provided GitHub Action does.

[conformance testing]: https://github.com/sigstore/sigstore-conformance
