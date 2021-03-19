import asyncio
from typing import List, Optional
from collections import Counter

import aiohttp
from bs4 import BeautifulSoup


base_page_url = 'https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B' \
                '0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%' \
                'B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D' \
                '0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'


async def find_last_occasion(letter: str, array: List) -> int:
    """
    Given a list of elements, finds position of the last instance of
    letter, assuming that there is such N that array[n] = letter
    for n in [0, N], and array[n] != letter for n > N.
    Assumes that 'Ё' is the same letter as 'Е'
    """
    low = 0
    high = len(array)
    if high == 0 or array[low] != letter or array[high-1] == letter:
        return -1
    while low + 1 < high:
        mid = (low+high) // 2
        if array[mid] == letter or (letter == 'Е' and array[mid] == 'Ё'):
            low = mid
        else:
            high = mid
    return low


async def process_letter(letter: str, letter_counter: Counter) -> None:
    """
    Given letter, update letter_counter accordingly
    """
    print(f'Started processing letter {letter}...')
    url = base_page_url + '&from=' + letter
    while url is not None:
        url = await process_page(url, letter, letter_counter)
    print(f'Done processing letter {letter}.')


async def process_page(url: str, letter: str, letter_counter: Counter) -> Optional[str]:
    """
    Find number of instances, beginning with the letter
    on the given url, and update letter_counter
    accordingly
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as page:
            text = await page.read()
            soup = BeautifulSoup(text, 'html.parser')
            li = soup.find('div', attrs={'class': 'mw-category-group'})
            if li is None:
                return None
            first_letters = [el.text[0] for el in li.find_all('li')]
            if first_letters[0] != letter:
                letter_counter.setdefault(letter, 0)
                return None
            if first_letters[-1] != letter:
                letter_counter[letter] += await find_last_occasion(
                    letter, first_letters) + 1
                return None
            letter_counter[letter] += len(first_letters)
            link_element = soup.find('a', string='Следующая страница')
            if link_element is None:
                return None
            url = 'https://ru.wikipedia.org/' + link_element.attrs['href']
    return url


def number_of_animals() -> str:
    loop = asyncio.get_event_loop()
    a = ord('А')
    letters = ''.join([chr(i) for i in range(a, a+32)])
    # a = ord('A')
    # letters += ''.join([chr(i) for i in range(a, a+26)])
    letter_counter = Counter()
    coroutines = [process_letter(letter, letter_counter)
                  for letter in letters]
    loop.run_until_complete(asyncio.gather(*coroutines))

    return '\n'.join(f'{letter}: {val}'
                     for letter, val in sorted(letter_counter.items()))


if __name__ == '__main__':
    res = number_of_animals()
    print(res)
