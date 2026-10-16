# NoteProof: Bitcoin timestamps and an AI-tagged knowledge graph for students' lecture notes

SEN0401 Special Topics: Blockchain · 2026-2027 Fall · Proposal · Method: BRSF software-development profile · Self-assessed grade 100/100

## Team, roles and work distribution

| Member | Student number | E-mail | Administrative roles | Development roles | Planned share |
| --- | --- | --- | --- | --- | --- |
| Arda Özcan | 2200004482 | 2200004482@stu.iku.edu.tr | Team lead | Architect, Back-end developer | 15% |
| Aysu Akdüzen | 2200004962 | 2200004962@stu.iku.edu.tr | Customer liaison | Requirements analyst | 14% |
| Eylem Sarıbal | 2000003742 | 2000003742@stu.iku.edu.tr | Work-log steward | Knowledge engineer | 14% |
| Aleyna Cebeci | 2100002803 | 2100002803@stu.iku.edu.tr | Work-log steward | AI and language-model engineer | 14% |
| Burak Sami Şirin | 2200004655 | 2200004655@stu.iku.edu.tr | Repository and release manager | Smart-contract developer, Release and operations | 15% |
| Erdener Çimen | 2200004744 | 2200004744@stu.iku.edu.tr | Process facilitator, Documentation lead | Front-end developer, Interaction and game designer | 14% |
| Emine Esra Çiçek | 2100004506 | 2100004506@stu.iku.edu.tr | Quality lead | Test engineer, AI and language-model engineer | 14% |

### Modules and features

| Module or feature | Kind | What it does | Delivers epic | Responsible member | Second member |
| --- | --- | --- | --- | --- | --- |
| Note ontology and SKOS course vocabulary | Module | Note, course and topic model on schema.org and PROV-O, the SKOS scheme of courses and topics, and the SHACL shapes | Tag notes with the course knowledge graph | Eylem Sarıbal · 2000003742 | Aleyna Cebeci · 2100002803 |
| Registration service | Module | Accepts uploads, hashes notes with SHA-256, records the registration and validates the tags | Register and timestamp notes on Bitcoin | Arda Özcan · 2200004482 | Burak Sami Şirin · 2200004655 |
| Bitcoin timestamp service | Module | Builds the daily Merkle tree, writes its root in an OP_RETURN output on signet and stores each note's proof | Register and timestamp notes on Bitcoin | Burak Sami Şirin · 2200004655 | Arda Özcan · 2200004482 |
| AI tagger | Feature | Suggests a note's course, topics and a two-sentence summary, limited to the SKOS vocabulary, for the author to confirm | Tag notes with the course knowledge graph | Aleyna Cebeci · 2100002803 | Eylem Sarıbal · 2000003742 |
| Copy warning and evaluation set | Feature | Flags notes similar to earlier ones by text embeddings; the 60 evaluation notes and 20 planted copies that measure the tagger and the warning | Search, copy warnings and proof pages | Emine Esra Çiçek · 2100004506 | Aleyna Cebeci · 2100002803 |
| Search and proof pages | Feature | Topic search with narrower topics, note cards with proof badges, and the public proof page | Search, copy warnings and proof pages | Erdener Çimen · 2200004744 | Aysu Akdüzen · 2200004962 |
| Student survey, pilot and acceptance | Module | The survey, the contact with the 3rd- and 4th-year students, the pilot with volunteers and the acceptance of each story | Search, copy warnings and proof pages | Aysu Akdüzen · 2200004962 | Emine Esra Çiçek · 2100004506 |

### Process leads

- Mission analysis: Arda Özcan
- Stakeholder needs and requirements: Aysu Akdüzen
- System/software requirements definition: Aysu Akdüzen
- Architecture definition: Arda Özcan
- Design definition: Aleyna Cebeci
- System analysis: Eylem Sarıbal
- Implementation: Burak Sami Şirin
- Integration: Arda Özcan
- Verification: Emine Esra Çiçek
- Transition: Burak Sami Şirin
- Validation: Aysu Akdüzen
- Operation: Burak Sami Şirin
- Maintenance: Erdener Çimen
- Disposal: Burak Sami Şirin

