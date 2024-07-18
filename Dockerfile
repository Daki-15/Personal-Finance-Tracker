FROM python:3.10-alpine

# Set working directory
WORKDIR /app

# Copy project
COPY . /app/

# Install dependencies
RUN pip install -r requirements.txt

# Command to run the application
CMD ["python", "main.py"]
