import sys
import time
from cryptopia_api import Api
import config


class PumpDumpCyriptopia:
    API = ()

    def __init__(self):
        # setup api
        KEY, SECRET = self.get_secret()
        self.API = Api(KEY, SECRET)

    def get_secret(self):
        return str(config.api_key), str(config.secret)

    def pumpDump(self, SYMBOL, percentageOfBtc=100, profitPercentage=100, buyingPercentage=60):
        # do before entering coin to save the API call during the pump
        BALANCE_BTC, ERROR = self.API.get_balance('BTC')
        if ERROR is not None:
            print ERROR
        PUMP_BALANCE = BALANCE_BTC["Available"] * (percentageOfBtc / 100)
        COIN_PRICE, ERROR = self.API.get_market(SYMBOL + "_BTC")
        if ERROR is not None:
            print ERROR

        ASK_PRICE = COIN_PRICE['AskPrice']

        COIN_SUMMARY, ERROR = self.API.get_market(SYMBOL + "_BTC")
        if ERROR is not None:
            print ERROR

        LAST_PRICE = COIN_SUMMARY['LastPrice']
        CLOSE_PRICE = COIN_SUMMARY['Close']

        ASK_BUY = ASK_PRICE + (buyingPercentage / 100 * ASK_PRICE)
        ASK_SELL = ASK_PRICE + (profitPercentage / 100 * ASK_PRICE)

        # calculates the number of PUMP_COIN(s) to buy, taking into
        # consideration Cryptopia's 0.20% fee.
        c_fee = 0.00201
        cryptoipa_fee = PUMP_BALANCE * c_fee
        NUM_COINS = float((PUMP_BALANCE - cryptoipa_fee)) / ASK_BUY

        if LAST_PRICE > CLOSE_PRICE + 0.20 * CLOSE_PRICE:
            print '\nYou joined too late or this was pre-pumped! \
                       Close Price : {:.8f} . Last Price : {:.8f}'.format(CLOSE_PRICE, LAST_PRICE)
            return

        BUY_PRICE = ASK_BUY * NUM_COINS
        SELL_PRICE = ASK_SELL * NUM_COINS
        PROFIT = SELL_PRICE - BUY_PRICE

        print '\n[+] Buy order placed for {:.8f} {} coins at {:.8f} BTC \
                  each for a total of {} BTC'.format(NUM_COINS, SYMBOL, ASK_BUY, BUY_PRICE)

        # TRADE, ERROR = self.API.submit_trade(SYMBOL + '/BTC', 'Buy', ASK_BUY, NUM_COINS)
        if ERROR is not None:
            print ERROR

        print '\n[+] Placing sell order at {:.8f} (+{}%)...'.format(ASK_SELL, profitPercentage)

        COINS_OWNED, ERROR = self.API.get_balance(SYMBOL)
        if ERROR is not None:
            print ERROR

        COINS_OWNED = COINS_OWNED['Available']
        while COINS_OWNED == 0:
            time.sleep(0.1)
            COINS_OWNED, ERROR = self.API.get_balance(SYMBOL)
            if ERROR is not None:
                print ERROR
                break
            COINS_OWNED = COINS_OWNED['Available']

        TRADE, ERROR = self.API.submit_trade(SYMBOL + '/BTC', 'Sell', ASK_SELL, NUM_COINS)
        if ERROR is not None:
            print ERROR

        print '\n[+] Sell order placed of {:.8f} {} coins at {:.8f} BTC each for \
                  a total of {:.8f} BTC'.format(NUM_COINS, SYMBOL, ASK_SELL, SELL_PRICE)

        print '[*] PROFIT if sell order fills: {:.8f} BTC'.format(PROFIT)
