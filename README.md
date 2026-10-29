# 未知伤亡维基中文翻译项目

![GitHub License](https://img.shields.io/github/license/dodo23333/cu-chinese-wiki-translations)
![GitHub Release](https://img.shields.io/github/v/release/dodo23333/cu-chinese-wiki-translations)
![Version](https://img.shields.io/badge/dynamic/yaml?label=beta-version&url=https%3A%2F%2Fraw.githubusercontent.com%2Fdodo23333%2Fcu-chinese-wiki-translations%2Fmain%2F%25E7%25BB%25B4%25E5%259F%25BA%25E4%25B8%25AD%25E6%2596%2587%25E4%25B8%25AD%25E9%2597%25B4%25E6%2596%2587%25E4%25BB%25B6.yaml&query=%24.version&color=orange)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/dodo23333/cu-chinese-wiki-translations/total?logo=github&color=blue)
![Nexus Downloads](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/dodo23333/ef17a6816a5bbc1928c4c1a329683a4a/raw/scavprototype-64-downloads.json)
![Coverage badge](https://raw.githubusercontent.com/dodo23333/cu-chinese-wiki-translations/python-coverage-comment-action-data/badge.svg)

本项目将上游中文翻译与维基中文制作组的补注分开维护，再合并为游戏可读取的语言文件。补注包含数值、功能说明和游戏心得。

Q群：521023836

如果只是单纯想反馈问题的话更建议直接开issue或者pr，要是不会可以进群反馈

## 贡献指南

请参考[Contributing.md](CONTRIBUTING.md)

## 关于颜色

调色板为Google UI

- 装备属性: `#91a7ff`
- 食物医疗: `#72d572`
- 配方用途: `#ffee58`
- 腐败耐久: `#ffa726`
- 生物血量: `#e84e40`
- 注释心得: `orange`

## 安装

这个项目使用[uv](https://docs.astral.sh/uv/getting-started/installation/),请确定你安装了它

克隆仓库：

```sh
git clone https://github.com/dodo23333/cu-chinese-wiki-translations.git
```

安装项目依赖：

```sh
uv sync
```

拉取上游翻译：

```sh
git submodule update --init --recursive --remote
```

完成！

## 开始使用

默认使用 `vendor/release/zh-CN.json`，该文件不存在时使用 `vendor/demo/zh-CN.json`，并在终端提示。`main` 是上游分支名，不属于文件路径。两者都不存在，或选中的文件无法读取、解析时，命令会报错。

本地合并只读取当前磁盘文件，不自动拉取上游。需要更新时先运行上面的子模块命令；Actions 构建会自行拉取上游 `main`。

运行以下命令即可：

```sh
uv run merge-trans
uv run merge-trans -v "基准翻译.json" -r "附加翻译.yaml" -o "最后产物.json"
uv run merge-trans --verbose --build-info build-info.md
```

- `-h | --help`：获取帮助
- `-v | --vendor`：明确指定基准文件；指定后不再自动选择或回退。
- `-r | --raw`：wiki汉化组补丁，默认：`维基中文中间文件.yaml`
- `-o | --output`：合并后文件，默认：`wiki-translations-official.json`
- `--verbose`：列出补注向基准新增的完整键路径。默认只显示数量。
- `--build-info PATH`：把终端显示的输入来源另存为 Markdown，方便核对或附在公告中。例如 `--build-info build-info.md` 会写到当前目录；若指定其他目录，请先创建该目录。

### 查看合并结果

命令会显示实际使用的基准文件、补注文件及它们的版本。合并结果默认保存在当前目录的 `wiki-translations-official.json`，原来的两份输入文件不会被修改。

“新增键数量”指补注中有、基准中没有的条目数量。这些条目仍会写入结果。如果想知道具体新增了哪些条目，使用 `--verbose` 查看完整键名。

补注没有涉及的内容保持上游原样。编辑补注时，请留意以下拼接规则：

- 键名以 `dsc` 结尾：在原文后换行，再追加补注。
- 其他文本：直接追加，不自动加空格或换行。需要分行时，应在补注开头写入换行。
- 列表：用补注中的整份列表替换基准列表。因此旧暂停提示目前单独留档，没有放入默认补注。
- 两边同一个键的数据类型不同：保留基准值，不用补注覆盖。

### 查看输入版本与修改状态

构建记录分别列出基准和补注的路径、文件内版本号、Git 提交号（`HEAD`）和文件状态。两种版本号用途不同：基准的 `version` 原样保留在输出 JSON 中；补注的 `version` 用于游戏中的语言名称，Actions 也会将它加到下载文件名中。

| 文件状态 | 含义 |
| --- | --- |
| `clean` | 该文件与记录的提交一致。 |
| `staged` | 该文件的修改已加入 Git 暂存区，但尚未提交。 |
| `unstaged` | 该文件有尚未加入暂存区的修改。 |
| `both` | 已暂存一部分修改，之后又修改了该文件。 |
| `untracked` | 该文件尚未纳入 Git 跟踪。 |
| `git unavailable` | 无法获取 Git 信息，例如文件不在 Git 仓库内；仍可正常合并。 |

命令始终读取磁盘上当前保存的内容。例如，暂存后又改了文字，合并时会使用后改的文字。有未提交修改时，提交号只能帮助找到修改前的版本，不能单凭它还原本次输入。

这些记录用于核对文件来源。文件成功合并后，数值、机制和游戏内显示仍需人工检查。

## 迁移与发布说明

[迁移记录](docs/migration/README.md) 保留本次迁移的处理决定。迁移收尾仅剩暂停提示改编，目录内附旧提示和可扩写的分组骨架，均不参与默认合并；改编完成后可删除整个目录。

Actions 只构建上游中文对应的补丁，构建信息会显示在运行摘要并随构建附件保存。推送版本 tag 时，发布步骤会加入该次构建输入和自动生成的更新记录。普通分支或 PR 构建不创建 Release。

[人工公告](docs/release-notes.md) 的第一行指定它适用的发布 tag，例如 `<!-- release-tag: v1.9.0 -->`（仅为格式示例）。只有发布 tag 与这一行完全匹配且正文非空时，公告正文才会加入 Release；不匹配、文件不存在或仍标为 `unreleased` 时，跳过人工正文并在日志中提示，不中止发布。准备发布前请同时更新这一行和公告正文。文件不会在发布后自动删除，同一个 tag 重跑时仍可使用对应公告。

## 致谢

- **Orsoniks**：《未知伤亡》游戏作者，感谢其构筑了令人着迷的独特世界观与优秀的游戏本体。
- **Oro Interactive**：本作发行商。
- **未知伤亡中文汉化组**：感谢汉化组的杰出翻译，为本项目提供核心基准汉化文本。
- **内华达刃脊**：曾长期提供多人联机部分的汉化文本，补全了维基中文早期的联机内容空缺。
- **软盘**：曾提供本项目早期版本的汉化文本，在维基中文初创阶段功不可没。
