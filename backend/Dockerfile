# Python base image
FROM python:3.11-slim

# Working directory
WORKDIR /app

# Copy requirements 
COPY requirements.txt .

# Dependencies install 
RUN pip install --no-cache-dir -r requirements.txt

# whole  backend copy
COPY . .

# Port expose 
EXPOSE 8000

# App run 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]