import urllib
import json


class ExchangeException(Exception):
    pass


class BaseCurrencyProvider(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def get_rate(self, currency_in, currency_out):
        raise NotImplementedError


class DummyCurrencyProvider(BaseCurrencyProvider):
    def __init__(self, exchange_rates=None, *args, **kwargs):
        super(DummyCurrencyProvider, self).__init__(*args, **kwargs)
        self.exchange_rates = exchange_rates or {
            ('eur', 'pln'): 4.24,
            ('pln', 'eur'): 0.25,
            ('usd', 'pln'): 3.8,
        }

    def get_rate(self, currency_in, currency_out):
        rate = self.exchange_rates.get((currency_in, currency_out))
        if not rate:
            raise ExchangeException('%s -> %s is not defined in exchange_rates ' % (currency_in, currency_out))
        return rate


class CurrencyProvider(BaseCurrencyProvider):
    url_template = url = "https://currency-api.appspot.com/api/{currency_in}/{currency_out}.json"

    def get_url(self, currency_in, currency_out):
        return self.url_template.format(currency_in=currency_in, currency_out=currency_out)

    def get_rate(self, currency_in, currency_out):
        connection = urllib.urlopen(self.get_url(currency_in, currency_out))
        result = connection.read()
        connection.close()

        result = json.loads(result)
        if not result.get('success'):
            raise ExchangeException(result.get('message'))
        return result['rate']


class CurrencyExchanger(object):
    def __init__(self, currency_provider_class=CurrencyProvider, *args, **kwargs):
        self.default_currency = kwargs.get('default_currency', )
        self.currency_provider_class = currency_provider_class
        self.currency_provider = self.currency_provider_class(exchange_rates=kwargs.get('exchange_rates', ))

    def exchange(self, *args):
        if self.default_currency:
            amount, currency_in = args
            currency_out = self.default_currency
        else:
            amount, currency_in, currency_out = args
        return amount * self.currency_provider.get_rate(currency_in, currency_out)
