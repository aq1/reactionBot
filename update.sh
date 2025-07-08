git pull
export REACTION_BOT_RELEASE=$(git rev-parse --short HEAD)
docker build -t reaction_bot:${REACTION_BOT_RELEASE} .
docker compose up -d
docker system prune -f
docker image prune -af

