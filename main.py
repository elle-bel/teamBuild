import random
import re
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    database="test",
    #password="put your password here"
)

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
        " need to apply \n -Minimum Level: input the minimum level all characters should be \n -Vision Types: your entry should be" +
        " either 4 words, all either a vision, or 'none', or it is simply 'none' (eg, geo geo none none)")
    elif (newInput == "random"):
        charasLeft = 4
        while charasLeft > 0:
            charnum = random.randint(1,tableSize)
            cursor.execute("SELECT genshinchara.name FROM genshinchara WHERE chara_id = (%s)", (charnum,))
            (charaname,)=cursor.fetchone()
            if charaname not in charas:
                charasLeft -= 1
                charas[charasLeft] = charaname
        for character in charas:
            print(character)
    
    #the cases for randomWith
    elif (newInput == "randomWith"):
            #int or 'none'
            minLevel = input("Input Minimum Level: ")

            #string of 4 words or 'none'
            #word processing is case insensitive
            while True:
                elts = input("Input 4 Vision Types: ")
                mymatch = re.search('^((?!(geo|cryo|pyro|hydro|anemo|none)).)*$', elts, re.IGNORECASE)
                if not mymatch: #contains words other than the visions/none
                    visList = elts.split()
                    for i in visList:
                            i = i.lower()
                    if len(visList) == 4 or (len(visList) == 1 and visList[0]=="none"):
                        break
            

