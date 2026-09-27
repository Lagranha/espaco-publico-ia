# 6. Archive protection

> No measure makes it impossible to copy content people can access. What the Espaço does is make using it to train AI **hard, illegitimate and detectable**, in four layers.

## 1. Technical layer: hard

| Measure | Where | What it does |
| --- | --- | --- |
| Everything behind login | Wiki.js (Guests without read) and Open WebUI (pending accounts) | Crawlers, which don't log in, see nothing |
| Known AI bots blocked | `Caddyfile` (`@robos_ia`) | GPTBot, ClaudeBot, CCBot, Google-Extended and others get 403 |
| Restrictive `robots.txt` | `deploy/robots.txt` | States the prohibition for bots that honor it |
| No bulk export | Wiki permissions; daily limit on the assistant | Makes copying the whole archive from inside harder |
| Approved accounts | `DEFAULT_USER_ROLE=pending` | Each account is checked before access |

## 2. Legal layer: illegitimate

- **[Community Guardianship License](../../templates/en/archive-license.md)**: expressly forbids training, fine-tuning or evaluating AI models on the archive, and collecting it by automated means.
- **Text and data mining reservation**, declared in the license text and in machine-readable form: `tdm-reservation: 1` and `X-Robots-Tag: noai` headers, set by Caddy.
- **[Terms of use](../../templates/en/terms-of-use.md)** accepted at sign-up, repeating the prohibition.

This creates grounds to act against violators. Brazil's legal framework on AI and copyright is still under discussion; an express reservation is the best available position meanwhile.

## 3. Detection layer: detectable

**Canary phrases** ([`tools/canarios.py`](../../tools/canarios.py)): invented, plausible, unique sentences (names of places and people that don't exist), inserted into some pages. If a commercial model one day answers about "the Tobunaba creek flood", it is strong evidence the archive was copied.

- Generate 10–20, insert each into a different page, mid-text.
- Keep the list (`canarios.csv`) **outside the repository** and outside the wiki.
- Once a quarter, ask the main commercial models about the canaries (`canarios.py perguntas`) and check the answers (`canarios.py verificar`).
- Tell curators where they are, so they are not "corrected".

## 4. The assistant's own layer: no leaks through use

The assistant is itself a way out for the archive: each answer sends passages to the AI provider. Therefore:

- only **Public AI**, whose terms forbid training on the data, without joining its voluntary data-donation program;
- **embeddings computed on the server**: the archive is never sent in bulk for indexing;
- a **gateway** that does not pass on who asked;
- a formal request to Public AI for exclusion from research sharing (see [Swiss public AI](03-swiss-public-ai.md#the-caveats-frankly)).

## What this does not solve

A registered person can copy pages by hand and publish them elsewhere, where a bot could collect them. The answer is social and legal: a culture of care for the archive, a clear license, canaries to prove origin. Content that cannot bear that risk at all should not enter the archive.
