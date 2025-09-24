FROM python:3.11-slim

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy project configuration first for better caching
COPY app/CPU_Analysis/pyproject.toml ./CPU_Analysis/

# Install dependencies
RUN pip install --upgrade pip && pip install -e CPU_Analysis[dev]

# Copy the entire CPU_Analysis
COPY app/CPU_Analysis ./CPU_Analysis

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--NotebookApp.token=", "--NotebookApp.password="]