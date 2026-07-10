# scripts/ — deterministic machinery

Where determinism lives (D-002). Planned population:

| Script | Step | Role |
|---|---|---|
| `test_schemas.py` | 1 (done) | Schema lint + fixture validation |
| `load_context.py` | 2 | Packet assembly: L0 + one project via indexes; namespace assertions; manifest |
| `transition.py` | 2 | The only writer of workflow state (SQLite + work-order `state:`) |
| index generators | 2 | `_index.yaml`, `_claim-keys.yaml`, `cited_by` maintenance |
| `schema_validate.py` | 2 | HK6 write-time validation + queue screens |
| `report_*.py` | 10 | status / digest / costs / expiry reports |

Run tests: `python scripts/test_schemas.py` (more runners land with each step).
