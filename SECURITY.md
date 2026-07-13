# Security and privacy policy

Frontier Handoff handles prompts, model outputs, logs, and context excerpts. These records can contain executable instructions, secrets, personal data, confidential material, or content a contributor has no right to publish. A `raw` label preserves bytes; it does not make unsafe publication acceptable.

## Never submit

- API keys, access tokens, session cookies, passwords, private keys, or credentials;
- private system prompts you do not have permission to publish;
- customer data or confidential conversations;
- private repository content;
- personal information without a lawful, necessary, and consented reason;
- proprietary source code, documents, datasets, or benchmarks without permission;
- malicious files or instructions intended to compromise contributors or evaluators.

Do not put live secrets in an issue, pull request, commit, artifact, screenshot, test fixture, or validation log. Examples must use unmistakably fake values.

## Treat artifacts as untrusted data

Model outputs may contain unsafe commands, fabricated links, prompt injection, or instructions to disclose data. Reading an artifact does not authorize executing it. Run experiments in an isolated environment, inspect commands before use, use least-privilege credentials, and obtain explicit authorization for external or irreversible actions.

## Reporting an exposure or vulnerability

Do not open a public issue containing the sensitive material.

1. If a credential may be live, revoke or rotate it immediately; repository cleanup is not a substitute.
2. Use the repository host's private vulnerability-reporting feature. On GitHub, use the repository's **Security** area and private vulnerability reporting when enabled.
3. If private reporting is unavailable, contact a maintainer through an already published private channel. If none exists, open a content-free public issue asking a maintainer to establish private contact.
4. Provide the affected path or commit, exposure type, first known occurrence, and safe reproduction details. Share the secret itself only when strictly necessary through an agreed secure channel.

This new repository does not yet publish a dedicated security address. Configuring a durable private contact is a maintainer follow-up before accepting outside submissions.

## Response expectations

Maintainers should privately acknowledge a report, preserve only necessary evidence, assess forks and caches as well as the current branch, remove public access where possible, rotate affected credentials, and communicate remediation. Git history rewriting does not erase clones, forks, archives, notifications, or third-party caches; affected parties must be notified when appropriate.

## Supported versions

Until the project publishes releases, only the current default branch is maintained. Historical artifacts remain preserved for research, but deprecated executable guidance is not security-supported.
