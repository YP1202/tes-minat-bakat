from flask import Flask, render_template, request, redirect, url_for
import json
from urllib.parse import quote, unquote

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

    # Rekomendasi berdasarkan kategori minat
    rekomendasi_data = {
        "Realistic": {
            "jurusan": ["Teknik Mesin", "Teknik Elektro", "Teknik Sipil"],
            "bakat": ["Mekanik", "Instalasi Listrik", "Pertukangan"],
            "saran": "Ikuti pelatihan teknis atau praktek kerja lapangan untuk mengasah keterampilanmu."
        },
        "Investigative": {
            "jurusan": ["Fisika", "Biologi", "Teknik Kimia"],
            "bakat": ["Penelitian", "Eksperimen", "Logika"],
            "saran": "Mulailah dengan eksperimen kecil di rumah atau klub sains sekolah/kampus."
        },
        "Artistic": {
            "jurusan": ["DKV", "Seni Musik", "Seni Tari"],
            "bakat": ["Kreativitas", "Ekspresi Diri", "Seni Visual"],
            "saran": "Tunjukkan karyamu di media sosial dan ikut komunitas kreatif."
        },
        "Social": {
            "jurusan": ["Psikologi", "Pendidikan", "Bimbingan Konseling"],
            "bakat": ["Empati", "Komunikasi", "Kerja Sosial"],
            "saran": "Coba ikut kegiatan sosial atau komunitas relawan."
        },
        "Enterprising": {
            "jurusan": ["Manajemen", "Bisnis", "Marketing"],
            "bakat": ["Kepemimpinan", "Negosiasi", "Public Speaking"],
            "saran": "Mulailah bisnis kecil-kecilan atau ikut organisasi."
        },
        "Conventional": {
            "jurusan": ["Administrasi", "Akuntansi", "Perpajakan"],
            "bakat": ["Ketelitian", "Rapi", "Terstruktur"],
            "saran": "Latih kemampuan pengelolaan dokumen dan data di Excel atau software keuangan."
        },
        "Linguistic": {
            "jurusan": ["Sastra", "Jurnalistik", "Pendidikan Bahasa"],
            "bakat": ["Menulis", "Berbicara", "Bahasa Asing"],
            "saran": "Tulis blog, puisi, atau cerpen dan ikut lomba literasi."
        },
        "Logical-Mathematical": {
            "jurusan": ["Matematika", "Statistik", "Ilmu Komputer"],
            "bakat": ["Analisis", "Pemecahan Masalah", "Berpikir Kritis"],
            "saran": "Belajar coding atau ikut olimpiade matematika."
        },
        "Spatial": {
            "jurusan": ["Arsitektur", "Desain Interior", "Geografi"],
            "bakat": ["Membaca Peta", "Visualisasi", "Orientasi Ruang"],
            "saran": "Coba aplikasi desain rumah atau ikuti kelas arsitektur."
        },
        "Bodily-Kinesthetic": {
            "jurusan": ["Pendidikan Jasmani", "Tari", "Kinesiologi"],
            "bakat": ["Koordinasi Tubuh", "Kekuatan Fisik", "Gerak"],
            "saran": "Gabung tim olahraga atau ikut kelas tari."
        }
    }

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
