import websockets
import asyncio
import json
import names
from colorama import Fore, init

init()

game_pin = int(input('Enter Game Pin: '))
bot_name = input('Enter Bot Name: ')


async def quickz():
    async with websockets.connect(f"wss://quickz.org/api/game?pin={game_pin}&name={bot_name}&token=false") as ws:
        while True:
            message = await ws.recv()
            msg = json.loads(message)

            if message == '{"ok":false,"error":"Invalid pin"}':
                print(Fore.RED + '[SOCKET] No game found.')
                break
            if message == '{"type":"join","ok":true,"late":false}':
                print(Fore.GREEN + f"[SOCKET] Joined game with name {bot_name}")
            if message == '{"type":"begin"}':
                print(Fore.CYAN + '[SOCKET] Game starting')
            if message == '{"type":"kick"}':
                print(Fore.RED + f"[SOCKET] {bot_name} was kicked!")
                break
            if msg['type'] == 'question':
                answer = msg['question']['answers'][0]['text']

                await ws.send(json.dumps({"type": "answer", "answer": answer}))

                print(Fore.BLUE + 'Question answered.')
            if msg['type'] == 'end':
                print(Fore.MAGENTA + '[SOCKET] Game ended')
                break


asyncio.get_event_loop().run_until_complete(quickz())
