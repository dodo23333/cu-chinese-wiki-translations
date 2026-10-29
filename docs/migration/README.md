# 上游结构迁移记录

本记录供这段迁移期维护使用。主文件已完成目录、键名及拼接格式整理，尚未发布新补丁；数值与机制注解不在本次全面复核范围内。

## 核对基准

- 原补注：仓库提交 `5376d6762c74b6706a8241883da8487413c01f67` 中的 `维基中文中间文件.yaml`。
- 上游：[Orsoniks/scavgame-locale](https://github.com/Orsoniks/scavgame-locale)，提交 `e6e1c87d11ea2219f357ad2b6c0a221474c7f82f` 的 `demo/zh-CN.json`。
- 这些提交记录本次核对的依据。日常构建继续跟随上游 `main`，优先 release 中文，缺失时回退 demo，不以本次核对版本限制构建。

## 条目去向

| 处理 | 数量 | 说明 |
| --- | ---: | --- |
| 原路径保留 | 768 | 包括高血容量的 8 条名称及描述注解 |
| 已确认迁移 | 3 | 见下表 |
| 联机文本停止维护 | 299 | 从主文件移出，原文保存在条目记录中 |
| 历史遗留不迁移 | 31 | 不再兼容旧界面与旧基准 |
| 待核对 | 4 | 保留原文，取得依据后再决定 |
| 当前上游无对应键 | 8 | 旧低血容量条目，不加入主文件 |

原有 1,113 条字典注解中，771 条进入当前主文件，342 条留在记录中。另有 104 条旧暂停提示，完整保存在 [旧暂停提示](pause-quotes-legacy.yaml)，原文与顺序均未改变；它不参与默认合并。

[条目记录 JSON](entries.json) 保存每条源路径、去向、处理状态，以及移出条目的原文。仍在主文件中的条目使用目标路径取值；撤销记录中的前置换行、恢复迁移前路径，再合入移出条目，可以还原全部原始字典注解。原元数据也有记录，暂停列表另见归档文件。

## 已完成的迁移

| 原路径 | 当前路径 |
| --- | --- |
| `main.xalorisspongedsc` | `main.heatfernspongedsc` |
| `main.lifepodheaterdsc` | `buildings.lifepodheaterdsc` |
| `buildings.xalorisdsc` | `buildings.heatferndsc` |

以下 11 条描述在追加到上游文本前补一个换行。其余原有补注文本未因这次结构整理而改写。

- `buildings.spikestabberdscused`
- `buildings.stalactitedscdropped`
- `other.watchweight`
- `other.hpbrainhealth`
- `other.hpconsciousness`
- `other.hpsickness`
- `other.hphappiness`
- `other.hphunger`
- `other.hpthirst`
- `other.hpradiation`
- `other.hpinfection`

## 暂不迁移的非联机条目

“当前上游无对应键”仅描述此次语言文件核对结果，不据此判断游戏机制是否删除。历史遗留项已决定不再维持旧写法；待核对项仍保留迁移可能。

| 原路径 | 处理 |
| --- | --- |
| `buildings.chipcapsuledsc` | 待核对 |
| `moodles.lowbloodvolume1` | 当前上游无对应键 |
| `moodles.lowbloodvolume2` | 当前上游无对应键 |
| `moodles.lowbloodvolume3` | 当前上游无对应键 |
| `moodles.lowbloodvolume4` | 当前上游无对应键 |
| `moodles.lowbloodvolume1dsc` | 当前上游无对应键 |
| `moodles.lowbloodvolume2dsc` | 当前上游无对应键 |
| `moodles.lowbloodvolume3dsc` | 当前上游无对应键 |
| `moodles.lowbloodvolume4dsc` | 当前上游无对应键 |
| `other.volumewarning` | 待核对 |
| `other.volumewarningtext` | 待核对 |
| `other.looatmount` | 历史遗留，不迁移 |
| `other.trapamount` | 历史遗留，不迁移 |
| `other.lootdepthmultiplier` | 历史遗留，不迁移 |
| `other.trapdepthincrease` | 历史遗留，不迁移 |
| `other.radlinedisable` | 历史遗留，不迁移 |
| `other.unchipped` | 历史遗留，不迁移 |
| `other.looatmountdsc` | 历史遗留，不迁移 |
| `other.trapamountdsc` | 历史遗留，不迁移 |
| `other.lootdepthmultiplierdsc` | 历史遗留，不迁移 |
| `other.trapdepthincreasedsc` | 历史遗留，不迁移 |
| `other.radlinedisabledsc` | 历史遗留，不迁移 |
| `other.unchippeddsc` | 待核对 |
| `other.resettodefaultdsc` | 历史遗留，不迁移 |
| `other.mainmenu` | 历史遗留，不迁移 |
| `other.screenbrightness` | 历史遗留，不迁移 |
| `other.gamma` | 历史遗留，不迁移 |
| `other.paneltip` | 历史遗留，不迁移 |
| `other.keybinds` | 历史遗留，不迁移 |
| `other.keybindsdsc` | 历史遗留，不迁移 |
| `other.custommusic` | 历史遗留，不迁移 |
| `other.custommusicdsc` | 历史遗留，不迁移 |
| `other.deceased` | 历史遗留，不迁移 |
| `other.statusreport` | 历史遗留，不迁移 |
| `other.firmware` | 历史遗留，不迁移 |
| `other.depth` | 历史遗留，不迁移 |
| `other.caloriesconsumed` | 历史遗留，不迁移 |
| `other.mentalstate` | 历史遗留，不迁移 |
| `other.timetaken` | 历史遗留，不迁移 |
| `other.missionstatus` | 历史遗留，不迁移 |
| `other.missionstatusfailure` | 历史遗留，不迁移 |
| `other.casualties` | 历史遗留，不迁移 |
| `other.unknown` | 历史遗留，不迁移 |

其中 `other.unchippeddsc` 的旧注解仍待核对，不能因为存在名称相近的预设或开局设置项就直接追加。完整界面名称也不按近似键名批量迁移，避免拼出重复名称。

联机文本为 `other.krokosha_coop_` 前缀的 299 条。后续由相应模组承担联机汉化，维基中文不再内置维护。感谢内华达刃脊长期以来提供的多人联机汉化。

## 后续处理

- 逐项核对四条待核对注解，有明确依据后修改主文件及条目记录。
- 对照新版暂停提示改编旧提示，把仍适用的内容揉入新版；完成前保留整份旧列表，不直接整表覆盖。
- 日常合并留意新增键数量，需要逐项检查时使用 `--verbose`。新增键仍按原规则插入，不自动过滤。
- 游戏内检查文本显示、数值和机制说明，按实际结果继续维护主文件。
- 完成后可删除本目录的短期记录；暂停提示归档应在改编完成后再删除。

## 本地核对

已核对条目总数、路径去向及原文可还原性。此次记录不等同于用户游戏内验收或线上发布记录。
