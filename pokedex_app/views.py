from django.shortcuts import render
import json
import urllib.request
from http import HTTPStatus
from urllib.error import HTTPError
# Create your views here.


def index(request):
    try:    
        if request.method == "POST":
            pokemon = request.POST.get('pokemon').lower()
            pokemon = pokemon.replace(" ", "%20")
            url_pokeapi = urllib.request.Request(
                f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
            url_pokeapi.add_header("User-Agent", "Mozilla/5.0")

            source = urllib.request.urlopen(url_pokeapi).read()
            list_data = json.loads(source)

            list_data["height"] = str(round(float(list_data["height"]) * 0.1, 1)) + " m"
            list_data["weight"] = str(round(float(list_data["weight"]) * 0.1, 1)) + " kg"

            data = {
                "number": str(list_data["id"]),
                "name": str(list_data["name"]).capitalize(),
                "height": str(list_data["height"]),
                "weight": str(list_data["weight"]),
                "types": [str(i["type"]["name"]).capitalize() for i in list_data["types"]],
                "sprite": str(list_data["sprites"]["front_default"]),
            }
            

        else:
            data = {}
        return render(request, "index.html", {"data": data})
    except HTTPError:
        data = {"error": "Pokemon no encontrado, intenta de nuevo"}
        return render(request, "index.html", {"data": data})
