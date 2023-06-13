# Base image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Update and install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    nano \
    unzip

# Clone the hunerDock repository
RUN git clone https://github.com/Crispae/hunderDock.git

# Change to the hunerDock directory
WORKDIR /app/hunderDock

# Install Python dependencies
RUN pip install flask flair==0.11.3

# Expose the port on which the Flask app will run (change if needed)
EXPOSE 4031

# Run the Flask app
CMD ["python3", "huner.py"]
