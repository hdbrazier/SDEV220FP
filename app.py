from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Database connection setup
conn = psycopg2.connect(
    host="localhost",
    database="giftedgown",
    user="postgres",
    password="hello123"
)
cur = conn.cursor()

@app.route('/')
def index():
    return render_template('user.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Collect form data
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    date = request.form['date']
    time = request.form['time']
    event_type = request.form['type']
    notes = request.form['notes']

    # Insert into the database
    cur.execute("""
        INSERT INTO appointments (first_name, last_name, email, phone, date, time, event_type, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (first_name, last_name, email, phone, date, time, event_type, notes))

    conn.commit()

    # Redirect to a dedicated thank-you page
    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
