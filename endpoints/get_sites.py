# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 06:52:04 2021

@author: Beau.Uriona
"""

from flask_restx import reqparse
from sqlalchemy import column
from sqlalchemy.orm import load_only

from snowexsql.db import get_db
from snowexsql.data import SiteData
from snowexsql.conversions import query_to_geopandas

from snow_ex import SnowException, DB_CONN_STR
from snow_ex import JSON_OPTIONS, JSON_OPTIONS_DESC

META_COLS = (
    SiteData.easting,
    SiteData.elevation,
    SiteData.geom,
    SiteData.latitude,
    SiteData.longitude,
    SiteData.northing,
    SiteData.pit_id,
    SiteData.registry,
    SiteData.site_id,
    SiteData.site_name,
    SiteData.site_notes,
    SiteData.slope_angle,
    SiteData.tree_canopy,
    SiteData.utm_zone,
    SiteData.vegetation_height
)

def get_sites_args():
    get_parser = reqparse.RequestParser()
    get_parser.add_argument(
        "siteId",
        type=str,
        default="ALL",
        required=False,
        help="enter a single site ID or a comma delineated list of sites",
        location="args",
    )
    get_parser.add_argument(
        "siteName",
        type=str,
        default="ALL",
        required=False,
        help="enter a single site ID or a comma delineated list of sites",
        location="args",
    )
    get_parser.add_argument(
        "format",
        type=str,
        default="geojson",
        required=False,
        help="pick a data format (default is csv)",
        location="args",
        choices=("csv", "json", "geojson"),
    )
    get_parser.add_argument(
        "orient",
        type=str,
        default="records",
        required=False,
        help=JSON_OPTIONS_DESC,
        location="args",
        choices=JSON_OPTIONS,
    )
    return get_parser


def filter_sites(stations, item, filter_list):
    if "ALL" in filter_list:
        return stations
    return [
        i for i in stations
        if any([i[item].startswith(filter_item) for filter_item in filter_list])
    ]


def get_sites(args, meta_cols=META_COLS, db_name=DB_CONN_STR):
    site_ids = [i.lower() for i in args.siteId.split(",")]
    site_names = [i.lower() for i in args.siteId.split(",")]
    if True:
        engine, session = get_db(db_name)
        # qry = session.query(SiteData.geom, SiteData.site_name).distinct()
        qry = session.query(
            SiteData.site_name,
            SiteData.latitude,
            SiteData.longitude,
            SiteData.easting,
            SiteData.northing,
            SiteData.utm_zone,
            SiteData.elevation,
            # SiteData.pit_id,
            # SiteData.registry,
            # SiteData.site_id,
            SiteData.site_notes,
            SiteData.slope_angle,
            SiteData.tree_canopy,
            SiteData.vegetation_height,
            SiteData.geom
        ).distinct()
        gdf_stations = query_to_geopandas(qry, engine).drop_duplicates(subset="site_name")
        session.close()
        # gdf_stations = filter_sites(gdf_stations, "site_id", site_ids)
        # gdf_stations = filter_sites(gdf_stations, "site_name", site_names)
        return gdf_stations, 200
    # except:
    #     return SnowException(
    #         "An error occured getting data from the db...",
    #         500,
    #     ), 500


if __name__ == "__main__":
    print("write some tests or something...")
