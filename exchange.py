class ExchangeException(Exception):
    pass


class BaseCurrencyProvider(object):
    def get_rate(self, currency_in, currency_out):
        raise NotImplementedError


class DummyCurrencyProvider(BaseCurrencyProvider):
    def __init__(self, exchange_rates=None):
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
    pass


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
