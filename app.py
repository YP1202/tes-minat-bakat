from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Data pertanyaan
data = [
    {"id": 1, "statement": "Saya senang memperbaiki atau membongkar benda elektronik.", "category": "Realistic"},
    {"id": 2, "statement": "Saya tertarik melakukan eksperimen ilmiah.", "category": "Investigative"},
    {"id": 3, "statement": "Saya menikmati menggambar, melukis, atau mendesain.", "category": "Artistic"},
    {"id": 4, "statement": "Saya suka membantu teman menyelesaikan masalah.", "category": "Social"},
    {"id": 5, "statement": "Saya percaya diri memimpin kelompok dalam diskusi.", "category": "Enterprising"},
    {"id": 6, "statement": "Saya senang mengatur dokumen atau data dengan rapi.", "category": "Conventional"},
    {"id": 7, "statement": "Saya menikmati menulis cerita atau puisi.", "category": "Linguistic"},
    {"id": 8, "statement": "Saya menyukai teka-teki logika dan soal matematika.", "category": "Logical-Mathematical"},
    {"id": 9, "statement": "Saya pandai memahami arah dan peta.", "category": "Spatial"},
    {"id": 10, "statement": "Saya suka bergerak, menari, atau berolahraga.", "category": "Bodily-Kinesthetic"},
]

@app.route('/')
def home():
    """Halaman utama."""
    return render_template('index.html')

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    """Halaman pertanyaan."""
    if request.method == 'POST':
        scores = {}
        for question in data:
            question_id = f"question_{question['id']}"
            response = int(request.form.get(question_id, 0))
            category = question['category']
            scores[category] = scores.get(category, 0) + response

        # Redirect ke halaman hasil dengan skor sebagai parameter
        return redirect(url_for('result', scores=scores))
    return render_template('questions.html', data=data)

@app.route('/result')
def results():
    """Halaman hasil."""
    scores = request.args.get('scores', {})
    if isinstance(scores, str):
        # Ubah dari string JSON-like ke dict
        import ast
        scores = ast.literal_eval(scores)

    # Temukan kategori dengan skor tertinggi
    max_category = max(scores, key=scores.get)
    result_message = (
        f"Berdasarkan hasil analisis, Anda memiliki kecenderungan dominan "
        f"pada kategori '{max_category}'. Anda memiliki potensi besar untuk mengembangkan kemampuan di bidang ini."
    )
    return render_template('result.html', scores=scores, result_message=result_message)

if __name__ == '__main__':
    app.run(debug=True)
