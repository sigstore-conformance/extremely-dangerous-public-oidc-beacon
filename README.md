# extremely-dangerous-public-oidc-beacon

> [!WARNING]
> **This action is deprecated and will stop working soon.**
>
> All users should switch to the new test token, which is more reliable and has a longer time-to-live. The new token identity is:
> * **Signing identity**: `untrusted-sa@sigstore-conformance.iam.gserviceaccount.com`
> * **Issuer**: `https://accounts.google.com`
>
> To download it as a 1:1 replacement of running this action:
>
> ```bash
> curl -sSfL https://storage.googleapis.com/sigstore-conformance-testing-token/untrusted-testing-token.txt -o oidc-token.txt
> ```

## Usage (Deprecated)

The repository includes an action that will download the current token into the
working directory (`./oidc-token.txt`):

    - uses: sigstore-conformance/extremely-dangerous-public-oidc-beacon@main

## Details

The workflow `trigger-extremely-dangerous-oidc-beacon.yml` dispatches
`extremely-dangerous-oidc-beacon.yml` on a schedule. The latter *intentionally*
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
