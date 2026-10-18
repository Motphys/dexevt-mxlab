"""Render README curves from TensorBoard training scalars.

Usage: uv run --no-sync python docs/media/plot_training.py WALK_RUN DANCE_RUN
"""

import argparse
import json
import math
from pathlib import Path

from plot_curves import TASKS, plot
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

TAGS = {"mean_return": "rollout/mean_return", "mean_ep_len": "rollout/mean_ep_len"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("walk_run", type=Path)
    parser.add_argument("dance_run", type=Path)
    args = parser.parse_args()
    series = {key: [] for key in TAGS}
    for (_, name, color), run in zip(TASKS, [args.walk_run, args.dance_run]):
        metadata = json.loads((run / "metadata.json").read_text())
        if not metadata.get("performance"):
            raise ValueError(f"Training has not completed; no final performance metadata in {run}")
        num_envs = metadata["performance"]["num_envs"]
        events = EventAccumulator(str(run), size_guidance={"scalars": 0}).Reload()
        for key, tag in TAGS.items():
            rows = [
                {"environment_steps": item.step * num_envs, "value": item.value}
                for item in events.Scalars(tag)
                if math.isfinite(item.value)
            ]
            if not rows:
                raise ValueError(f"No finite values for {tag} in {run}")
            series[key].append((name, color, rows, "value"))
    for key, title, ylabel in [
        ("mean_return", "Training curves · episode return", "Mean episode return"),
        ("mean_ep_len", "Training curves · episode length", "Mean episode length (control steps)"),
    ]:
        plot(
            series[key],
            f"training-{key}.svg",
            title,
            ylabel,
            f"TensorBoard tag: {TAGS[key]}. Raw finite logged samples, no smoothing; seed 1, 2,048 environments.",
        )


if __name__ == "__main__":
    main()
