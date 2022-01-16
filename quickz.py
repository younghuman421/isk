import websockets
import asyncio
import json
import names
from colorama import Fore, init

class Quickz:
    def __init__(self):
        pass

    async def play(self, game_pin, bot_name):
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
    
    async def flood(self, game_pin):
        bot_name = names.get_first_name()

        async with websockets.connect(f"wss://quickz.org/api/game?pin={game_pin}&name={bot_name}&token=false") as ws:
            message = await ws.recv()

            if message == '{"type":"join","ok":true,"late":false}': print(Fore.GREEN + f"[SOCKET] Joined game with name {bot_name}")
