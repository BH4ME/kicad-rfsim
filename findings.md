# Findings & Decisions

## Requirements
- 将原项目 fork 到用户 GitHub 账号 `BH4ME`。
- 制作完整 macOS 版本，用户本机已有 KiCad。
- 每次修改更新版本号；按语义化版本处理，补丁变更递增最后一位，大改递增 minor。
- 在上下文压缩前把工作内容写入 Markdown，恢复后读取这些文件。
- 保留整个项目功能，而不是只做一个能加载的空壳插件。

## Research Findings
- Fork 已创建：`https://github.com/BH4ME/kicad-rfsim`。
- 本地目录：`/Users/bh4me_macair/Documents/ChatGPT/autopcb/kicad-rfsim-macos`。
- Git 远程：`origin` 是用户 fork，`upstream` 是 `NBalciunas/kicad-rfsim`。
- 当前上游提交：`efa0ea9 readme pic change`。
- 原项目是 KiCad 10 RFsim 插件，Python 代码位于 `plugins/`，验证脚本位于 `validation/`。
- `metadata.json` 的 v1.2.0 只声明 `windows` 平台。
- README 的安装流程依赖 Windows：`openEMS_x64_v*_msvc.zip`、`C:\openEMS`、KiCad Python、Python 3.14 venv。
- 插件运行分成两部分：KiCad Python 负责 GUI/结果显示；solver Python 负责 numpy、h5py、CSXCAD 和 openEMS。
- `plugins/solverenv.py` 已有 `venv/bin/python` 分支和 `OPENEMS_PATH`/`RFSIM_PYTHON` 环境变量，但默认候选路径仍包含 Windows 路径。
- `plugins/runner.py` 只在 Windows 下调用 `os.add_dll_directory`，Unix 分支可以避开该逻辑；GUI 子进程的 Windows 隐藏窗口标志也按 `os.name` 条件处理。
- 目前没有官方 macOS 构建、macOS 发布资产或 macOS 安装说明；源码“可能可移植”不等于已经支持。
- openEMS 官方源码 CI 已有 macOS ARM job，推荐通过 `update_openEMS.sh <prefix> --with-CTB --python` 构建；官方 release v0.0.36 仍只有通用 Windows ZIP，v0.37.0-rc3 才包含 RFsim 电感/Series RLC 所需的 `SetLEtype` 能力。
- 第三方 `vinn-ie/homebrew-openems` tap 提供 Apple Silicon 配方，但当前 pin 到 openEMS 0.0.36；可用于基础端口/R/C 仿真，完整 R/L/C 功能应使用 v0.37+ 源码构建。
- KiCad 10 帮助明确 macOS ActionPlugin 目录为 `~/Documents/KiCad/10.0/scripting/plugins`；本机 KiCad 为 10.0.3，通用 Python 3.9.13，`import pcbnew` 和 `wx` 可用。
- KiCad Python 3.9 对 `h5py`、`matplotlib`、`numpy` 需要兼容约束；安装器使用 `numpy<2.1`、`h5py<3.13`、`matplotlib<3.8`。
- 本机验证发现 `tempfile.TemporaryDirectory(ignore_cleanup_errors=True)` 是 Python 3.9 不兼容语法，已改为可移植调用。
- 完整功能包括 PCB 几何提取、端口、R/L/C 及寄生、S 参数、Touchstone、场动画、NF2FF 远场和结果绘图；每个激励端口需要一次 FDTD 运行。

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 优先抽象平台运行时，而不是复制一套 macOS 插件 | 减少 Windows 回归风险并保持上游同步能力 |
| 使用环境变量覆盖 openEMS 和 solver Python 路径 | 适合 macOS Homebrew、conda、venv 和用户自编译目录 |
| 在安装/诊断阶段提供明确的依赖检查 | macOS 的主要风险是动态库、Python ABI 和 KiCad Python 包路径 |
| macOS 发布前保留 headless runner 验证 | 可在没有 GUI 的情况下确认模型到 Touchstone 的核心链路 |
| macOS 首版从现有 1.2.0 增加 minor 版本 | 平台支持是功能级变更；具体版本以实现范围和发布结果为准 |
| source build 作为完整 solver 默认建议 | 官方 macOS 二进制缺失，第三方 0.0.36 不含最新 lumped-element API |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| fork CLI 第一次使用了错误的 `--org` 参数 | 已改为个人账号 fork，成功创建仓库 |
| 网络 git clone 初次不完整 | 使用 `gh repo clone` 获取完整工作树，状态正常 |

## Resources
- Fork: https://github.com/BH4ME/kicad-rfsim
- Upstream: https://github.com/NBalciunas/kicad-rfsim
- openEMS: https://openems.de
- KiCad Plugin and Content Manager metadata: `metadata.json`
- Runtime discovery: `plugins/solverenv.py`
- Solver process: `plugins/runner.py`

## Visual/Browser Findings
- 无需截图；已通过 GitHub API 和本地源码核对仓库信息。
