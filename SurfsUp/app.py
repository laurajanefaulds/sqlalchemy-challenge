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

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

# reflect the tables


# Save references to each table


#################################################
# Flask Setup
#################################################


app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Create our session (link) from Python to the DB (inside each function)

# session = Session(engine)
@app.route('/')
def home():
    content = (
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
    )   
                
    return content 


#################################################
# Run the app
#################################################
if __name__ == "__main__":
    app.run()
