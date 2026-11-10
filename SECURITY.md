# Security Policy

## Supported project

Security reports are accepted for the current default branch of this repository and the published KVB ENTERPRISES website:

- Repository: https://github.com/ViviBeri/tax-business
- Website: https://viviberi.github.io/tax-business/

Older commits and generated copies are not maintained as separate supported releases. If a report affects a deployed version, include the affected page or commit where known.

## Report a vulnerability privately

**Do not open a public GitHub issue or pull request containing vulnerability details, exploit code, personal data, or information that could help someone attack visitors.**

Use GitHub's private vulnerability reporting feature:

1. Open the repository's **Security** tab.
2. Select **Report a vulnerability** (GitHub private vulnerability reporting).
3. Include the details requested below and submit the report privately.

If the private reporting option is unavailable, contact the repository owner through their GitHub profile and ask for a private security-reporting channel. Do not send exploit details through the website's public enquiry form, WhatsApp business number, or a public discussion.

## What to include

Please provide enough information to reproduce and assess the issue safely:

- A concise description and potential security impact.
- Affected URL, file path, commit, or version.
- Reproduction steps and the minimum proof of concept needed to demonstrate the issue.
- Required browser, platform, or configuration details.
- Whether the issue is reproducible and whether you believe it is being actively exploited.
- A suggested mitigation, if known.
- Your preferred name or handle for acknowledgment (optional).

Do not include real customer data, credentials, access tokens, or other people's personal information. Redact sensitive values from screenshots and logs.

## Scope

In scope:

- HTML, CSS, JavaScript, and generated pages maintained in this repository.
- The Python site builder and repository-maintained scripts.
- GitHub Actions workflows and repository configuration maintained here.
- Security issues that could compromise visitor confidentiality, integrity, or availability through this project's code or configuration.

Out of scope:

- Vulnerabilities in GitHub, GitHub Pages infrastructure, Google Analytics, WhatsApp, browsers, hosting providers, or other third-party services. Report those to the relevant provider.
- Issues that require access to accounts, systems, or data you do not own or have explicit permission to test.
- Purely theoretical hardening suggestions without a demonstrated security impact, general bugs without a security consequence, and social-engineering or physical attacks.
- Denial-of-service testing, spam, destructive tests, or automated scanning that degrades the live website or third-party services.

Please test only against systems and data you own or are explicitly authorized to assess. Avoid accessing, modifying, or retaining visitor information.

## Response and coordinated disclosure

The project is maintained by a small maintainer group; reports are handled by repository maintainers on a need-to-know basis. The project does not currently claim a dedicated security response team or a 24/7 response service.

Maintainers aim to:

1. Acknowledge a report within **5 business days**.
2. Triage and provide an initial assessment within **10 business days**, where the report contains enough information to reproduce it.
3. Keep the reporter informed about material status changes and coordinate a fix and disclosure timeline.

These are response goals, not guaranteed service levels. Complex reports may require more time; maintainers will explain delays where possible.

For a confirmed vulnerability, maintainers will assess impact and affected versions, develop and test a fix, and coordinate public disclosure with the reporter. A **90-day disclosure period** is a planning guideline, not an inflexible deadline; active exploitation, severity, fix readiness, and user risk may justify a different mutually discussed timeline.

Where appropriate, maintainers may publish a GitHub Security Advisory and request a CVE through a suitable CVE Numbering Authority. Embargoed advance notification is not promised and will be considered only if there is a clear user-protection need and a manageable set of affected downstream providers.

After a fix is available, maintainers will publish the relevant advisory or release information, affected versions, mitigations, and upgrade guidance. If a complete fix is not immediately possible, maintainers may publish a mitigation and clearly explain remaining exposure.

## Recognition and rewards

There is no bug bounty or guaranteed financial reward for reports. With the reporter's permission, maintainers may acknowledge their contribution in an advisory or release note.

## Safe-harbor commitment

For security research conducted in good faith, within this policy's scope, and in a way that avoids harm to users and systems, maintainers will not initiate or recommend legal action. This commitment does not authorize access to systems or data outside the stated scope, testing that disrupts services, or violations of applicable law. If you are unsure whether a test is permitted, stop and request clarification through a private channel before proceeding.

## Maintainer handling checklist

When a report arrives, maintainers should:

- Keep the report private and restrict access to people needed for triage and remediation.
- Acknowledge receipt and agree on the preferred communication method.
- Reproduce the issue safely; record affected files, commits, versions, impact, and severity.
- Distinguish a security vulnerability from intended behavior, a non-security bug, or a feature request.
- Develop and test fixes privately where practical; avoid publishing exploit-enabling details before users can update.
- Coordinate disclosure timing and reporter credit.
- Publish an advisory or clear security notice with affected versions, fixes, workarounds, and upgrade instructions.
- Review related code and tests for similar weaknesses.

This policy is adapted for a small static-site project from Google's OSS Vulnerability Guide. The project does not operate a formal embargo list or a paid vulnerability reward program.
