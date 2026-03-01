# ---- Base Image ----
FROM python:3.11-slim

# ---- Set Working Directory ----
WORKDIR /app

# ---- Copy requirements first (Docker cache optimization) ----
COPY requirements.txt .

# ---- Install dependencies ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project files ----
COPY . .

# ---- Expose port ----
EXPOSE 8000

# ---- Run API ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]