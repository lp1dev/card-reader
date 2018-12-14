#!/bin/env python
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.ATR import ATR
from smartcard.util import toHexString
from time import sleep

ATRS = {}

def     get_smartcards_list():
    global ATRS
    with open('./smartcard_list.txt') as f:
        lines = f.readlines()
        cursor = None
        for line in lines:
            if line.startswith("#"):
                continue
            elif line.startswith("3B"):
                cursor = line.replace('\n', '').replace('\t', '')
                ATRS[cursor] = ""
            elif cursor is not None:
                ATRS[cursor] += line

def     send(reader):
    response, sw1, sw2 = reader.transmit([0xFF, 0xCA, 0x00, 0x00, 0x00])
    print('Response :', response)
    print(sw1, sw2)
                
def	main():
    global ATRS
    get_smartcards_list()
    cardtype = AnyCardType()
    while True:
        cardrequest = CardRequest( timeout=120, cardType=cardtype )
        cardservice = cardrequest.waitforcard()
        cardservice.connection.connect()
        atrBytes = cardservice.connection.getATR()
        atr = ATR(atrBytes)
        print(atr)
        print('historical bytes: ', toHexString(atr.getHistoricalBytes()))
        print('checksum: ', "0x%X" % atr.getChecksum())
        print('checksum OK: ', atr.checksumOK)
        print('T0  supported: ', atr.isT0Supported())
        print('T1  supported: ', atr.isT1Supported())
        print('T15 supported: ', atr.isT15Supported())
        if (ATRS[toHexString(atrBytes)]):
            print(ATRS[toHexString(atrBytes)])
        print(cardservice.connection)
        send(cardservice.connection)
        sleep(5)
    return 0

if __name__ == '__main__':
  main()
