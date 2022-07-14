# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 08:08:59 2021

@author: Beau.Uriona
"""

from os import path

import pandas as pd

THIS_DIR = path.dirname(path.abspath(__file__))
STATIC_DIR = path.join(THIS_DIR, "static")

def rename_btype(topo_dict):
    geom = topo_dict["objects"]["hucall_simplified"]["geometries"]
    for g in geom:
        g["properties"]["btype"] = g["properties"].pop("type")
    topo_dict["objects"]["hucall_simplified"]["geometries"] = geom
    return topo_dict



def frmt_geo_response(gdf, frmt="geojson", orient="records"):
    if isinstance(gdf, Exception):
        return gdf
    if frmt == "geojson":
        return gdf.to_json()
    df = pd.DataFrame(gdf.drop(columns="geom"))
    if frmt == "json":
        index = True
        if orient in ["split", "table"]:
            index = False
        return df.to_json(index=index, orient=orient)
    if frmt == "csv":
        return df.to_csv(index=False)


def get_gdf_attrs(gdf, b_attr="btype", unique=False):
    if not b_attr in gdf.columns:
        return []
    b_attrs = gdf[b_attr]
    if unique:
        b_attrs = b_attrs.unique()
    return list(b_attrs)


def filter_geom(gdf, val, b_attr="btype", filter_type="eq"):
    wildcard_custom_dict = {"xx_8": 4, "xx2_8": 5, "xx3": 3}
    val = str(val).lower()
    if val == "all":
        return gdf
    if filter_type == "eq":
        if val.startswith("xx"):
            str_len = wildcard_custom_dict.get(val, 4)
            return gdf[gdf[b_attr].str.len() == str_len]
        return gdf[gdf[b_attr].str.lower() == val]
    if filter_type == "in":
        if isinstance(val, str):
            val = [i.strip() for i in val.split(",")]
        return gdf[gdf[b_attr].str.lower().isin(val)]
    return gdf


if __name__ == "__main__":
    
    pass
