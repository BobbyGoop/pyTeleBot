import json
from difflib import get_close_matches


data = json.load(open("resources/dictionary.json"))

def retrive_definition(word):

    word = word.lower()
    if word in data:
        return data[word]
    elif word.title() in data:
        return data[word.title()]
    elif word.upper() in data:
        return data[word.upper()]
    else:
        return word


def searching():
    # Input from user
    word_user = input("Enter a word: ")

    # Retrive the definition using function and print the result
    output = retrive_definition(word_user)
    if output != word_user:
        if type(output) == list:
            for item in output:
                print("-", item)
    else:
        searching_matches(output)


def searching_matches(output):
    if len(get_close_matches(output, data.keys())) != 0:
        print("Возможно вы имели ввиду %s? (Да или Нет):" % get_close_matches(output, data.keys(), cutoff=0.8)[0])
        action = str(input())
        # -- If the answers is yes, retrive definition of suggested word
        if (action.lower == "да"):
            print(data[get_close_matches(output, data.keys())[0]])
        elif (action.lower == "нет"):
            print("Тогда такого слова не существует")
    else:
        print(" такого слова не существует")

if __name__ == '__main__':
    while True:
        searching()
