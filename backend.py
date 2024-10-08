import os
import enchant
import requests
from typing import Optional

class Translator():
    request_header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    urban_dict_query = "http://api.urbandictionary.com/v0/define?term="
    openai_query = "https://api.openai.com/v1/chat/completions"
    
    def __init__(self, api_key, openai_model="gpt-4o"):
        self.openai_model = openai_model
        self.eng_dict = enchant.Dict("en_US")
        
        self.api_key = api_key
        
    def fetch_slang_def(self, *words, upvoted_req=200, downvoted_max=200, ratio_req=2.0, char_count_req=50) -> list:
        """Fetches the most commonly acceptable definition of a slang word by determining whether
    there are more than 100+ upvotes and the ratio of upvoted to downvoted is
    greater than or equal to 1.5 (customizable ratio and upvote requirement)."""
        slang_words = []
        for word in words:
            if self.eng_dict.check(word) is True: # if word is formal
                slang_words.append(None)
                continue
            
            defined_words = requests.get(Translator.urban_dict_query + word, headers=Translator.request_header).json()
            
            if defined_words["list"]:  # if any defined words exist in urban dict
                for word_entry in defined_words["list"]:  # go through all the word entries
                    upvoted = int(word_entry["thumbs_up"])
                    downvoted = int(word_entry["thumbs_down"])
                    
                    definition: str = word_entry['definition']
                    definition = definition.replace('[', '').replace(']', '') # remove possible hyperlinks denoted by brackets
                    
                    char_count = len(definition.replace(" ", ""))
                    
                    try:
                        # perchance thumbs down could be 0
                        vote_ratio = upvoted / downvoted
                        
                    except ZeroDivisionError:
                        vote_ratio = float(upvoted)
                        
                    if upvoted >= upvoted_req and downvoted <= downvoted_max and vote_ratio >= ratio_req and char_count <= char_count_req:
                        definition = definition.replace('(', '').replace(')', '')
                        definition = f"({word}: {definition})"
                        slang_words.append(definition)
                        break
                    
                    else:
                        # word definition does not meet standards
                        continue
            elif not defined_words["list"]:
                # word does not exist in urban
                slang_words.append(None)
            else:
                # search for next word if not all words found yet
                continue
            #idk how tf this works but it def detects all possible tokens
            continue
        
        return slang_words


    """
    User Prompt (as list): ["why", "you", "cappin"]
    UrbanDictionary Get Results: [None, None, "lying"]
    Expected Translation: ["why", "you", "lying"]
    """

    def __intercept_slang_def(self, orig_input: str, slang_term: str) -> Optional[str]:
        """Determines whether to add the slang definition in place of the user input
        or keep it as-is."""
        if slang_term is not None:
            return slang_term
        else:
            return orig_input
            
    def translate_to_language(self, user_input: str, target_language: str, initial_language='English') -> str:
        """Intercepts user input's slang with Urban Dictionary's definition and uses GPT 3.5's
        interpretation to gramatically fill out context within input (if applicable), before
        translating via Google Translate"""
        user_input_list = user_input.split()
        slang_terms = self.fetch_slang_def(*user_input_list)
        
        # TODO OPTIMIZE SOON
        replaced_user_input = list(map(self.__intercept_slang_def, user_input_list, slang_terms))

        if any(slang_terms): # if there is at least 1 value from urban dict
            # use openai's gpt to interpret into the correct language
            prompt = [
                {
                    "role": "system",
                    "content": f"You are working as a translation helper to help older generation speakers to understand modern English and its slang from newer generations. \
                    Your job is to translate {initial_language} content (possibly with slang) and convey it in a formal setting such that anyone could understand it."
                },
                {
                    "role": "system",
                    "content": f"You are given a piece of text in {initial_language} that may contain slang; you must convert this text formally into {target_language}. \
                    The slang will be in parentheses for you to identify them, listing the actual word that should be used in the text, followed by the definition of the slang. \
                    With this contextual evidence, rewrite the given piece of text, while preserving as much of the original sentence structure as possible, \
                    to write the piece of text formally."
                },
                {
                    "role": "user",
                    "content": " ".join(replaced_user_input)
                }
            ]   
            
            gpt_headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            gpt_data = {
                "model": self.openai_model,
                "messages": prompt
            }

            convert_query = requests.post(Translator.openai_query, headers=gpt_headers, json=gpt_data).json()

            print(convert_query)
            formal_translated = convert_query['choices'][0]['message']['content']
        
        else: 
            # no slang found
            formal_translated = user_input
            
        return formal_translated

    def translate_language_to_language(self, text: str, source_language: str, target_language: str) -> str:
        prompt = [
            {
                "role": "system",
                "content": f"Translate the given text from {source_language} into {target_language}, taking into account \
                any slang, idioms, and/or subtext. Write the text formally, containing the original structure as much as possible."
            },
            {
                "role": "user",
                "content" : text
            }
        ]
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": self.openai_model,
            "messages" : prompt
        }
        response = requests.post(self.openai_query, json=data, headers=headers).json()
        translated_text = response['choices'][0]['message']['content']
        return translated_text
    
    
if __name__ == '__main__':
    openai_key = os.getenv("OPENAI_API_KEY")
    x = Translator(openai_key)
    while True:
        try:
            translation_direction = int(input("Enter translation direction (1: Slang to Language, 2: Language to Language): "))
            match translation_direction:
                case 1:
                    slang_term = input("Enter a slang sentence (in English): ")
                    target_language = input("Enter target language (e.g., Spanish): ")
                    translated_text = x.translate_to_language(slang_term, target_language)
                    print(f"Translated slang sentence: {translated_text}")
                    break
                case 2:
                    text = input(f"Enter desired text to translate: ")
                    source_language = input("Enter source language (e.g., 'en' for English): ")
                    target_language = input("Enter target language (e.g., 'es' for Spanish): ")
                    translated_language = x.translate_language_to_language(text, source_language, target_language)
                    print(f"Translated text to new language: {translated_language}")
                    break
                case _:
                    print("Invalid translation direction.")
                    continue
        except ValueError:
            print("Invalid translation direction.")
            continue