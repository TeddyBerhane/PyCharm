from gameClasses import obj_wrapper as wrap
from ast import literal_eval
# from player import Player
from msvcrt import getch, putch
import time, os, sys, pygame.mixer

pygame.mixer.init()

global inv, health, points, gameAmmo, gun, gunDamage
inv = {}
health = 75
points = 0
gameAmmo = 0
gun = False
gunDamage = 0
# Open and parse XML game map

with open('game.xml', 'r') as fin:
    xml_file = fin.read()
gameXml = wrap(xml_file)
building = gameXml[1]

# Make a dictionary that maps the room coordinates to the corresponding room data in the XML game map
room_dict = {}
for room in building.Room:
    coord = room.attrs['coord']
    strCoord = str(coord)
    tupCoord = literal_eval(strCoord)
    room_dict[tupCoord] = room

with open('game.xml', 'r') as fin:
    xml_file = fin.read()
gameXml = wrap(xml_file)
justFotItems = gameXml[1]

itemRoomDict = {}
for room in justFotItems.Room:
    coord = room.attrs['coord']
    strCoord = str(coord)
    tupCoord = literal_eval(strCoord)
    itemRoomDict[tupCoord] = room


def homeScreen():
    """Make a home screen for the game along with the intro for the game. Uses the first "Room" tag from XML
    game tag with coordinates (100, 100) ***This coordinate is not reachable in the game***"""
    global inv, health, points, gameAmmo, gun, gunDamage
    intro = room_dict[(100, 100)].Des[0].value
    printASCII(intro)
    command = ord(getch())
    if command == 13:
        os.system('CLS')
        inv = {}
        health = 75
        points = 0
        gameAmmo = 0
        gun = False
        gunDamage = 0
        play()
    elif command == 27:
        print '\n\n\t\t\t\t\tGood Bye!'
        time.sleep(2)
        sys.exit()
    else:
        os.system('CLS')
        print '\n\n\n\tI don\'t understand your command. Please press ENTER to play, or ESC to exit. ' \
              'Please try again. \n\n'
        homeScreen()


def lookForItems(current_room):
    items = room_dict[current_room].Items
    if items:
        for item in items:
            print "\nYou see a " + item.attrs['item'].upper()
            print '\nTo pick up items, type (grab/take + item).'
            command = get_command()
            update_state(current_room, command)
        return current_room
    else:
        print '\n\nNo items in here.'
        time.sleep(1)
        os.system('CLS')
        return current_room


def speak(current_room):
    for mono in room_dict[current_room].Mono:
        if mono:
            monoText = mono.value
            # monoName = mono.attrs['person']
            words = monoText.split('\n')
            for line in words:
                print line
                time.sleep(1)
            room_dict[current_room].Mono = False
    return current_room


def pickUpItem(current_room):
    global inv, gameAmmo
    items = room_dict[current_room].Items
    if items:
        for item in items:
            new_item = item.attrs['item']
            str_item = str(new_item)
            # Player().addToInv(str_item, current_room)
            inv[str_item] = current_room
            print '\n\n', item.ItemDes[0].value
            print '\nYou picked up a(an) ' + str_item
            if item.ItemArt:
                fileName = item.ItemArt[0].value
                printASCII(fileName)
            if item.ItemSound:
                soundFile = item.ItemSound[0].value
                playSound(soundFile)
            if item.Ammo:
                ammo = literal_eval(item.Ammo[0].value)
                gameAmmo += ammo
            del room_dict[current_room].Items[0]
        return current_room
    else:
        print '\n\nThere are not any items to pick up.'
        time.sleep(1)
        os.system('CLS')
        return current_room