### Work log

14 entries; chain intact; head fingerprint 6c50f9f875f2d69af0c0c904e0721bd8b65bd1f576655301f06f9a6c259ce115.

| No. | Time (UTC) | Member | Process | Hours | What | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-10-16 14:16 | Arda Özcan | Mission analysis | 2 | Compared four project ideas (repair passport, signet quests, lecture-note proof, designer artwork proof) and chose NoteProof with the team |  |
| 2 | 2026-10-16 14:19 | Aysu Akdüzen | Stakeholder needs and requirements | 1.5 | Analysed the 20 survey responses and wrote the problem statement with their numbers |  |
| 3 | 2026-10-16 14:23 | Arda Özcan | Stakeholder needs and requirements | 1.5 | Designed the five-question student survey and shared it in the 3rd- and 4th-year WhatsApp groups |  |
| 4 | 2026-10-16 14:24 | Aysu Akdüzen | Validation | 1.5 | Checked the problem statement and the objectives’ baselines against the survey export |  |
| 5 | 2026-10-16 14:24 | Eylem Sarıbal | System analysis | 1.5 | Listed the 14 chapters of Mastering Bitcoin as the first topics of the SEN0401 vocabulary |  |
| 6 | 2026-10-16 14:25 | Eylem Sarıbal | Design definition | 1.5 | Drafted the SKOS scheme with broader and narrower links for the Transactions chapter |  |
| 7 | 2026-10-16 14:25 | Aleyna Cebeci | System analysis | 1.5 | Compared text extraction from PDFs and photos (pypdf and Tesseract) for the AI tagger |  |
| 8 | 2026-10-16 14:26 | Aleyna Cebeci | Design definition | 1.5 | Wrote a first prompt that limits the tagger’s topics to the vocabulary and tried it on three notes |  |
| 9 | 2026-10-16 14:26 | Burak Sami Şirin | System analysis | 1.5 | Read the OP_RETURN section of Mastering Bitcoin and Nakamoto’s timestamp server section and summarised how one Merkle root goes on chain |  |
| 10 | 2026-10-16 14:27 | Burak Sami Şirin | Implementation | 1.5 | Set up a Bitcoin Core node on signet and got test coins from a faucet |  |
| 11 | 2026-10-16 14:27 | Erdener Çimen | Design definition | 1.5 | Sketched the search page and the note card with its proof badge |  |
| 12 | 2026-10-16 14:28 | Erdener Çimen | Transition | 1.5 | Accepted the repository invitation and wrote the README with the project summary |  |
| 13 | 2026-10-16 14:28 | Emine Esra Çiçek | System analysis | 1.5 | Compared text-similarity methods (TF-IDF and sentence embeddings) for the copy warning |  |
| 14 | 2026-10-16 14:29 | Emine Esra Çiçek | Verification | 1.5 | Reviewed the test cases of the seven stories and the definition of done |  |

## 1. Mission

### Customer

| Customer (organisation or role) | Contact person or role | How and when you reached them | Relation | What they get from it |
| --- | --- | --- | --- | --- |
| 3rd- and 4th-year Software Engineering students at İstanbul Kültür University | 3rd- and 4th-year students who answered our survey | Google Form survey shared in the 3rd- and 4th-year WhatsApp groups on 16 October 2026, 20 responses | Owner of the system | one archive where their notes are found by course and topic, credited to the students who registered them, with a proof anyone can check |

### End users

| User group (short name) | Who exactly | What they do with the system | How often | Device or channel |
| --- | --- | --- | --- | --- |
| Note author | students who write their own lecture notes and share them with classmates | uploads a note, confirms its course and topics, and receives a timestamp proof | Weekly | phone or laptop browser |
| Note reader | students who look for notes before quizzes and exams | searches notes by course and topic and checks who registered each note first | Weekly | phone |
| Note verifier | a classmate, a lecturer or a club jury settling who had a note first | opens a note's proof page and checks when and by whom it was registered | Occasionally | laptop browser |

### Problem

