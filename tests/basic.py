# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 13:43:34 2022

@author: Beau.Uriona
"""

from datetime import datetime

from requests import Session

DOMAIN = "https://api.snowdata.info/"

basic_endpoint_tests = {
    "stations": {
            "getMeta": "state=UT&network=SNTL&format=json",
            "getSites": "state=UT&network=SNTL&format=json",
    },
    "data": {
        "getBasinDaily": "basinType=ut_8&basinName=bear&format=json",
        "getBasinMonthly": "basinType=ut_8&basinName=bear&format=json",
        "getDaily": "triplet=1099:UT:SNTL&format=json",
        "getForecasts": "triplet=09180500:UT:USGS&usePrimary=true&format=json",
        "getMonthly": "triplet=1099:UT:SNTL&format=json",
    },
    "stats": {
        "getNormals": "triplet=1099:UT:SNTL&format=json",
    },
    "basin": {
        "getBasins": "basinType=ut_8",
        "getParents": "state=UT",
        "getSites": "basinType=ut_8&basinName=bear",
        
    },
    "wsor": {
        "getFcstData": "state=UT&pubMonth=4&pubYear=2020",
        "getPrecDaily": "state=UT&pubDay=10&pubMonth=4&pubYear=2020",
        "getPrecData": "state=UT&pubMonth=4&pubYear=2020",
        "getResData": "state=UT&pubMonth=4&pubYear=2020",
        "getSnowDaily": "state=UT&pubDay=10&pubMonth=4&pubYear=2020",
        "getSnowData": "state=UT&pubMonth=4&pubYear=2020",
    }
}

failed_tests = []
with Session() as sesh:
    for ns, endpoints in basic_endpoint_tests.items():
        print(f"Working on {ns} methods...")
        for endpoint, args in endpoints.items():
            url = f"{DOMAIN}{ns}/{endpoint}?{args}"
            req = sesh.get(url)
            if not req.ok:
                print(f"  Failed! - {ns}/{endpoint} failed!")
                failed_tests.append(
                    {
                        "url": url,
                        "domain": DOMAIN,
                        "ns": ns,
                        "endpoint": endpoint,
                        "args": args,
                        "time": datetime.now(),
                    }
                )
            else:
                print(f"  Success! - {ns}/{endpoint} returned 200!")