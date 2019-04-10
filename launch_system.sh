#!/usr/bin/env bash
docker exec -ti octopus_ws_control python main.py
docker exec -ti octopus_ws_emitter python main.py