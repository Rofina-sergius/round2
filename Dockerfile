# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 5000  # Change to 8000 for Django

# Run the application
CMD ["python", "app.py"]  # Change to "python manage.py runserver" for Django
