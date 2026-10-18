# 展示素材

## 视频与曲线

- 平地行走：[MP4](dexevt-walk-flat.mp4) / [GIF](dexevt-walk-flat.gif)
- WBT dance：[MP4](dexevt-wbt-dance.mp4) / [GIF](dexevt-wbt-dance.gif)
- [训练回报曲线](training-mean_return.svg)
- [训练 episode 长度曲线](training-mean_ep_len.svg)

MP4 为 960×720、60 fps，GIF 为 560×420、15 fps。行走视频 12 秒，舞蹈视频 16 秒。

## 录制回放

训练完成后，在项目根目录执行：

```bash
uv run --no-sync mxlab play env=dexevt-walk-flat num_envs=1 seed=1 record_video=true record_seconds=12 record_width=960 record_height=720
uv run --no-sync mxlab play env=dexevt-wbt-dance num_envs=1 seed=1 record_video=true record_seconds=16 record_width=960 record_height=720
```

视频输出到对应训练目录的 `play_video.mp4`。使用 `policy=/path/to/checkpoint.pt` 可指定策略。

## 生成曲线

[绘图脚本](plot_training.py) 读取两个训练目录的 TensorBoard 事件，生成回报与 episode 长度 SVG，使用[布局工具](plot_curves.py) 绘制。

```bash
uv run --no-sync python docs/media/plot_training.py /path/to/walk-run /path/to/dance-run
```

曲线使用 `rollout/mean_return` 和 `rollout/mean_ep_len`，横轴为训练环境步数。
