#!/bin/bash
python app.py &
sleep 3
python telegram_bot.py
