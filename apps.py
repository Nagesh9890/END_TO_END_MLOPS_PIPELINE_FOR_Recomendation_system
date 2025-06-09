import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the data from Excel into a DataFrame
df = pd.read_excel('product_database.xlsx')

# Preprocess the text data
df['Text'] = df['Product_Name'] + ' ' + df['Brand'] + ' ' + df['Category'] + ' ' + df['Color'] + ' ' + df['Size']

# Initialize the TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Create the TF-IDF matrix
tfidf_matrix = vectorizer.fit_transform(df['Text'])

# Compute the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get top n similar products
def get_similar_products(product_name, n=5):
    # Get the index of the product
    index = df[df['Product_Name'] == product_name].index[0]
    
    # Get the similarity scores of the product with all other products
    similarity_scores = list(enumerate(cosine_sim[index]))
    
    # Sort the products based on similarity scores
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # Get the indices of the top n similar products
    top_indices = [i[0] for i in similarity_scores[1:n+1]]
    
    # Return the top n similar products
    return df.iloc[top_indices]['Product_Name']

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the input data from the request
    data = request.get_json()
    
    # Extract the product name and n value from the input
    product_name = data['product_name']
    n = data.get('n', 5)
    
    # Get the similar products
    similar_products = get_similar_products(product_name, n)
    
    # Return the recommended similar products as a JSON response
    return jsonify(similar_products.tolist())

if __name__ == '__main__':
    app.run(debug=True)
