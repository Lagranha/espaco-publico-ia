# 1. Proposal

> Espaço Público IA ("Public AI Space") is a living archive of the city, online and free, with an AI assistant that answers from it. The archive grows with what residents solve, is protected against use for training commercial AI, and the AI runs on borrowed Swiss public infrastructure rather than big tech.

## The idea

Public libraries gave everyone access to books without charging by the page. Espaço Público IA applies the same logic to artificial intelligence and to knowledge about one's own city. The inspiration is a suggestion by researcher Evgeny Morozov: create intermediary institutions, like libraries, that offer AI as public infrastructure rather than a pay-per-use service.

It is the online version of the [Laboratório Público de IA](https://github.com/Lagranha/laboratorio-publico-ia), which runs on a computer inside a library. Here, any registered person can use it from home, on a phone or computer.

## Four core ideas

**1. A city archive in three layers.** Official documents (laws, plans, service guides), local memory (interviews, stories, studies) and solution records (how residents solved real problems). The assistant always says which layer each piece of information comes from, so accounts are not mistaken for official documents.

**2. An archive that grows with use.** Whoever solves a problem can write a solution record, which is reviewed and added. When the assistant cannot answer, the question becomes a gap, and the community is invited to fill it.

**3. A protected archive.** The content is under community guardianship: it serves the community and may not be used to train AI models, especially commercial ones. Protection combines mandatory sign-up, a dedicated license, bot blocking and canary phrases to detect misuse.

**4. AI from public infrastructure.** Answers come from **Apertus**, an open model built by Swiss public universities (EPFL, ETH Zurich and the Swiss National Supercomputing Centre, CSCS), used through the **Public AI Inference Utility**, a nonprofit service. The archive stays on our server; only the question and the needed passages travel to generate each answer.

## Who it is for

Residents who need to understand a public service or solve a problem; municipal council members, local journalists, teachers and students; associations, cooperatives and small businesses; library and school facilitators, who use it in workshops.

## What this is not

- Not a generic chatbot: the assistant answers from the city's archive and says when it doesn't know.
- Not independent of everything: the Swiss service uses compute partners, including Amazon Web Services. Dependence on large companies is **minimal and transparent**, not zero. See [Swiss public AI](03-swiss-public-ai.md).
- Not a substitute for presence: it works best tied to physical spaces (libraries, schools, associations) with facilitators.