def req(new_room, current_room):
    """Checks to see if the room the player is trying to enter has a requirement.If so a message is printed and the
    location of the play stays the same, otherwise the player can proceed into the the room. This is retrieved from
    the XML game map tag 'Req' """

    require = room_dict[new_room].Req
    if require:
        for item in require:
            if item.attrs['item'] in inv.keys():
                print '\n\nSince you have a(an) ' + item.attrs['item'] + ' you have access to this room.'
                command = get_command()
                verb, noun = parseCommand(command)
                if verb in ['use', 'Use', 'USE', 'u', 'U'] and (noun == item.attrs['item'] or
                noun == item.attrs['item'].lower() or noun == item.attrs['item'].split()[1] or
                noun == item.attrs['item'].lower().split()[1]):
                    if item.ReqSound:
                        soundFile = item.ReqSound[0].value
                        sound = pygame.mixer.Sound(soundFile)
                        sound.play()
                    room_dict[new_room].Req = False
                    return new_room
                else:
                    print 'Clearly, you can\'t use that here!!.'
                    time.sleep(1)
                return current_room
            else:
                print '\n', item.ReqMes[0].value
                time.sleep(2)
        return current_room
    else:
        return new_room


def inventory(current_room):
    global inv, health, points, gameAmmo
    if inv == {}:
        print '\nYou don\'t have anything in your inventory.'
        time.sleep(1)
        return current_room
    else:
        print '\n**INVENTORY LIST**\n\t\t\t\tHEALTH:', health, '\tPOINTS:', points, '\t  AMMO:', gameAmmo
        for i, item in enumerate(inv):
            print i + 1, item + '\n'
        print '\nPress Tab to hide your inventory list.'
        command = get_command()
        verb, noun = parseCommand(command)
        if command in ['tab', 'i', 'I']:
            return current_room
        elif verb in ['look', 'info', 'tell', 'view']:
            for key in inv.keys():
                if noun.lower() in [key.lower(), key.lower().split()[1]]:
                    room = lookInventory(current_room, noun.lower())
                    return room
        elif verb in ['use', 'Use', 'u', 'U']:
            for key in inv.keys():
                if noun.lower() in [key.lower(), key.lower().split()[1]]:
                    room = useInventory(current_room, noun.lower())
                    return room
        else:
            print 'Not a valid command.'
            time.sleep(1)
            os.system('CLS')
            describe(room_dict[current_room])
    return inventory(current_room)


def lookInventory(current_room, name):
    global inv
    for key in inv.keys():
        if name in [key.lower(), key.lower().split()[1]]:
            coord = inv.get(key,'That\'s not in your backpack.')
            item = itemRoomDict[coord].Items
            des = item[0].ItemDes[0].value
            print des
            if item[0].ItemArt:
                fileName = item[0].ItemArt[0].value
                printASCII(fileName)
            if item[0].ItemSound:
                soundFile = item[0].ItemSound[0].value
                playSound(soundFile)
            print '\nPress Tab to hide details.'
            command = get_command()
            if command in ['tab', 'i', 'I']:
                return current_room
    else:
        print 'Unrecognized command...'
        time.sleep(1)
        inventory(current_room)
    return current_room


def useInventory(current_room, name):
    global inv
    for key in inv.keys():
        if (name == key or
            name == key.lower() or
            name == key.split()[1] or
            name == key.lower().split()[1]):
            coord = inv.get(key,'That\'s not in your backpack.')
            item = itemRoomDict[coord].Items
            use = item[0].ItemUse
            if use:
                healthValue = item[0].attrs['healthValue']
                intHealthValue = literal_eval(healthValue)
                expValue = item[0].attrs['expValue']
                intExpValue = literal_eval(expValue)
                print 'You have used', item[0].attrs['item'], '\nYou have gained', intHealthValue, 'health points.', \
                    '\nYou have gained', intExpValue, 'points.'
                use = item[0].ItemUse
                print use[0].value
                global health
                global points
                if health >= 100:
                    health = 100
                else:
                    health += intHealthValue
                points += intExpValue
                print '\n\n\nHealth:', health
                print '\nExperience:', points
                if item[0].ItemArt:
                    fileName = item[0].ItemArt[0].value
                    printASCII(fileName)
                for k in inv.keys():
                    if k == item[0].attrs['item']:
                        del inv[k]
                print '\nPress Tab to return to game.'
                command = get_command()
                if command in ['tab', 'i', 'I']:
                    return current_room
            else:
                print 'This item cannot be used.'
                time.sleep(1)
    return current_room


