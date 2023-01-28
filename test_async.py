import asyncio
import requests
from random import randint
from typing import AsyncIterable
from time import perf_counter

MAX_POKEMON = 898


def http_get_sync(url: str):  # move to a separate file
    response = requests.get(url)
    return response.json()


async def http_get(url: str):
    return await asyncio.to_thread(http_get_sync, url)


async def get_pokemon_name():
    pokemon_id = randint(1, MAX_POKEMON)
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    pokemon = await http_get(pokemon_url)
    return pokemon["name"]


async def get_next_pokemon(total: int) -> AsyncIterable[str]:
    for i in range(total):
        name = await get_pokemon_name()
        yield name


async def main():
    time_before = perf_counter()
    names = [name async for name in get_next_pokemon(20)]
    print(names)
    print(f"Время асинхронного вывода:{perf_counter() - time_before} \n")

    # лучше использовать метод gather, it's faster 12X
    time_before = perf_counter()
    result = await asyncio.gather(*[get_pokemon_name() for _ in range(20)])
    print(result)
    print(f"Время асинхронного вывода:{perf_counter() - time_before} \n")


# async def get_random_pokemon_name() -> str:
#     pokemon_id = randint(1, MAX_POKEMON)
#     pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
#     pokemon = await http_get(pokemon_url)
#     return str(pokemon["name"])
#
#
# async def next_pokemon(total: int) -> AsyncIterable[str]:
#     for _ in range(total):
#         name = await get_random_pokemon_name()
#         yield name
#
#
# async def main():
#     # retrieve the next 10 pokemon names
#     async for name in next_pokemon(10):
#         print(name)
#
#     # asynchronous list comprehensions
#     names = [name async for name in next_pokemon(10)]
#     print(names)


if __name__ == "__main__":
    asyncio.run(main())
