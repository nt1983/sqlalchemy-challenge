from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources\hawaii.sqlite")
# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station
# Create our session (link) from Python to the DB
session=Session(engine)


#Create an app, being sure to pass __name__
app=Flask(__name__)

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"For below URL, enter start date in format: YYYY-MM-DD<br/>"
        f"/api/v1.0/<start><br/>"
        f"For below URL, enter start date and end date in format: YYYY-MM-DD/YYYY-MM-DD <br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """precipitation data in json format"""
    # Find the most recent date in the data set.
    recent_date=session.query(func.max(Measurement.date)).first()[0]
    # Calculate the date one year from the last date in data set.
    date_point=dt.datetime.strptime(recent_date, '%Y-%m-%d')-dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    prcp_scores=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=date_point).all()
    #Change result to dictionary
    p_dict= {date:prcp for date,prcp in prcp_scores}
    session.close()
    return jsonify(p_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Design a query to find the most active stations (i.e. what stations have the most rows?)
    # List the stations and the counts in descending order.
    most_active=session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc())
    active=most_active.all()
    all_station=list(np.ravel(active))
    session.close()
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Find the most recent date in the data set.
    recent_date=session.query(func.max(Measurement.date)).first()[0]
    # Calculate the date one year from the last date in data set.
    date_point=dt.datetime.strptime(recent_date, '%Y-%m-%d')-dt.timedelta(days=365)
    most_active=session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc())
    # Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
    active_station_id=most_active.first()[0]
    session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station==active_station_id).all()
    # Using the most active station id
    # Query the last 12 months of temperature observation data for this station
    temp_observation=session.query(Measurement.tobs).filter(Measurement.station==active_station_id).filter(Measurement.date>=date_point).all()
    yearly_temp=list(np.ravel(temp_observation))
    session.close()
    return jsonify(yearly_temp)

@app.route("/api/v1.0/<start>")
def start_date(start=None):
    date_result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date>=start).all()
    d_result=list(np.ravel(date_result))
    session.close()
    return jsonify(d_result)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start=None, end=None):
    result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    full_result=list(np.ravel(result))
    session.close()
    return jsonify(full_result)
    
if __name__ == '__main__':
    app.run(debug=False)


