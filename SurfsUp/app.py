# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Database Setup
# reflect an existing database into a new model
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
# Create our session (link) from Python to the DB (inside each function)
session = Session(engine)

@app.route('/')
def home():
    session = Session(engine)
    content = (
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs<br>"
        "/api/v1.0/start_date<br/>"
 #       "/api/v1.0/<start/<end><br>"
    )
    return content

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    most_recent_date_str = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.date.fromisoformat(most_recent_date_str)
    last_year_date = most_recent_date - dt.timedelta(days=365)
    scores = session.query(Measurement.date, Measurement.prcp)\
                .filter(Measurement.date >= last_year_date)\
                .all()
    scores_dict = []
    for score in scores:
        score_dict = {
            "date": score.date,
            "prcp": score.prcp
        }
        scores_dict.append(score_dict)
    return jsonify(scores_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    total_stations = session.query(Station.station).all()
    total_stations_dict = []
    for station in total_stations:
        station_dict = {
            "station": station.station
        }
        total_stations_dict.append(station_dict)
    return jsonify(total_stations_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    active_station = session.query(Measurement.station, func.count(Measurement.station))\
                            .group_by(Measurement.station)\
                            .order_by(desc(func.count(Measurement.station)))\
                            .all()
    most_active_station_id = active_station[0][0]
    most_recent_date_str = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.date.fromisoformat(most_recent_date_str)
    last_year_date = most_recent_date - dt.timedelta(days=365)
    last_twelve_months = session.query(Measurement.tobs, Measurement.date)\
        .filter(Measurement.station == most_active_station_id)\
        .filter(Measurement.date >= last_year_date)\
        .all()
    last_twelve_months_dict = []
    for date_temp in last_twelve_months:
        date_temp_dict = {
            "date": date_temp.date,
            "tobs": date_temp.tobs
        }
        last_twelve_months_dict.append(date_temp_dict)
    return jsonify(last_twelve_months_dict)


@app.route("/api/v1.0/start_date/<start_date>")
def temperature_start(start_date=None):
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    session = Session(engine)

    f_start_date = dt.date.fromisoformat(start_date)
    temp_stats = session.query(
        func.min(Measurement.tobs), 
        func.max(Measurement.tobs), 
        func.avg(Measurement.tobs)
    ).filter(Measurement.date >= f_start_date).all()

    session.close()

    start_date_dict = []
    for row in temp_stats:
        stat_dict = {
            "minimum temperature": row[0],
            "maximum temperature": row[1],
            "average temperature": row[2]
        }
        start_date_dict.append(stat_dict)

    return jsonify(start_date_dict)


# @app.route("/api/v1.0/start_end_date/<start>/<end>")
# def temperature_start_end(start=None, end=None):
#     start_date = dt.date.fromisoformat(start)
#     end_date = dt.date.fromisoformat(end)
#     temp_stats = session.query(
#         func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
#         .filter(Measurement.date >= start_date)\
#         .filter(Measurement.date <= end_date)\
#         .all()
#     start_end_date_dict = []
#     for row in temp_stats:
#         stat_dict = {
#             "minimum temperature": row[0],
#             "maximum temperature": row[1],
#             "average temperature": row[2]
#         }
#         start_end_date_dict.append(stat_dict)
#     return jsonify(start_end_date_dict)

# Run the app
if __name__ == "__main__":
    app.debug = True
    app.run()
