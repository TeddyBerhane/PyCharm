from gameClasses import obj_wrapper as wrap
from ast import literal_eval
from operator import itemgetter
from player import Player
from msvcrt import getch, putch
import time, os, sys, pygame.mixer
from Q2API.util import logging
import traceback, pickle
pygame.mixer.init()

def main():
    # Open and parse XML game map
    with open('game.xml', 'r') as fin:
        xml_file = fin.read()
    gameXml = wrap(xml_file)
    building = gameXml[1]

    global room_dict
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

    single_word_commands = {"n": "go north",
                            "e": "go east",
                            "s": "go south",
                            "w": "go west",
                            "l": "look around",
                            "": "BAD_COMMAND"}

    verbs = {"go": "go", "g": "go", "walk": "go",
            "take": "take", "t": "take", "grab": "take"}

    def homeScreen():
        """Make a home screen for the game along with the intro for the game. Uses the first "Room" tag from XML
        game tag with coordinates (100, 100) ***This coordinate is not reachable in the game***"""
        intro = room_dict[(100, 100)].Des[0].value
        sound = room_dict[(100, 100)].Sound[0].value
        printASCII(intro)
        playSound(sound)
        command = ord(getch())
        if command == 13:
            os.system('CLS')
            P = Player()
            pygame.mixer.stop()
            play(P)
        elif command == 9:
            os.system('CLS')
            loadGame()
        elif command == 27:
            print '\n\n\t\t\t\t\tGood Bye!'
            time.sleep(2)
            sys.exit()
        else:
            print '\n\n\n\tI don\'t understand your command. Please press ENTER to play, or ESC to exit. ' \
                  'Please try again. \n\n'
            time.sleep(2)
            os.system('CLS')
            homeScreen()

    def lookForItems(current_room, P):
        items = room_dict[current_room].Items
        if items:
            for item in items:
                print "\nYou see a " + item.attrs['item'].upper()
                print '\nTo pick up items, type (grab/take + item).'
                command = get_command()
                update_state(current_room, command, P)
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
                words = monoText.split('\n')
                for line in words:
                    print line
                    time.sleep(1)
                room_dict[current_room].Mono.remove(mono)
                room_dict[current_room].children.remove(mono)
        return current_room

    def pickUpItem(current_room, P):
        items = room_dict[current_room].Items
        if items:
            for item in items:
                new_item = item.attrs['item']
                points = literal_eval(item.attrs['expValue'])
                P.points += points
                str_item = str(new_item)
                P.addToInv(str_item, current_room)
                print '\n\n', item.ItemDes[0].value
                print '\nYou picked up a(an) ' + str_item, '\n\nYou gained', points, 'points.'
                if item.ItemArt:
                    fileName = item.ItemArt[0].value
                    printASCII(fileName)
                if item.ItemSound:
                    soundFile = item.ItemSound[0].value
                    playSound(soundFile)
                if item.Ammo:
                    ammo = literal_eval(item.Ammo[0].value)
                    P.increaseAmmo(ammo)
                items.remove(item)
                room_dict[current_room].children.remove(item)
            return current_room
        else:
            print '\n\nThere are not any items to pick up.'
            time.sleep(1)
            os.system('CLS')
        return current_room

    def req(new_room, current_room, P):
        """Checks to see if the room the player is trying to enter has a requirement.If so a message is printed and the
        location of the play stays the same, otherwise the player can proceed into the the room. This is retrieved from
        the XML game map tag 'Req' """
        require = room_dict[new_room].Req
        if require:
            for item in require:
                if item.attrs['item'] in P.inv.keys():
                    print '\n\nSince you have a(an) ' + item.attrs['item'] + ' you have access to this room.'
                    command = get_command()
                    verb, noun = parseCommand(command)
                    if verb in ['use', 'Use', 'USE', 'u', 'U'] and (noun == item.attrs['item'] or
                    noun == item.attrs['item'].lower() or noun == item.attrs['item'].split()[1] or  #todo lower case the input to avoid doing all the different checks for all the inputs.
                    noun == item.attrs['item'].lower().split()[1]):
                        if item.ReqSound:
                            soundFile = item.ReqSound[0].value
                            sound = pygame.mixer.Sound(soundFile)
                            sound.play()
                        require.remove(item)
                        room_dict[new_room].children.remove(item)
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

    def inventory(current_room, P):
        if P.inv == {}:
            print '\nYou don\'t have anything in your inventory.'
            time.sleep(1)
            return current_room
        else:
            print '\n**INVENTORY LIST**\n\t\t\t\tHEALTH:', P.health, '\tPOINTS:', P.points, '\t  AMMO:', P.ammo
            for i, item in enumerate(P.inv):
                print i + 1, item + '\n'
            print '\nPress Tab to hide your inventory list.'
            command = get_command()
            verb, noun = parseCommand(command)
            if command in ['tab', 'i', 'I']:
                return current_room
            elif verb in ['look', 'info', 'tell', 'view']:
                for key in P.inv.keys():
                    if noun.lower() in [key.lower(), key.lower().split()[1]]:
                        room = lookInventory(current_room, noun.lower(), P)
                        os.system('CLS')
                        return room
            elif verb in ['use', 'Use', 'u', 'U']:
                for key in P.inv.keys():
                    if noun.lower() in [key.lower(), key.lower().split()[1]]:
                        room = useInventory(current_room, noun.lower(), P)
                        os.system('CLS')
                        return room
            else:
                print 'Not a valid command.'
                time.sleep(1)
                os.system('CLS')
                describe(room_dict[current_room], P)
        return inventory(current_room, P)

    def lookInventory(current_room, name, P):
        for key in P.inv.keys():
            if name in [key.lower(), key.lower().split()[1]]:
                coord = P.inv.get(key, 'That\'s not in your backpack.')
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
            inventory(current_room, P)
        return current_room

    def useInventory(current_room, name, P):
        for key in P.inv.keys():
            if (name == key or
                name == key.lower() or
                name == key.split()[1] or
                name == key.lower().split()[1]):
                coord = P.inv.get(key,'That\'s not in your backpack.')
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
                    P.increaseHealth(intHealthValue)
                    P.increasePoints(intExpValue)
                    print '\n\n\nHealth:', P.health
                    print '\nPoints:', P.points
                    if item[0].ItemArt:
                        fileName = item[0].ItemArt[0].value
                        printASCII(fileName)
                    for k in P.inv.keys():
                        if k == item[0].attrs['item']:
                            del P.inv[k]
                    print '\nPress Tab to return to game.'
                    command = get_command()
                    if command in ['tab', 'i', 'I']:
                        os.system('CLS')
                        return current_room
                else:
                    print 'This item cannot be used.'
                    time.sleep(1)
                    os.system('CLS')
        return current_room

    def checkStat(current_room, P):
        print '\nHEALTH:', P.health, '\n\nPOINTS:', P.points, '\n\nAMMO:', P.ammo
        raw_input('\nPress Enter to continue...')
        os.system('CLS')
        return current_room

    def useItem(current_room, noun, P):
        for key in P.inv.keys():
            if (noun == key.lower() or
                noun == key.split()[1] or
                noun == key.lower().split()[1]):
                coord = P.inv.get(key,'That\'s not in your backpack.')
                use = itemRoomDict[coord].Items[0].attrs['use']
                if use == 'True':
                    damage = literal_eval(itemRoomDict[coord].Items[0].attrs['damage'])
                    P.addToGunDamage(damage)
                    print '\n\n***Your', key, 'is enabled, and ready for use.***' \
                    '\n\nYou have', P.ammo, 'rounds left to use.' \
                    '\n\nTo fire', key, 'Press the PAGE DOWN button.' \
                    '\nYou can put away the', key, 'by typing (hide +', key, ')'
                    P.useGun(key)
                    raw_input('\n\nPress Enter to continue...')
                    os.system('CLS')
                    return current_room
                else:
                    print key.upper(), 'is not available'
                    time.sleep(1)
                    os.system('CLS')
        return current_room

    def putAwayItem(current_room, noun, P):
        for key in P.inv.keys():
            if (noun == key.lower() or
                noun == key.split()[1] or
                noun == key.lower().split()[1]):
                coord = P.inv.get(key, 'That\'s not in your backpack.')
                use = itemRoomDict[coord].Items[0].attrs['use']
                if P.gun and use == 'True':
                    P.gun = False
                    itemRoomDict[coord].Items[0].attrs['ammo'] = str(P.ammo)
                    print '\n\nYou have put the', key, 'away.'
                    time.sleep(1)
                    os.system('CLS')
                    return current_room
                else:
                    print key.upper(), 'is not in use'
                    time.sleep(1)
                    os.system('CLS')
        return current_room

    def shootGun(current_room, P):
        if P.gun == 'Shot Gun' and P.ammo > 0:
            for key, value in P.inv.iteritems():
                if key == 'Shot Gun':
                    sound = itemRoomDict[value].Items[0].UseSound
                    soundFile = sound[0].value
                    playSound(soundFile)
                    P.decreaseAmmo()
                    print '\n\nRemaining Rounds:', P.ammo
                    time.sleep(1)
                    os.system('CLS')
                    return current_room
        elif P.gun == 'Hand Grenade' and P.ammo > 0:
            for key,value in P.inv.iteritems():
                if key == 'Hand Grenade':
                    sound = itemRoomDict[value].Items[0].UseSound
                    soundFile = sound[0].value
                    playSound(soundFile)
                    P.decreaseAmmo()
                    for k in P.inv.keys():
                        if k == key:
                            del P.inv[k]
                    print '\n\nRemaining Rounds:', P.ammo
                    time.sleep(1)
                    os.system('CLS')
                    return current_room
        elif P.gun != None and P.ammo <= 0:
            print 'You\'re out of ammo!!'
            time.sleep(1)
            os.system('CLS')
            return current_room
        else:
            print '\n\nPunching the air is not going to help you out...'
            P.health -= 1
            time.sleep(1)
            os.system('CLS')
            return current_room

    def printASCII(fileName):
        with open('Art\\' + fileName) as fin:
            art = fin.read()
        print '\n', art

    def playSound(soundFile):
        sound = pygame.mixer.Sound('Sounds\\' + soundFile)
        sound.play()

    def engage(current_room, P):
        mon = room_dict[current_room].Monster
        if mon:
            for item in mon:
                monDes = item.MonsterDes[0].value
                print monDes, '\n\nUse your weapon to fight back!!'
                monName = item.attrs['name']
                monDamage = literal_eval(item.attrs['damage'])
                monHealth = literal_eval(item.attrs['health'])
                monPoints = literal_eval(item.attrs['experience'])
                monSound = item.MonsterAttack[0].value
                monArt = item.MonsterArt[0].value
                battleMusic = item.BattleMusic[0].value
                monsterHealth = monHealth
                while P.health > 0:
                    playSound(battleMusic)
                    playSound('heartbeat.wav')
                    print '\n\nYour Health:', P.health
                    print '\n\n', monName, 'Health:', monsterHealth
                    command = get_command()
                    if P.gun and command == 'shoot':
                        shootGun(current_room, P)
                        printASCII(monArt)
                        playSound(monSound)
                        print '\n\nYou shot the', monName, 'but he\'s still attacking you.'
                        P.decreaseHealth(monDamage)
                        monsterHealth -= P.gunDamage
                    if monsterHealth <= 0:
                        P.increasePoints(monPoints)
                        print '\n\nYou have defeated the', monName, '!! \n\n You have gained,', monPoints, 'points:'
                        if P.health < 30:
                            print '\n\nWhoa!! That was close. You should look for fix your self up!'
                        raw_input('\n\nPress Enter Champ! ')
                        P.monster.append(current_room)
                        pygame.mixer.fadeout(2)
                        mon.remove(item)
                        room_dict[current_room].children.remove(item)
                        os.system('CLS')
                        return current_room
                    elif not P.gun and command == 'shoot':
                        print '\n\nYou punched the', monName, '!!'
                        printASCII(monArt)
                        playSound(monSound)
                        P.decreaseHealth(monDamage)
                        time.sleep(1)
                        pygame.mixer.fadeout(2)
                        monsterHealth -= 10
                    elif command in ['tab', 'i', 'I']:
                        inventory(current_room, P)
                        engage(current_room, P)
                    elif command != 'shoot' and command not in ['tab', 'i', 'I']:
                        print '\n\nDo something you\'re becoming', monName, 'food!!!'
                        time.sleep(1)
                        P.decreaseHealth(monDamage)
                else:
                    print '\n\nYou gave it a good run, but your limbs were devoured by the', monName, '.'
                    pygame.mixer.stop()
                    os.system('CLS')
                    printASCII('Lose.txt')
                    playSound('zoombieWins.wav')
                    playSound('loser.wav')
                    time.sleep(5)
                    os.system('CLS')
                    score(P)
        else:
            return current_room

    def play(P):
        # Where all the fun takes place!!
        os.system('CLS')
        current_coord = P.coord
        while True:
            current_room = room_dict.get(current_coord)
            describe(current_room, P)
            playSound('walk around.wav')
            command = get_command()
            current_coord = update_state(current_coord, command, P)
            pygame.mixer.stop()
            current_coord = engage(current_coord, P)

    def quitGame(current_room, P):
        os.system('CLS')
        printASCII('save.txt')
        print '\n\n\t\t\tWOULD YOU LIKE TO SAVE YOUR GAME? Enter YES/NO.'
        command = get_command()
        if command in ['y', 'yes', 'YES', 'Yes']:
            os.system('CLS')
            printASCII('save.txt')
            saveGame(current_room, P)
        elif command in ['n', 'no', 'NO', 'No']:
            os.system('CLS')
            printASCII('quit.txt')
            score(P)
            main()
        elif command == 'tab':
            return current_room
        else:
            print 'That\'s not a valid command.'
            time.sleep(1)
            os.system('CLS')

    def score(P):
        try:
        #********************************Writing*************************************************
            printASCII('scores.txt')
            name = raw_input('\n\n\nEnter you name to record your score:')
            saveScore = (P.points, name.upper())
            with open('Art\\high_scores.txt', 'a+b') as fout:
                fout.write(str(saveScore) + '\n')
            print '\n\nYou can see your score by pressing TAB on the home screen.'.center(100)
            time.sleep(2)
            os.system('CLS')
        except:
            sys.exit()

    def showScore():
        #********************************Reading*************************************************
        printASCII('highscoreascii.txt')
        try:
            scores = []
            with open('Art\\high_scores.txt', 'r') as fin:
                fileOpen = fin.read()
            for line in fileOpen[:-1].split('\n'):
                score = literal_eval(line)
                scores.append(score)
            sortScore = sorted(scores, key=itemgetter(0), reverse=True)
            print '\n\n'
            for points, name in sortScore:
                print (name + ' ' * 5 + str(points)).rjust(52) + '\n'
        except:
            print '\n\n\n\nSorry. Cannot display high scores at this moment.'

    def saveGame(current_room, P):
        os.system('CLS')
        fileName = raw_input("\n\n\n\nEnter you name:")
        P.coord = current_room
        if len(fileName) > 1:
            try:
                gameData = building.flatten_self()
                with open('Saved_Games\\' + fileName.lower() + ".xml", "w") as fout:
                    fout.write(gameData)
                with open('Saved_Games\\' + fileName.lower() + '.txt', 'w')as fout2:
                    pickle.dump(P, fout2)
                print ("\n\n\n\nYour game has been saved," + fileName)
            except:
                print ('\n\n\n\nThere was a problem saving your game,' + fileName)
            time.sleep(1)
            os.system('CLS')
            return current_room
        else:
            print 'Please enter a valid name.'
            time.sleep(1)
            quitGame(current_room, P)

    def loadGame():
        global room_dict
        showScore()
        print '\n\n\n\n\n\n\n\n\n'
        printASCII('load.txt')
        print '\n\n\n\n\nEnter your name:'
        fileName = get_command()
        if fileName == 'tab':
            os.system('CLS')
            homeScreen()
        P = Player()
        try:
            with open('Saved_Games\\' + fileName.lower() + '.txt', 'r') as fin:
                Load = pickle.load(fin)
            P.coord = Load.coord
            P.monster = Load.monster
            P.health = Load.health
            P.inv = Load.inv
            P.ammo = Load.ammo
            P.points = Load.points
            P.gun = Load.gun
            P.gunDamage = Load.gunDamage
            with open('Saved_Games\\' + fileName.lower() + '.xml', 'r') as fin2:
                loadFile = fin2.read()
            game = wrap(loadFile)
            building = game[1]
            room_dict = {}
            for room in building.Room:
                coord = room.attrs['coord']
                strCoord = str(coord)
                tupCoord = literal_eval(strCoord)
                room_dict[tupCoord] = room
            play(P)
        except:
            print '\n\n\n\n\n\t\t\tA saved game for', fileName, 'is not found.'
            time.sleep(3)
            os.system('CLS')
            homeScreen()

    def describe(current_room, P):
        if P.gun != None and P.gun != False:
            print current_room.Des[0].value
            print '\n'
            print (str(P.ammo)+'  '+ chr(220)+chr(205)+chr(203)+chr(205)+chr(190)).rjust(97)
        else:
            print current_room.Des[0].value
        for art in current_room.Art:
            if art:
                fileName = current_room.Art[0].value
                printASCII(fileName)
        for sound in current_room.Sound:
                if sound:
                    soundFile = current_room.Sound[0].value
                    playSound(soundFile)
        for exits in current_room.Exit:
            if exits.value == 'Winner':
                time.sleep(10)
                os.system('CLS')
                score(P)
        print '\n\nPress TAB or ("I" + Enter) to view your inventory.'
        print '\n\nWould you like to look around? Press ("L" + Enter) to look.'

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

    def update_state(current_room, command, P):
        verb, noun = parseCommand(command)
        if verb in ["go", 'g', 'G', 'GO', 'move', 'MOVE']:
            if noun in ['n', 'north', "N", "NORTH", 'up', 'UP']:
                new_room = (current_room[0], current_room[1] + 1)
                checked_room = exits(new_room, current_room)
                check_req = req(checked_room, current_room, P)
                os.system('CLS')
                return check_req
            elif noun in ['e', 'east', 'E', 'EAST']:
                new_room = (current_room[0] + 1, current_room[1])
                checked_room = exits(new_room, current_room)
                check_req = req(checked_room, current_room, P)
                os.system('CLS')
                return check_req
            elif noun in ['w', 'west', 'W', 'WEST']:
                new_room = (current_room[0] - 1, current_room[1])
                checked_room = exits(new_room, current_room)
                check_req = req(checked_room, current_room, P)
                os.system('CLS')
                return check_req
            elif noun in ['s', 'south', 'S', 'SOUTH', 'down', 'DOWN']:
                new_room = (current_room[0], current_room[1] - 1)
                checked_room = exits(new_room, current_room)
                check_req = req(checked_room, current_room, P)
                os.system('CLS')
                return check_req
            elif noun in ['', ' ']:
                print 'You have to specify which direction you would like to move. Try again.'
                time.sleep(1)
                os.system('CLS')
                return current_room
        elif verb in ['look', 'l', 'Look', 'L', 'LOOK', 'see']:
            if hasattr(room_dict[current_room], "Items") and noun in ['around', 'room', '', ' ']:
                room = lookForItems(current_room, P)
                return room
            else:
                print '\nThere arn\'t any items in here..'
                time.sleep(1)
                os.system('CLS')
            return current_room
        elif verb in ['take', 'grab', 'get']:
            try:
                if hasattr(room_dict[current_room], "Items") and noun.lower() in \
                        [room_dict[current_room].Items[0].attrs['item'].lower(),
                         room_dict[current_room].Items[0].attrs['item'].lower().split()[1]]:
                    location = pickUpItem(current_room, P)
                    print '\nBackpack: ', P.inv.keys()
                    raw_input('\nPress Enter to continue...')
                    os.system('CLS')
                    return location
                else:
                    print '\nThere\'s nothing worth taking.'
                    time.sleep(1)
                    os.system('CLS')
                    return current_room
            except:
                print '\nThere\'s nothing worth taking.'
                time.sleep(1)
                os.system('CLS')
                return current_room
        elif room_dict[current_room].Mono and verb in ['talk', 't', 'speak']:
            if hasattr(room_dict[current_room], "Mono") and noun.lower() in \
                    [room_dict[current_room].Mono[0].attrs['person'].lower(),
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
            room = inventory(current_room, P)
            os.system('CLS')
            return room
        elif verb == 'q':
            quitGame(current_room, P)
        elif verb in ['stat', 'health']:
            location = checkStat(current_room, P)
            os.system('CLS')
            return location
        elif verb in ['use', 'Use', 'u', 'U']:
            location = useItem(current_room, noun, P)
            os.system('CLS')
            return location
        elif verb in ['hide', 'store']:
            location = putAwayItem(current_room, noun, P)
            os.system('CLS')
            return location
        elif verb == 'shoot':
            location = shootGun(current_room, P)
            return location
        else:
            print '\nThat\'t not a command.'
            time.sleep(1)
            os.system('CLS')
        return current_room

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

logger = logging.out_file_instance('Logs\\Zombie Raid')
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        exception_string = traceback.format_exc()
        logger.write_line([exception_string])
        print exception_string
