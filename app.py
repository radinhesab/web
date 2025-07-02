from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'radin-secret-key'

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

DB_FILE = 'db/group_tax.db'

@app.route('/')
def index():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        name = request.form['name']
        company_type = request.form['company_type']
        national_id = request.form['national_id']
        phone = request.form['phone']
        logo = request.files['logo']
        
        if logo:
            logo_path = os.path.join(UPLOAD_FOLDER, logo.filename)
            logo.save(logo_path)
        else:
            logo_path = ''

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO companies (name, company_type, national_id, phone, logo_path) VALUES (?, ?, ?, ?, ?)",
                       (name, company_type, national_id, phone, logo_path))
        conn.commit()
        conn.close()

        flash('شرکت با موفقیت ثبت شد ✅')
        return redirect('/register')
    
    return render_template('register_company.html')
    
if __name__ == '__main__':
    app.run(debug=True)
