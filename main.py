import random
import re
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    database="test",
    password="Tr@sh-Murd3r-Chi1d"
)

class AllCharaCheck(Exception):
    pass

cursor = conn.cursor()
cursor.execute("SELECT * FROM genshinchara")

print("All entries:")
for row in cursor:
    print(row)

while True:
    #gets the table size after every iteration, since some commands can add rows
    cursor.execute("SELECT COUNT(chara_id) FROM genshinchara")
    (tableSize,)=cursor.fetchone()
    charas = ["name", "name", "name", "name"]

    newInput = input("Enter Command (type 'help' for more): ")
    if (newInput == "quit"): break
    elif (newInput == "help"): 
        print("Current Commands: \n -'quit': quits the program \n-'random': randomly selects a team of 4 \n" + 
        "-'randomWith': randomly selects a team of 4 with additional constraints. type 'none' if the constraint does not" +
        " need to apply \n ->Minimum Level: input the minimum level all characters should be \n ->Vision Types: your entry should be" +
        " either 4 words, all either a vision, or 'none', or it is simply 'none' (eg, geo geo none none) \n-'levelUp': takes a "+
        "character name and level to update the data")
    elif (newInput == "random"):
        charasLeft = 4
        arrCounter = list(range(1,tableSize+1)) #creates a list mimicking the table
        try:
            while charasLeft > 0:
                charnum = random.randint(1,tableSize)
                cursor.execute("SELECT genshinchara.name FROM genshinchara WHERE chara_id = (%s)", (charnum,))
                (charaname,)=cursor.fetchone()
                #could throw valueError
                if charnum in arrCounter:
                    arrCounter.remove(charnum)
                if len(arrCounter) == 0:
                    raise AllCharaCheck 

                if charaname not in charas:
                    charasLeft -= 1
                    charas[charasLeft] = charaname
            for character in charas:
                print(character)
        except AllCharaCheck:
                if len(arrCounter) == 0:
                    print("You do not have enough characters")
                    break
    
    #the cases for randomWith
    elif (newInput == "randomWith"):
            #int or 'none'
            while True:
                minLevelst = input("Input Minimum Level (at least 1): ")
                if minLevelst == "none":
                    break
                else:
                    try:
                        minLevel = int(minLevelst)
                    except:
                        continue
                    break

            #string of 4 words or 'none'
            #word processing is case insensitive
            while True:
                elts = input("Input 4 Vision Types (or only 'none'): ")
                mymatch = re.search('^((?!(geo|cryo|pyro|hydro|anemo|electro|none)).)*$', elts, re.IGNORECASE)
                if not mymatch: #contains words other than the visions/none
                    visList = elts.split()
                    #make everything have a capital at the start
                    for i, item in enumerate(visList):
                        visList[i] = item.title()
                    if len(visList) == 4:
                        break
                    elif len(visList) == 1 and visList[0]=="None":
                        for i in range(0,3):
                            visList.append("None")
                        break
            #now doing the processing
            arrCounter = list(range(1,tableSize+1)) #creates a list mimicking the table
            charasLeft = 4
            try:
                #charnum is the ID, thus when doing a non-vision limited search charnum is assigned right away, but it is queried for when doing vision-limited search
                while charasLeft > 0:
                    #using the charaCounter because same number of visions required
                    cursor.execute("SELECT COUNT(chara_id) FROM genshinchara WHERE " + (" " if visList[charasLeft - 1] =="None" else "vision = '" + visList[charasLeft-1] + "' AND ") +"level >= " + ("0" if minLevelst == "none" else minLevelst))
                    (querynum,) = cursor.fetchone()
                    if (querynum == 1):
                        charnumvLim = 0
                    elif (querynum == 0):
                        raise AllCharaCheck
                    else:
                        charnumvLim = random.randint(0,querynum-1) #because OFFSET starts at 0
                    instring = ("SELECT genshinchara.chara_id, genshinchara.name, genshinchara.level, genshinchara.vision FROM genshinchara WHERE " + (" " if visList[charasLeft - 1] =="None" else "vision = '" + visList[charasLeft-1] + "' AND ") 
                    + "level >= " + ("0" if minLevelst == "none" else minLevelst) +" LIMIT 1 OFFSET " + str(charnumvLim))
                    cursor.execute(instring)
                    (charnum, charaname, charlevelst, charvision)=cursor.fetchone()
                    charlevel = int(charlevelst)

                    if len(arrCounter) == 0:
                        raise AllCharaCheck 
                    if charnum in arrCounter:
                        arrCounter.remove(charnum)
                    else: # we already processed this character
                        continue
                    
                    #now guaranteed that the character has a valid vision and level (at charasLeft-1 in visList)
                    if charaname not in charas:
                        charasLeft -= 1
                        charas[charasLeft] = charaname
                        #one of the following
                        if charvision in visList:
                            visList.remove(charvision)
                        elif "None" in visList:
                            visList.remove("None")
                for character in charas:
                    print(character)
            except AllCharaCheck:
                print("You do not have enough characters meeting your criteria", flush=True)
            

