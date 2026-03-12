FROM python:3.10-slim

WORKDIR /app

# System dependencies (gcc needed for some torch builds)
RUN apt-get update && apt-get install -y \
    gcc g++ curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY . .

# FIX #5: COPY must come before RUN chmod — previous version had wrong order

RUN chmod +x start.sh
EXPOSE 8000 8501
CMD ["./start.sh"]