"""
"""
import click
import json
import os, os.path
import requests


jazz_musicians = [title.strip() for title in """
Art_Pepper
Bill_Evans
Bud_Powell
Cannonball_Adderley
Charlie_Parker
Eddie_Gómez
Hank_Mobley
Herbie_Hancock
Jim_Hall_(musician)
John_Coltrane
Kenny_Burrell
McCoy_Tyner
Miles_Davis
Milt_Jackson
Paul_Chambers
Paul_Motian
Philly_Joe_Jones
Ron_Carter
Scott_LaFaro
Sonny_Clark
Sonny_Rollins
Thelonious_Monk
Wes_Montgomery
""".split()]

scientists = [title.strip() for title in """
Ada_Lovelace
Alan_Turing
Alonzo_Church
Albert_Einstein
Barbara_McClintock
Carl_Friedrich_Gauss
Charles_Babbage
Charles_Darwin
Claude_Shannon
David_Hilbert
Dmitri_Mendeleev
Donald_Knuth
Enrico_Fermi
Francis_Crick
Frederick_Sanger
Gregor_Mendel
Henri_Poincaré
Isaac_Newton
James_Clerk_Maxwell
James_Watson
John_von_Neumann
Jonas_Salk
Kurt_Gödel
Leonhard_Euler
Linus_Pauling
Louis_Pasteur
Marie_Curie
Max_Planck
Michael_Faraday
Niels_Bohr
Noam_Chomsky
Paul_Dirac
Pierre_de_Fermat
Richard_Feynman
Rosalind_Franklin
Terence_Tao
Thomas_Bayes
""".split()]

writers =  [title.strip() for title in """
Albert_Camus
C._S._Lewis
Charles_Dickens
Cormac_McCarthy
Dave_Eggers
Don_DeLillo
Douglas_Adams
E._B._White
Edgar_Allan_Poe
Ernest_Hemingway
F._Scott_Fitzgerald
Frank_Herbert
Franz_Kafka
George_Orwell
Haruki_Murakami
Iain_Banks
Isaac_Asimov
J._D._Salinger
James_Joyce
Jane_Austen
Jennifer_Egan
Jorge_Luis_Borges
Kurt_Vonnegut
Margaret_Atwood
Mark_Twain
Neal_Stephenson
Philip_K._Dick
Ray_Bradbury
William_Gibson
Ursula_K._Le_Guin
""".split()]

# see: how to get plain text out of wikipedia
# - prop=extracts makes us use the TextExtracts extension
# - exintro limits the response to content before the first section heading
# - explaintext makes the extract in the response be plain text instead of HTML

url_template = 'https://en.wikipedia.org/w/api.php?' + \
               '&'.join([
                    'action=query',
                    'format=json',
                    'titles={title}',
                    'prop=extracts',
                    #'exintro',
                    'explaintext'
                ])

data = [
    {
        'category': 'scientists',
        'data_dir': 'data/scientists',
        'titles': scientists,
    },
    {
        'category': 'jazz musicians',
        'data_dir': 'data/jazz_musicians',
        'titles': jazz_musicians,
    },
    {
        'category': 'writers',
        'data_dir': 'data/writers',
        'titles': writers,
    },
]

def grab(category, titles, data_dir):
    print(f'Grabbing {category}')
    os.makedirs(data_dir, exist_ok=True)

    for title in titles:

        url = url_template.format(**locals())
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if 'query' not in data:
            raise RuntimeError(title)

        for page_id, page in data['query']['pages'].items():
            print(f"{page_id:8} {page['title']}")
            path = os.path.join(data_dir, f'wikipedia_{title}.json')
            with open(path, 'w') as f:
                json.dump(page, f)

for d in data:
    grab(**d)