Students in our department share their lecture notes with each other, but the notes end up scattered across WhatsApp groups, photographed pages and a few Drive folders. In a survey of 20 third- and fourth-year students on 16 October 2026, 17 said they share their own notes, 3 of them regularly; 10 of the 17 share them in WhatsApp groups and 9 send photos of the pages. Five of the 20 said a note of theirs had been passed on or sold without their name or permission, and 5 more could not tell, because nobody can follow a note once it is shared. Nobody can prove who had a note first either: file dates change whenever a file is copied, and the owner of a shared folder can edit or replace anything in it. Before an exam, the median student needs 10 to 20 minutes to find a note on one topic, and 13 of the 20 need 10 minutes or more, scrolling through chats with no way to tell which copy is the original. Authors get no credit for their work and readers study from whatever copy they find; 14 of the 20 said they would use an archive that finds notes by course and topic and proves whose note each one is.

### Mission statement

Give every Note author a way to register a lecture note and receive a proof, anchored on the Bitcoin signet in the way Nakamoto's timestamp server describes, that the note existed in their hands on that day; let an AI tagger file each note under a shared course and topic vocabulary; and let every Note reader find notes by topic, see who registered each one first, and be warned about copies of earlier notes.

Origin: Derived

### Outcome

A student uploads a note after class, confirms the course and topics the AI suggests, and the next day holds a proof linked to a Bitcoin transaction; before the exam a classmate searches a topic, finds that note with its author and date, and anyone can check the proof without trusting the archive or the people who run it.

## 2. Scope

### Areas

| Area | Where it lives | How big it is today |
| --- | --- | --- |
| Note registration and Bitcoin timestamping | register/ and anchor/ | notes scattered in chats and folders, with no proof of who had them first |
| Course knowledge graph and AI tagging | ontology/, shapes/ and tagger/ | no shared course and topic vocabulary today |
| Search, copy warnings and proof pages | web/ and search/ | searching means scrolling through chats today |

### Deliverables

| Deliverable | Area | Layer | Kind |
| --- | --- | --- | --- |
| Registration service that hashes each note with SHA-256 and records who registered it and when (PROV-O) | Note registration and Bitcoin timestamping | Product layer | Functional |
| Daily Merkle-root timestamp on Bitcoin signet with a Merkle-path proof for every note | Note registration and Bitcoin timestamping | Product layer | Functional |
| Only a 32-byte root on chain: no note content, names or student numbers | Note registration and Bitcoin timestamping | Product layer | Non-functional |
| Note ontology on schema.org, a SKOS vocabulary of courses and topics, and SHACL shapes | Course knowledge graph and AI tagging | Product layer | Functional |
| AI tagger that suggests a note's course, topics and a short summary for the author to confirm | Course knowledge graph and AI tagging | Product layer | Functional |
| Evaluation set of 60 notes with known topics and 20 planted copies | Course knowledge graph and AI tagging | Work layer | Functional |
| Topic search that also finds narrower topics, with answers that cite the notes | Search, copy warnings and proof pages | Product layer | Functional |
| Copy warning that compares a new note with earlier timestamped notes | Search, copy warnings and proof pages | Product layer | Functional |
| Public proof page that checks a note file against the Bitcoin transaction without the archive's server | Search, copy warnings and proof pages | Product layer | Functional |
| Search results and proof checks appear in under 3 seconds on a phone | Search, copy warnings and proof pages | Product layer | Non-functional |

### Exclusions

| Left out | Why |
| --- | --- |
| Bitcoin mainnet transactions and real fees | the course project runs on signet; the proof works the same way and needs no real money |
| Proving who originally wrote a note | a timestamp proves that a file existed and who registered it at that time; it cannot show that the registrant did not copy it from an unregistered source |
| Deciding plagiarism cases or punishing students | the system shows evidence; decisions stay with people such as lecturers and the class |
| Lecturers' slides, textbook pages and other people's material | the archive is for students' own notes; others' material is outside its purpose and its copyright |

### Domain entities

