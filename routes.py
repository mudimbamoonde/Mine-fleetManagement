from app import app
from flask import render_template,request,redirect,url_for
from dbquery import *

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




@app.route("/json")
def get_vehicle_to_json():
    return get_vehicle_registered()



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8089,debug=True)