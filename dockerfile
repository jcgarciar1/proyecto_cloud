# Use an official Python runtime as the base image
FROM ubuntu

# Set the working directory in the container to /app
RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN pip install gunicorn

# Copy the rest of the application code to the container
COPY . .

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8000 for the Flask development server to listen on
EXPOSE 8000

# Define the command to run the Flask development server
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--workers=5"]