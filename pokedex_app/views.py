from django.shortcuts import render
import json
import urllib.request
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

            traducciones = {
                "number": "Número",
                "name": "Nombre",
                "height": "Altura",
                "weight": "Peso",
                "types": "Tipo",
                "Fire": "Fuego",
                "Water": "Agua",
                "Grass": "Planta",
                "Electric": "Eléctrico",
                "Psychic": "Psíquico",
                "Ice": "Hielo",
                "Dragon": "Dragón",
                "Dark": "Siniestro",
                "Fairy": "Hada",
                "Normal": "Normal",
                "Fighting": "Lucha",
                "Flying": "Volador",
                "Poison": "Veneno",
                "Ground": "Tierra",
                "Rock": "Roca",
                "Bug": "Bicho",
                "Ghost": "Fantasma",
                "Steel": "Acero"
            }

            data = {
                "number": str(list_data["id"]),
                "name": str(list_data["name"]).capitalize(),
                "height": str(list_data["height"]),
                "weight": str(list_data["weight"]),
                "types": [str(i["type"]["name"]).capitalize() for i in list_data["types"]],
                "sprite": str(list_data["sprites"]["front_default"]),
            }

            data_traducido = {}
            for clave, valor in data.items():
                clave_traducida = traducciones.get(clave, clave)
                if isinstance(valor, list):
                    valor_traducido = [traducciones.get(v, v) for v in valor]
                else:
                    valor_traducido = traducciones.get(valor, valor)
                data_traducido[clave_traducida] = valor_traducido

            return render(request, "index.html", {"data": data_traducido})

        else:
            data = {}
            return render(request, "index.html", {"data": data})

    except HTTPError:
        data = {"error": "Pokémon no encontrado, intenta de nuevo"}
        return render(request, "index.html", {"data": data})
