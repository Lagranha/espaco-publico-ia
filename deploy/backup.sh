#!/usr/bin/env bash
# Backup do Espaço Público IA / backup
# Uso / usage (na pasta deploy/): bash backup.sh /caminho/do/destino
set -euo pipefail

DESTINO="${1:?Informe a pasta de destino / give a destination folder}"
ALVO="$DESTINO/espaco-publico-ia-$(date +%Y-%m-%d)"
mkdir -p "$ALVO"

# Banco da wiki (o acervo vivo)
docker compose exec -T db pg_dump -U wikijs wiki | gzip > "$ALVO/wiki.sql.gz"

# Dados do assistente (contas, conversas, índice do acervo, lacunas)
PROJETO=$(basename "$(pwd)")
docker run --rm -v "${PROJETO}_open-webui":/dados -v "$ALVO":/backup alpine \
  tar czf /backup/open-webui.tar.gz -C /dados .

# Configuração (sem o .env, que tem segredos: guarde-o à parte, com cuidado)
cp Caddyfile docker-compose.yml robots.txt "$ALVO/"

echo "Backup salvo em / saved to: $ALVO"
ls -lh "$ALVO"
