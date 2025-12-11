# 1. Use an official Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy dependency list and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the application code
COPY . .

# 5. Expose the port Flask will run on
EXPOSE 5000

# 6. Set environment variables (Flask uses PORT inside app.py)
ENV PORT=5000

# 7. Command to start the app
CMD ["python", "app.py"]