| Entity | What it is | Created? | Used? | Retired? |
| --- | --- | --- | --- | --- |
| Note | a student's own lecture note file (PDF, photo or text), a schema:CreativeWork identified by its SHA-256 hash | Created — yes | Used — yes | Retired — yes |
| Registration | a PROV-O activity recording which student account registered which note hash, and when | Created — yes | Used — yes | Retired — no |
| Topic | a SKOS concept for a course topic, such as 'Transaction fees' under SEN0401, with broader and narrower topics | Created — yes | Used — yes | Retired — no |
| Daily timestamp | a signet transaction whose OP_RETURN output holds the Merkle root of one day's note hashes | Created — yes | Used — yes | Retired — no |
| Proof | a note's Merkle path and the txid, which anyone can check against the block | Created — yes | Used — yes | Retired — no |

### Project kinds

Provenance and trust › Blockchain-anchored provenance; Semantic search and question answering. Stack layers they need: Identifiers and publishing, Provenance and metadata, AI and knowledge graphs, Query, Vocabularies and taxonomies.

### Semantic technologies, by stack layer

- AI and knowledge graphs: GraphRAG pattern
- Data model: RDFLib
- Governance and compliance: KVKK personal-data regime
- Identifiers and publishing: Stable IRI and negotiation practice
- Provenance and metadata: PROV-O provenance ontology
- Query: SPARQL 1.1 and 1.2
- Serialisation: JSON-LD 1.1 contexts, RDFLib
- Storage and serving: Oxigraph
- Validation: SHACL shapes, pySHACL
- Vocabularies and taxonomies: schema.org, SKOS concept schemes

Each note is described as a schema.org CreativeWork, and PROV-O records the registration activity: which student account registered which hash, and when, so the archive's history is standard linked data that the proof page can show. A SKOS concept scheme holds the courses and their topics, starting from SEN0401's fourteen chapters, with broader and narrower links; the AI tagger may only choose concepts from it, and a SPARQL property path over skos:narrower lets a search for 'Transactions' also find notes on 'Transaction fees'. SHACL shapes, run with pySHACL, refuse a note without a course, an unknown topic or an unconfirmed tag. Records travel as JSON-LD, RDFLib handles them in Python and Oxigraph stores them. Search answers follow the GraphRAG pattern: the model only phrases notes the graph returns and cites them. Stable IRIs give every proof a permanent link, and the KVKK regime decides that only hashes reach the chain.

## 3. Goals

| Goal | Facing | Covers area | Why this goal |
| --- | --- | --- | --- |
| Every shared note carries a proof of when and by whom it was registered, checkable without the archive | Mission-facing | Note registration and Bitcoin timestamping | this is the credit authors lack today |
| Every note is tagged with a course and topics from the shared vocabulary | Scope-facing | Course knowledge graph and AI tagging | an untagged note cannot be found |
| Readers find notes by topic and are warned about copies of earlier notes | Scope-facing | Search, copy warnings and proof pages | search and the copy warning are what readers use |
| No note content or personal data reaches the chain, and no AI tag is saved without the author's confirmation | Containment-facing | Note registration and Bitcoin timestamping | KVKK forbids the first; trust in the archive forbids the second |

### Specification

The system lets a student upload a lecture note as a PDF, a photo or text. It computes the note's SHA-256 hash and records the registration with PROV-O. An AI tagger reads the note's text and suggests a course, topics from the SKOS vocabulary and a two-sentence summary; nothing is saved until the author confirms, and the SHACL shapes refuse a note without a course or with an unknown topic. A copy check compares the new note with earlier notes and links possible copies to the earlier note's proof. Once a day the timestamp service builds a Merkle tree of the day's hashes and writes its root in an OP_RETURN output of a Bitcoin signet transaction, giving each note a Merkle path. Readers search by course and topic, including narrower topics. A public proof page recomputes a note's hash, walks its Merkle path and shows the block time, without needing the archive's server.

### Test scenarios

| Kind | Scenario (Given / When / Then) |
| --- | --- |
| Nominal | Given a note registered and confirmed today, when the daily timestamp has one confirmation, then the note's proof page shows its hash, its Merkle path, the signet txid and the block time |
| Rejection | Given a note file that was changed by one character after it was timestamped, when its proof is checked, then the hash does not match and the page says it is not the registered file |
| Rejection | Given a note whose author picks a topic that is not in the vocabulary, when the author confirms it, then the note is refused and the author is asked to choose a topic from the list |

