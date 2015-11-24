class ExchangeException(Exception):
    pass


class CurrencyExchanger(object):
    def __init__(self, *args, **kwargs):
        self.exchange_rates = kwargs.get('exchange_rates', )
        self.default_currency = kwargs.get('default_currency', )

    def get_rate(self, currency_in, currency_out):
        rate = self.exchange_rates.get((currency_in, currency_out))
        if not rate:
            raise ExchangeException('%s -> %s is not defined in exchange_rates ' % (currency_in, currency_out))
        return rate

    def exchange(self, *args):
        if self.default_currency:
            amount, currency_in = args
            currency_out = self.default_currency
        else:
            amount, currency_in, currency_out = args
        return amount * self.get_rate(currency_in, currency_out)
