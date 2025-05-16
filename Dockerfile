
FROM python:3.11-slim


WORKDIR /app

# Copy requirements file into container
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy all your app code into container
COPY . .

# Command to run your FastAPI app using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
