# 换单服务端（升级骨架包 v2.1）

版本：v2.1（2025-09-19 21:54:40）  
在 v2 基础上修复与增强：
- **新增 /health 健康检查**，安装脚本据此验证服务可用；
- **安装脚本创建 LOG_DIR**（如 /var/log/huandan），避免 systemd 追加日志目录不存在；
- **其余结构与接口保持不变**（后台直打、导入向导、对齐工具、版本包、客户端更新、自检升级、旧客户端兼容）。

## 在线安装（与历史命令一致）
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/aidaddydog/huandan.server/main/scripts/bootstrap_online.sh)
```

## 常见问题
- SumatraPDF.exe 404：将可执行文件放到 `runtime/` 目录即可。
- 找不到 PDF：检查 DB `TrackingFile.file_path` 或 `storage/pdfs/{tracking}.pdf` 是否存在。

