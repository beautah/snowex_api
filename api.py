# -*- coding: utf-8 -*-
"""
Created on Thu Jul 2 11:10:17 2021
@author: Beau.Uriona
"""

# TODO: how do we handle the PREC 23:59 readings
# TODO: refactor getDaily (for sites) to use the same source aws_plots json like the basin charts, and therefore return stats

import fiona
from flask_cors import CORS
from flask import Flask, make_response, request, render_template
from flask_restx import Api, Resource

from snow_ex import API_ROOT, API_DESC, set_headers
from geo_tools import frmt_geo_response
from endpoints.get_sites import get_sites_args, get_sites

fiona.supported_drivers["KML"] = "rw"

app = Flask(
    __name__, 
    static_url_path="/static", 
    static_folder="static", 
    template_folder="templates"
)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["JSON_SORT_KEYS"] = False
CORS(app)

RESPONSE_CODES = {
    200: "Success!",
    206: "Some requests were successful, but not all",
    404: "Data not found",
    400: "Invalid request",
    500: "Server error, if issue persists contact beau.uriona@usda.gov",
}

api = Api(
    app,
    version="0.0.1",
    title="snow-ex API",
    description=API_DESC,
    contact="beau.uriona@gmail.com",
)


def abort_error(msg="Uh oh... unclassified error...", code=500):
    api.abort(code, msg)


stations = api.namespace(
    "stations", description="methods to get site metadata/site-lists based on filters"
)
data = api.namespace(
    "data", description="methods to get timeseries data for stations/basins"
)


@app.route("/examples/<path:example_path>")
def render_example_templates(example_path, api_root=API_ROOT):
    return render_template(example_path, api_root=api_root)


### getStations endpoint
@stations.route("/getSites")
@api.doc(
    responses=RESPONSE_CODES,
    # params={
    #     "siteId": "site(s) ID filter, use comma delineated string for multiple",
    # },
)
class Sites(Resource):
    """Return list of sites and site metadata"""

    get_parser = get_sites_args()

    @api.expect(get_parser)
    @api.doc(description="Returns site list based on limited filter set")
    def get(self):
        """returns site list and associated metadata"""
        args = self.get_parser.parse_args()
        gdf_sites, code = get_sites(args)
        response = frmt_geo_response(gdf_sites, args.format)
        if code != 200:
            abort_error(msg=response.message, code=response.code)
        return set_headers(make_response(response, 200), args.format)


if __name__ == "__main__":

    import sys
    import argparse
    from flask_cors import CORS

    cli_desc = """
    Deploy non-production version of awdb API, used for local dev
    """
    parser = argparse.ArgumentParser(description=cli_desc)
    parser.add_argument(
        "-V", "--version", help="show program version", action="store_true"
    )
    parser.add_argument(
        "-d", "--debug", help="run in debugging mode", action="store_true"
    )
    parser.add_argument(
        "-p",
        "--port",
        help="host on this port",
        default=5000,
        type=int,
    )
    args = parser.parse_args()

    if args.version:
        print(f"{api.title} v{api.version}")
        sys.exit(0)

    CORS(app)
    app.run(debug=args.debug, port=args.port)
