from flask import Flask,request,redirect,url_for
from flask import render_template
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import mysql.connector

app = Flask(__name__,static_url_path='/static')




@app.route("/")
def dashboard():
    
    return render_template("index.html",waste = get_hourly_waste(),hours =get_hourly(),maintenance=get_maintenance_vehicle(), shift=get_Shifts(),data=v_status())



# Display infomation about saved/stored vehicles
@app.route("/vehicle")
def vehicle():
    print(get_vehicle_registered())
    return render_template("vehicle.html",data=v_status(),vih=get_vehicle_registered())

# Maintenance Tracker
@app.route("/maintenance")
def maintenance():
    return render_template("maintenanceTracker.html",data=v_status(),vih=get_vehicle_registered(),maintenance=get_maintenance_vehicle())



# Post Route, sending data to the database
@app.route("/vehicle",methods=['POST','GET'])
def add_vehicle():
    try:
        equip = request.form["equip"]
        model = request.form["model"]
        spc = request.form["spc"]
        quty = request.form["quty"]
        vr = (equip,model,spc,quty)
        return insert_vehicle(vr)
    except Exception as e:
        return f"Error Processing this form: {e}"
    
    
# Shifts
@app.route("/shift")
def shift():
    return render_template("Shifts.html", shift=get_Shifts())


@app.route("/shift",methods=["GET","POST"])
def add_shift():
    try:
        morning = request.form["Morning"]
        afternoon = request.form["Afternoon"]
        target = request.form["target"]
        insql = (morning,afternoon,target)
        return insert_shift(insql)
    except Exception as e:
        return redirect(url_for("shift", error=f"Error Processing this form: {e}"))
        

@app.route("/hourly")
def hourly_tonnages():
    total = sum( int(data[3]) for data in get_hourly())
    total_waste =sum( int(data[3]) for data in get_hourly_waste()) 
    return render_template("Actual_Hourly.html",total=total,total_waste=total_waste,waste = get_hourly_waste(),hours =get_hourly(), shift=get_Shifts())

@app.route("/hourly",methods=["POST","GET"])
def add_hourly():
        try:
            actualHourfrom = request.form["actualHourfrom"]
            actualHourto = request.form["actualHourto"]
            actual_volume = request.form["actual_volume"]
            shift = request.form["shift"]
            shiftID = shift.split(",")[0]
            shiftName = shift.split(",")[1]
            
            hourly = (actualHourfrom,actualHourto,actual_volume,shiftName,shiftID)
            return insert_hourly(hourly)
        except Exception as e:
            return render_template("Actual_Hourly.html", error=f"Error Processing this formX: {e}")
            # return redirect(url_for("hourly", error=f"Error Processing this form: {e}"))



@app.route("/waste",methods=["POST","GET"])
def add_hourly_waste():
        try:
            actualHourfrom = request.form["actualHourfrom"]
            actualHourto = request.form["actualHourto"]
            actual_volume = request.form["actual_volume"]
            shift = request.form["shift"]
            shiftID = shift.split(",")[0]
            shiftName = shift.split(",")[1]
            
            hourly = (actualHourfrom,actualHourto,actual_volume,shiftName,shiftID)
            return insert_hourly_waste(hourly)
        except Exception as e:
            return render_template("Actual_Hourly.html", error=f"Error Processing this formX: {e}")
            # return redirect(url_for("hourly", error=f"Error Processing this form: {e}"))
@app.route("/drillblast",methods=["POST","GET"])
def drill_blast():
        if request.method == 'POST':
            try:
                blastedVolume = request.form["blastedVolume"]
                numberOfDaysRequired = request.form["numberOfDaysRequired"]
                actual_volumeMovedPayDay = request.form["actual_volumeMovedPayDay"]
                # numberOfDaysRequireds = 0
                
                # if get_vehicle_registered()[1] == "Tiper":
                #     numberOfDaysRequireds =  blastedVolume / get_vehicle_registered()[4]
                
                kpi = (blastedVolume,numberOfDaysRequired,actual_volumeMovedPayDay)
                return insert_blasted_kpi(kpi)
            except Exception as e:
                return render_template("drillblast.html", error=f"Error Processing this formX: {e}")
        else:
           return render_template("drIllblast.html", drill=get_drillblast())
    


