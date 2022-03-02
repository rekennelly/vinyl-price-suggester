import requests
import config

BASE_URL = "https://api.discogs.com/"
GRADES_DICT = {"M": "Mint (M)", "NM": "Near Mint (NM or M-)", "VG+": "Very Good Plus (VG+)", "VG": "Very Good (VG)", "G+": "Good Plus (G+)", "G": "Good (G)", "F": "Fair (F)", "P": "Poor (P)"}

class Error(Exception):
   """Base class for other exceptions"""
   pass

class InvalidReleaseIdError(Error):
	"""Exception raised for errors in the input release id."""
	pass

class InvalidRecordGradeError(Error):
	"""Exception raised for errors in the input record grade."""
	pass

def get_price_suggestion(release_id, record_grade):
	""" 
	Get price suggestion from given release id

	Parameters:
	release_id (int): Validated release id
	record_grade (string): Validated record grade abbreviation

	Returns:
	int: suggested price
	"""
	price_suggestions = requests.get(BASE_URL + "marketplace/price_suggestions/" + str(release_id), config.auth).json()
	price_suggestions_key = GRADES_DICT[record_grade]
	suggestion_dict = price_suggestions[price_suggestions_key]
	suggested_price = suggestion_dict["value"]
	suggestion_currency = suggestion_dict["currency"]

	return suggested_price, suggestion_currency

def get_release_info(release_id):
	"""
	Get the info from a given release id

	Parameters:
	release_id (int): Validated release id

	Returns:
	string: release name
	list: list containing artist(s) name(s) as string
	"""
	release = requests.get(BASE_URL + "/releases/" + str(release_id), config.auth).json()
	release_name = release["title"]
	artists = release["artists"]
	release_artists = []
	for artist in artists:
		release_artists.append(artist["name"])
	return release_name, release_artists

def get_user_input():
	"""
	Get user inputs of release ID and record grade

	Returns:
	int: release ID
	string: record grade
	"""
	while True:
		try: 
			release_id_input = int(input("Enter the release ID for the price suggestion: "))
			if release_id_input < 1:
				raise(InvalidReleaseIdError)
			break
		except ValueError:
			print("ERROR: Not a valid release ID.")
		except InvalidReleaseIdError:
			print("ERROR: Release ID must be a positive integer.")
	print("====================== Record Grading Options =====================")
	print("Mint (M)             Near Mint (NM)          Very Good Plus (VG+)")
	print("Very Good (VG)       Good Plus (G+)          Good (G)")
	print("===================================================================")
	valid_inputs = ["M", "NM", "VG+", "VG", "G+", "G", "F", "P"]
	while True:
		try:
			record_grade_input = input("Enter the code in parentheses of the record's grade: ")
			if record_grade_input in valid_inputs:
				break
			else:
				raise(InvalidRecordGradeError)
		except InvalidRecordGradeError:
			print("ERROR: Invalid record grade. Please input a grade from the following list.")
			print("[M, NM, VG+, VG, G+, G, F, P]")
	return release_id_input, record_grade_input	

def main():
	# Get release id & record grade from user
	release_id, record_grade = get_user_input()
	# Get release name & artist(s) from Discogs
	release_name, artists = get_release_info(release_id)
	# Format artist(s) names for albums with more than one artist
	release_artists = ", ".join(artists)
	# Get price
	suggested_price, currency = get_price_suggestion(release_id, record_grade)
	formatted_price_USD = "${:,.2f}".format(suggested_price)

	print(f"Suggested price for {GRADES_DICT[record_grade]} copy of {release_name} — {release_artists}: {formatted_price_USD}")
		

main()

