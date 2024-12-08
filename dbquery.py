from flask import render_template,request,redirect,url_for
from app import app,connect_db

def get_vehicle_registered(id=None):
    """Fetch vehicle data from the database."""
    data = []
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        if id is None:
            cursor.execute("SELECT * FROM mobile_epq order by id desc")
            data = cursor.fetchall()  # Fetch all rows from the query result
        else:
            cursor.execute(f"SELECT * FROM mobile_epq WHERE id='{id}'")
            data = cursor.fetchall()
          
    except Exception as e:
        print(f"Error fetching vehicle data: {e}")
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
    return data



def get_Shifts(id=None):
    """Fetch Shift from the database."""
    data = []
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        if id is None:
            cursor.execute("SELECT * FROM shifts order by id desc")
            data = cursor.fetchall()  # Fetch all rows from the query result
            print("ID: ",id,data)
        else:
            cursor.execute(f"SELECT * FROM shifts WHERE id='{id}'")
            data = cursor.fetchall()
            print("single ",data)
            
    except Exception as e:
        print(f"Error fetching shift data: {e}")
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
    return data



def get_hourly(id=None):
    """Fetch Hourly from the database."""
    data = []
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        if id is None:
            cursor.execute("SELECT * FROM hourly_Ore WHERE DATE(created_at) = CURDATE()  order by id desc")
            data = cursor.fetchall()  # Fetch all rows from the query result
        else:
            cursor.execute(f"SELECT * FROM hourly_Ore WHERE id='{id}'")
            data = cursor.fetchall()
            # print(f"data: {data}")
           
    except Exception as e:
        return (f"Error fetching hourly_Ore data: {e}")
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
    return data


def get_hourly_waste(id=None):
    """Fetch Hourly WASTE from the database."""
    data = []
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        if id is None:
            cursor.execute("SELECT * FROM hourly_waste WHERE DATE(created_at) = CURDATE()  order by id desc")
            data = cursor.fetchall()  # Fetch all rows from the query result
        else:
            cursor.execute(f"SELECT * FROM hourly_waste WHERE id='{id}'")
            data = cursor.fetchall()
    except Exception as e:
        return (f"Error fetching hourly_waste data: {e}")
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
    return data


def get_drillblast(id=None):
    """Fetch drillblast  from the database."""
    data = []
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        if id is None:
            cursor.execute("SELECT * FROM drill_blast   order by id desc")
            data = cursor.fetchall()  # Fetch all rows from the query result
        else:
            cursor.execute(f"SELECT * FROM drill_blast WHERE id='{id}' ")
            data = cursor.fetchall()  # Fetch all rows from the query result
    
    except Exception as e:
        return (f"Error fetching Drill and blast KPI data: {e}")
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
    return data

# Count Ready Vehicles
def get_maintenance_count_vehicle(status):
      """Fetch vehicle data from the database."""
      data = []
      conn = None
      try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        # cursor.execute(f"SELECT count(*) AS Ready FROM equipment  WHERE status ='{status}' ")
        cursor.execute(f"SELECT count(*) FROM mobile_epq INNER JOIN equipment as e ON e.equipment = mobile_epq.equipment WHERE e.equipment='Tiper' AND e.status='{status}'")
        data = cursor.fetchall()  # Fetch all rows from the query result
        
      except Exception as e:
        print(f"Error fetching vehicle data: {e}")
      finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
      return data

def v_status():
    ready  = get_maintenance_count_vehicle("Ready")
    down  = get_maintenance_count_vehicle("Down")
    sg  = get_maintenance_count_vehicle("Shift Change")
    status = (ready,down,sg)
    return status
    
    
def get_maintenance_vehicle():
      """Fetch vehicle Maintenance data from the database."""
      data = []
      conn = None
      try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mobile_epq INNER JOIN equipment as e ON e.equipment = mobile_epq.equipment WHERE e.equipment !='Tiper' order by mobile_epq.id desc")
        data = cursor.fetchall()  # Fetch all rows from the query result
      except Exception as e:
        print(f"Error fetching vehicle data: {e}")
      finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
      return data

    
def insert_vehicle(vehicle_data):
    """
    Insert a new vehicle into the database.
       Args:
        vehicle_data (tuple): A tuple containing (id, make, model, year) for the vehicle.
    id            | int(10)      | NO   | PRI | NULL    | auto_increment |
| equipment     | varchar(250) | NO   |     | NULL    |                |
| model         | varchar(250) | NO   |     | NULL    |                |
| specification | varchar(250) | NO   |     | NULL    |                |
| quantity 
    
    """
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        sql = "INSERT INTO mobile_epq (equipment, model, specification,quantity) VALUES (%s, %s, %s,%s)"
        cursor.execute(sql, vehicle_data)  # Execute the SQL with the provided data
        conn.commit()  # Commit the transaction
        return f"Vehicle {vehicle_data} inserted successfully."
    except Exception as e:
        return f"Error inserting vehicle {vehicle_data}: {e}"
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
            

