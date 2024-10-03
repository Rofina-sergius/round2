from elasticsearch import Elasticsearch
import pandas as pd
import json

# Connect to Elasticsearch with increased request timeout
es = Elasticsearch("http://localhost:9200",http_auth=('elastic', 'elastic'), request_timeout=120)

# Check connection to Elasticsearch
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Could not connect to Elasticsearch")
    exit()  # Stop execution if unable to connect

# Define the index name
index_name = "employee_data"

# Create an index (with ignore=400 moved to the .options() method)
es.options(ignore_status=[400]).indices.create(index=index_name)
print(f"Index {index_name} created!")

# Test Elasticsearch with a simple query
try:
    res = es.search(index=index_name, body={"query": {"match_all": {}}})
    print("Sample query response:", res)
except Exception as e:
    print(f"Error in querying Elasticsearch: {e}")

# Load employee data
data = pd.read_csv('Employee Sample Data 1.csv', encoding='ISO-8859-1')

# Convert DataFrame to JSON format for indexing and index each row
for i, row in data.iterrows():
    doc = row.to_dict()
    try:
        # Index each row into Elasticsearch
        es.index(index=index_name, body=doc)
    except Exception as e:
        print(f"Error indexing row {i}: {e}")

print("Employee data indexed successfully!")
