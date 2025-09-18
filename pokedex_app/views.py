from django.shortcuts import render
import json
import urllib.request
# Create your views here.
def index(request):
    if request.method == "POST":
        pokemon = request.POST.get('pokemon').lower()
        pokemon = pokemon.replace(" ", "%20")
        url_pokeapi = urllib.request.Request(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        url_pokeapi.add_header("User-Agent", "Mozilla/5.0")

        source = urllib.request.urlopen(url_pokeapi).read()
        list_data = json.loads(source)

        data = {
            "number": str(list_data["id"]),
            "name": str(list_data["name"]).capitalize(),
            "height": str(list_data["height"]) + " dm",
            "weight": str(list_data["weight"]) + " hg",
            "sprite": str(list_data["sprites"]["front_default"]),
        }

    else:
        data = {}
    return render(request, "index.html", {"data": data})