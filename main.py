import requests
from bs4 import BeautifulSoup
from requests import Response
from typing import Tuple

LANGUAGES = {1: 'Arabic',
             2: 'German',
             3: 'English',
             4: 'Spanish',
             5: 'French',
             6: 'Hebrew',
             7: 'Japanese',
             8: 'Dutch',
             9: 'Polish',
             10: 'Portuguese',
             11: 'Romanian',
             12: 'Russian',
             13: 'Turkish'}


def get_link(translate_from: str, translate_to: str, word_to_translate: str) -> str:
    return f'https://context.reverso.net/translation/{LANGUAGES[translate_from].lower()}-{LANGUAGES[translate_to].lower()}/{word_to_translate}'


def get_request(url: str) -> Response:
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    return r


def scrap_website(response: Response) -> Tuple[list, list]:
    soup = BeautifulSoup(response.content, 'html.parser')
    translation_content = soup.find('div', id='translations-content')
    translation_text = translation_content.text.split("\n")
    translation_text = [line.strip() for line in translation_text if line.strip() != ""]
    examples = [example.text.strip() for example in soup.find_all('div', {'class': ['src', 'trg']}) if example.text.strip()]
    return translation_text, examples


def main() -> None:
    print("Hello, you're welcome to the translator. Translator supports: ")
    for i, language in LANGUAGES.items():
        print(f'{i}. {language}')

    language_info_from = int(input("Type the number of your language: "))
    language_info_to = int(input("Type the number of a language you want to translate to or '0' to translate to all languages:"))
    word_to_translate = input('Type the word you want to translate: ')

    if language_info_to == 0:
        open(f'{word_to_translate}.txt', 'w').close()
        for language in range(1, len(LANGUAGES) + 1):
            if language == language_info_from:
                continue
            else:
                translate(language_info_from, language, word_to_translate)
    else:
        translate(language_info_from, language_info_to, word_to_translate)


def translate(language_info_from: int, language_info_to: int, word_to_translate: str, n_of_examples: int = 1) -> None:
    url = get_link(language_info_from, language_info_to, word_to_translate)
    r = get_request(url)
    translation, examples = scrap_website(r)
    show_results(language_info_to, translation, examples, word_to_translate, n_of_examples)


def show_results(language: str, translation: list, examples: list, word: str, n_of_examples: int = 5) -> None:
    with open(f"{word}.txt", "a+", encoding='utf-8') as f:
        f.write(f"{LANGUAGES[language]} Translations: \n")
        for index in range(n_of_examples):
            f.write(f"{translation[index]}\n")
        f.write("\n")
        f.write(f"{LANGUAGES[language]} Examples: \n")
        for index in range(0, n_of_examples * 2, 2):
            f.write(f'{examples[index]}\n')
            f.write(f'{examples[index + 1]}\n')
        f.write("\n")

    print(f"{LANGUAGES[language]} Translations: ")
    for index in range(n_of_examples):
        print(translation[index])
    print("")
    print(f"{LANGUAGES[language]} Examples: ")
    for index in range(0, n_of_examples * 2, 2):
        print(examples[index])
        print(f'{examples[index + 1]}\n')


if __name__ == "__main__":
    main()
