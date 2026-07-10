# 未知伤亡维基中文翻译项目
![GitHub License](https://img.shields.io/github/license/dodo23333/cu-chinese-wiki-translations)
![GitHub Release](https://img.shields.io/github/v/release/dodo23333/cu-chinese-wiki-translations)
![Version](https://img.shields.io/badge/dynamic/yaml?label=beta-version&url=https%3A%2F%2Fraw.githubusercontent.com%2Fdodo23333%2Fcu-chinese-wiki-translations%2Fmain%2F%25E7%25BB%25B4%25E5%259F%25BA%25E4%25B8%25AD%25E6%2596%2587%25E4%25B8%25AD%25E9%2597%25B4%25E6%2596%2587%25E4%25BB%25B6.yaml&query=%24.version&color=orange)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/dodo23333/cu-chinese-wiki-translations/total?logo=github&color=blue)
![Nexus Downloads](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/dodo23333/ef17a6816a5bbc1928c4c1a329683a4a/raw/scavprototype-64-downloads.json)
![Coverage badge](https://raw.githubusercontent.com/dodo23333/cu-chinese-wiki-translations/python-coverage-comment-action-data/badge.svg)

此项目旨在分离**基准翻译**（例如官方汉化与软盘汉化）与维基中文制作组的**附加翻译**,并且通过github妥善进行项目管理

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

初始化submodule：
```sh
git submodule update --init
```

完成！

## 开始使用
此项目通过`merge_data.py`合并基准翻译与附加翻译，例如：
- `vendor/zh-CN.json` + `维基中文中间文件.yaml` = `维基中文_基于官方翻译.json`
- `基准汉化_软盘.json` + `维基中文中间文件.yaml` = `维基中文_基于软盘翻译.json`

运行以下命令即可：
```sh
uv run merge-trans [-h] [-v "基准翻译.json"] [-r "附加翻译.yaml"] [-o "最后产物.json"]
```
- `-h | --help`：获取帮助
- `-v | --vendor`：基准翻译，默认：`vendor/zh-CN.json`
- `-r | --raw`：wiki汉化组补丁，默认：`维基中文中间文件.yaml`
- `-o | --output`：合并后文件，默认：`维基中文_基于官方翻译.json`
