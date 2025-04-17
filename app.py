from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    cur = db.execute('SELECT * FROM appointments ORDER BY date, time')
    appointments = cur.fetchall()
    return render_template('admin.html', appointments=appointments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'gifted123':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_appointment():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    date = request.form['date']
    time = request.form['time']
    client = request.form['client']
    db = get_db()
    db.execute('INSERT INTO appointments (date, time, client) VALUES (?, ?, ?)', (date, time, client))
    db.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_appointment(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    db = get_db()
    db.execute('DELETE FROM appointments WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit_appointment(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    date = request.form['date']
    time = request.form['time']
    client = request.form['client']

    db = get_db()
    db.execute('UPDATE appointments SET date = ?, time = ?, client = ? WHERE id = ?', (date, time, client, id))
    db.commit()
    return redirect(url_for('home'))

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        if new_password != confirm_password:
            return render_template('reset_password.html', error="Passwords do not match")
        session['admin_password'] = new_password  # Demo purpose only
        return render_template('reset_password.html', message="Password has been reset.")
    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)
