# Import the dependencies.
import pandas as pd
import numpy as np
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from datetime import datetime

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

# reflect the tables
print(Base.classes.keys())

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

# Define the homepage 
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

#################################################
# Flask Routes
#################################################

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the most recent date in the database
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    # Calculate the date one year ago from the last data point
    one_year_ago = pd.to_datetime(recent_date) - pd.DateOffset(years=1)

    # Convert the `Timestamp` to a string in the format 'YYYY-MM-DD'
    one_year_ago_str = one_year_ago.strftime('%Y-%m-%d')

    # Perform a query to retrieve date and precipitation data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago_str).all()

    # Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)


# Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    results = session.query(Station.station).all()

    # Unravel results into a list
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)

# Temperature Observations route for the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    # Find the most recent date in the data set
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    # Calculate the date one year ago from the most recent date
    one_year_ago = pd.to_datetime(recent_date) - pd.DateOffset(years=1)

    # Convert the `Timestamp` to a string in the format 'YYYY-MM-DD'
    one_year_ago_str = one_year_ago.strftime('%Y-%m-%d')

    # Find the most active station
    most_active_station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]

    # Query the last 12 months of temperature observation data for this station
    results = (
        session.query(Measurement.tobs)
        .filter(Measurement.station == most_active_station)
        .filter(Measurement.date >= one_year_ago_str)
        .all()
    )

    # Convert the results to a list
    temperature_data = list(np.ravel(results))

    # Return the JSON representation of the temperature data
    return jsonify(temperature_data)


# Start route to calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Convert the start date from the URL parameter to a datetime object
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Perform the query to calculate min, avg, and max temperature for all dates greater than or equal to start date
    results = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        )
        .filter(Measurement.date >= start_date.strftime("%Y-%m-%d"))
        .all()
    )

    # Unpack the results into a list of statistics
    temp_stats = list(np.ravel(results))

    return jsonify(temp_stats)

# Start/End route to calculate TMIN, TAVG, and TMAX for dates between the start and end date inclusive
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Convert the start and end dates from the URL to datetime objects
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Query for min, avg, and max temperature between start and end dates
    results = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        )
        .filter(Measurement.date >= start_date.strftime("%Y-%m-%d"))
        .filter(Measurement.date <= end_date.strftime("%Y-%m-%d"))
        .all()
    )

    # Unpack the results into a list of statistics
    temp_stats = list(np.ravel(results))

    # If no data found, handle the case by returning an empty list or a message
    if temp_stats == [None, None, None]:
        return jsonify({"error": "No data found for the given date range"}), 404

    return jsonify(temp_stats)


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
