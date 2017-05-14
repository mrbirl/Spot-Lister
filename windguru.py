import json
import requests

results = {}

region_ids = {
	'Africa': 2,
	'Asia': 142,
	'Oz & NZ': 53,
	'Caribbean': 29,
	'Central America': 13,
	'Europe': 150,
	'North America': 21,
	'Oceania': 9,
	'South America': 5
}

''' For each region, get a list of areas '''
for region_name, region_id in region_ids.iteritems():
	region_req_url = 'http://old.windguru.cz/int/ajax/wg_ajax_json_select.php?' \
				   'q=zeme&id_georegion=%d&exist_spots=1&id_model=0' % region_id
	region_response = requests.get(region_req_url).json()
	area_info = {}

	''' For each area, get a list of spots '''
	for area_item in region_response['zeme']:
		area_id = int(area_item[0])
		area_name = area_item[1]
		area_req_url = 'http://old.windguru.cz/int/ajax/wg_ajax_json_select.php?'\
					   'q=spots&id_zeme=%d&id_region=0&id_georegion=%d&cats=4' % (area_id, region_id)
		area_response = requests.get(area_req_url).json()
		area_spots = {}

		try:
			for spot in area_response['spots']:
				spot_id = spot[0]
				spot_name = spot[1]
				# spot_location = spot[2]  # Not gathering location for now
				area_spots[spot_name] = spot_id  # Save this spot info
				# print 'Added spot %s to area %s in region %s' % (spot_name, area_name, region_name)
		except:
			print 'FAILED: %s %s %d' % (region_name, area_name, (int(area_id)))

		if area_spots:  # Don't save places with no spots
			area_info[area_name] = area_spots  # Save this areas info

	if area_info:  # Only save areas that aren't empty
		results[region_name] = area_info

with open('windguru_spots.json', 'w') as wf:
	json.dump(results, wf, sort_keys=True, indent=4)

print 'Done'









