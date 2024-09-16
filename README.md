# akasha-py

## Introduction

akasha-py is an async API wrapper for [akasha.cv](https://akasha.cv/) written in Python.  
akasha.cv is a Genshin Impact leaderboard website.  
Developing something for Hoyoverse games? You might be interested in [other API wrappers](https://github.com/seriaati#api-wrappers) written by me.  
> Note: I am not the developer of akasha.cv.

## Important Notes

A couple things I want to address:  

- This wrapper is currently in-progress, some features may not work as expected, many features are also missing.
- The developer of akasha.cv mentioned to me that they change their API very frequently (and without notice), so this wrapper may break at any time.
- This wrapper was made because I wanted to integrate akasha into my [Discord bot](https://github.com/seriaati/hoyo-buddy), but I eventually stopped working on it. Therefore, this wrapper is not my current priority, but I will fix issues if you submit them.

## Installation

```bash
# poetry
poetry add akasha-py

# pip
pip install akasha-py
```

## Usage

Interact with the API using the `akasha.AkashaAPI` class.  
You can find all available methods that `AkashaAPI` provides in the [client.py](https://github.com/seriaati/akasha-py/blob/main/akasha/client.py) file.  
A quick example is provided below:

```py
import asyncio

import akasha


async def main() -> None:
    uid = 901211014
    async with akasha.AkashaAPI(akasha.Language.CHINESE_SIMPLIFIED) as api:
        # await api.refresh_user(uid)

        characters = await api.get_calculations_for_user(uid)
        for character in characters:
            calc = character.calculations[0]

            print(f"Character: {character.name}")
            print(f"Weapon: {calc.weapon.name}")
            print(f"Top {calc.top_percent:.2f}% ({calc.ranking}/{calc.out_of})")
            print(f"Damage: {round(calc.result)}")
            print()

            print("Leaderboard top 3:")
            async for board in api.get_leaderboards(calc.id, max_page=1, page_size=3):
                print(
                    f"{board.rank}. {board.owner.nickname} | Damage: {round(board.calculation.result)}"
                )
            print(f"Leadboard URL: https://akasha.cv/leaderboards/{calc.id}")

            print("=" * 50)


asyncio.run(main())
```

## Questions, Issues, Feedback, Contributions

Whether you want to make any bug reports, feature requests, or contribute to the wrapper, simply open an issue or pull request in this repository.  
If GitHub is not your type, you can find me on [Discord](https://discord.com/invite/b22kMKuwbS), my username is @seria_ati.
