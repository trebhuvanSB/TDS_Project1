# Use the combined Python 3.13 and Node.js 20 image as base
FROM nikolaik/python-nodejs:python3.13-nodejs20-bullseye

# Set the working directory
WORKDIR /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Copy the Python requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY src/ ./src/

# Expose the port the app runs on
EXPOSE 8000

# Set environment variable to disable Python output buffering
ENV PYTHONUNBUFFERED=1

RUN npm install -g prettier@3.4.2

RUN npx -v && prettier -v

# Command to run the application
CMD ["python", "src/main.py"]
