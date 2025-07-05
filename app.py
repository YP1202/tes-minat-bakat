from flask import Flask, render_template, request, redirect, url_for
import json
from urllib.parse import quote, unquote
from data_bank import data, rekomendasi_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        scores = {}
        for question in data:
            question_id = f"question_{question['id']}"
            response = int(request.form.get(question_id, 0))
            category = question['category']
            scores[category] = scores.get(category, 0) + response

        # Encode skor ke dalam format JSON dan quote agar aman di URL
        scores_json = quote(json.dumps(scores))
        return redirect(url_for('results', scores=scores_json))

    return render_template('questions.html', data=data)

@app.route('/result')
def results():
    # Decode skor dari URL
    scores_raw = request.args.get('scores', '{}')
    scores = json.loads(unquote(scores_raw))

    max_category = max(scores, key=scores.get)

    result_message = (
        f"Berdasarkan hasil analisis, Anda memiliki kecenderungan dominan "
        f"pada kategori '{max_category}'. Anda memiliki potensi besar untuk mengembangkan kemampuan di bidang ini."
    )

    recommendation = rekomendasi_data.get(max_category, {
        "jurusan": [],
        "bakat": [],
        "saran": "Belum ada saran spesifik untuk kategori ini."
    })

    return render_template(
        'result.html',
        scores=scores,
        result_message=result_message,
        max_category=max_category,
        recommendation=recommendation
    )

if __name__ == '__main__':
    app.run(debug=True)
