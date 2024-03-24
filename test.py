with open('supported_langs.txt') as newin:
    languages = sorted(newin.read().splitlines())

with open('langs.txt', "w") as newout:
    for line in languages:
        print(line, file=newout)