def checkStat(current_room):
    global health, points, gameAmmo
    print '\nHEALTH:', health, '\n\nPOINTS:', points, '\n\nAMMO:', gameAmmo
    raw_input('\nPress Enter to continue...')
    os.system('CLS')
    return current_room


def useItem(current_room, noun):
    global gun, gameAmmo, inv, gunDamage
    for key in inv.keys():
        if (noun == key.lower() or
            noun == key.split()[1] or
            noun == key.lower().split()[1]):
            coord = inv.get(key,'That\'s not in your backpack.')
            use = itemRoomDict[coord].Items[0].attrs['use']
            if use == 'True':
                damage = literal_eval(itemRoomDict[coord].Items[0].attrs['damage'])
                gunDamage = damage
                print '***Your', key, 'is enabled, and ready for use.***' \
                '\n\nYou have', gameAmmo, 'rounds left to use.' \
                '\n\nTo fire', key, 'Press the PAGE DOWN button.' \
                '\nYou can put away the', key, 'by typing (hide +', key, ')'
                gun = True
                raw_input('\n\nPress Enter to continue...')
                os.system('CLS')
                return current_room
            else:
                print key.upper(), 'is not available'
                time.sleep(1)
                os.system('CLS')
    return current_room


def putAwayItem(current_room, noun):
    global gun, gameAmmo, inv
    for key in inv.keys():
        if (noun == key.lower() or
            noun == key.split()[1] or
            noun == key.lower().split()[1]):
            coord = inv.get(key,'That\'s not in your backpack.')
            use = itemRoomDict[coord].Items[0].attrs['use']
            if gun and use == 'True':
                gun = False
                itemRoomDict[coord].Items[0].attrs['ammo'] = str(gameAmmo)
                print '\n\nYou have put the', key, 'away.'
                time.sleep(1)
                os.system('CLS')
                return current_room
            else:
                print key.upper(), 'is not in use'
                time.sleep(1)
                os.system('CLS')
    return current_room


def shootGun(current_room):
    global gameAmmo, gun, health
    if gun and gameAmmo > 0:
        for key, value in inv.iteritems():
            sound = itemRoomDict[value].Items[0].UseSound
            if sound:
                soundFile = sound[0].value
                sound = pygame.mixer.Sound(soundFile)
                sound.play()
                gameAmmo -= 1
                print '\n\nRemaining Rounds:', gameAmmo
                time.sleep(1)
                os.system('CLS')
                return current_room
    elif gun and gameAmmo <= 0:
        print 'You\'re out of ammo!!'
        time.sleep(1)
        os.system('CLS')
        return current_room
    else:
        print '\n\nPunching the air is not going to help you out...'
        health -= 1
        time.sleep(1)
        os.system('CLS')
    return current_room


def printASCII(fileName):
    with open(fileName) as fin:
        art = fin.read()
    print '\n', art


def playSound(soundFile):
    sound = pygame.mixer.Sound(soundFile)
    sound.play()


def engage(current_room):
    global inv, health, gameAmmo, points, gunDamage, gun
    mon = room_dict[current_room].Monster
    if mon:
        for item in mon:
            monDes = item.MonsterDes[0].value
            print monDes, '\n\nUse your weapon to fight back!!'
            monName = item.attrs['name']
            monDamage = literal_eval(item.attrs['damage'])
            monHealth = literal_eval(item.attrs['health'])
            monPoints = literal_eval(item.attrs['points'])
            monSound = item.MonsterAttack[0].value
            monArt = item.MonsterArt[0].value
            monsterHealth = monHealth
            while health > 0:
                print '\n\nYour Health:', health
                print '\n\n', monName, 'Health:', monsterHealth
                command = get_command()
                if gun and command == 'shoot':
                    shootGun(current_room)
                    printASCII(monArt)
                    playSound(monSound)
                    print '\n\nYou shot the', monName, 'but he\'s still attacking you.'
                    health -= monDamage
                    monsterHealth -= gunDamage
                if monsterHealth <= 0:
                    points += monPoints
                    print '\n\nYou have defeated the', monName, '!! \n\n You have gained,', monPoints, 'points:'
                    if health < 30:
                        print '\n\nWhoa!! That was close. You should look for fix your self up!'
                    raw_input('\n\nPress Enter Champ! ')
                    room_dict[current_room].Monster = False
                    os.system('CLS')
                    return current_room
                elif not gun and command == 'shoot':
                    print '\n\nYou punched the', monName, '!!'
                    printASCII(monArt)
                    playSound(monSound)
                    health -= monDamage
                    time.sleep(1)
                    monsterHealth -= 1
                elif command in ['tab', 'i', 'I']:
                    inventory(current_room)
                    engage(current_room)
                elif command != 'shoot' and command not in ['tab', 'i', 'I']:
                    print '\n\nDo something you\'re becoming', monName, 'food!!!'
                    time.sleep(1)
                    health -= monDamage
            else:
                print '\n\nYou gave it a good run, but your limbs were devoured by the', monName, '.'
                printASCII('Lose.txt')
                playSound('zoombieWins.wav')
                time.sleep(5)
                homeScreen()
            return current_room
    else:
        return current_room


