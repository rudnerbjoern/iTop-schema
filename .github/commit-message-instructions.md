# Commit-message generation

This file is the canonical commit-message convention for this repository. It
is referenced by `AGENTS.md`, the repository Copilot instructions, and the
VS Code workspace configuration.

Generate a message only for the staged change. Use English and this header:

```text
:<icon>: <type>(<scope>): <imperative outcome>
```

Requirements:

- Keep the raw header, including the shortcode, at or below 80 characters.
- Use lower-case `type` and `scope`; require one concise capability scope.
- Start the summary with a lower-case imperative verb and omit its final period.
- Describe the outcome, not a file list.
- Use exactly one deterministic type and icon:
  - `:sparkles: feat`
  - `:bug: fix`
  - `:recycle: refactor`
  - `:zap: perf`
  - `:test_tube: test`
  - `:memo: docs`
  - `:package: build`
  - `:gear: ci`
  - `:wrench: chore`
- Prefer a project scope that identifies the affected contract or capability:
  - `schema` for changes shared by supported iTop schema versions.
  - `schema-3.2` or `schema-3.3` for version-specific schema changes.
  - `generator` for schema combination and generated `dist` output.
  - `validation` for XML validation behavior and diagnostics.
  - `cli` for the command-line entry points and their user-facing behavior.
- Use a technical scope such as `tests`, `ci`, `deps`, `docs`, `tooling`, or
  `agents` only for a genuinely cross-cutting or technical change.
- Use `release` only for published-version metadata or changes to the stable
  `Latest` schema reference. Do not imply a release for development work.
- Omit the body for a small self-explanatory change.
- Otherwise add `Why:` followed by the motivation, then `Changes:` with only
  the material effects.
- Add a `BREAKING CHANGE:` footer for an incompatible contract or migration.
- Never invent verification results, issue identifiers, effects, or rationale.
- Never include secrets, personal data, or sensitive diagnostic details.

Examples:

```text
:sparkles: feat(schema-3.3): support a new design node
:bug: fix(validation): reject unsafe schema includes
:recycle: refactor(generator): centralize schema combination
:test_tube: test(validation): cover malformed XML diagnostics
:memo: docs(schema): clarify published schema URLs
:package: build(deps): pin Python tooling versions
:gear: ci(schema): combine supported schemas in one workflow
:wrench: chore(agents): document Windows test execution
```