def insert_maintenance_vehicle(maintenance_vehicle_data):
    """
    Insert a maintenance_vehicle into the database.
    
    """
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        sql = "INSERT INTO equipment (equipment, lastDayOfService, lastOfService,NextDue,meID,Status) VALUES (%s, %s, %s,%s,%s, %s)"
        cursor.execute(sql, maintenance_vehicle_data)  # Execute the SQL with the provided data
        conn.commit()  # Commit the transaction
        # return f"Vehicle {maintenance_vehicle_data} inserted successfully."
        return redirect(url_for("maintenance", msg=f"Vehicle {maintenance_vehicle_data} inserted successfully."))
    except Exception as e:
        return redirect(url_for("maintenance",error=f"Error inserting maintenance_vehicle {maintenance_vehicle_data}: {e}"))
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
            

# Insert Shift With Value : 0->Insert,1->update
def insert_shift(shift_data,value=0,id=None):
    """
    Insert a shift_data into the database.
    
    """
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        if value ==0:
            sql = "INSERT INTO shifts (Morning, Afternoon, Target,Total,created_at,modified_at) VALUES (%s, %s, %s,Target,NOW(),NOW())"
            cursor.execute(sql, shift_data)  # Execute the SQL with the provided data
            conn.commit()  # Commit the transaction
            return redirect(url_for("shift", msg=f"Shift {shift_data} Created successfully."))
        elif value==1:
            sql = f"UPDATE  shifts SET Morning = %s, Afternoon = %s, Target = %s ,Total = Target ,modified_at= now() WHERE id='{id}'"
            cursor.execute(sql, shift_data)  # Execute the SQL with the provided data
            conn.commit()  # Commit the transaction
            return redirect(url_for("shift", msg=f"Shift {shift_data} Updated successfully."))
    except Exception as e:
        return redirect(url_for("shift",error=f"Error on action Shift {shift_data}: {e}"))
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
            
         
# Insert Shift With Value : 0->Insert,1->update
def insert_hourly(hourly_data,value=0,id=None):
    """Insert a hourly into the database."""
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        if value ==0:
            sql = "INSERT INTO hourly_Ore (actual_hour_from,actual_hour_to, actual_volume, ShiftName,shifID, created_at,modified_at) VALUES (%s, %s, %s,%s,%s,now(),now())"
            cursor.execute(sql, hourly_data)  # Execute the SQL with the provided data
        elif value==1:
            sql = f"UPDATE hourly_Ore SET actual_hour_from=%s,actual_hour_to=%s, actual_volume=%s, ShiftName=%s,shifID=%s,modified_at=now() WHERE id='{id}'"
            cursor.execute(sql, hourly_data)  
            
        conn.commit()  # Commit the transaction
        return render_template("Actual_Hourly.html",hours=get_hourly(), msg=f"Hourly {hourly_data} Created successfully.")
    except Exception as e:
        return render_template("Actual_Hourly.html",error=f"Error inserting Hourly {hourly_data}: {e}")
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection   
            
def insert_hourly_waste(hourly_data):
    """
    Insert a hourly waste into the database.
    
    """
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        sql = "INSERT INTO hourly_waste (actual_hour_from,actual_hour_to, actual_volume, ShiftName,shifID, created_at,modified_at) VALUES (%s, %s, %s,%s,%s,now(),now())"
        cursor.execute(sql, hourly_data)  # Execute the SQL with the provided data
        conn.commit()  # Commit the transaction
        return render_template("Actual_Hourly.html",hours=get_hourly(), msg=f"Hourly {hourly_data} Created successfully.")
    except Exception as e:
        return render_template("Actual_Hourly.html",error=f"Error inserting Hourly {hourly_data}: {e}")
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection 
            

def insert_blasted_kpi(blastKPI):
    """
    Insert a insert_blasted_kpi  into the database.
    
    """
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        sql = "INSERT INTO drill_blast (blastedVolume,numberOfDaysRequired, actual_volumeMovedPayDay,created_at,modified_at) VALUES (%s, %s,%s,now(),now())"
        cursor.execute(sql, blastKPI)  # Execute the SQL with the provided data
        conn.commit()  # Commit the transaction
        return render_template("drillblast.html",hours=get_drillblast(), msg=f" drillblast Created successfully.")
    except Exception as e:
        return render_template("drillblast.html",error=f"Error inserting drillblast: {e}")
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection 