### Use cases

Note author: upload a note, confirm the AI's tags, get a proof. Note reader: search by topic, open a note, see its author and date. Note verifier: open a proof page and check it. 3rd- and 4th-year students: own the archive and decide its upload rules.

## 4. Objectives

| Objective | Goal | Measured by | How exactly it is measured | Now | Target | Direction |
| --- | --- | --- | --- | --- | --- | --- |
| Notes with a valid timestamp proof within 24 hours | Every shared note carries a proof of when and by whom it was registered, checkable without the archive | Derived | share of pilot notes whose Merkle path verifies against a confirmed signet transaction within 24 hours of upload, % | 0 | 100 | Increase |
| Notes tagged with a valid course and topics | Every note is tagged with a course and topics from the shared vocabulary | Counted | share of pilot notes whose confirmed tags pass the shapes, % | 0 | 100 | Increase |
| AI topic suggestions accepted unchanged | Every note is tagged with a course and topics from the shared vocabulary | Judged | share of suggested topics that authors confirm without correction on the 60 evaluation notes, % | 0 | 80 | Increase |
| Minutes to find a note on a topic before an exam | Readers find notes by topic and are warned about copies of earlier notes | Counted | median minutes a student needs to find a note on one topic: now, the middle of the survey's median answer (10 to 20 minutes, 20 students); in the pilot, timed for 20 searches | 15 | 2 | Decrease |
| Planted copies caught by the copy warning | Readers find notes by topic and are warned about copies of earlier notes | Counted | share of the 20 planted copies in the evaluation set that the copy warning flags, % | 0 | 90 | Increase |
| Note content, personal data or unconfirmed tags leaked | No note content or personal data reaches the chain, and no AI tag is saved without the author's confirmation | Counted | OP_RETURN outputs holding anything but a 32-byte root, plus saved tags the author did not confirm | 0 | 0 | Hold |

### Activity model

Swimlanes: Note author · NoteProof services · Bitcoin signet · Note reader or verifier

A. Register a note1. Start: the note author uploads a note (PDF, photo or text).2. The registration service checks the file type and size. [not allowed] → the upload is refused with the reason → end.3. It computes the note's SHA-256 hash. [hash already registered] → the page shows the earlier registration and its proof → end.4. Fork, in parallel:   4a. The AI tagger extracts the text and suggests a course, topics from the SKOS vocabulary and a two-sentence summary.   4b. The copy checker compares the text with earlier notes.5. Join: the author sees the suggestions and any similar earlier note.6. The author confirms or corrects every tag. [author cancels] → nothing is saved → end.7. pySHACL validates the confirmed tags against the shapes. [invalid] → the violations are shown and the author returns to step 6.8. [similar earlier note found] → the note is marked as a possible copy and linked to the earlier note's proof.9. The note and its PROV-O registration are stored and its hash is queued; the author sees "proof pending". End of the author's flow.

B. Daily timestamp (time event: every day at 23:00)10. The timestamp service collects the day's queued hashes. [queue empty] → end.11. It builds the Merkle tree and puts the 32-byte root in an OP_RETURN output.12. It broadcasts the transaction to the Bitcoin signet through Bitcoin Core and waits for one confirmation. [not confirmed within 6 blocks] → it bumps the fee and broadcasts again.13. It stores the txid, the block height and each note's Merkle path, and marks the notes "timestamped". End.

C. Find and check a note14. The reader searches by course and topic; the search also covers narrower topics.15. The reader opens a note card with its author, date and proof badge.16. On the proof page the browser recomputes the file's hash, walks its Merkle path and fetches the block from a public signet node.17. [hash and root match] → "proven", with the block time. [no match] → "not the registered file". End.

### Sequence model

