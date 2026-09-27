# 5. The living archive

> The archive is the heart of the project; the assistant is just one way to consult it. It has three layers, grows through solution records and gaps, and every piece of information carries its provenance and date.

## The three layers

| Layer | Wiki path | What goes in | Who adds it | How the assistant presents it |
| --- | --- | --- | --- | --- |
| Official documents | `oficial/` | Municipal laws, master plan, acts, public-service guides | Curators | "According to Law X..." |
| Local memory | `memoria/` | Interviews, stories, studies about the city | Curators, with consent | "According to residents of district X..." |
| Solution records | `fichas/` | How residents solved real problems | Contributors, reviewed | "A resident reports that..." plus a note that it is an account |

## How the archive grows

**Solution records.** Someone who solved a problem writes a record from the [template](../../wiki-modelos/ficha-de-solucao.md) under `fichas/rascunhos/`. A curator reviews it: removes personal data, checks that channels and procedures exist, adjusts the language, then moves it to `fichas/`. On the next sync it reaches the assistant. Records of attempts that failed are valuable too.

**Validity.** Each record has a date. After 12 months (configurable), the sync adds a "may be out of date" notice to its text, and the assistant repeats it. When someone confirms the path still works, editing the record (updating its verification date) removes the notice.

**Gaps.** When the assistant answers "I could not find this in the archive.", the gap filter stores the question with no data about who asked. The sync groups repeated questions and publishes the list, most frequent first, on the internal page `curadoria/lacunas`. Curators review it, remove personal data and copy worthwhile questions to the public `lacunas` page. Residents and facilitators help find sources.

**Documents and memories.** Added on the curators' initiative, by partners (city council, municipal archive, university) or by community request, following the entry criteria below.

## Entry criteria (approved by the council)

Content enters the archive if it:

1. has a known, reliable origin;
2. can be shared (public domain, permission or consent);
3. does not expose third parties' personal data;
4. helps someone in the city understand something or solve a problem.

## Roles

| Role | Can | How to become one |
| --- | --- | --- |
| Reader | Consult the assistant and the wiki, comment | Approved sign-up |
| Contributor | Write draft records, suggest documents | Ask a curator, after a workshop or a first approved record |
| Curator | Approve records, add documents, handle gaps | Nominated by the council; trained in ethics and data |
| Council | Set rules, license, AI provider | See [governance](08-governance.md) |

## Good practice when writing for the archive

- One topic per page: short pages are retrieved more precisely by the assistant.
- A title that says what the page answers: "How to request tree pruning", not "Trees".
- Always the date and source at the top.
- Scanned documents need OCR first (`ocrmypdf in.pdf out.pdf -l por`); paste the text into the page and attach the PDF.
