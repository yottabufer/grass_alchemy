#!/bin/bash
docker compose exec backend alembic upgrade head
read -p 'Press Enter to continue...'
