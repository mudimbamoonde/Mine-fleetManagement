from app import app
from flask import render_template,request,redirect,url_for,session
from dbquery import *

import folium

@app.route("/")
def dashboard():
    if session:
        """Embed a map as an iframe on a page."""
        m = folium.Map([-15.583333, 28.283333], zoom_start=12)

        # set the iframe width and height
        m.get_root().width = "1000px"
        m.get_root().height = "450px"
        group_1 = folium.FeatureGroup("first group").add_to(m)
        folium.Marker((-15.583333, 28.2100000), icon=folium.Icon("red")).add_to(group_1)
        folium.Marker((-15.553300, 28.2100000), icon=folium.Icon("red")).add_to(group_1)
        
        # Mine Location
        folium.CircleMarker(
                location=[-15.583333, 28.283333],
                radius=450,
                fill=True,
                popup=folium.Popup("The Pit"),
            ).add_to(m)
        
        iframe = m.get_root()._repr_html_()
        return render_template("index.html",iframe=iframe,waste = get_hourly_waste(),hours =get_hourly(),maintenance=get_maintenance_vehicle(), shift=get_Shifts(),data=v_status())
    else:
        return render_template("login.html",msg="Please Login!!")


# Display infomation about saved/stored vehicles
@app.route("/vehicle")
def vehicle():
     if session:
        print(get_vehicle_registered())
        return render_template("vehicle.html",data=v_status(),vih=get_vehicle_registered())
     else:
        return render_template("login.html",msg="Please Login!!")

# Maintenance Tracker
@app.route("/maintenance")
def maintenance():
    if session:
        return render_template("maintenanceTracker.html",data=v_status(),vih=get_vehicle_registered(),maintenance=get_maintenance_vehicle())
    else:
        return render_template("login.html",msg="Please Login!!")



# Post Route, sending data to the database
@app.route("/vehicle",methods=['POST','GET'])
def add_vehicle():
    if session:
        try:
            equip = request.form["equip"]
            model = request.form["model"]
            spc = request.form["spc"]
            quty = request.form["quty"]
            vr = (equip,model,spc,quty)
            return insert_vehicle(vr)
        except Exception as e:
            return f"Error Processing this form: {e}"
    else:
        return render_template("login.html",msg="Please Login!!")

# /vehicle/edit/{{data[0]}}
@app.route("/vehicle/edit/<int:id>")
def edit_vehicle(id):
       return render_template("edit_vehicle.html",_edit=get_vehicle_registered(id))

    
    
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


#Edit Shift /shift/edit/{{data[0] }}
@app.route("/shift/edit/<int:id>")
def edit_shift(id):
    print("info ",get_Shifts(id))
    return render_template("edit_shifts.html", shift_edit=get_Shifts(id))
            
        
@app.route("/shift/edit/<int:id>",methods=["POST","GET"])
def edit_shiftr_update(id):
        try:
                sid = request.form["sid"]
                morning = request.form["Morning"]
                afternoon = request.form["Afternoon"]
                target = request.form["target"]
                update = (morning,afternoon,target)
                print("Update ",get_Shifts(sid))
                return insert_shift(update,1,sid)
        except Exception as e:
            return (f"Error: {e} ")
    


# Hourly {ore | waste}
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
            
#Edit hourly /hourly/edit/{{data[0] }}
@app.route("/hourly/edit/<int:id>")
def edit_hourly(id):
    print(f"hourly {get_hourly(id)[0][1]}")
    return render_template("edit_hourly.html", _edit=get_hourly(id),shift=get_Shifts())
           
@app.route("/hourly/edit/<int:id>",methods=["POST","GET"])
def edit_hourly_update(id):
        try:
            actualHourfrom = request.form["actualHourfrom"]
            actualHourto = request.form["actualHourto"]
            actual_volume = request.form["actual_volume"]
            shift = request.form["shift"]
            shiftID = shift.split(",")[0]
            shiftName = shift.split(",")[1]
            
            hourly = (actualHourfrom,actualHourto,actual_volume,shiftName,shiftID)
            return insert_hourly(hourly,1,id=id)
        except Exception as e:
            return render_template("Actual_Hourly.html", error=f"Error Processing this formX: {e}")

