"""Reverso Context (context.reverso.net) API for Python"""

import asyncio
import json
from typing import Iterator

import aiohttp
from bs4 import BeautifulSoup

from .const import HEADERS, Translation, WordUsageExample

__all__ = ["ReversoContextAPI"]


class ReversoContextAPI(object):
    """Class for Reverso Context API (https://voice.reverso.net/)"""

    def __init__(
        self,
        source_texts: list = ["пример"],
        source_lang: str = "de",
        target_lang: str = "en",
        examples_count: int = 3,
        trans_count: int = 3,
    ):
        self.examples_count = examples_count
        self.trans_count = trans_count

        self.source_texts = source_texts
        self.source_lang = source_lang
        self.target_lang = target_lang

    def __get_translations(self, response: dict, word: str) -> Translation:
        """Returns Translation namedtuple"""
        trans_ls = []
        for index, item in enumerate(response["dictionary_entry_list"]):
            trans_ls.append(item["term"])

            if index == self.trans_count - 1:
                break

        return Translation(source_word=word, translation=trans_ls)

    def __get_examples(self, response: dict) -> list[WordUsageExample]:
        """Returns list of WordUsageExample"""
        examples = []
        for index, ex in enumerate(response["list"]):
            source = BeautifulSoup(ex["s_text"], features="lxml")
            target = BeautifulSoup(ex["t_text"], features="lxml")
            example = WordUsageExample(source_text=source.text, target_text=target.text)
            examples.append(example)
            if index == self.examples_count - 1:
                break

        return examples

    async def __do_post(
        self, session: aiohttp.ClientSession, url: str, word: list[str]
    ) -> tuple[Translation, list[WordUsageExample]]:
        post_data = json.dumps(
            {
                "source_text": word,
                "target_text": "",
                "source_lang": self.source_lang,
                "target_lang": self.target_lang,
            }
        )
        async with session.post(url=url, data=post_data) as response:
            response = await response.json()

            translations = self.__get_translations(response, word)
            examples = self.__get_examples(response)

            return translations, examples

    async def __make_words(self) -> Iterator[str]:
        for word in self.source_texts:
            yield word

    async def __async_post_request(self) -> list[tuple]:
        """Performing asynchronous post request to given url"""

        url = "https://context.reverso.net/bst-query-service"
        async with aiohttp.ClientSession(
            headers=HEADERS, connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as session:
            post_tasks = []
            async for w in self.__make_words():
                post_tasks.append(self.__do_post(session, url, w))

            res = await asyncio.gather(*post_tasks)

            return res

    def get_data(self) -> list[tuple[Translation, list[WordUsageExample]]]:
        """Runs async post request and return response"""
        response = asyncio.run(self.__async_post_request())

        return response
