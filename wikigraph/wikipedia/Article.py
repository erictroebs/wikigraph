import logging
from collections import OrderedDict
from os import path
from re import findall, search
from urllib.parse import unquote

from requests import get as http_get


class Article:
    """
    This class represents a Wikipedia article which is identified by it's
    unique name. Further allows parsing the corresponding source code to
    extract several features like other linked articles.
    """

    def __init__(self, identifier, language='en', cache_directory=None):
        """
        :param identifier: unique identifier (the name after /wiki/)
        :param language: article language ('en', 'de', etc)
        :param cache_directory: directory to cache received articles in
        """
        # set properties
        self.identifier = identifier.strip()
        self.language = language
        self.cache_directory = cache_directory

    @staticmethod
    def from_url(url, cache_directory=None):
        """
        :param url: url to Wikipedia article
        :param cache_directory: directory to cache received articles in
        :return:
        """
        result = search(r'^https?://([a-z]+)\.wikipedia\.org/wiki/(.*?)$', url)
        if not result:
            raise ValueError

        identifier = result.group(2)
        language = result.group(1)

        return Article(identifier, language, cache_directory=cache_directory)

    def __str__(self):
        return f'https://{self.language}.wikipedia.org/wiki/{self.identifier}'

    @property
    def unescaped_identifier(self):
        return unquote(self.identifier).replace('_', ' ')

    def __get(self):
        # Article identifiers can contain slashes which must not be interpreted
        # as directory delimiters at any file system operation.
        # https://de.wikipedia.org/wiki/Bob_Marley/Auszeichnungen_f%C3%BCr_Musikverk%C3%A4ufe
        safe_identifier = self.identifier.replace('/', '_')

        if self.cache_directory is None:
            cache_file = None
        else:
            cache_file = path.join(self.cache_directory, safe_identifier + '.html')

        text = ''

        # load cached text if file exists
        if cache_file is not None and path.exists(cache_file):
            logging.info(self.__str__() + ' (from cache)')
            with open(cache_file, 'r', encoding='utf-8') as file:
                text = file.read()

        # If text variable is empty either the cache file did not exist or it
        # did not contain any data for whatever reason.
        # In this case we load the data via http and save it to the cache file.
        if text.strip() == '':
            logging.info(self.__str__())
            text = http_get(self.__str__()).text

            if cache_file is not None:
                with open(cache_file, 'w', encoding='utf-8') as file:
                    file.write(text)

        return text

    def linked_articles(self):
        """
        parse article text and extract all linked Wikipedia article identifiers

        :return: list of identifiers
        """
        # find all references using regular expressions
        matches = findall(r'href="/wiki/([^:]*?)"', self.__get())

        # remove anchor
        matches = map(lambda m: m.split('#')[0], matches)

        # remove duplicates
        matches = OrderedDict.fromkeys(matches)

        # filter links to the article itself
        matches = filter(lambda m: m != self.identifier, matches)

        # map to Article list
        return list(map(
            lambda m: Article(m, language=self.language, cache_directory=self.cache_directory),
            matches
        ))
