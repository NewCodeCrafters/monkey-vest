import requests
from decimal import Decimal

# API details
API_URL = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/convert"
API_HEADERS = {
    "x-rapidapi-key": "0d68d5c233msh6df685900d19a54p12a234jsn7cdaf6f6616f",
    "x-rapidapi-host": "currency-conversion-and-exchange-rates.p.rapidapi.com"
}

# Static fallback rates
STATIC_RATES = {
    "USD_NGN": Decimal(1680),  # Example rate: 1 USD = 1680 NGN
    "NGN_USD": Decimal(1 / 1680)  # Example rate: 1 NGN = 0.000595 USD
}


def convert_ngn_to_usd_static(amount):
    """Convert NGN to USD using a static rate."""
    return Decimal(amount) * STATIC_RATES["NGN_USD"]


def convert_usd_to_ngn_static(amount):
    """Convert USD to NGN using a static rate."""
    return Decimal(amount) * STATIC_RATES["USD_NGN"]


def fetch_dynamic_conversion_rate(source, destination):
    """Fetch the dynamic conversion rate using the API."""
    querystring = {"from": source.upper(), "to": destination.upper(), "amount": "1"}
    response = requests.get(API_URL, headers=API_HEADERS, params=querystring)
    if response.status_code == 200:
        rate = response.json().get("info", {}).get("rate")
        if rate:
            return float(rate)
        else:
            raise ValueError("Invalid response format: 'rate' not found.")
    else:
        raise ConnectionError(f"API request failed with status code {response.status_code}")


def currency_converter(source, destination, amount, use_dynamic_rate=True):
    """
    Convert currency from source to destination.

    Args:
        source (str): Source currency code (e.g., "USD").
        destination (str): Destination currency code (e.g., "NGN").
        amount (float): Amount to convert.
        use_dynamic_rate (bool): Use API for dynamic rates if True, fallback to static rates otherwise.

    Returns:
        float: Converted amount.
    """
    source, destination = source.upper(), destination.upper()

    if use_dynamic_rate:
        try:
            rate = fetch_dynamic_conversion_rate(source, destination)
        except (ConnectionError, ValueError):
            print("Failed to fetch dynamic rate. Falling back to static rate.")
            rate = STATIC_RATES.get(f"{source}_{destination}")
    else:
        rate = STATIC_RATES.get(f"{source}_{destination}")

    if not rate:
        raise ValueError(f"No conversion rate available for {source} to {destination}.")

    return float(amount) * rate


# Example Usage
if __name__ == "__main__":
    # Static rate example
    print("Static Conversion: 100 NGN to USD =", convert_ngn_to_usd_static(100))
    print("Static Conversion: 100 USD to NGN =", convert_usd_to_ngn_static(100))

    # Dynamic conversion example
    try:
        converted_amount = currency_converter("USD", "NGN", 100, use_dynamic_rate=True)
        print("Dynamic Conversion: 100 USD to NGN =", converted_amount)
    except Exception as e:
        print("Error during dynamic conversion:", e)
