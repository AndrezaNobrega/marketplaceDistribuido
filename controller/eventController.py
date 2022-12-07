import asyncio
import requests
import time
import json
from .peers import marketplaces as mps

marketplaces = mps.marketplaces

def orderEvent(items, clock, id):
    clock[id] += 1
    res = []
    for i in range(len(marketplaces)):
        if ((marketplaces[i]['porta']-3030)!=id):
            url = f"http://localhost:{marketplaces[i]['porta']}/compra"
            PARAMS = {'query':items}
            r = requests.get(url, PARAMS)
            res.append(r)

    # a função assincrona deve:
        # Atualizar relogio
        # enviar mensagens
        # retornar apos resposta de todos os peers

    print('orderEvent')
    time.sleep(5)
    return res