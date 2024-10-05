import shutil
import time
import json
import requests
import urllib.parse
from PIL import Image, ImageDraw
from urllib.request import urlopen

def main():
    # support for transforming cards
    transformable = False
    # start the loop of looking for card names to search
    File_Name_Input = str(input('Enter file name to save to: '))
    file_output_name = f'{File_Name_Input}.png'
    while True:
        # print("Pro-tip: end the card name with a period to search for an exact name.")
        Card_Query = str(
            input(f'[{File_Name_Input}] Enter name of card to fetch or <ENTER> to reset image: '))

        if Card_Query.lower() == 'flip' or Card_Query.lower() == 'transform':
            if transformable:
                if showing_front:
                    downloadCard(back, file_output_name)
                    print("Flipped!")
                    showing_front = False
                else:
                    downloadCard(front, file_output_name)
                    print("Flipped!")
                    showing_front = True
            else:
                print("Transform card not loaded")
            continue

        if Card_Query.lower() == 'clear' or Card_Query.lower() == '':
            # clear the image and loop
            print('Resetting image...')
            shutil.copy2('blank.png', file_output_name)
            continue

        if Card_Query.lower() == 'exit please':
            # Exit the program
            print('Bye bye!  Thanks for being polite!')
            shutil.copy2('blank.png', file_output_name)
            exit()

        try:
            card = RobustSearch(Card_Query)
        except:
            print(f'Invalid query: "{Card_Query}"')
            continue
        if len(card['data']) == 0:
            print(f'No results for: {Card_Query}')
            continue

        card = findPrintingsOfCard(card)

        showing_front = True
        # check for Transform
        if card['DoubleSided'] == True:
            transformable = True
            front = card['FrontArt']
            back = card['BackArt']
        else:
            transformable = False
            front = card['FrontArt']
            back = card['FrontArt']
        # Pull down the image!
        downloadCard(front, file_output_name)
        # Communicate success!
        print('Downloaded ' + card["Name"] +
              '.  Type "Clear" or a new card to clear the image')
        if transformable:
            print("Type 'Flip' or 'Transform' to see the back side")

# Reused functions

def findPrintingsOfCard(card): 
    printings = card
    i = 1

    if len(printings['data']) != 1:
        # print("Card: " + Card_Name)
        for card in printings['data']:
            print(i, ":", card['Set'].upper(), ":", card['Name'], ":", card['Type'])
            i = i + 1
        # Select a printing
        set_select = selectPrintingPrompt(i)
    else:
        set_select = 1
    return printings['data'][int(set_select) - 1]


def selectPrintingPrompt(total_options):
    while True:
        set_select = input("Select a printing: ")
        try:
            set_select = int(set_select)
            if int(set_select) > total_options or int(set_select) < 1:
                print('Please pick a printing from the list!\n')
                continue
        except ValueError:
            print("Number not typed, selecting printing #1")
            set_select = 1
            return set_select
        return set_select

def downloadCard(cardSide, file_output_name):
    Card_uri = cardSide
    # time.sleep(0.05)
    # file = urlopen(Card_uri)
    # with open(file_output_name, 'wb') as cardFile:
    #     cardFile.write(file.read())

    im = Image.open(requests.get(Card_uri, stream=True).raw)
    im = add_corners(im, 25)
    im.save(file_output_name)

def RobustSearch(CardQuery):
    query = CardQuery
    query = urllib.parse.quote_plus(query)
    url = f'https://api.swu-db.com/cards/search?q=name:{query}&format=json'
    try:
        response = urlopen(url)
        json_response = json.load(response)
        return json_response
    except:
        raise Exception("Invalid card")

def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


if __name__ == '__main__':
    main()