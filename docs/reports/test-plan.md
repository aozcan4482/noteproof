# Test plan review

Owner: emine (Quality lead, P09 Verification) · Second: arda · Task: EMN-R2 · Rule set v2.0

This document checks the seven test cases of the proposal (stories S1–S7) and the four Definition of Done
criteria one by one: is there an automated test, in which file, and if it is missing, whose task adds it.
It is the starting point of the test report (EMN-6, `docs/reports/test-report.md`).

## Snapshot

| | |
| --- | --- |
| Date | 2026-11-25 |
| `main` | No code and no tests yet (proposal files only) |
| Code under test | `TestBranch` (PR #3, commit `547c0bb`): `anchor/`, `copywarn/`, `evalset/` |
| Local run | `python -m pytest -q` → **60 passed, 1 skipped** (the regtest test is skipped when `bitcoind` is not installed) |
| CI | Only `.github/workflows/copywarn.yml` (runs `tests/copywarn`); the general `ci.yml` does not exist yet |

Status values: **Covered** = an automated test checks the acceptance criterion · **Partial** = some parts are
tested, the end-to-end criterion is not · **Missing** = no automated test.

## Stories (proposal test cases)

| Story | Proposal test case | Automated test today | Status | Missing part → task (owner) |
| --- | --- | --- | --- | --- |
| S1 Upload and get a proof | Upload a note PDF, check its hash, registration time and, after anchoring, its proof | `tests/anchor/test_daily.py::test_40_notes_one_transaction_and_valid_proofs` checks the proof half (proofs verify offline and on chain) | Partial | Upload → hash + registration time via the API: ARD-4 (arda, "S1 acceptance test"). Full flow upload → daily timestamp → proof: EMN-4 (emine) |
| S2 One transaction per day | Register 40 notes, run the daily timestamp on regtest, verify every Merkle path against the transaction | `tests/anchor/test_daily.py::test_40_notes_one_transaction_and_valid_proofs` (fake node); `tests/anchor/test_regtest.py::test_40_notes_anchored_on_regtest` (real `bitcoind`, skipped without it) | Covered locally | Regtest test must run in CI without being skipped: BRK-2 (burak) |
| S3 AI suggests course and topics | Upload the 60 evaluation notes and compare suggested topics with the known ones | — | Missing | S3 acceptance test with `FakeLLM`: ALY-4 (aleyna). O3 measurement on the 60 notes: ALY-5 (aleyna), needs EMN-2 (emine) |
| S4 Unknown topic is refused | Confirm a note with a topic outside the vocabulary and expect a refusal | — | Missing | Shape rejects an unknown topic: EYL-5 (eylem). API returns 422 `shape_violation` and stores nothing: ARD-4 (arda). End-to-end: EMN-4 (emine) |
| S5 Search finds narrower topics | Search "Transactions" and expect notes on its narrower topics | — | Missing | S5 acceptance test in `tests/search/`: ERD-5 (erdener), needs EYL-3 (eylem) |
| S6 Possible-copy warning | Upload the 20 planted copies and count how many are flagged | `tests/copywarn/test_checker.py::test_s6_acceptance_nearly_identical_note_is_linked_to_earlier_proof`; `tests/copywarn/test_evalset.py::test_evaluation_meets_the_90_percent_target_on_synthetic_notes` (20/20 on synthetic notes) | Covered (synthetic data) | Measurement on the 60 real notes and 20 planted copies: EMN-2, EMN-3 (emine) |
| S7 Check a proof without the archive | Verify a note file on the proof page with the archive's server switched off | `tests/anchor/test_daily.py::test_changed_file_is_not_the_registered_file` checks the Python verifier | Partial | Browser verifier on shared vectors: BRK-3 (burak) + ERD-2 (erdener, `tests/web/`). Proof page offline scenario: ERD-3 (erdener). Manual acceptance: AYS-1 (aysu) |

## Mandatory rejection scenarios (`01` section 7)

| Scenario | Automated test today | Status | Missing part → task (owner) |
| --- | --- | --- | --- |
| A file changed by one character after timestamping → "not the registered file" | `tests/anchor/test_daily.py::test_changed_file_is_not_the_registered_file` (Python side, message "kayıtlı dosya değil") | Partial | Same check in the browser: ERD-2, ERD-3 (erdener). End-to-end: EMN-4 (emine) |
| A topic outside the vocabulary → the note is refused | — | Missing | EYL-5 (eylem), ARD-4 (arda), EMN-4 (emine) |

## Definition of Done

| Criterion | Proposal check | Today | Status | Missing part → task (owner) |
| --- | --- | --- | --- | --- |
| 1. All tests pass in CI | GitHub Actions on every push, with a regtest node for the timestamp tests | `copywarn.yml` runs only `tests/copywarn`; `tests/anchor` is not run in CI | Partial | General `ci.yml` with `bitcoind`: BRK-2 (burak) |
| 2. Notes conform to the shapes | pySHACL in the registration service's tests | No `shapes/` and no `register/` yet | Missing | EYL-5 (eylem), ARD-4 (arda), EYL-7 (eylem) |
| 3. Only 32-byte roots reach the chain | A test decoding every OP_RETURN output of the test run | `tests/anchor/test_daily.py::test_only_32_byte_roots_reach_the_chain`; `tests/anchor/test_opreturn.py::test_tx_holds_only_root`, `test_only_32_bytes_allowed` | Covered locally | Run in CI: BRK-2 (burak). Signet measurement for O6: BRK-8 (burak) |
| 4. AI tagger and copy warning meet their targets | The 60-note evaluation set, run in CI | `copywarn.yml` runs `python -m evalset.run_copywarn` once `evalset/manifest.csv` has rows; it is empty today | Partial | 60 notes and 20 planted copies: EMN-2, EMN-3 (emine). Tagger measurement in CI: ALY-5 (aleyna) |

## Findings for the owners

1. **Story numbers in test names** (`03` section 8: "each story's acceptance criterion is at least one test whose
   name contains the story"). `tests/anchor/` has the S2 and S7 tests but their names do not contain the story
   (e.g. `test_40_notes_one_transaction_and_valid_proofs`). Request to burak: rename or add `test_s2_...` and
   `test_s7_...` while doing BRK-4.
2. **No general CI.** Until BRK-2 is merged, `tests/anchor` (including the S2 regtest test) never runs in CI.
   DoD 1 and DoD 3 cannot be ticked on any PR before that.
3. **Three stories have no test at all** (S3, S4, S5). Their tests are already part of ALY-4, ARD-4/EYL-5 and ERD-5;
   all of these are past or at their due date (23–27 Nov) and none has started on any branch.
4. **End-to-end tests** (EMN-4) depend on ARD-4 and ARD-6. Until they are in `main`, EMN-4 is written against the
   API in `02` section 7 with `NP-STUB`.

## How this plan is kept up to date

Each row moves to **Covered** only when the named test is in `main` and green in CI (`05` section 1.1). The final
status of every row goes into `docs/reports/test-report.md` (EMN-6) with the CI run link.
