# Production notes template (SK-C1) — kept current per piece, auditable & remixable

Copy to `video/hyperframes/<project>/<piece>/PRODUCTION-NOTES.md`.

```markdown
# <piece> — production notes

## STORYBOARD
- source: runs/<id>/storyboard/storyboard.yaml (sha256 <hash>)
- script: <parent run + locked hash>
- scenes: <count>; duration <s>; platform <spec>

## DESIGN
- tokens: tokens.css @ <hash> (⚑ derived/ratified status)
- safe areas: <AR row from wrapper-rules §2>
- disclosure block: <DISC-* id>, scenes <range>, placement <where>
- type scale / motion notes: <what a future editor needs>

## BUILD
- sub-compositions: <list, one line each — what it does, what it reuses>
- upstream patterns used: <vendored skill + pattern name>
- variables: <what is configurable for re-versioning>

## RENDERS
- v1: <date> · manifest <id> · <verdict/QC pointer> · <kept/superseded>

## DEVIATIONS
- <zero, or each: requested vs delivered + the escalation record>

## REUSE CANDIDATES
- <sub-compositions worth proposing for the library, with the proposal ID once filed>
```
