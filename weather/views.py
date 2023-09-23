from django.shortcuts import render
import json
import urllib.request

# Create your views here.
def index(request):
    if request.method == "POST":
        city = request.POST['city'].strip()
        key = "eac2ab0c72eadc83a33598439aae4f50"

        try:
            res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=eac2ab0c72eadc83a33598439aae4f50').read()

            json_data = json.loads(res)
            data = {
                'country_code': str(json_data['sys']['country']),
                'coordinate': str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
                'temp': str(json_data['main']['temp']) + 'k',
                'pressure': str(json_data['main']['pressure']),
                'humidity': str(json_data['main']['humidity']),
                'city': str(json_data['name'])
            }
        except:
            data = {'city': 'City not found'}
    else:
        data = {'city':''}
    return render(request, 'index.html', data)
