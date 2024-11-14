import requests

url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/convert"

# querystring = {"from":"USD","to":"NGN","amount":"1"}

# headers = {
# 	"x-rapidapi-key": "0d68d5c233msh6df685900d19a54p12a234jsn7cdaf6f6616f",
# 	"x-rapidapi-host": "currency-conversion-and-exchange-rates.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

def convert_ngn_to_usd_rate(source, amount):
    rate = float(amount)/1680
    return rate

def convert_usd_to_ngn_rate(source, amount):
    rate = float(amount)*1680
    return rate

def currency_converter(source, destination, amount):
    querystring = {}
    querystring['from'] = source.upper()
    querystring["to"] = destination.upper()
    querystring['amount'] = 1
    headers = {
        "x-rapidapi-key": "0d68d5c233msh6df685900d19a54p12a234jsn7cdaf6f6616f",
        "x-rapidapi-host": "currency-conversion-and-exchange-rates.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    response_info = response.json().get("info").get('rate')
    return response_info

