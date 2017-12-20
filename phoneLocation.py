import phonenumbers
from phonenumbers import geocoder
import requests

def lambda_handler(event, context = None):
  phone_number = event["params"]["querystring"]["phone"]
  phone_number = '+' + phone_number
  print phone_number
  try:
    v = phonenumbers.parse(phone_number, None)
  except:
    v = None
  if v and v.country_code == 1:
    # This is a US number, so lets do the geocoder

    state = geocoder.description_for_number(v, "en")
    country_code = "US"
    return {"country_code": country_code, "state": state}
  if v and v.country_code == 91:
    # This is India, so we may get some more info about this guy
    country_code = "IN"
    phone_without = str(v.national_number)
    url = 'https://avneesh-indian-phone-number-info-v1.p.mashape.com/getphoneinfo'
    params = {
      'mobile_number': phone_without[:4]
    }
    headers = {
      'X-Mashape-Key': 'gi7WK8GMREmshSQcmqWtPalrLYrap1D3t32jsnMgtJqq0NafUR',
      'Accept': 'application/json'
    }
    r = requests.get(url, params = params, headers = headers)

    if r.status_code == 200 and 'location' in r.json().keys():
      state = r.json()['location']
      if state == 'Kolkatta':
	state = 'Kolkata'
      if state == 'Andra Pradesh':
	state = 'Andhra Pradesh'
      if state == 'Maharastra':
        state = 'Maharashtra'
      if state == 'Gujarat':
        state = 'Gujrat'
      if state == 'Goa&Maharashtra':
        state = 'Maharashtra'
      if state == 'Uttar Pradesh(East)':
        state = 'Uttar Pradesh East'
      if state == 'Uttar Pradesh(West)':
        state = 'Uttar Pradesh West'
      if state == 'Madhya Pradesh & Chhattisgarh':
        state = 'Madhya Pradesh'
      if state == 'karnataka':
        state = 'Karnataka'
      if state == 'Bihar & Jharkhand':
        state = 'Bihar'
      if state == 'Orissa':
        state = 'Odisha'
      if state == 'Uttar Pradesh(west) & Uttarakhand':
        state = 'Uttar Pradesh West'
      if state == 'Uttar Pradesh(west) & Uttarkhand':
        state = 'Uttar Pradesh West'
      if state == 'Tata Docomo':
        return None
      return {'country_code': country_code, "state": state}
  return None
