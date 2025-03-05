from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

csv_file_path = 'articles_data.csv' 
df = pd.read_csv(csv_file_path)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/search', methods=['GET'])
def search():
 
    keyword = request.args.get('keyword', '').lower()

    if not keyword:
        return jsonify({"error": "Please provide a keyword to search."}), 400

    matching_rows = df[df['title'].str.lower().str.contains(keyword)]

    if matching_rows.empty:
        return jsonify({"message": "No articles found with the given keyword."}), 404

    results = matching_rows.to_dict(orient='records')

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)