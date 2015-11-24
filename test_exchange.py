import pytest
import mock
from exchange import CurrencyExchanger, ExchangeException, DummyCurrencyProvider, CurrencyProvider

exchange_rates = {
    ('eur', 'pln'): 4.24,
    ('pln', 'eur'): 0.25,
    ('usd', 'pln'): 3.8,
}


def test_euro_to_pln_with_default_dummy_backend():
    e = CurrencyExchanger(currency_provider_class=DummyCurrencyProvider)
    assert e.exchange(1, 'eur', 'pln') == 4.24
    assert e.exchange(2, 'eur', 'pln') == 8.48
    assert e.exchange(1, 'pln', 'eur') == 0.25


def test_euro_to_pln():
    e = CurrencyExchanger(exchange_rates=exchange_rates, currency_provider_class=DummyCurrencyProvider)
    assert e.exchange(1, 'eur', 'pln') == 4.24
    assert e.exchange(2, 'eur', 'pln') == 8.48
    assert e.exchange(1, 'pln', 'eur') == 0.25


def test_euro_to_pln_with_default_pln():
    e = CurrencyExchanger(exchange_rates=exchange_rates, default_currency='pln',
                          currency_provider_class=DummyCurrencyProvider)
    assert e.exchange(1, 'eur') == 4.24
    assert e.exchange(2, 'eur') == 8.48


def test_exchanger_with_not_existing_data():
    e = CurrencyExchanger(exchange_rates=exchange_rates, currency_provider_class=DummyCurrencyProvider)
    assert e.exchange(1, 'usd', 'pln') == 3.8
    with pytest.raises(ExchangeException):
        assert e.exchange(1, 'pln', 'usd') == 4.24


def test_with_real_backend():
    e = CurrencyExchanger(currency_provider_class=CurrencyProvider)
    print '>>>>>>>', e.exchange(1, 'eur', 'pln')
