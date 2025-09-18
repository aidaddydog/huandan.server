# Huandan 仓库骨架（可直接复制）

此包已包含：应用源码（`src/`）、配置（`config/`）、部署脚本（`scripts/`）、热修示例（`scripts/hotfix/`）。

## 最简单用法（不想看步骤）
在仓库根目录直接运行：
```bash
sudo bash quickstart.sh
```
它会：
1) 复制示例环境文件到 `/etc/huandan.env`（如已存在则跳过）；
2) 顺序执行模块化部署脚本；
3) 打印服务状态与一键日志命令。

## 常用命令（可选）
- 一键部署：`make deploy`
- 仅更新模板/静态：`make update-templates`
- 更新代码+依赖后重启：`make update-app`
- 查看服务日志：`make logs`

> 目标系统：Ubuntu 24.x（以 24.04 LTS 为准）；运行方式：venv + systemd；默认监听 `0.0.0.0:8000`。
