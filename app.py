from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load your dataset
df = pd.read_excel("Nlp with images.xlsx")

# Clean the 'Name' column (remove leading/trailing spaces)
df['Movie Title'] = df['Movie Title'].astype(str).str.strip()

# Recommendation function based on name match
def movie_rec(movie_name):
    movie_name = movie_name.strip()
    if movie_name not in df['Movie Title'].values:
        return []

    index = df[df['Movie Title'] == movie_name].index[0]
    
    movie_indices = list(range(index, min(index + 10, len(df))))
    result = df.iloc[movie_indices][['Movie Title', 'Ratinng', 'genre', 'act', 'img']]
    return result.to_dict(orient='records')

# Flask route
@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []

    if request.method == 'POST':
        name = request.form['movie_name'].strip()
        if name:  # ✅ Only run if name is not empty
            recommendations = movie_rec(name)

    return render_template("index.html", recommendations=recommendations)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)