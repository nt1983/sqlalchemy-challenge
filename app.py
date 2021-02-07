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
        f"/api/v1.0/start<br/>"
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
    prcp=list(np.ravel(prcp_scores))
    session.close()
    return jsonify(prcp)




if __name__ == '__main__':
    app.run(debug=False)