# Post maintenance, sending data to the database
@app.route("/maintenance",methods=['POST','GET'])
def save_maintenance_vehicle():
    try:
        equip = request.form["equip"]
        lastDayServiced = request.form["lastDayServiced"]
        lastServiced = request.form["lastServiced"]
        nextDue = request.form["nextDue"]
        status = request.form["status"]
        equipID = request.form["equipID"]
        services = (equip,lastDayServiced,lastServiced,nextDue,equipID,status)
        return insert_maintenance_vehicle(services)
    except Exception as e:
        return redirect(url_for("maintenance", error=f"Error Processing this form: {e}"))



# mine Planing
@app.route("/vehicle/data")
def planed_inputs():
   return render_template("inputData.html")


@app.route("/login")
def login():
    return render_template("login.html")


def connect_db():
    """ Connect to the MySQL database """
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return connection

@app.route("/json")
def get_vehicle_to_json():
    return get_vehicle_registered()




def get_vehicle_registered():
    """Fetch vehicle data from the database."""
    data = []
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mobile_epq order by id desc")
        data = cursor.fetchall()  # Fetch all rows from the query result
    except Exception as e:
        print(f"Error fetching vehicle data: {e}")
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
    return data



def get_Shifts():
    """Fetch Shift from the database."""
    data = []
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM shifts order by id desc")
        data = cursor.fetchall()  # Fetch all rows from the query result
    except Exception as e:
        print(f"Error fetching shift data: {e}")
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
    return data



def get_hourly():
    """Fetch Hourly from the database."""
    data = []
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hourly_Ore WHERE DATE(created_at) = CURDATE()  order by id desc")
        data = cursor.fetchall()  # Fetch all rows from the query result
    except Exception as e:
        print(f"Error fetching hourly_Ore data: {e}")
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
    return data


def get_hourly_waste():
    """Fetch Hourly WASTE from the database."""
    data = []
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hourly_waste WHERE DATE(created_at) = CURDATE()  order by id desc")
        data = cursor.fetchall()  # Fetch all rows from the query result
    except Exception as e:
        print(f"Error fetching hourly_Ore data: {e}")
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
    return data


def get_drillblast():
    """Fetch drillblast  from the database."""
    data = []
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM drill_blast   order by id desc")
        data = cursor.fetchall()  # Fetch all rows from the query result
    except Exception as e:
        print(f"Error fetching Drill and blast KPI data: {e}")
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
            

def insert_shift(shift_data):
    """
    Insert a shift_data into the database.
    
    """
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        sql = "INSERT INTO shifts (Morning, Afternoon, Target,Total,created_at,modified_at) VALUES (%s, %s, %s,Target,NOW(),NOW())"
        cursor.execute(sql, shift_data)  # Execute the SQL with the provided data
        conn.commit()  # Commit the transaction
        return redirect(url_for("shift", msg=f"Shift {shift_data} Created successfully."))
    except Exception as e:
        return redirect(url_for("shift",error=f"Error inserting Shift {shift_data}: {e}"))
    finally:
        if cursor:
            cursor.close()  # Close the cursor
        if conn:
            conn.close()   # Close the connection
            
         
def insert_hourly(hourly_data):
    """
    Insert a hourly into the database.
    
    """
    conn = None
    try:
        conn = connect_db()  # Assuming `connect_db` is defined elsewhere
        cursor = conn.cursor()
        sql = "INSERT INTO hourly_Ore (actual_hour_from,actual_hour_to, actual_volume, ShiftName,shifID, created_at,modified_at) VALUES (%s, %s, %s,%s,%s,now(),now())"
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
            

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8089,debug=True)