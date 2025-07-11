from django.shortcuts import render
import json
import urllib.request
import pycountry  # ✅ NEW: Import pycountry

# ✅ Helper to convert country code to country name
def get_country_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name
    except:
        return country_code  # fallback if not found

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        # ✅ Use correct API version 2.5
        res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=a7ed080582eb0be6013d39f5f3f994c4').read()
        json_data = json.loads(res)  # ✅ Fixed typo from json_loads to json.loads

        country_code = str(json_data['sys']['country'])
        country_name = get_country_name(country_code)

        data = {
            "country": country_name,  # ✅ Use full country name
            "coordinate": str(json_data['coord']['lon']) + ', ' + str(json_data['coord']['lat']),
            "temp": str(json_data['main']['temp']) + 'k',
            "pressure": str(json_data['main']['pressure']),
            "humidity": str(json_data['main']['humidity']), 
        }
    else:
        city = ''
        data = {}

    return render(request, 'index.html', {'city': city, 'data': data})
