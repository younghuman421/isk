from quickz import Quickz
import asyncio

game_pin = int(input('Enter Game Pin: '))

async def flood_game():
    client = Quickz()
    
    while True: # a while true is done because the maximum amount of players that can join a game is 4 (while true will override that), because of the poor servers quickz has. 
        await client.flood(game_pin)


asyncio.get_event_loop().run_until_complete(flood_game())
