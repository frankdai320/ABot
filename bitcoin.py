import json
import time

import requests

STATS_URL = 'https://api.blockchain.info/stats'
SATOSHI = 100000000


class Update:
    def __init__(self, url):
        self.url = url
        self.updated = 0
        self.data = None

    def update(self):
        try:
            response = requests.get(self.url).content.decode()
        except requests.RequestException:
            return
        try:
            self.data = json.loads(response)
        except ValueError:
            return
        self.updated = time.time()

    def get_data(self):
        """Get the data of this update. May return None."""
        if self.data is None or time.time() - self.updated > 60 * 10:
            self.update()
        return self.data


update = Update(STATS_URL)


def btc_message():
    data = update.get_data()
    if data is None:
        return 'Could not get Bitcoin data.'
    price = data.get('market_price_usd', -1)
    fees = data.get('total_fees_btc', 0) / SATOSHI
    fees_usd = fees * price
    transactions = data.get('n_tx', 0)
    if transactions == 0:
        transactions = 1  # avoid zero division
    avg_fee = fees_usd / transactions

    return 'BTC at ${:,.2f} with avg. fees per transaction at ${:,.2f}.'.format(price, avg_fee)