The upload page sends the file to the registration service, which computes the SHA-256 hash, extracts the text and asks the tagger and the copy checker in parallel. The tagger asks the language model for concepts limited to the SKOS vocabulary and returns them; the copy checker compares the text's embedding with earlier notes and returns any match. The author confirms; the service asks pySHACL to validate and stores the note and its PROV-O registration in Oxigraph. Each night the timestamp service reads the day's hashes, builds the Merkle tree, asks the Bitcoin Core signet node to fund and broadcast an OP_RETURN transaction, waits for a confirmation and stores the txid and each Merkle path. The proof page recomputes the hash in the browser, walks the path and asks a public signet node for the block.

## 5. Backlog

Kind of development: Initial development

### Epics

| Epic | Pursues objective |
| --- | --- |
| Register and timestamp notes on Bitcoin | Notes with a valid timestamp proof within 24 hours |
| Tag notes with the course knowledge graph | Notes tagged with a valid course and topics |
| Search, copy warnings and proof pages | Minutes to find a note on a topic before an exam |

### Stories

| Epic | As a | I want | So that | Acceptance (Given / When / Then) | Category | Design concern | Value 1–10 | Time 1–10 | Risk 1–10 | Size 1–10 | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Register and timestamp notes on Bitcoin | Note author (end user) | to upload my note and get a proof of when I registered it | I can show later that I had it first | Given my note PDF When I upload it Then I see its SHA-256 hash and registration time, and after the next daily timestamp a proof linked to a signet transaction | New capability | Data | 9 | 7 | 6 | 4 | 5.5 |
| Register and timestamp notes on Bitcoin | Note author (end user) | every note registered in a day to be timestamped in one Bitcoin transaction | proofs cost one transaction a day instead of one per note | Given 40 notes registered today When the daily timestamp runs Then one signet transaction holds their Merkle root and each note has its own Merkle path | New capability | Security | 8 | 6 | 8 | 5 | 4.4 |
| Tag notes with the course knowledge graph | Note author (end user) | the AI to suggest my note's course and topics for me to confirm | tagging takes seconds and uses the same words as everyone else | Given a note about transaction fees When I upload it Then the AI suggests SEN0401 and the topic 'Transaction fees' from the vocabulary, and nothing is saved until I confirm | New capability | Interaction | 7 | 5 | 5 | 5 | 3.4 |
| Tag notes with the course knowledge graph | Note author (end user) | to be stopped when my note has no course or an unknown topic | the archive stays searchable | Given a note whose topic is not in the vocabulary When I confirm it Then it is refused and I am asked to pick a topic from the list | New capability | Data | 5 | 4 | 6 | 2 | 7.5 |
| Search, copy warnings and proof pages | Note reader (end user) | to search a topic and also find notes on its narrower topics | I find the right note before an exam in minutes | Given notes tagged 'Transaction fees' and 'Fee rate' When I search 'Transactions' in SEN0401 Then both notes are listed with their authors and registration dates | New capability | User interface | 9 | 7 | 4 | 4 | 5 |
| Search, copy warnings and proof pages | Note reader (end user) | to be warned when a note looks like a copy of an earlier one | I credit the student who had it first | Given a note nearly identical to one registered a week earlier by another student When it is uploaded Then it is marked as a possible copy and linked to the earlier note's proof | New capability | Architecture | 7 | 4 | 7 | 5 | 3.6 |
| Search, copy warnings and proof pages | Note verifier (end user) | to check a note's proof from a link without an account | I can settle who had a note first without trusting the archive | Given a note file and its proof link When I open the proof page while the archive's server is offline Then the page recomputes the hash, walks the Merkle path and shows the block time of the signet transaction | New capability | Interface | 8 | 4 | 7 | 3 | 6.3 |

### Definition of done

| Criterion | How it is checked |
| --- | --- |
| All tests pass in continuous integration | GitHub Actions on every push, with a regtest node for the timestamp tests |
| Notes conform to the shapes | pySHACL in the registration service's tests |
| Only 32-byte roots reach the chain | a test decoding every OP_RETURN output of the test run |
| The AI tagger and copy warning meet their targets | the 60-note evaluation set, run in CI |

### Class model

