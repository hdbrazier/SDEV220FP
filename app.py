from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
from database.pipeline import get_all_appointments
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

# Database connection setup
conn = psycopg2.connect(
    host="localhost",
    database="giftedgown",
    user="postgres",
    password=os.getenv("DB_PASSWORD")
)
cur = conn.cursor()

@app.route('/')
def index():
    return render_template('user.html')

@app.route('/admin')
def admin():
    # Use the get_all_appointments function from pipeline.py
    appointments = get_all_appointments()
    return render_template('admin.html', appointments=appointments)

@app.route('/submit', methods=['POST'])
def submit():
    # Collect form data
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    full_name = f"{first_name} {last_name}"
    email = request.form['email']
    phone = request.form['phone']
    date = request.form['date']
    time = request.form['time']
    # Combine date and time into appointment_time
    appointment_time = f"{date} {time}"
    event_type = request.form['type']
    gender_identity = request.form.get('gender_identity', '')  # Optional field
    notes = request.form['notes']

    # Insert into the database
    cur.execute("""
        INSERT INTO appointments (full_name, email, phone, appointment_time, event_type, gender_identity, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (full_name, email, phone, appointment_time, event_type, gender_identity, notes))

    conn.commit()

    # Redirect to a dedicated thank-you page
    return redirect(url_for('thank_you'))

@app.route('/api/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Build dynamic update query based on provided fields
        update_fields = []
        update_values = []
        
        # Check which fields were provided and add them to update query
        field_mapping = {
            'first_name': None,  
            'last_name': None,   
            'full_name': 'full_name',
            'email': 'email',
            'phone': 'phone',
            'date': None,      
            'time': None,        
            'appointment_time': 'appointment_time',
            'event_type': 'event_type',
            'gender_identity': 'gender_identity',
            'notes': 'notes'
        }
        
        if 'first_name' in data or 'last_name' in data:
            # Get current full_name to modify just the part that changed
            cur.execute("SELECT full_name FROM appointments WHERE id = %s", (appointment_id,))
            current_name = cur.fetchone()
            
            if current_name:
                name_parts = current_name[0].split(' ', 1)
                current_first = name_parts[0] if len(name_parts) > 0 else ''
                current_last = name_parts[1] if len(name_parts) > 1 else ''
                
                new_first = data.get('first_name', current_first)
                new_last = data.get('last_name', current_last)
                
                data['full_name'] = f"{new_first} {new_last}"
        
        # Handle date + time => appointment_time
        if 'date' in data or 'time' in data:
            # Get current appointment_time to modify just the part that changed
            cur.execute("SELECT appointment_time FROM appointments WHERE id = %s", (appointment_id,))
            current_time = cur.fetchone()
            
            if current_time and current_time[0]:
                current_datetime = current_time[0]
                current_date = current_datetime.strftime('%Y-%m-%d')
                current_time_str = current_datetime.strftime('%H:%M:%S')
                
                new_date = data.get('date', current_date)
                new_time = data.get('time', current_time_str)
                
                data['appointment_time'] = f"{new_date} {new_time}"
        
        # Updated query
        for client_field, db_field in field_mapping.items():
            if client_field in data and db_field: 
                update_fields.append(f"{db_field} = %s")
                update_values.append(data[client_field])
        
        if update_fields:
            # Add appointment_id to values list
            update_values.append(appointment_id)
            
            # Update fields that have been provided
            update_query = f"""
                UPDATE appointments 
                SET {', '.join(update_fields)}
                WHERE id = %s
                RETURNING id
            """
            
            cur.execute(update_query, update_values)
            updated_row = cur.fetchone()
            conn.commit()
            
            if updated_row:
                return jsonify({'success': True, 'message': f'Appointment {appointment_id} updated successfully'})
            else:
                return jsonify({'success': False, 'message': f'Appointment {appointment_id} not found'}), 404
        else:
            return jsonify({'success': False, 'message': 'No fields to update provided'}), 400
            
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
