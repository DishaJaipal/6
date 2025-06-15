# Use Python image
FROM python:3.10

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Expose the port Railway assigns
EXPOSE $PORT

# Command to run your Flask app
CMD ["python", "main.py"]
