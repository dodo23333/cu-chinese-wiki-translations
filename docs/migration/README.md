# 上游结构迁移记录

本轮字典补注迁移已收尾，仅剩暂停提示改编。这里保留处理决定和改编材料，不再维护逐条清单；暂停提示迁入主文件后，可删除整个目录。

## 已完成的处理

| 原路径 | 处理 |
| --- | --- |
| `main.xalorisspongedsc` | 迁到 `main.heatfernspongedsc` |
| `main.lifepodheaterdsc` | 迁到 `buildings.lifepodheaterdsc` |
| `buildings.xalorisdsc` | 迁到 `buildings.heatferndsc` |
| `other.unchippeddsc` | 改写后迁到 `other.runsetunchippeddsc`，保留新手提醒和含蓄的结局提示；不沿用旧文中混合开局设置与地层事件的说明 |

- 保留其余匹配上游的补注，并为 11 处文本拼接补齐换行。
- 放弃旧版界面与旧基准兼容，移出 31 条历史遗留内容。
- 放弃 `buildings.chipcapsuledsc`、`other.volumewarning`、`other.volumewarningtext`，未找到可确认的对应目标。
- 放弃上游无对应键的 8 条旧低血容量补注，不再作为待迁移项。
- 停止内置多人联机汉化，移出 `other.krokosha_coop_` 前缀的 299 条文本。

原补注见提交 `5376d6762c74b6706a8241883da8487413c01f67`。本轮对照上游提交 [`e6e1c87`](https://github.com/Orsoniks/scavgame-locale/tree/e6e1c87d11ea2219f357ad2b6c0a221474c7f82f) 的 `demo/zh-CN.json` 与 `release/EN.json`；这些是核对依据，不限制日常构建跟随上游更新。已移出条目的明细可从 Git 历史查阅，无需另行维护 JSON 清单。

## 暂停提示

- [旧暂停提示](pause-quotes-legacy.yaml)：保留原有 104 条提示的原文与顺序，供改编时取材。
- [分组骨架](pause-quotes-template.yaml)：可粘贴到 `维基中文中间文件.yaml` 末尾，再逐组填写。

当前公开 Release 英文将 `pauseQuotes` 分为 `normal`、`dying`、`happy`、`depressed`、`combat`、`combatelder`，另有两组剧透占位符。骨架保留六个已公开名称；其余分组等实际名称和文本公开后再补。

骨架默认全部注释。待正式版中文提供对应分组后，对照当时的文本改编旧提示，填入每组完整的中文列表，再取消 `pauseQuotes:` 和已完成分组前的注释；未改编的组保持注释，沿用上游内容。列表会整组替换，因此不能只填新增提示，也不要启用空列表或占位文字。

旧提示中的通用技巧可放入日常分组，伤病、情绪和战斗相关提示再按情境整理。目前主文件仍不包含 `pauseQuotes`，合并结果沿用上游提示。
