#!/bin/bash

# Обновление системы и установка нужных пакетов
apt update
apt install -y python3 python3-pip git

# Клонируем твой репозиторий
cd /root
git clone https://github.com/Blackwoodey/tour-turum-webapp.git

cd tour-turum-webapp

# Устанавливаем зависимости Python
pip3 install fastapi uvicorn

# Запускаем сервер (в фоне)
nohup uvicorn server:app --host 0.0.0.0 --port 8000 &
