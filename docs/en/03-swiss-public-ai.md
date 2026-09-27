# 3. Swiss public AI: Apertus and Public AI

> The Espaço uses **Apertus**, the Swiss public universities' open model, through the **Public AI Inference Utility**, a nonprofit service with an OpenAI-compatible API. It is cheap but not free, and not free of big tech: it is the **least-dependent viable option** today, with the caveats below. Information checked September 2026.

## Why Apertus

- **Built by public institutions:** the Swiss AI Initiative, with EPFL, ETH Zurich and the Swiss National Supercomputing Centre (CSCS).
- **Truly open:** weights, code **and training data** are open, which is rare. You can know what the model read.
- **Multilingual:** trained on many languages. **Test in your language** with your community's questions before deciding (`tools/avaliar_modelos.py`).
- **Runs anywhere:** if Public AI ceases to exist, the same model can run at a university.

## The service: Public AI Inference Utility

| Item | Status (September 2026) |
| --- | --- |
| What it is | A nonprofit, open-source service giving access to public models |
| API | `https://api.publicai.co/v1`, OpenAI-compatible (`/chat/completions`); requires a key and a `User-Agent` header |
| Key | Sign up at [platform.publicai.co](https://platform.publicai.co), API Keys section |
| Cost | Per token; **US$2 starter credit**; then top-up or contribution via OpenCollective |
| Rate limit | Free: 100 requests/min; Plus: 200; Pro: 300 |
| Embeddings | Not offered: that's why the Espaço computes embeddings on its own server |

### Models and prices (per million tokens)

| Model | Context | Input | Output | Suggested use |
| --- | --- | --- | --- | --- |
| `swiss-ai/apertus-v1.5-8b` | 262k | US$0.10 | US$0.20 | Internal tasks; tests; chat on a very tight budget |
| `swiss-ai/apertus-v1.5-70b` | 262k | US$0.82 | US$2.92 | Conversations with residents (default) |

Source: [Public AI model catalog](https://platform.publicai.co/models). Prices change: check before budgeting.

### Cost per question

A typical archive question sends about 2,500 tokens (instructions, archive passages, history) and receives about 400.

| Model | Per question | 10,000 questions/month |
| --- | --- | --- |
| Apertus 70B | ≈ US$0.003 | ≈ US$32 |
| Apertus 8B | ≈ US$0.0003 | ≈ US$3 |

Rough estimate; measure real usage with `tools/avaliar_modelos.py`, which records tokens.

## The caveats, frankly

[Public AI's terms](https://publicai.co/tc) state that it:

1. **Does not use data to train models**, except for users who join a voluntary program ("Data Flywheel"). The Espaço **should not join**.
2. **Keeps technical logs for up to 90 days.**
3. **May share conversations with academic researchers**, under data use agreements, for non-commercial research.
4. **Uses compute partners**: CSCS (Swiss public), Exoscale (Swiss cloud) and **Amazon Web Services**, among others, and states it **does not control** what those partners do with the data.
5. Is governed by Massachusetts law, requires users to be **18 or older**, presents itself as aimed at **research and education**, and forbids political campaigning.

**What this means for the Espaço:** the whole archive never leaves the server, but passages and questions go through Public AI and possibly a commercial partner. Therefore:

- tell users **not to write personal data** in questions;
- keep out of the archive anything that could not, in the worst case, be seen by third parties;
- **write to Public AI** introducing the project and ask for: (a) an institutional or data processing agreement; (b) exclusion from research sharing; (c) preferential routing to CSCS infrastructure; (d) confirmation that use by a public service with facilitated users fits their terms;
- record the answer in council minutes and review the choice every six months.

## Exit plan (switch provider in a day)

The gateway concentrates the switch: change the `:8081` block in the `Caddyfile` and the model name in `.env`. Alternatives, from least to most dependent:

1. **A university running Apertus** (or another open model) with vLLM or Ollama on its own GPU: zero big tech. The long-term destination.
2. **A national cloud provider with GPUs**, running the same open model.
3. **Another open-model inference provider** with a no-retention contract.

Because Apertus is open, switching does not change the assistant's behavior.
