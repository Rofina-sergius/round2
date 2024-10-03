from flask import Flask, render_template, url_for
from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib.pyplot as plt
import os

# Initialize the Flask app
app = Flask(__name__)

# Create a directory for saving visualizations if not exists
if not os.path.exists('static/images'):
    os.makedirs('static/images')

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Define the index name
index_name = "employee_data"

# Helper function to query data from Elasticsearch and return a DataFrame
def fetch_data():
    res = es.search(index=index_name, body={"query": {"match_all": {}}}, size=1000)
    employee_data = [hit['_source'] for hit in res['hits']['hits']]
    df = pd.DataFrame(employee_data)
    
    # Clean up 'Annual Salary' column (remove $ and commas, convert to float)
    df['Annual Salary'] = df['Annual Salary'].replace('[\$,]', '', regex=True).astype(float)
    
    return df

# Route to the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to display the age distribution
@app.route('/age-distribution')
def age_distribution():
    df = fetch_data()
    
    # Plot age distribution
    plt.figure(figsize=(8, 6))
    plt.hist(df['Age'], bins=10, alpha=0.7, color='blue')
    plt.title('Age Distribution of Employees')
    plt.xlabel('Age')
    plt.ylabel('Frequency')

    # Save the plot
    plt.savefig('static/images/age_distribution.png')
    plt.close()
    
    return render_template('age_distribution.html', image_file=url_for('static', filename='images/age_distribution.png'))

# Route to display the salary distribution
@app.route('/salary-distribution')
def salary_distribution():
    df = fetch_data()

    # Plot salary distribution
    plt.figure(figsize=(8, 6))
    plt.hist(df['Annual Salary'], bins=10, alpha=0.7, color='green')
    plt.title('Annual Salary Distribution of Employees')
    plt.xlabel('Annual Salary ($)')
    plt.ylabel('Frequency')

    # Save the plot
    plt.savefig('static/images/salary_distribution.png')
    plt.close()

    return render_template('salary_distribution.html', image_file=url_for('static', filename='images/salary_distribution.png'))

# Route to display gender distribution
@app.route('/gender-distribution')
def gender_distribution():
    df = fetch_data()

    # Plot gender distribution
    plt.figure(figsize=(8, 6))
    gender_counts = df['Gender'].value_counts()
    plt.bar(gender_counts.index, gender_counts.values, color=['blue', 'pink'])
    plt.title('Gender Distribution of Employees')
    plt.xlabel('Gender')
    plt.ylabel('Number of Employees')

    # Save the plot
    plt.savefig('static/images/gender_distribution.png')
    plt.close()

    return render_template('gender_distribution.html', image_file=url_for('static', filename='images/gender_distribution.png'))

if __name__ == '__main__':
    app.run(debug=True)
