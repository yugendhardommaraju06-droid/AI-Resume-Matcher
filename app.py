from flask import Flask, render_template, request
import os
from resume_parser import extract_text_from_pdf
from preprocess import preprocess_text
from matcher import match_resume_to_job

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match():
    resume = request.files['resume']
    job_desc = request.form['job_description']

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
    resume.save(file_path)

    resume_text = extract_text_from_pdf(file_path)

    if resume_text is None:
        return "Invalid or corrupted PDF file. Please upload a valid resume PDF."

    resume_clean = preprocess_text(resume_text)
    job_clean = preprocess_text(job_desc)

    score = match_resume_to_job(resume_clean, job_clean)

    return render_template('result.html', score=score)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)