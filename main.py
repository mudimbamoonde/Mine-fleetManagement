# Main application file
# Database connection and queries
# GPS tracking logic
# Route optimization logic
# Labor calculation logic
# Machine service tracking
# Data visualization (dashboard)
# Config file for API keys and other settings
# config.py

# Google Maps API Key for geolocation
GOOGLE_MAPS_API_KEY = 'AIzaSyD7G9q4lOY7vsdd85vSq-XzYncMSB52ff4'

# Database configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'fleetmgr'
# database.py
import mysql.connector
# from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def connect_db():
    """ Connect to the MySQL database """
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return connection

def save_vehicle_data(vehicle_id, location, speed):
    """ Save vehicle data into the database """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vehicle_data (vehicle_id, location, speed) VALUES (%s, %s, %s)", 
                    (vehicle_id, str(location), speed))
        conn.commit()
        conn.close()
        print(f"{vehicle_id}: Saved info!!")
    except Exception as  e:
        print("Error:" , e)

def get_vehicle_registered():
    """ pull vehicle data into the database """
    data = []
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT*FROM vehicle")         
    conn.commit()
    conn.close()


def get_vehicle_data(vehicle_id):
    """ Get vehicle data from the database """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicle_data WHERE vehicle_id = %s", (vehicle_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def get_machine_service_status(machine_id):
    """ Retrieve service status of the machine """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM machine_service WHERE machine_id = %s", (machine_id,))
    status = cursor.fetchone()
    conn.close()
    return status
# gps_tracker.py
from geopy.distance import geodesic
import time

class GPSTracker:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.location = (0, 0)  # Initial coordinates (latitude, longitude)
        self.speed = 0  # Initial speed

    def update_location(self, new_location):
        """ Update the vehicle's location and calculate speed """
        old_location = self.location
        self.location = new_location
        distance = geodesic(old_location, new_location).meters
        self.speed = distance / 60  # Assuming location update every minute
        print(f"Vehicle {self.vehicle_id}: Speed: {self.speed} km/h, Location: {self.location}")

    def get_location(self):
        return self.location

    def get_speed(self):
        return self.speed

# Example usage
tracker = GPSTracker(vehicle_id=1)
tracker.update_location((40.712776, -74.005974))  # Example coordinates
# route_optimizer.py
import googlemaps
# from config import GOOGLE_MAPS_API_KEY

class RouteOptimizer:
    def __init__(self):
        self.gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

    def get_optimal_route(self, origin, destination):
        """ Calculate optimal route using Google Maps API """
        directions = self.gmaps.directions(
            origin,
            destination,
            mode="driving",
            departure_time="now"
        )
        return directions

# Example usage
optimizer = RouteOptimizer()
route = optimizer.get_optimal_route("New York, NY", "Los Angeles, CA")
print(route)
# machine_service.py

class MachineService:
    def __init__(self):
        self.run_hours = 0

    def log_run_hours(self, hours):
        """ Add run hours to the machine """
        self.run_hours += hours
        print(f"Machine run hours logged: {self.run_hours} hours")

    def check_for_service(self):
        """ Check if the machine is due for service based on run hours """
        if self.run_hours >= 1000:  # Example threshold for service
            return "Machine needs service"
        else:
            return "Machine is fine"

# Example usage
machine = MachineService()
machine.log_run_hours(1200)  # Logging 1200 hours of usage
status = machine.check_for_service()
print(status)
# labor_calculator.py
class LaborCalculator:
    def __init__(self):
        self.machine_downtime = 0
        self.breakdowns = 0

    def calculate_labor(self, total_machines, hours_worked):
        """ Calculate ideal labor requirements """
        labor_needed = total_machines * hours_worked / 8  # Assuming 8 hours shift
        labor_needed += self.breakdowns * 2  # Double labor for broken machines
        return labor_needed

    def report_breakdowns(self, machine_id):
        """ Log breakdowns """
        self.breakdowns += 1
        print(f"Machine {machine_id} breakdown logged.")
        
# Example usage
calculator = LaborCalculator()
required_labor = calculator.calculate_labor(total_machines=10, hours_worked=8)
print(f"Labor needed: {required_labor} workers")

# dashboard.py
import plotly.graph_objects as go
import pandas as pd

def create_dashboard(vehicle_data):
    """ Create an interactive dashboard for fleet management """
    df = pd.DataFrame(vehicle_data)
    
    fig = go.Figure()
    
    # Create a plot for vehicle speeds
    fig.add_trace(go.Scatter(x=df['vehicle_id'], y=df['speed'], mode='lines+markers', name='Speed'))

    fig.update_layout(title="Vehicle Speeds",
                      xaxis_title="Vehicle ID",
                      yaxis_title="Speed (km/h)")
    
    fig.show()

# Example usage
vehicle_data = [
    {"vehicle_id": 1, "speed": 40},
    {"vehicle_id": 2, "speed": 50},
    {"vehicle_id": 3, "speed": 30},
]
create_dashboard(vehicle_data)

# app.py
# pip install --trusted-host pypi.python.org
# --trusted-host pypi.org --trusted-host files.pythonhosted.org pytest-xdist
from gps_tracker import GPSTracker
from route_optimizer import RouteOptimizer
from labor_calculator import LaborCalculator
from machine_service import MachineService
from dashboard import create_dashboard
import time

def main():
    # Initialize necessary objects
    tracker = GPSTracker(vehicle_id=1)
    optimizer = RouteOptimizer()
    labor_calculator = LaborCalculator()
    machine_service = MachineService()

    # Simulate GPS updates for a vehicle
    tracker.update_location((40.712776, -74.005974))  # Example location
    time.sleep(5)  # Simulate delay
    tracker.update_location((40.730610, -73.935242))  # Another example location

    # Save the vehicle data to the database
    vehicle_id = tracker.vehicle_id
    save_vehicle_data(vehicle_id, tracker.get_location(), tracker.get_speed())

    # Simulate route optimization
    route = optimizer.get_optimal_route("New York, NY", "Los Angeles, CA")
    print("Optimal Route:", route)

    # Log and check machine service status
    machine_service.log_run_hours(1200)
    service_status = machine_service.check_for_service()
    print(service_status)

    # Simulate labor calculation
    labor_needed = labor_calculator.calculate_labor(total_machines=5, hours_worked=8)
    print(f"Labor needed: {labor_needed} workers")

    # Create dashboard
    vehicle_data = [
        {"vehicle_id": 1, "speed": tracker.get_speed()},
        {"vehicle_id": 2, "speed": 50},
    ]
    create_dashboard(vehicle_data)

if __name__ == "__main__":
    pass
    # main()

