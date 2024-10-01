# sqlalchemy-challenge

## Overview

  ### This project conducts a climate analysis on historical weather data for Honolulu, Hawaii using Python, SQLAlchemy, and Flask. The analysis involves performing queries on a SQLite database to extract precipitation and temperature data. The findings are then used to build a Flask API that serves climate data through various endpoints.

## Files and Structure
  ### -climate_starter.ipynb: Jupyter notebook for climate data exploration and analysis.
  ### -app.py: Flask application to create API routes based on the climate data.
  ### -Resources/: Folder containing the SQLite database (hawaii.sqlite) with climate data.

## Analysis Tasks

### Part 1: Climate Data Exploration

  #### Precipitation Analysis:
  
    #### -Retrieve the last 12 months of precipitation data.
    ### -Store results in a DataFrame and generate visual plots.
    #### Station Analysis:
    #### -Calculate total number of weather stations.
    #### -Identify most active station and analyze its temperature data.

### Part 2: Flask API Development

  #### Create an API with the following endpoints:
    
    #### 1) /: Homepage listing available routes.
    #### 2) - /api/v1.0/precipitation: Precipitation data for the last year.
    #### 3) - /api/v1.0/stations: List of weather stations.
    #### 4) /api/v1.0/tobs: Temperature observations for the most active station.
    #### 5) /api/v1.0/<start> and /api/v1.0/<start>/<end>: Minimum, average, and maximum temperatures for a specified date range.

## How to Run
  ### -Clone the repository.
  ### -Set up a virtual environment and install dependencies.
  ### -Run the Jupyter notebook (climate_starter.ipynb) for analysis.
  ### -Start the Flask application (app.py) to access the API.

## Dependencies
  ### Python 3.7+
  ### SQLAlchemy
  ### Flask
  ### Pandas
  ### Matplotlib
