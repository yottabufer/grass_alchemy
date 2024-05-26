#!/bin/bash
docker compose exec backend pytest
read -p 'Press Enter to continue...'
