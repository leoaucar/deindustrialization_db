import requests
import json

r = requests.get("https://servicodados.ibge.gov.br/api/v3/agregados/1705/periodos/-6/variaveis?localidades=BR")
response = json.loads(r.text)

print(response)