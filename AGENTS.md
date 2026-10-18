# Contributor / agent guidance

This repository demonstrates an external MotrixLab project: custom robot, task,
MDP, assets and training presets live here. MotrixLab provides the framework.

- Keep `motrixlab` as the sole direct runtime dependency. Do not import builtin
  `motrix_envs` or `motrix_robots`, or reference another local checkout.
- Use the packaged `mxlab` CLI; do not copy training/play orchestration here.
- Keep environment and robot discovery in the corresponding Python entry-point
  groups. Keep Hydra training recipes in root `configs/task/`; registration must
  not mutate Hydra search paths.
- Use `@configclass` for declarative configs and `@dispatch` for Manager kernel
  entry methods; standalone Numba-compatible helpers may use `@njit`.
- Preserve original copyright/SPDX notices on copied code. Asset licensing is
  separate from code licensing; document asset sources and redistribution terms.
- Use an activated `.venv` or `uv run --no-sync` after installation. Initial sync
  currently requires `GIT_LFS_SKIP_SMUDGE=1` for upstream framework checkout.
- Run `ruff check .`, `ruff format --check .`, and `pytest` before proposing changes.
  Plugin tests are integration tests; full GPU training is separate acceptance.
- Record one-time build/install/hardware evidence in change descriptions, not in
  brittle tests asserting a specific migration layout or fixed hyperparameter values.
