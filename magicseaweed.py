import json
import requests

results = {}

# 12 regions, all have the same url format just loop through for all details
for region_id in range(1, 13):

	region_req_url = ' http://magicseaweed.com/api/mdkey/continent/%d?depth=4' % region_id
	region_response = json.loads(requests.get(region_req_url).text)

	region_name = region_response[0]['name']  # It's a dict in a list

	area_results = {}

	''' MSW nests things more heavily, so we'll stick to just 3 tiers so
	it's the same as WindGuru. Will skip past one category.'''

	for mid_region in region_response[0]['regions']:

		for area in mid_region['countries']:
			area_name = area['name']

			area_spots = {}

			for spot in area['spots']:
				# Save spots for this area
				area_spots[spot['name']] = spot['url']

			area_results[area_name] = area_spots
			print 'Finished ' + area_name

	results[region_name] = area_results

with open('magicseaweed_spots.json', 'w') as wf:
	json.dump(results, wf, sort_keys=True, indent=4)

print 'Done'