def play():
    # Where all the fun takes place!!
    os.system('CLS')
    current_coord = (0, 0)
    while True:
        current_room = room_dict.get(current_coord)
        describe(current_room)
        command = get_command()
        current_coord = update_state(current_coord, command)
        current_coord = engage(current_coord)


def quitGame(current_room):
    global inv, health, points, gameAmmo, gun, gunDamage
    print '\n\n\t\t\tWOULD YOU LIKE TO SAVE YOUR GAME? Enter YES/NO.'
    command = get_command()
    if command in ['y', 'yes', 'YES', 'Yes']:
        saveGame(current_room)
    elif command in ['n', 'no', 'NO', 'No']:
        print '\n\nUntil Next Time...'
        time.sleep(1)
        os.system('CLS')
        homeScreen()
    elif command == 'tab':
        return current_room
    else:
        print 'That\'s not a valid command.'
        time.sleep(1)


def saveGame(current_room):
    # currentLocation = room_dict[current_room]
    fileName = raw_input("Enter you name: ")
    gameInfo = gameXml[1].flatten_self()
    with open('Saved_Games\\' + fileName + ".xml", "w") as fout:
        fout.write(gameInfo)
    print "Your game has been saved,", fileName
    return current_room


def describe(current_room):
    print current_room.Des[0].value
    for art in current_room.Art:
        if art:
            fileName = current_room.Art[0].value
            printASCII(fileName)
    print '\n\nPress TAB or ("I" + Enter) to view your inventory.'
    print '\n\nWould you like to look around this room? Press ("L" + Enter) to look.'

def get_command():
    """Uses the msvcrt module to get key codes from buttons pressed to navigate through the game. The arrows,
    enter, tab, Page Down, and escape keys are used so far."""
    cmd = ""
    while 1:
        key = ord(getch())
        if key == 224:
            key = ord(getch())
            cmd = arrow_keys.get(key, "")
            return cmd
        elif key == 13:
            putch("\n")
            break
        elif key == 8:
            cmd = cmd[:-1]
            putch(chr(8))
            putch(" ")
            putch(chr(8))
        elif key == 27:
            cmd = 'q'
            return cmd
        elif key == 9:
            cmd = 'tab'
            return cmd
        else:
            putch(chr(key))
            cmd += chr(key)
    return cmd


arrow_keys = {72: "n",
              77: "e",
              75: "w",
              80: "s",
              81: 'shoot'}


