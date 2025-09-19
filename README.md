# 换单服务端（升级骨架包）

版本：v2（2025-09-19 21:42:35）  
目标：**保留旧客户端兼容**的同时，新增“后台直打、导入向导、磁盘↔数据库对齐、版本包管理、客户端更新包管理、单笔查单/打印上报”等能力；
提供**一键在线安装**脚本（与历史命令一致）与**模块化分层**，便于后续扩展。

## 快速开始（开发）
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 一键在线安装（生产，与历史命令一致）
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/aidaddydog/huandan.server/main/scripts/bootstrap_online.sh)
```
> 可选参数：`--with-nginx` 开启 80 反代；环境变量：`REPO/BRANCH/APP_PORT/INSTALL_DIR/SERVICE_NAME`。

## 功能清单
- **后台列表页直打**：`POST /api/v1/print/merge`（服务端合并 PDF → 浏览器打印）
- **导入向导**：`/api/v1/import/orders`（CSV/XLSX）、`/api/v1/import/pdfs_zip`（ZIP）
- **对齐工具**：`/api/v1/align/scan`、`/api/v1/align/fix`
- **版本包管理**：`/api/v1/version/build`、`/api/v1/version/list`、`/api/v1/version/rollback`
- **客户端更新包**：`/api/v1/client/update/upload`、`/api/v1/client/update/check`
- **单笔查单/上报**：`/api/v1/lookup`、`/api/v1/print/report`
- **兼容旧客户端**：`/api/v1/version`、`/api/v1/mapping`、`/api/v1/file/{tracking}`、`/api/v1/runtime/sumatra`

## 日志/排障
- 服务日志：`journalctl -u huandan.service -e -n 200`
- Nginx（若启用）：`tail -n 200 /var/log/nginx/error.log`

