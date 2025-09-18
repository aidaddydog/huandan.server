#!/usr/bin/env bash
set -Eeuo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export LOG="/var/log/huandan-deploy.log"

for f in 01-prepare.sh 02-venv.sh 03-sync-app.sh 04-systemd.sh 05-migrate.sh 06-firewall.sh 99-restart.sh; do
  echo -e "\n==== 运行 $f ====\n"
  bash "$DIR/$f"
done

echo -e "\n全部步骤完成。若失败，可查看：tail -n 200 $LOG"