def update_state(current_room, command):
    global inv, gun, gameAmmo, health, points
    verb, noun = parseCommand(command)
    if verb in ["go", 'g', 'G', 'GO', 'move', 'MOVE']:
        if noun in ['n', 'north', "N", "NORTH", 'up', 'UP']:
            new_room = (current_room[0], current_room[1] + 1)
            checked_room = exits(new_room, current_room)
            check_req = req(checked_room, current_room)
            os.system('CLS')
            return check_req
        elif noun in ['e', 'east', 'E', 'EAST']:
            new_room = (current_room[0] + 1, current_room[1])
            checked_room = exits(new_room, current_room)
            check_req = req(checked_room, current_room)
            os.system('CLS')
            return check_req
        elif noun in ['w', 'west', 'W', 'WEST']:
            new_room = (current_room[0] - 1, current_room[1])
            checked_room = exits(new_room, current_room)
            check_req = req(checked_room, current_room)
            os.system('CLS')
            return check_req
        elif noun in ['s', 'south', 'S', 'SOUTH', 'down', 'DOWN']:
            new_room = (current_room[0], current_room[1] - 1)
            checked_room = exits(new_room, current_room)
            check_req = req(checked_room, current_room)
            os.system('CLS')
            return check_req
        elif noun in ['', ' ']:
            print 'You have to specify which direction you would like to move. Try again.'
            time.sleep(1)
            os.system('CLS')
            return current_room
    elif verb in ['look', 'l', 'Look', 'L', 'LOOK', 'see']:
        if hasattr(room_dict[current_room], "Items") and noun in ['around', 'room', '', ' ']:
            room = lookForItems(current_room)
            return room
        else:
            print '\nThere arn\'t any items in here..'
            time.sleep(1)
            os.system('CLS')
        return current_room
    elif verb in ['take', 'grab', 'get']:       #todo lower case the input to avoid doing all the different checks for all the inputs.
        if hasattr(room_dict[current_room], "Items") and noun.lower() in [room_dict[current_room].Items[0].attrs['item'].lower(),
                            room_dict[current_room].Items[0].attrs['item'].lower().split()[1]]:
            location = pickUpItem(current_room)
            global inv
            print '\nBackpack: ', inv.keys()
            raw_input('\nPress Enter to continue...')
            os.system('CLS')
            return location
        else:
            print '\nThere\'s nothing worth taking.'
            time.sleep(1)
            os.system('CLS')
        return current_room
    elif room_dict[current_room].Mono and verb in ['talk', 't', 'speak']:
        if hasattr(room_dict[current_room], "Mono") and noun.lower() in [room_dict[current_room].Mono[0].attrs['person'].lower(),
                          room_dict[current_room].Mono[0].attrs['person'].lower().split()[1]]:
            room = speak(current_room)
            raw_input('Press Enter to continue...')
            os.system('CLS')
            return room
        else:
            print '\n\nWho are you talking to?? You might be losing your mind.'
            time.sleep(1)
            os.system('CLS')
        return current_room
    elif verb in ['tab', 'i', 'I']:
        room = inventory(current_room)
        os.system('CLS')
        return room
    elif verb == 'q':
        quitGame(current_room)
    elif verb in ['stat', 'health']:
        location = checkStat(current_room)
        return location
    elif verb in ['use', 'Use', 'u', 'U']:
        location = useItem(current_room, noun)
        return location
    elif verb in ['hide', 'store']:
        location = putAwayItem(current_room, noun)
        return location
    elif verb == 'shoot':
        location = shootGun(current_room)
        return location
    else:
        print '\nThat\'t not a command.'
        time.sleep(1)
        os.system('CLS')
    return current_room


single_word_commands = {"n": "go north",
                        "e": "go east",
                        "s": "go south",
                        "w": "go west",
                        "l": "look around",
                        "": "BAD_COMMAND"}

verbs = {"go": "go", "g": "go", "walk": "go",
         "take": "take", "t": "take", "grab": "take"}


def parseCommand(command):
    command = single_word_commands.get(command, command)
    words = command.split()
    verb = words[0]
    noun = " ".join(words[1:])
    return verb, noun


def exits(new_room, current_room):
    """Checks to see the available exits of a room are. These exits are retrieved from the XML game map under
    the tag 'Exit'"""
    exitList = []
    for eachExit in room_dict[current_room].Exit:
        exitCoord = literal_eval(eachExit.value)
        exitList.append(exitCoord)
    if new_room in exitList:
        return new_room
    else:
        print 'You can\'t go that way.'
        time.sleep(1)
    return current_room


homeScreen()

# room = room_dict[(0, 2)]
# del new_room[0]
# print type(room.Items)
# print room_dict[(0, 2)].flatten_self()