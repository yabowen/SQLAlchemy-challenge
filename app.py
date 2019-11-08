import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask,jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    """List all available api routes."""
    return(
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date,Measurement.prcp).all()
    precipitation = list(np.ravel(results))
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def station():
    stations = session.query(Station.station).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>'2016-06-24').all()
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def temps_start(start):
    temps_1 = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
        ).filter(Measurement.date>=start).all()
    return jsonify(temps_1)

@app.route("/api/v1.0/<start>/<end>")
def temps_both(start,end):
    temps_2 = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
        ).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    return jsonify(temps_2)

if __name__ == "__main__":
    app.run(debug=True)