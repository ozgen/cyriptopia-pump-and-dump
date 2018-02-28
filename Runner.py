import  CyriptopiaPumpAndDump
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', type=str, help='Market Symbol (Ex: XVGBTC - XVGETH)', required=True)

    coin_name = parser.parse_args()
    CyriptopiaPumpAndDump.PumpDumpCyriptopia().pumpDump(str(coin_name.symbol).upper())

