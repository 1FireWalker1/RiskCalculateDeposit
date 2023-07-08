#!/bin/bash

pytest > logs/pytest.log
STATUS=$?

cat logs/pytest.log

if [ $STATUS -ne 0 ] && [ $DEBUG -ne 0 ]; then
  echo 'Tests failed!'
  exit $STATUS
fi

uvicorn app.main:app --proxy-headers --host "0.0.0.0" --port $PORT