.PHONY: deploy update-app update-templates restart logs open-port

deploy:
	bash scripts/deploy/deploy_all.sh

update-app:            ## 更新应用代码（同步 + 依赖 + 重启）
	bash scripts/deploy/02-venv.sh
	bash scripts/deploy/03-sync-app.sh
	bash scripts/deploy/05-migrate.sh
	bash scripts/deploy/99-restart.sh

update-templates:      ## 仅更新模板/静态资源（快速）
	bash scripts/deploy/03-sync-app.sh
	bash scripts/deploy/99-restart.sh

restart:
	bash scripts/deploy/99-restart.sh

logs:
	journalctl -u huandan.service -e -n 200

open-port:
	bash scripts/deploy/06-firewall.sh
