# extremely-dangerous-public-oidc-beacon

This repository exists to provide two workflows:
`extremely-dangerous-oidc-beacon.yml` and
`trigger-extremely-dangerous-oidc-beacon.yml`.

`trigger-extremely-dangerous-oidc-beacon.yml` dispatches
`extremely-dnagerous-oidc-beacon.yml` on a schedule. The latter *intentionally*
leaks an OIDC identity token corresponding to its workflow identity. It does this
so that members of the Sigstore community have access to a uniform identity token
for [conformance testing].

These workflows are intentionally isolated in their own repository, within
an otherwise unused GitHub organization, to minimize the possibility
that users will incorrectly trust these identity tokens. The workflow
names also include `extremely-dangerous` to emphasize that identity tokens
originating from them must not be trusted for anything except testing purposes.

[conformance testing]: https://github.com/sigstore/sigstore-conformance
