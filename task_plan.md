# Task Plan: macOS 版 KiCad RFsim

## Goal
把 NBalciunas/kicad-rfsim fork 到 BH4ME 账号，并将插件、openEMS 运行环境、安装说明、版本发布和测试流程完整适配到 macOS；每次变更遵循语义化版本号并保留可恢复的 Markdown 进度记录。

## Current Phase
Phase 5: Delivery (complete)

## Phases

### Phase 1: Requirements & Discovery
- [x] 确认用户目标和版本策略
- [x] Fork 到 `BH4ME/kicad-rfsim`
- [x] 检查原项目结构、平台限制和本机环境
- [x] 将发现写入 `findings.md`
- **Status:** complete

### Phase 2: macOS 适配设计
- [x] 确认 KiCad、Python、openEMS、CSXCAD 的 macOS 可用组合
- [x] 梳理 Windows 专属路径、动态库和安装流程
- [x] 设计跨平台路径、启动器、打包与版本策略
- **Status:** complete

### Phase 3: Implementation
- [x] 实现 macOS/Unix 运行时适配
- [x] 更新插件元数据、安装脚本和文档
- [x] 加入版本文件和发布检查
- [x] 保持 Windows 路径兼容
- **Status:** complete

### Phase 4: Testing & Verification
- [x] 运行 Python 单元/验证脚本
- [x] 在本机 KiCad 中验证插件加载和 GUI/solver 启动
- [x] 验证最小仿真和 Touchstone 输出
- [x] 检查 macOS 打包内容与版本号
- **Status:** complete

### Phase 5: Delivery
- [x] 提交到 fork
- [x] 创建 macOS 版本标签/Release（已验证）
- [x] 汇总安装方法、已验证范围和剩余限制
- **Status:** complete

## Key Questions
1. 本机 KiCad 的版本、架构（Apple Silicon/Intel）和内置 Python 版本是什么？
2. openEMS/CSXCAD 是否有可直接使用的 macOS 构建，还是需要本地编译？
3. 插件是否能在不改 KiCad 核心的情况下使用用户指定的 solver Python？
4. macOS 发布是 Universal 还是按 arm64/x86_64 分发？
5. 版本策略是否按 SemVer：补丁变更递增 patch，大功能递增 minor，破坏性变更递增 major？

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 使用独立目录 `kicad-rfsim-macos` | 避免覆盖当前 `autopcb` 工作区中的用户内容 |
| `origin` 指向 `BH4ME/kicad-rfsim`，`upstream` 指向原仓库 | 便于同步上游与推送 fork |
| 默认采用 SemVer | 与现有 `metadata.json` 的 1.2.0 版本兼容；macOS 支持属于 minor 级功能 |
| 先做跨平台代码和运行时适配，再做真实 KiCad 验证 | 先消除可静态检查的 Windows 假设，再验证本机环境 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| `gh repo fork ... --remote=false` 参数不受支持 | 1 | 改用 GitHub CLI 的个人账号 fork 命令 |
| 把个人账号 `BH4ME` 传给 `--org` | 1 | 改为不传 `--org` 的个人 fork |
| 初次 git clone 在超时后留下无 HEAD 的空仓库 | 1 | 使用 `gh repo clone` 重新获取，已成功检出 main |

## Notes
- 用户要求在上下文压缩前写入 Markdown；本文件、`findings.md` 和 `progress.md` 是持续恢复依据。
- 不把“能安装插件”当成“完整 macOS 版”；必须验证 solver、GUI、最小仿真和打包。
