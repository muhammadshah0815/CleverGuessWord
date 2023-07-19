'''

@author: Muhammad Shah    mas292

'''

import random


def handleUserInputDifficulty():
    '''
    This function asks the user if they would like
    to play the game in (h)ard or (e)asy mode,
    then returns the corresponding number of misses
    allowed for the game.
    '''

    print("How many misses do you want? Hard has 8 and Easy has 12.")
    a = input(str("(h)ard or (e)asy> "))
    numMisses = 0
    if a == 'h':
        numMisses = 8
    else:
        numMisses = 12

    return numMisses


def createDisplayString(lettersGuessed, missesLeft, guessedWordAsList):
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    '''

    letternotguessedstring="abcdefghijklmnopqrstuvwxyz"
    letternotguessedlist=[l for l in letternotguessedstring]
    for l in lettersGuessed:
        if l in letternotguessedstring:
            letternotguessedlist[letternotguessedstring.index(l)]=" "

    newString2 = ' '.join(guessedWordAsList)
    return "letters not yet guessed: " + ''.join(letternotguessedlist) + "\n"\
           + \
           "misses remaining = " + \
           str(missesLeft) + "\n" + newString2


def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    '''
    print(displayString)
    a = input(str("letter> "))
    while a in lettersGuessed:
        print("you already guessed that")
        a = input(str("letter> "))

    return a

def handleUserInputDebugMode():
    ''' asks user for input on debug mode and returns True if debug mode on'''
    a=str(input("Which mode do you want: (d)ebug or (p)lay: "))
    if a=='d':
        return True
    else:
        return False

def handleUserInputWordLength():
    ''' asks user for word length and returns that integer'''
    a = int(input("How many letters in the word you'll guess: "))
    return a

def createTemplate(currTemplate, letterGuess, word):
    ''' updates the current template. if a letter is guessed correctly,
    this function replaces the underscore with the actual letter'''
    newlst=[l for l in word]
    currTemplatelst=[l for l in currTemplate]
    index=0
    for l in newlst:
        if l==letterGuess:
            currTemplatelst[index]=l
        index+=1
    return ''.join(currTemplatelst)

def getNewWordList(currTemplate, letterGuess, wordList, debug):
    ''' updates the current template on every word in wordlist. if a letter is guessed correctly,
        createTemplate replaces the underscore with the actual letter.The function returns a 2-tuple. The first element of the return tuple is a new template (string), and the second element of the return tuple is the new list of possible secret words, each of which matches the template.'''
    lst=[]
    lst2=[]
    d={}
    index=0
    for x in wordList:
        lst.append(createTemplate(currTemplate, letterGuess, x))
        lst2.append(x)
        d[createTemplate(currTemplate, letterGuess, x)]=[]
    for x in lst:
        d[x].append(lst2[index])
        index+=1



    a=sorted([(k, v) for k,v in d.items()], key=lambda x: (-len(x[1]),
                                                           -x[0].count("_")))
    getNewWordList.word = a[0][1][random.randint(0, len(a[0][1])-1)]
    if debug==True:
        for k, v in sorted(d.items()):

            print(k + " : " + str(len(v)))
        print("# keys = " + str(len(d.keys())))
        print("(word is " + getNewWordList.word + ")")
        print("# possible words:", sum([len(v) for k, v in sorted(d.items())],
                                        0))
    return a[0]
#print(getNewWordList("____", "O", [ "OBOE", "NOON", "ODOR", "ROOM", "SOLO",
# "TRIO", "GOTO", "OATH", "OXEN", "PICK", "FRAT", "HOOP"],debug=True))

def processUserGuessClever(guessedLetter, guessedWordAsList, missesLeft):
    '''updates misses if letter is guessed. if it is not guessed correctly,
    the function counts it as a miss, and updates missesleft accordingly'''
    if guessedLetter not in guessedWordAsList:
        missesLeft-=1
        return [missesLeft, False]
    else:
        return [missesLeft, True]

def runGame(filename):
    '''
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    '''

    debug = handleUserInputDebugMode()

    with open(filename, 'r') as f:
        uneditedwordlist = [ line.strip() for line in f ]
    wordlength = handleUserInputWordLength()
    missesLeft = handleUserInputDifficulty()

    wordList=[]
    lettersGuessed=""
    guessedWordAsList=[]

    for x in uneditedwordlist:
        if len(x)==wordlength:
            wordList.append(x)

    for x in range(int(wordlength)):
        guessedWordAsList.append("_")

    while (missesLeft != 0) or ("_" in guessedWordAsList):
        displaystring=createDisplayString(lettersGuessed, missesLeft,
                                  guessedWordAsList)
        guessedLetter = handleUserInputLetterGuess(lettersGuessed, displaystring)
        lettersGuessed+=guessedLetter
        a=getNewWordList(guessedWordAsList, guessedLetter, wordList, debug)
        guessedWordAsList=a[0]
        wordList=a[1]
        word = a[1][random.randint(0, len(a[1]) - 1)]
        b=processUserGuessClever(guessedLetter, guessedWordAsList, missesLeft)
        missesLeft=b[0]
        if b[1]==False:
            print("you missed:", guessedLetter, "not in word")
        if "_" not in guessedWordAsList:
            print("you guessed the word: " + guessedWordAsList)
            return True
        if missesLeft == 0:
            print("you're hung!!")
            print("word is", getNewWordList.word)
            return False




if __name__ == "__main__":
    '''
    Running GuessWord.py should start the game, which is done by calling runGame, therefore, we have provided you this code below.
    '''
    y=runGame("/Users/shah/Downloads/assign3f22-transform/data/lowerwords.txt")
    p=0
    q=0
    if y == True:
        q += 1
    else:
        p += 1
    a=input(str("Do you want to play again? y or n> "))
    while a!='n':
        y=runGame('/Users/shah/Downloads/assign3f22-transform/data/lowerwords.txt')
        if y==True:
            q+=1
        else:
            p+=1
        a = input(str("Do you want to play again? y or n> "))
    print("You won", q, "game(s) and lost", p)






'''gameStatus = False
    guesses = 0
    lettersGuessed = ""
    actualguessedWord = []
    guessedWordAsList = []
    for letter in theWord:
        actualguessedWord.append(letter)
    for letter in theWord:
        guessedWordAsList.append("_")
    guessedWordAsList.pop()
    while (missesLeft != 0) or ("_" in guessedWordAsList):
        print(createDisplayString(lettersGuessed, missesLeft,
                                  guessedWordAsList))
        guessedLetter = handleUserInputLetterGuess(lettersGuessed, missesLeft)
        guesses += 1
        c = processUserGuess(guessedLetter, theWord, guessedWordAsList,
                             missesLeft)
        if guessedLetter not in actualguessedWord:
            missesLeft -= 1
            print("you missed:", guessedLetter, "not in word")
            print()
        if missesLeft == 0:
            gameStatus = False
            print("you're hung!!")
            print("word is", theWord)
            break
        if "_" not in guessedWordAsList:
            gameStatus = True
            print("you guessed the word:" + theWord)
            break
        lettersGuessed += guessedLetter
    print("you made", guesses, "guesses with", totalMisses, "misses")
    return gameStatus'''