Warsztaty PYAGH z testowania
============================

Start
=====

Na początek stworzymy wirtualne środowisko pythona.

    virtualenv venv

Następnie je aktywujemy:

    source venv/bin/activate

Oraz zainstalujemy zależności:

    pip install pip --upgrade
    pip install -r requirements.txt


Co chcemy zaimplementować?
==========================

Biblioteke kantora walut.

Jak go chcemy używać?
=====================

    from exchange import CurrencyExchanger

    e = CurrencyExchanger()
    e.exchange(1, 'eur', 'pln')
    >>> 4.24
    e.exchange(1, 'eur', 'usd')
    >>> 1.064

Uruchomienie testów
===================

    py.test

Pobieranie aktualnych kursów przez API
======================================

Użyjemy biblioteki requests

