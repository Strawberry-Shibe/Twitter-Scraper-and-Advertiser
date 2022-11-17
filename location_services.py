from geopy.geocoders import Nominatim
import country_converter as coco


def get_country(locator, lat, long):
	coords = (lat, long,)
	location = locator.reverse(coords, language="en").raw

	return location["address"]["country"]


def get_country_code(country):
	return coco.convert(names=country, to='ISO3')


def coord_to_code(lat, long):
	locator = Nominatim(user_agent="myGeocoder")
	country = get_country(locator, lat, long)
	country_code = get_country_code(country)
	return country_code


if __name__ == "__main__":
	latitude = -49.18657710771038
	longitude = 70.29676495934203
	print(coord_to_code(latitude, longitude))
