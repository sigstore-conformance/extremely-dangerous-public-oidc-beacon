# extremely-dangerous-public-oidc-beacon

> [!WARNING]
> **This action is deprecated, do not use it. For historical purposes, see git history**
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
