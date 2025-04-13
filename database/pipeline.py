def get_all_appointments(): 
  query = "SELECT * FROM appointments ORDER BY appointment_time DESC"
  cursor.execute(query)
  return cursor.fetchall()

def get_appointments_by_event_type(): 
  query = "SELECT * FROM appointments WHERE event_type = "
  cursor.execute(query, (event_type,))
  return cursor.fetchall()

def search_appointments_by_name(full_name):
  query = "SELECT * FROM appointments WHERE full_name = "
  cursor.execute(query, ())
  return cursor.fetchall()
