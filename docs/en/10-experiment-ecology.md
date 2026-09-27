# 10. An ecology of experiments

> The Espaço is not a finished recipe but a starting point for testing different ways of living with AI. Each space runs short experiments, observes what people became able to do, and decides to keep, modify or abandon. Abandoning is a legitimate result.

## Why

You cannot decide in advance, in a meeting, everything a technology like AI should be. Uses and values themselves emerge in practice: it is by using a tool that a group discovers whether it feels like care or surveillance, whether it invites learning or shortcuts. Rules set in advance and applied from outside tend to become a checklist, disconnected from what actually happens.

The idea comes from an essay by Evgeny Morozov (*Nueva Sociedad* no. 323, 2026; English original in *The Ideas Letter*, 2025): instead of asking only "how should we govern AI?", ask **"what institutions make it possible to explore, in an organized way, different technological arrangements and different ways of living with them?"**. The answer is not a single model but an ecology of local experiments (municipal, school-based, community) each with its own priorities, real resources and freedom to change course.

He also notes that the chat interface, which makes the model seem like a conversation partner rather than a library, was a product decision to drive use and attachment. Some experiments below test the opposite.

## Principles

1. **Short cycles:** 4 to 6 weeks, one clear question per experiment.
2. **The criterion is capability:** what people became able to do, understand or do together that they couldn't before, and **for whom**.
3. **Record everything, including what failed.** A well-recorded abandoned experiment is worth as much as a successful one.
4. **Any space can propose.** Library, school, association, residents' group.
5. **The council handles risks, not merit.** It approves experiments looking at personal data, safety and the archive license; it does not decide in advance whether the idea is good.
6. **Room for what doesn't fit metrics.** Some cycles are reserved for free proposals that may never fit an indicator.

## Menu of experiments

| # | Experiment | What changes | Question tested | How to set up |
| --- | --- | --- | --- | --- |
| 1 | **Library mode** | The interface stops simulating conversation: the assistant first shows archive passages and pages, and only then, if asked, a short summary | Does showing sources first increase reading and reduce delegation? | Assistant with the [`library-mode.md`](../../prompts/en/library-mode.md) prompt |
| 2 | **Questions only** | The assistant never answers directly; it only asks questions and points to what to read | Does a group learn more when it must build the answer? | [`questions-only.md`](../../prompts/en/questions-only.md) prompt |
| 3 | **Archive first** | The wiki is the entry point; the assistant is reached only from a page ("ask about this page") | Is the archive read and corrected more when it is the center? | A link on each wiki page to the assistant with a pre-filled question (Open WebUI accepts a `?q=` URL parameter; check your version) |
| 4 | **Side-by-side reading** | A group reads a hard document together (call for proposals, law) and uses the assistant only to explain terms and passages | Is AI more helpful as dictionary and commentator than as summarizer? | Document Reader + in-person or online workshop |
| 5 | **From individual to collective** | Solution records gain the question "does this affect other people?"; if so, the case is referred to an association, council or ombudsman | Do individual solutions become shared issues? | New field in the [solution record](../../wiki-modelos/ficha-de-solucao.md) |
| 6 | **Questioning history** | A school class writes local-memory pages and uses the assistant to compare official versions with residents' accounts | Do students come to see history from their own place? | School partnership; `memoria/` layer |
| 7 | **In our language** | Local glossary, expressions and speech variants go into the archive and prompts; in partnership, an Indigenous or immigrant language of the region | Does the tool work for people who speak differently from the norm? | Only with the speaking community leading and deciding |
| 8 | **A model of our own** | A small open model is fine-tuned on the curated archive, on a university GPU, and compared to the general model with search | Does a model shaped by the local archive answer better, or differently? | Requires council authorization and authors' consent (new field in the [consent form](../../templates/en/oral-history-consent.md)); never commercial |
| 9 | **No AI** | The same workshop is run without the assistant, with the archive printed or on screen | What does AI actually add? What does it take away? | Comparison group; same question, same facilitators |
| 10 | **Free proposal** | Any arrangement a group wants to test | — | Experiment log + risk approval |

## Running a cycle

1. **Propose.** Fill in the [experiment log](../../templates/en/experiment-log.md) and publish it under `experimentos/` in the wiki.
2. **Approve risks.** The council checks personal data, safety and the archive license. It does not judge merit.
3. **Set up.** In Open WebUI, each variant is a separate assistant with a name and version: "Archive Assistant · library mode · v1". Never change the main assistant during an experiment.
4. **Run for 4–6 weeks** with a defined group (a class, a workshop, a library's users).
5. **Observe** through facilitators' notes, conversations with participants and, only with explicit consent, anonymized usage excerpts.
6. **Evaluate in a circle** with participants, using the questions below.
7. **Decide and record.** Keep, modify (new cycle) or abandon. The log stays in `experimentos/` and, if useful to other cities, is shared on the project's GitHub (an issue labeled `experimento`).

## Questions for observing and evaluating

These questions are not a checklist; they are for opening the conversation in the circle.

- What did people become able to do, understand or do together that they couldn't before?
- Whom did it work for? Whom didn't it work for, and why?
- Did use feel like **care** or **surveillance**? **Learning** or **shortcut**?
- Did people become more able to act on their own, or more dependent on the tool?
- What was surprising?
- Did any value or concern emerge that wasn't anticipated when the experiment began?
- What would another space need to know to try the same?

## A network, not a model

The repository is a starting point. Each city can create its own variants, and the network's value lies in sharing the logs: what was tried, what people became able to do, what was abandoned. Over time, the collection of logs is worth more than any default configuration.
