Executing the application.
## LOCAL (two terminals)
uvicorn app.main:app --reload           # terminal 1
streamlit run streamlit_app.py          # terminal 2

## DOCKER — pass API_URL so Streamlit finds FastAPI inside container
docker build -t text-summarizer .
docker run -p 8000:8000 -p 8501:8501 \
  -e API_URL=http://localhost:8000 \
  text-summarizer