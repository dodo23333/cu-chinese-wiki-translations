# 未知伤亡维基中文翻译项目

![GitHub License](https://img.shields.io/github/license/dodo23333/cu-chinese-wiki-translations)
![GitHub Release](https://img.shields.io/github/v/release/dodo23333/cu-chinese-wiki-translations)
![Version](https://img.shields.io/badge/dynamic/yaml?label=beta-version&url=https%3A%2F%2Fraw.githubusercontent.com%2Fdodo23333%2Fcu-chinese-wiki-translations%2Fmain%2F%25E7%25BB%25B4%25E5%259F%25BA%25E4%25B8%25AD%25E6%2596%2587%25E4%25B8%25AD%25E9%2597%25B4%25E6%2596%2587%25E4%25BB%25B6.yaml&query=%24.version&color=orange)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/dodo23333/cu-chinese-wiki-translations/total?logo=github&color=blue)
![Nexus Downloads](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/dodo23333/ef17a6816a5bbc1928c4c1a329683a4a/raw/scavprototype-64-downloads.json)
![Coverage badge](https://raw.githubusercontent.com/dodo23333/cu-chinese-wiki-translations/python-coverage-comment-action-data/badge.svg)

本项目将上游中文翻译与维基中文制作组的补注分开维护，再合并为游戏可读取的语言文件。补注包含数值、功能说明和游戏心得。

当前正在按上游的新结构整理补注，尚未发布新的补丁版本。后续不再维护旧版游戏及旧基准兼容，也不再内置多人联机汉化。感谢内华达刃脊长期以来提供的多人联机汉化；联机汉化请使用相应模组。

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
- `--build-info PATH`：将本次构建输入记录写为 Markdown，父目录需已存在。

基准没有的补注键仍会加入结果，不会因提示而被过滤。补注未覆盖的基准内容保持原样。以 `dsc` 结尾的字符串在追加时自动换行，其他字符串直接拼接；列表仍是整份替换，使用自定义补注时请留意。

每次运行都会显示两份输入的路径、文件内版本、所属仓库当前提交号和该文件的修改状态。暂存与未暂存修改可以同时存在，命令始终读取磁盘内容。带修改状态的提交号只表示基点，不能完整还原未提交内容；Git 信息不可获取时仍可合并。

输出 JSON 保留基准的游戏版本字段；补丁版本用于语言名称和产物文件名，两者分别记录。选中正式版基准并不意味着所有数值和机制注解均已完成游戏内核对。

## 迁移与发布说明

[迁移记录](docs/migration/README.md) 汇总本次条目去向及待办，旧暂停提示单独留档，不参与默认合并。完整改编后可删除这份短期记录及相应归档。

Actions 只构建上游中文对应的补丁，构建信息会显示在运行摘要并随构建附件保存。推送版本 tag 时，发布步骤会组合 [本次公告](docs/release-notes.md)、该次构建输入和自动生成的更新记录；准备下次发布时请更新公告正文。普通分支或 PR 构建不创建 Release。
