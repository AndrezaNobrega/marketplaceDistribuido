import asyncio
import time
from .peers import marketplaces


async def orderEvent(items):
    # await res from all 
    # a função assincrona deve:
        # Atualizar relogio
        # enviar mensagens
        # retornar apos resposta de todos os peers

    print('orderEvent')
    time.sleep(5)
    return 'OK'