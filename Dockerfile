# Building the image
FROM python:3.12-slim

# The working directory
WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffred logging
ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED = 1


# Copy the requirements
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy all the code
COPY . .

# Commands to run
CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "8000"]





