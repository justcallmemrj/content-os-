-- SQLite DDL v1 — Phase 7 §4 verbatim. Live DB (state/workflow.sqlite) is
-- gitignored per DEC-BUILD-004; this file is the versioned contract.
CREATE TABLE IF NOT EXISTS runs(run_id TEXT PRIMARY KEY, task_id TEXT, project TEXT, profile TEXT,
  parent_run TEXT, state TEXT, contains_pii INTEGER DEFAULT 0,
  created_at TEXT, updated_at TEXT);
CREATE TABLE IF NOT EXISTS transitions(run_id TEXT, seq INTEGER, from_state TEXT, to_state TEXT,
  initiator TEXT, event TEXT, gate_results TEXT /*json*/, artifact_hashes TEXT /*json*/,
  ts TEXT, PRIMARY KEY(run_id, seq));
CREATE TABLE IF NOT EXISTS escalations(id INTEGER PRIMARY KEY, run_id TEXT, stage TEXT, rule TEXT,
  memo_path TEXT, resolved_by TEXT, resolution TEXT, ts TEXT);
CREATE TABLE IF NOT EXISTS evals(id INTEGER PRIMARY KEY, run_id TEXT, rubric TEXT, target TEXT,
  scores TEXT /*json*/, required_pass INTEGER, composite REAL, ts TEXT);
CREATE TABLE IF NOT EXISTS costs(id INTEGER PRIMARY KEY, run_id TEXT, stage TEXT, agent TEXT,
  model TEXT, input_tokens INTEGER, output_tokens INTEGER, usd REAL, ts TEXT);
