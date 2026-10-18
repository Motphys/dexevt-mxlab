"""Dependency-free SVG layout shared by TensorBoard showcase plots."""

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS = [("dexevt-walk-flat", "Flat walking", "#087f8c"), ("dexevt-wbt-dance", "WBT dance", "#ae4d28")]


def plot(series, output, title, ylabel, note):
    width, height = 1120, 420
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1120" height="420" rx="16" fill="#f7f9fc"/>',
        '<g font-family="DejaVu Sans,Arial,sans-serif" fill="#172b4d">',
        f'<text x="32" y="35" font-size="21" font-weight="700">{html.escape(title)}</text>',
        f'<text x="32" y="58" font-size="12" fill="#526581">{html.escape(note)}</text>',
    ]
    for i, (name, color, rows, key) in enumerate(series):
        left, top, pw, ph = 84 + i * 550, 115, 435, 225
        xs = [float(r["environment_steps"]) / 1e6 for r in rows]
        ys = [float(r[key]) for r in rows]
        lo, hi = min(ys), max(ys)
        pad = (hi - lo) * 0.12 or max(abs(hi) * 0.1, 0.001)
        lo, hi = lo - pad, hi + pad
        xmax = max(xs)
        parts.append(f'<text x="{left}" y="88" font-size="16" font-weight="700">{name}</text>')
        for j in range(5):
            y = top + ph * j / 4
            val = hi - (hi - lo) * j / 4
            parts.extend(
                [
                    f'<path d="M{left},{y}h{pw}" stroke="#dce3ed"/>',
                    f'<text x="{left - 10}" y="{y + 4}" text-anchor="end" font-size="11">{val:.4g}</text>',
                ]
            )
            x = left + pw * j / 4
            parts.append(
                f'<text x="{x}" y="{top + ph + 22}" text-anchor="middle" font-size="11">{xmax * j / 4:.2f}</text>'
            )
        coords = [(left + x / xmax * pw, top + (hi - y) / (hi - lo) * ph) for x, y in zip(xs, ys)]
        points = " ".join(f"{x:.2f},{y:.2f}" for x, y in coords)
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="3"/>')
        for x, y in coords:
            parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.5" fill="{color}"/>')
        parts.extend(
            [
                f'<text x="{left + pw / 2}" y="{top + ph + 46}" text-anchor="middle" font-size="12">'
                "Training environment steps (millions)</text>",
                f'<text transform="translate({left - 62},{top + ph / 2}) rotate(-90)" '
                f'text-anchor="middle" font-size="12">{html.escape(ylabel)}</text>',
            ]
        )
    parts.append("</g></svg>")
    (ROOT / output).write_text("\n".join(parts) + "\n")