#Edit hourly /hourly/edit/{{data[0] }}
@app.route("/hourly_waste/edit/<int:id>")
def edit_hourly_waste(id):
    print(f"hourly {get_hourly_waste(id)[0][1]}")
    return render_template("edit_hourly_waste.html", _edit=get_hourly_waste(id),shift=get_Shifts())
           
@app.route("/hourly_waste/edit/<int:id>",methods=["POST","GET"])
def edit_hourly_waste_update(id):
        try:
            actualHourfrom = request.form["actualHourfrom"]
            actualHourto = request.form["actualHourto"]
            actual_volume = request.form["actual_volume"]
            shift = request.form["shift"]
            shiftID = shift.split(",")[0]
            shiftName = shift.split(",")[1]
            
            hourly_waste = (actualHourfrom,actualHourto,actual_volume,shiftName,shiftID)
            return insert_hourly_waste(hourly_waste,1,id=id)
        except Exception as e:
            return render_template("Actual_Hourly.html", error=f"Error Processing this formX: {e}")
           

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
    
@app.route("/drillblast/edit/<int:id>")
def edit_drill_blast(id):
           return render_template("edit_drIllblast.html", drill=get_drillblast(id))
   
   
@app.route("/drillblast/edit/<int:id>",methods=["POST","GET"])
def update_drill_blast(id):
        if request.method == 'POST':
            try:
                blastedVolume = request.form["blastedVolume"]
                numberOfDaysRequired = request.form["numberOfDaysRequired"]
                actual_volumeMovedPayDay = request.form["actual_volumeMovedPayDay"]
                kpi = (blastedVolume,numberOfDaysRequired,actual_volumeMovedPayDay)
                return insert_blasted_kpi(kpi,value=1,id=id)
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


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        import hashlib
        username = request.form["username"]
        password = request.form["password"]
        auth = (username,hashlib.md5(password.encode('utf-8')).hexdigest())
        conn = None
       
        try:
            data = []
            conn = connect_db()  # Assuming `connect_db` is defined elsewhere
            cursor = conn.cursor()
            sql = "SELECT*FROM users WHERE username=%s AND password=%s"
            cursor.execute(sql,auth)  # Execute the SQL with the provided data
            data = cursor.fetchone() 
            
            if data:
                session["loggedin"] =  True
                session["id"] = data[0]
                session["fullname"] = data[1]
                session["role"] = data[2]
                session["username"] = data[3]
                return render_template("index.html",msg = 'Logged in successfully!',waste = get_hourly_waste(),hours =get_hourly(),maintenance=get_maintenance_vehicle(), shift=get_Shifts(),data=v_status())
            else:
                return render_template("login.html",msg = 'Incorrect username/password!')
        except Exception as e:
            return render_template("login.html",msg =f"Error: {e} ")

        finally:
            if cursor:
                cursor.close()  # Close the cursor
            if conn:
                conn.close()   # Close the connection
            
    else: 
       return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userdata', None)
    return redirect(url_for('login'))


@app.route("/user/register")
def registerUser():
    return render_template("register_user.html")

@app.route("/user/register",methods=["POST","GET"])
def save_users():
   import hashlib
   try:
        fname = request.form["fname"]
        role = request.form["role"]
        username = request.form["username"]
        password = hashlib.md5(request.form["password"].encode('utf-8')).hexdigest()
        user = (fname,role,username,password)
        return insert_user(user)
   except Exception as e:
       return render_template("users.html",user=get_users(),error=e)
   


@app.route("/user")
def users():
    return render_template("users.html",user=get_users())


@app.route("/users/profile")
def users_profile():
    return render_template("myprofile.html",user=get_users())


@app.route("/json")
def get_vehicle_to_json():
    return get_vehicle_registered()



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8089,debug=True)