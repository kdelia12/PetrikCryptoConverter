import requests
import json

class CryptoConvertBotException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise CryptoConvertBotException('Quote and base must be different')

        try:
            quote_ticker = quote
        except KeyError:
            raise CryptoConvertBotException(f'Cannot process currency {quote}')

        try:
            base_ticker = base
        except KeyError:
            raise CryptoConvertBotException(f'Cannot process currency {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise CryptoConvertBotException(f'Cannot process amount {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[base_ticker] * amount

        return total_base

# End of file
