from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
    {"id": 11, "statement": "Saya bisa mengenali nada dan irama dalam musik.", "category": "Musical"},
    {"id": 12, "statement": "Saya bisa memahami dan bekerja sama dengan orang lain.", "category": "Interpersonal"},
    {"id": 13, "statement": "Saya sering merenung dan memahami diri sendiri dengan baik.", "category": "Intrapersonal"},
    {"id": 14, "statement": "Saya tertarik dengan tanaman, hewan, atau lingkungan alam.", "category": "Naturalistic"},
    {"id": 15, "statement": "Saya senang menggunakan alat seperti palu, bor, atau obeng.", "category": "Realistic"},
    {"id": 16, "statement": "Saya senang menganalisis data atau pola.", "category": "Investigative"},
    {"id": 17, "statement": "Saya suka menciptakan sesuatu dari bahan bekas.", "category": "Artistic"},
    {"id": 18, "statement": "Saya sering menjadi tempat curhat teman-teman saya.", "category": "Social"},
    {"id": 19, "statement": "Saya suka berbicara di depan umum dan mempengaruhi orang lain.", "category": "Eterprising"},
    {"id": 20, "statement": "Saya senang membuat daftar dan mengatur jadwal.", "category": "Conventional"},
    {"id": 21, "statement": "Saya suka menulis jurnal atau blog pribadi.", "category": "Linguistic"},
    {"id": 22, "statement": "Saya tertarik pada eksperimen ilmiah dan teori matematika.", "category": "Logical-Mathematical"},
    {"id": 23, "statement": "Saya bisa membayangkan bentuk 3D dengan mudah.", "category": "Spatial"},
    {"id": 24, "statement": "Saya bisa meniru gerakan orang lain dengan cepat.", "category": "Bodily-Kinesthetic"},
    {"id": 25, "statement": "Saya mudah mengingat lirik lagu dan nada.", "category": "Musical"},
    {"id": 26, "statement": "Saya senang bekerja dalam kelompok atau tim.", "category": "Interpersonal"},
    {"id": 27, "statement": "Saya memahami emosi dan alasan saya bertindak.", "category": "Intrapersonal"},
    {"id": 28, "statement": "Saya gemar mengamati serangga, burung, atau tumbuhan.", "category": "Naturalistic"},
    {"id": 29, "statement": "Saya suka mengeksplorasi dan mencoba hal-hal baru secara langsung.", "category": "Realistic"},
    {"id": 30, "statement": "Saya penasaran tentang bagaimana sesuatu bekerja di balik layar.", "category": "Investigative"}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        return redirect(url_for('questions', name=name, age=age))
    return render_template('index.html')

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        scores = {}
        for item in data:
            try:
                answer = int(request.form.get(f'question_{item["id"]}', 0))
                scores[item['category']] = scores.get(item['category'], 0) + answer
            except ValueError:
                return "Invalid input received", 400
        return redirect(url_for('result', scores=scores))

    name = request.args.get('name')
    age = request.args.get('age')
    return render_template('questions.html', data=data, name=name, age=age)

@app.route('/result')
def result():
    import ast
    scores = request.args.get('scores', '{}')
    if isinstance(scores, str):
        scores = ast.literal_eval(scores)

    max_category = max(scores, key=scores.get)
    result_message = (
        f"Berdasarkan analisis, Anda memiliki kecenderungan minat/bakat dominan "
        f"pada kategori {max_category}. Ini menunjukkan bahwa Anda memiliki kemampuan atau "
        f"potensi tinggi dalam bidang ini."
    )
    return render_template('result.html', scores=scores, result_message=result_message)

if __name__ == '__main__':
    app.run(debug=True)

