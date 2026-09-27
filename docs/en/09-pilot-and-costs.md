# 9. Pilot and costs

> A 12-week pilot in one city, with an anchor institution, 50–100 initial documents and 100–300 invited users. Estimated monthly cost R$200–600 (about US$40–110), plus stipends.

## Stages

1. **Weeks 1–2: groundwork.** Anchor institution and council; server online; Public AI account and a letter requesting an institutional agreement.
2. **Weeks 3–4: initial archive.** 50–100 pages under `oficial/` and `memoria/`; 10 solution records written in in-person workshops; canaries inserted.
3. **Weeks 5–6: closed test.** 20 people (facilitators, council members, librarians) use it and do "Check the source"; Apertus 8B vs 70B test with `tools/avaliar_modelos.py`; prompt adjustments.
4. **Weeks 7–12: invitation-only opening.** Sign-up via partner institutions (libraries, schools, associations); home activities; two online circles; first gaps filled.
5. **Week 12: evaluation.** Public report and council decision.

## Approximate costs (Brazil, September 2026)

| Item | Monthly | Note |
| --- | --- | --- |
| Server (4–8 vCPU, 16 GB, no GPU) | R$0–400 | Zero if provided by a university or city hall; otherwise a national provider (get quotes) |
| AI (Public AI, Apertus 70B) | ≈ US$3–32 | 1,000 to 10,000 questions a month; see [calculation](03-swiss-public-ai.md#cost-per-question) |
| Domain and email | ≈ R$20 | |
| Stipends: technician (10 h/week) and curation (10 h/week) | R$2,000–3,000 | The main cost is people |

AI cost is small compared to the rest: borrowed public infrastructure makes the service viable for small cities.

## What to measure

- **Quality:** share of answers with a correct source ("Check the source" activity).
- **Archive growth:** approved records, gaps filled, documents added.
- **Meaningful use:** questions per person, reported problems solved, partner institutions using it in workshops.
- **Protection:** blocked bot attempts (Caddy logs), canaries checked.
- **Cost per question**, checked on the Public AI dashboard.

Don't count screen time or messages per day as success.

## Phase 2

- **Single sign-on** for wiki and assistant (OpenID Connect, with Keycloak or Authentik).
- A "turn this conversation into a record" button that pre-fills the template with what was solved.
- A network of cities sharing one server, each with its own archive and council.
- Moving inference to a Brazilian university GPU running Apertus: zero big-tech dependence.
- Integration with an automatic Official Gazette reader (sister project "Diário Oficial em Linguagem Simples") as a source for the official layer.
