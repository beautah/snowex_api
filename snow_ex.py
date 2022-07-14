# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 06:51:48 2021

@author: Beau.Uriona
"""

from os import getenv
from io import BytesIO
from datetime import date, timedelta

import pandas as pd
import geopandas as gpd

from geo_tools import frmt_geo_response

API_ROOT = getenv("API_ROOT", "")
API_DESC = "RESTful Access to the SnowEx PostGIS database."
DB_CONN_STR = 'snow:hackweek@db.snowexdata.org/snowex'
JSON_KWARGS = {"sort_keys": True, "indent": 2}
JSON_OPTIONS = ("split", "records", "index", "columns", "values")
JSON_OPTIONS_DESC = """
'split' : dict like {'index' -> [index], 'columns' -> [columns], 'data' -> [values]}
'records' : list like [{column -> value}, … , {column -> value}]
'index' : dict like {index -> {column -> value}}
'columns' : dict like {column -> {index -> value}}
'values' : just the values array
"""


class SnowException(Exception):
    def __init__(self, message, code=500):
        super().__init__(message)
        self.code = code
        self.message = message


def frmt_response(results, frmt="json", orient="records"):
    if isinstance(results, Exception):
        return results
    if isinstance(results, gpd.GeoDataFrame):
        return frmt_geo_response(results, frmt=frmt, orient=orient)
    df = results
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame.from_dict(results)
    if frmt == "json":
        index = True
        if orient in ["split", "table"]:
            index = False
        return df.to_json(index=index, orient=orient, date_format="iso")
    if frmt == "csv":
        return df.to_csv(index=False)
    if frmt == "plotly":
        return format_plotly(results)
    if frmt == "geojson":
        return points_to_geojson(df)
    if frmt == "kml":
        return geojson_to_kml(points_to_geojson(df))

def geojson_to_kml(geoj):
    gdf = gpd.GeoDataFrame.from_features(geoj["features"])
    byteIO = BytesIO()
    gdf.to_file(byteIO, driver="KML")
    byte_str = byteIO.getvalue()
    return byte_str.decode('UTF-8')

def points_to_geojson(df):
    features = []
    for idx, row in df.iterrows():
        prop = row.to_dict()
        lat = prop.pop("latitude")
        lon = prop.pop("longitude")
        elev = prop.pop("elevation")
        feature = {
            "type": "Feature",
            "properties": prop,
            "geometry": {"type": "Point", "coordinates": [lon, lat, elev]},
        }
        features.append(feature)
    return {"type": "FeatureCollection", "features": features}


def format_plotly(df):
    data = []
    cols = df.columns
    for n in range(1, len(cols)):
        clean_data = df.iloc[:, [0, n]].dropna()
        if clean_data.empty:
            continue
        trace = {
            "x": clean_data.iloc[:, 0].to_list(),
            "y": clean_data.iloc[:, 1].to_list(),
            "name": cols[n],
        }
        data.append(trace)
    return {"data": data}


def set_headers(response, frmt="csv", filename="export"):
    frmt = frmt.lower()
    filename = f"{filename}.{frmt}"
    frmt_dict = {
        "csv": "text/csv",
        "json": "text/json",
        "plotly": "text/json",
        "geojson": "text/json",
        "topojson": "text/json",
        "kml": "text/html",
    }

    if frmt.lower() in ["kml"]:
        disp = "Content-Disposition"
        response.headers[disp] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = frmt_dict.get(frmt, "text/html")
    return response


def parse_date(date_arg):
    today = date.today()
    if date_arg.isnumeric():
        date_arg = today - timedelta(days=abs(int(date_arg)))
    elif date_arg.lower() == "por":
        date_arg = date(1900, 1, 1)
    elif date_arg.lower() == "today":
        date_arg = today
    elif date_arg.lower() == "wy":
        yr_offset = 1 if today.month < 10 else 0
        date_arg = date(today.year - yr_offset, 10, 1)
    else:
        try:
            pd.to_datetime(date_arg, infer_datetime_format=True)
        except Exception:
            return None
    return date_arg



class DictToArgs:
    def __init__(self, arg_dict=None, **kwargs):
        if arg_dict is not None:
            for key, value in arg_dict.items():
                setattr(self, key, value)
        for key, value in kwargs.items():
            setattr(self, key, value)
                
                
if __name__ == "__main__":
    print("write some tests or something...")
