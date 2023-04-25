# extremely-dangerous-public-oidc-beacon

This repository exists to provide a single workflow:
`extremely-dangerous-oidc-beacon.yml`.

This workflow runs on a schedule, and *intentionally* leaks an OIDC identity
token corresponding to its workflow identity. It does this so that members
of the Sigstore community have access to a uniform identity token
for [conformance testing].

This workflow is intentionally isolated in its own repository, within
an otherwise unused GitHub organization, to minimize the possibility
that users will incorrectly trust these identity tokens. The workflow's
name also includes `extremely-dangerous` to emphasize that identity tokens
originating from it must not be trusted for anything except testing purposes.

[conformance testing]: https://github.com/sigstore/sigstore-conformance