Note is a schema:CreativeWork identified by its SHA-256 hash, with a title, a file type, a summary, one Course and one or more Topics. Course and Topic are skos:Concepts in one scheme, linked by skos:broader and skos:narrower. Registration is a prov:Activity that generated the Note's record, associated with a StudentAccount (pseudonymous) at a time. A new version of a note is a new Note linked by prov:wasRevisionOf. DailyTimestamp holds a date, a Merkle root, a signet txid and a block height; every Note has one Proof, its Merkle path, pointing to a DailyTimestamp. CopyWarning links a Note to an earlier Note with a similarity score.

### Test cases

| For story | Test case | Test data |
| --- | --- | --- |
| to upload my note and get a proof of when I registered it | upload a note PDF and check its hash, registration time and, after anchoring, its proof | one sample note PDF |
| every note registered in a day to be timestamped in one Bitcoin transaction | register 40 notes, run the daily timestamp on regtest and verify every Merkle path against the transaction | 40 sample notes and a funded regtest wallet |
| the AI to suggest my note's course and topics for me to confirm | upload the 60 evaluation notes and compare the suggested topics with the known ones | the 60-note evaluation set |
| to be stopped when my note has no course or an unknown topic | confirm a note with a topic outside the vocabulary and expect a refusal | one note with an unknown topic |
| to search a topic and also find notes on its narrower topics | search 'Transactions' and expect notes on its narrower topics | notes tagged with a topic and its narrower topics |
| to be warned when a note looks like a copy of an earlier one | upload the 20 planted copies and count how many are flagged | 20 planted copies of evaluation notes |
| to check a note's proof from a link without an account | verify a note file on the proof page with the archive's server switched off | one timestamped note and a public signet node |

### Architecture — Component diagram

Component diagram: RegistrationService (hashing, PROV-O, pySHACL) writing to Oxigraph; Tagger, the only component that calls the language model for tags, limited to the SKOS concepts; CopyChecker comparing text embeddings; TimestampService holding the signet wallet key and talking to a Bitcoin Core node; SearchService answering SPARQL; ProofPage verifying in the browser.

### Data — Class diagram

Design-level class diagram: Note (schema:CreativeWork), Course and Topic (skos:Concept), Registration (prov:Activity), StudentAccount (prov:Agent, pseudonymous), DailyTimestamp, Proof and CopyWarning; NoteShape requires a hash, a course and at least one topic from the scheme, and no class holds a real name or student number.

### Interaction — Sequence diagram

Sequence: the author uploads a note; the page shows the AI's suggested course, topics and summary; the author confirms or changes each one from the vocabulary list; the page sends the confirmed tags; the service validates them and returns the registration time and the note's pending proof.

### Interface — Component diagram

Component boundary: the proof is a small JSON-LD file with the note's hash, its Merkle path, the txid and the block height; the ProofPage needs only this file, the note file and any public signet node, so it works when the archive's server is gone; the registration API returns the named shape violations.

### Security — State machine diagram

State machine of a note: uploaded, tagged, confirmed, registered, timestamped, superseded. Only the author moves a note from tagged to confirmed; only confirmed notes are queued for the daily timestamp; a timestamped note is never edited - a new version is a new note that revises it; a file whose hash does not match its proof is shown as not the registered file.

### User interface — design model

Storyboard: an upload page with a drop area and the AI's suggestions as removable chips; a search page with course and topic filters and note cards showing author, date and a proof badge (pending, proven or altered); a proof page with the hash, the Merkle path drawn as a small tree, the txid and the block time; Turkish labels, phone first.

## 6. Course-specific

### Blockchain design

The project is a direct implementation of the timestamp server in section 3 of Nakamoto's Bitcoin paper: hash the items, publish the hash widely, and the publication proves the items existed at that time; each new block includes the previous one, so every later block reinforces the timestamp. We use the Bitcoin signet through a Bitcoin Core node and its RPC interface, with regtest for automated tests. Each note is hashed with SHA-256; once a day the hashes form a Merkle tree (section 7 of the paper, from Bayer, Haber and Stornetta) and one transaction spends a UTXO into an OP_RETURN output carrying the 32-byte root, so any number of notes costs one transaction. A note's proof is its Merkle path and the txid; checking it is like simplified payment verification (section 8): the verifier needs the path and the block, not a full node. A blockchain is needed because the archive and whoever runs it can change dates in their own database; only a public record that nobody can rewrite without redoing the proof-of-work of that block and every block after it gives a time that no single party controls. Only the root goes on chain, never note content or personal data.

