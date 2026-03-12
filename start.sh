#!/bin/bash
set -e

echo "Starting FastAPI backend..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

#Wait until FastAPI is actually responding before starting Streamlit

echo "Waiting for FastAPI to be ready..."

until curl -sf http://localhost:8000/ > /dev/null; do

  sleep 1

done

echo "FastAPI is up!"


echo "Starting Streamlit frontend..."
streamlit run streamlit_app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true \     # FIX #10: skips email prompt; required in Docker

  --server.fileWatcherType none