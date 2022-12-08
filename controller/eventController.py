import asyncio
import requests
import time
import json
from .peers import marketplaces as mps

marketplaces = mps.marketplaces

def orderEvent(items, clock, id):
    res = []
    for i in range(len(marketplaces)):
        if ((marketplaces[i]['porta']-3030)!=id):
            url = f"http://localhost:{marketplaces[i]['porta']}/compra"
            r = requests.post(url,json=json.dumps({"clock":clock,"items":items}))
            print('res text')
            print(r.text)
            res.append(json.loads(r.text))  # res contém as n respostas

    # a função assincrona deve:
        # enviar mensagens (o relogio é atualizado apenas no server.)
        # retornar apos resposta de todos os peers

    time.sleep(5)
    return json.dumps({"clock":clock,"res":res})

def addEvent(produto):
    # enviar post para os outros servidores com o produto novo
    res = []
    for i in range(len(marketplaces)):
        if ((marketplaces[i]['porta']-3030)!=id):
            url = f"http://localhost:{marketplaces[i]['porta']}/adicionar"
            r = requests.post(url,json=json.dumps({"produto":produto}))
            print('res text')
            print(r.text)
            res.append(json.loads(r.text))  # res contém as n respostas
        
    return json.dumps({'res':res})