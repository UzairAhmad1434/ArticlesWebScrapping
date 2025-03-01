from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load the CSV file into a Pandas DataFrame
csv_file_path = 'articles_data.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file_path)

# Route to serve the frontend
@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML frontend

# Route to handle search requests
@app.route('/search', methods=['GET'])
def search():
    # Get the keyword from the query parameters
    keyword = request.args.get('keyword', '').lower()

    if not keyword:
        return jsonify({"error": "Please provide a keyword to search."}), 400

    # Filter the DataFrame to find rows where the title contains the keyword
    matching_rows = df[df['title'].str.lower().str.contains(keyword)]

    if matching_rows.empty:
        return jsonify({"message": "No articles found with the given keyword."}), 404

    # Convert the matching rows to a list of dictionaries
    results = matching_rows.to_dict(orient='records')

    # Return the results as JSON
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)