## Plan and risks

| Date | Deliverable | Lead |
| --- | --- | --- |
| 2026-10-30 | Course vocabulary, note ontology and shapes; registration with SHA-256 | Eylem Sarıbal |
| 2026-11-13 | Daily Bitcoin signet timestamps and the public proof page | Burak Sami Şirin |
| 2026-11-27 | AI tagger, copy warning and topic search | Aleyna Cebeci |
| 2026-12-11 | Pilot with 3rd- and 4th-year volunteers, evaluation report and tagged release v1.0.0 | Arda Özcan |

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| A copier registers a note before its real author does | Medium | High | authors register on the day they write; the copy warning links later copies to the earlier proof; the exclusions state what a timestamp cannot prove |
| The AI suggests wrong topics | Medium | Medium | topics must come from the SKOS scheme, the author confirms every tag, and the evaluation set measures accuracy in CI |
| Students upload slides or textbook pages instead of their own notes | Medium | Medium | upload rules, a report button and removal from the archive; only hashes are on chain, so removal is complete |
| Too few students use it to make search useful | Medium | High | pilot in a quiz week with volunteers from the 3rd- and 4th-year groups and seed the archive with the team's own notes |
| The signet faucet or node is unavailable | Medium | Low | keep a funded test wallet and fall back to regtest for demonstrations |

Repository: https://github.com/aozcan4482/noteproof — Confirmed on GitHub 2026-10-16 (public, created 2026-10-16)

## References

1. Nakamoto, S. (2008). Bitcoin: A Peer-to-Peer Electronic Cash System.
2. Antonopoulos, A. M. & Harding, D. A. (2023). Mastering Bitcoin, 3rd ed. O'Reilly.
3. Haber, S. & Stornetta, W. S. (1991). How to time-stamp a digital document. Journal of Cryptology 3(2).
4. Bayer, D., Haber, S. & Stornetta, W. S. (1993). Improving the efficiency and reliability of digital time-stamping. In Sequences II, Springer.
5. Todd, P. (2016). OpenTimestamps: Scalable, Trust-Minimized, Distributed Timestamping with Bitcoin.
6. Alm, K. (2019). BIP 325: Signet. Bitcoin Improvement Proposals.
7. W3C (2013). PROV-O: The PROV Ontology. W3C Recommendation.
8. W3C (2009). SKOS Simple Knowledge Organization System Reference. W3C Recommendation.
9. W3C (2017). Shapes Constraint Language (SHACL). W3C Recommendation.
10. Law No. 6698 on the Protection of Personal Data (KVKK), Türkiye.

## Self-assessment

| Part | Weight | Grade | Criteria met |
| --- | --- | --- | --- |
| Team and work | 10% | 100/100 | 12 of 12 |
| Mission | 20% | 100/100 | 7 of 7 |
| Scope | 15% | 100/100 | 8 of 8 |
| Goal | 15% | 100/100 | 7 of 7 |
| Objective | 10% | 100/100 | 3 of 3 |
| Backlog | 20% | 100/100 | 10 of 10 |
| Course-specific | 5% | 100/100 | 1 of 1 |
| Plan and references | 5% | 100/100 | 3 of 3 |
| Overall | 100% | 100/100 |  |

### Member grades (Proposal)

Project grade 100 (60%), team grade 100 (20%), individual contribution (20%).

| Member | Student number | Individual | Member grade |
| --- | --- | --- | --- |
| Arda Özcan | 2200004482 | 100 | 100 |
| Aysu Akdüzen | 2200004962 | 100 | 100 |
| Eylem Sarıbal | 2000003742 | 100 | 100 |
| Aleyna Cebeci | 2100002803 | 100 | 100 |
| Burak Sami Şirin | 2200004655 | 100 | 100 |
| Erdener Çimen | 2200004744 | 100 | 100 |
| Emine Esra Çiçek | 2100004506 | 100 | 100 |

