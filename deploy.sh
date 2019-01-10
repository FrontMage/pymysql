#!/bin/bash
export CFG_PATH=./mysql.json 
gunicorn -w 4 -b 0.0.0.0:5000 main:app
