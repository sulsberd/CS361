# Helper to call an FCC API to grab the correct census tract for a given lat/lon.
def get_fips(latitude, longitude):
	census_tract = requests.get("http://data.fcc.gov/api/block/find?format=json&latitude=%f&longitude=%f&showall=true" % (latitude, longitude))
	return census_tract.json()