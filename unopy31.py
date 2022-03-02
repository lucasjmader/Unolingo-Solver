#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import sys
import keyboard
import copy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui
import time
from selenium.webdriver.common.action_chains import ActionChains



sys.setrecursionlimit(9000)


#open scrabble file and make ogwordpool
my_file = open("scrab2.txt", "r")
content = my_file.read()
ogwordpool = content.split("\n")
my_file.close()


#class for words in the board that need to be finished
class wordspace():
    def __init__(self, row1, col1, row2, col2):
        self.row1 = row1
        self.col1 = col1
        self.row2 = row2
        self.col2 = col2
        self.wordpool = ogwordpool
        self.val = str
        self.ogval = str
        self.length = row2 - row1 + col2 - col1 + 1

#class for letter spaces
class space():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.horletpool = []
        self.vertletpool = []
        self.letterpool = []
        self.val= str
        self.ogval = str


#make ogletterpool
abc = 'abcdefghijklmnopqrstuvwxyz'
ogletterpool = list(abc)
for i, letet in enumerate(ogletterpool):
    ogletterpool[i] = ogletterpool[i].upper()
letleft = ogletterpool


#start webdriver in fullscreen at 75% zoom
PATH = 'chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.get("https://games.usatoday.com/games/uclick-unolingo")
driver.maximize_window()



#wait for user to press q
while True:
    try:
        if keyboard.is_pressed('q'):
            break
    except:
        break






#switch frames
driver.switch_to.default_content()
frame = driver.find_element_by_id('embedFrame')
driver.switch_to.frame(frame)



#fill selspacelist with starting values of spaces
selspacelist = []
for i in range(100):
    if i%10 == 0: selspacelist.append([])
    workstr = 'p' + str(i)
    workstr = f'"{workstr}"'    
    if driver.find_elements_by_xpath('//*[@id=' + workstr + ']')[0].get_attribute("class") == 'blank':
        selspacelist[-1].append('0')
    elif driver.find_elements_by_xpath('//*[@id=' + workstr + ']')[0].get_attribute("class") == 'user ui-droppable':
        selspacelist[-1].append('1')
    else:
        selspacelist[-1].append(driver.find_elements_by_xpath('//*[@id=' + workstr + ']')[0].get_attribute('innerHTML'))





#create spacelist with instances of space class. assign each space its ogval based on value in board
spacelist = []

#create spacelist
for row, roww in enumerate(selspacelist):
    currentlist = []
    for col, entry in enumerate(roww):
        workspace = space(row, col)
        workspace.ogval = selspacelist[row][col]
        currentlist.append(workspace)
    spacelist.append(currentlist)
    
for row, roww in enumerate(spacelist):
    for col, entry in enumerate(roww):
        spacelist[row][col].val = copy.deepcopy(spacelist[row][col].ogval)
        
        
    











# #find coordinates of each space using pyautogui
# tl = (pyautogui.locateOnScreen('tl1.png'))
# bl = (pyautogui.locateOnScreen('bl2.png'))
# br = (pyautogui.locateOnScreen('br4.png'))
#
# workstring = str(br)
# workstring = list(workstring)
#
# elist = []
# clist = []
#
# for i, letter in enumerate(workstring):
#     if letter == '=':
#         elist.append(i)
#     elif letter == ',' or letter == ')':
#         clist.append(i)
#
# combstr = ''
# for pos in range(elist[0]+1, clist[0]):
#     dig = workstring[pos]
#     combstr += dig
# x1 = int(combstr)
#
# combstr = ''
# for pos in range(elist[1]+1, clist[1]):
#     dig = workstring[pos]
#     combstr += dig
# y0 = int(combstr) -10
#
# workstring = str(bl)
# workstring = list(workstring)
#
# elist = []
# clist = []
#
# for i, letter in enumerate(workstring):
#     if letter == '=':
#         elist.append(i)
#     elif letter == ',' or letter == ')':
#         clist.append(i)
#
# combstr = ''
# for pos in range(elist[0]+1, clist[0]):
#     dig = workstring[pos]
#     combstr += dig
#
# combstr2 = ''
# for pos in range(elist[2]+1, clist[2]):
#     dig = workstring[pos]
#     combstr2 += dig
#
# x0 = int(combstr)+int(combstr2) + 5
#
# workstring = str(tl)
# workstring = list(workstring)
#
# elist = []
# clist = []
#
# for i, letter in enumerate(workstring):
#     if letter == '=':
#         elist.append(i)
#     elif letter == ',' or letter == ')':
#         clist.append(i)
#
# combstr = ''
# for pos in range(elist[1]+1, clist[1]):
#     dig = workstring[pos]
#     combstr += dig
# y1 = int(combstr)
#
# width = x1 - x0
#
# height = y1 - y0
#
# class pagspace:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
# xper = (width/10)+3
# yper = (height/10)-3
#
# tempx = x0
# tempy= y0
#
# pagspacelist = []
# for row in range(10):
#     tempx = x0
#     pagspacelist.append([])
#     for col in range(10):
#         pagspacelist[row].append(pagspace(tempx, tempy))
#         tempx += xper
#     tempy += yper










horwords = []
vertwords = []



#function to find the position of the space that is at the end of the given word
def findhorendspace(row, col):
    if col == 9:
        return col
    letter = spacelist[row][col].ogval
    nextletter = spacelist[row][col + 1].ogval
    if nextletter == '0':
        return col
    else:
        return(findhorendspace(row, col+1))

def searchhor(row, col):
    global horwords
    if row <= 9 and col <= 9:
        letter = spacelist[row][col].ogval
        if letter == '0':
            if col == 9 and row != 9:
                searchhor(row+1, 0)
            else:
                searchhor(row,col+1)
        else:
            if col == 9 and row != 9:
                searchhor(row+1, 0)
            elif letter != '0':
                answer = findhorendspace(row, col)
                if answer != col:
                    workcol1 = col
                    workrow1 = row
                    workcol2 = answer
                    workrow2 = row
                    workwordspace = wordspace(workrow1, workcol1, workrow2, workcol2)
                    horwords.append(workwordspace)
                    if answer <= 7:
                        searchhor(row, answer+1)
                    else:
                        searchhor(row+1, 0)
                elif answer == col:
                    searchhor(row, col+1)



#function to find the position of the space that is at the end of the given word
def findvertendspace(row, col):
    if row == 9:
        return row
    letter = spacelist[row][col].ogval
    nextletter = spacelist[row + 1][col].ogval
    if nextletter == '0':
        return row
    else:
        return(findvertendspace(row+1, col))

    
#function to search for all vert words and add them to vertwords list
def searchvert(row, col):
    global vertwords
    if row <= 9 and col <= 9:
        letter = spacelist[row][col].ogval
        if letter == '0':
            if row == 9 and col != 9:
                searchvert(0, col+1)
            else:
                searchvert(row+1,col)
        else:
            if row == 9 and col != 9:
                searchvert(0, col+1)
            elif letter != '0':
                answer = findvertendspace(row, col)
                if answer != row:
                    workcol1 = col
                    workrow1 = row
                    workcol2 = col
                    workrow2 = answer
                    workwordspace = wordspace(workrow1, workcol1, workrow2, workcol2)
                    vertwords.append(workwordspace)
                    if answer <= 7:
                        searchvert(answer+1, col)
                    else:
                        searchvert(0, col+1)
                elif answer == row:
                    searchvert(row+1, col)
                    
searchhor(0, 0)
searchvert(0,0)



#assign each wordspace its ogval
for i, word in enumerate(horwords):
    currentstr = ''
    row = word.row1
    for col in range(word.col1, word.col2+1):
        letter = spacelist[row][col].ogval
        letter = str(letter)
        currentstr += letter
    horwords[i].ogval = currentstr

#assign each wordspace its ogval
for i, word in enumerate(vertwords):
    currentstr = ''
    col = word.col1
    for row in range(word.row1, word.row2+1):
        letter = spacelist[row][col].ogval
        letter = str(letter)
        currentstr += letter
    vertwords[i].ogval = currentstr



#set each wordspace's val equal to their ogval
for i, word in enumerate(vertwords):
    vertwords[i].val = vertwords[i].ogval
    
for i, word in enumerate(horwords):
    horwords[i].val = horwords[i].ogval



#assign wordpools to wordspaces

#function to see if a word is eligible to be in a wordspace's wordpool
def iswordpossible(word1,word2):
    wordsofar = word1
    word = word2
    if len(word) != len(wordsofar):
        return False
    for i, letter2 in enumerate(word):
        letter = wordsofar[i]
        if letter != '1' and letter != letter2:
            return False
    return True



#add accurate wordpools to each horword
for i, thiswordspace in enumerate(horwords):
    list2 = []
    wordsofar = thiswordspace.val
    wordsofar = wordsofar.upper()
    wordsofar = list(wordsofar)
    for j, word in enumerate(thiswordspace.wordpool):
        word = list(word)
        if iswordpossible(wordsofar, word):
            word = ''.join(word)
            list2.append(word)
    horwords[i].wordpool = list2
    
#add accurate wordpools to each vertword
for i, thiswordspace in enumerate(vertwords):
    list2 = []
    wordsofar = thiswordspace.val
    wordsofar = wordsofar.upper()
    wordsofar = list(wordsofar)
    for j, word in enumerate(thiswordspace.wordpool):
        word = list(word)
        if iswordpossible(wordsofar, word):
            word = ''.join(word)
            list2.append(word)
    vertwords[i].wordpool = list2



#if space already has letter, make its letterpools that letter
for i, row in enumerate(spacelist):
    for j, thisspace in enumerate(row):
        value = thisspace.ogval
        if value == '1' or value == '0':
            continue
        else:
            spacelist[i][j].letterpool.clear()
            spacelist[i][j].horletpool.clear()
            spacelist[i][j].vertletpool.clear()
            spacelist[i][j].letterpool.append(value)
            spacelist[i][j].horletpool.append(value)
            spacelist[i][j].vertletpool.append(value)



#hor letterpool
for thiswordspace in horwords:
    row = thiswordspace.row1
    startcol = thiswordspace.col1
    endcol = thiswordspace.col2
    for word in thiswordspace.wordpool:
        word = list(word)
        for letpos, letter in enumerate(word):
            col = startcol + letpos
            currentlist = []
            correspace = spacelist[row][col]   
            thisogval = correspace.ogval
            if thisogval == '1':
                if letter in correspace.horletpool:
                    continue
                else:
                    spacelist[row][col].horletpool.append(letter)



#vert letterpool
for thiswordspace in vertwords:
    startrow = thiswordspace.row1
    endrow = thiswordspace.row2
    col = thiswordspace.col1
    for word in thiswordspace.wordpool:
        word = list(word)
        for letpos, letter in enumerate(word):
            row = startrow + letpos
            currentlist = []
            correspace = spacelist[row][col]   
            thisogval = correspace.ogval
            if thisogval == '1':
                if letter in correspace.vertletpool:
                    continue
                else:
                    spacelist[row][col].vertletpool.append(letter)



#combine letpools
for row, lisp in enumerate(spacelist):
    for col, thisspace in enumerate(lisp):
        horpool = thisspace.horletpool
        vertpool = thisspace.vertletpool
        letpool = thisspace.letterpool
        let2 = []
        hor2 = []
        vert2 = []
        if len(horpool) > 0 and len(vertpool) > 0:
            for i, letter in enumerate(horpool):
                if letter in vertpool:
                    hor2.append(letter)
            for i, letter in enumerate(vertpool):
                if letter in horpool:
                    vert2.append(letter)
            for i, letter in enumerate(horpool):
                if letter not in spacelist[row][col].letterpool:
                    spacelist[row][col].letterpool.append(letter)
            for i, letter in enumerate(vertpool):
                if letter not in spacelist[row][col].letterpool:
                    spacelist[row][col].letterpool.append(letter) 
            spacelist[row][col].horletpool = hor2
            spacelist[row][col].vertletpool = vert2
        else:
            spacelist[row][col].letterpool = horpool + vertpool
            


#if only one letter in letpool, make val that letter
for row, lisp in enumerate(spacelist):
    for col, thisspace in enumerate(lisp):
        letterpool = thisspace.letterpool
        if len(letterpool) == 1 and thisspace.val == '1':
            spacelist[row][col].val =letterpool[0]
            letleft.remove(letterpool[0])



#update wordpools for horword spaces based on letterpools for each letter
for i, thiswordspace in enumerate(horwords):
    list2 = []
    wordsofar = thiswordspace.val
    wordsofar = wordsofar.upper()
    wordsofar = list(wordsofar)
    row = thiswordspace.row1
    startcol = thiswordspace.col1
    #get wordpool
    list2 = []
    for j, word in enumerate(thiswordspace.wordpool):
        word = list(word)
        #get letter
        for k, letter in enumerate(word):
            letterrow = row
            lettercol = startcol + k
            correspace = spacelist[row][lettercol]
            correpool = correspace.letterpool
            if letter not in correpool:
                if j not in list2:
                    list2.append(j)
    for m, wordd in enumerate(list2):
        del horwords[i].wordpool[m]



#update wordpools for vertword spaces based on letterpools for each letter
for i, thiswordspace in enumerate(vertwords):
    list2 = []
    wordsofar = thiswordspace.val
    wordsofar = wordsofar.upper()
    wordsofar = list(wordsofar)
    startrow = thiswordspace.row1
    col = thiswordspace.col1
    #get wordpool
    list2 = []
    for j, word in enumerate(thiswordspace.wordpool):
        word = list(word)
        #get letter
        for k, letter in enumerate(word):
            letterrow = startrow + k
            lettercol = col
            correspace = spacelist[letterrow][lettercol]
            correpool = correspace.letterpool
            if letter not in correpool:
                if j not in list2:
                    list2.append(j)
    for m, wordd in enumerate(list2):
        del vertwords[i].wordpool[m]



#if only one letter in letpool, make val that letter
for row, lisp in enumerate(spacelist):
    for col, thisspace in enumerate(lisp):
        letterpool = thisspace.letterpool
        if len(letterpool) == 1 and spacelist[row][col].val == '1':
            spacelist[row][col].val =letterpool[0]
            letleft.remove(letterpool[0])








class boardclass:
    def __init__(self):
        self.wordspacelist = []
        self.spacelist = []
        self.letleft = []
        self.horwords = []
        self.vertwords = []



# reorganize wordlists
# start with sorting hor and vert separately

list1 = []
list2 = []

#for wordspace
for i, ws in enumerate(vertwords):
    #get wordpool
    wp = copy.deepcopy(ws.wordpool)
    #temp list
    werklist = []
    #get length of wordpool
    lengt = len(wp)
    #add length and pos of wordspace to list
    werklist = [lengt, i]
    #add temp list to list1
    list1.append(werklist)
    
    
#for list in list1
for i, nested in enumerate(list1):
    #get length
    valu = nested[0]
    #get pos
    poz = nested[1]
    #if empty, add
    if i == 0:
        list2.append(nested)        
    else:
        for j,nested2 in enumerate(list2):
            valu2 = nested2[0]
            if valu < valu2:
                list2.insert(j, nested)
                break
            elif j == len(list2) - 1:
                list2.append(nested)
                break



lisp = []
for nested in list2:
    pos = nested[1]
    lisp.append(copy.deepcopy(vertwords[pos]))

vertwords = copy.deepcopy(lisp)



# reorganize wordlists
# start with sorting hor and vert separately
list1 = []
list2 = []
for i, ws in enumerate(horwords):
    wp = copy.deepcopy(ws.wordpool)
    werklist = []
    lengt = len(wp)
    werklist = [lengt, i]
    list1.append(werklist)
    
for i, nested in enumerate(list1):
    valu = nested[0]
    poz = nested[1]
    if i == 0:
        list2.append(nested)        
    else:
        for j,nested2 in enumerate(list2):
            valu2 = nested2[0]
            if valu < valu2:
                list2.insert(j, nested)
                break
            elif j == len(list2) - 1:
                list2.append(nested)
                break

lisp = []

for nested in list2:
    pos = nested[1]
    lisp.append(copy.deepcopy(horwords[pos]))
    
horwords = copy.deepcopy(lisp)


#combine horwords and vertwords
allwords = horwords + vertwords



#create first instance of boardclass
firstboard = boardclass()
firstboard.wordspacelist = copy.deepcopy(allwords)
firstboard.spacelist = copy.deepcopy(spacelist)
firstboard.letleft = copy.deepcopy(letleft)
firstboard.horwords = copy.deepcopy(horwords)
firstboard.vertwords = copy.deepcopy(vertwords)



#assign each wordspace its val
def horwordsvals(board, horwords):
    for i, word in enumerate(horwords):
        currentstr = ''
        row = copy.deepcopy(word.row1)
        for col in range(word.col1, word.col2+1):
            letter = copy.deepcopy(board[row][col].val)
            letter = str(letter)
            currentstr += letter
        horwords[i].val = currentstr
    return horwords
        
        
#assign each wordspace its val
def vertwordsvals(board, vertwords):
    for i, word in enumerate(vertwords):
        currentstr = ''
        col = copy.deepcopy(word.col1)
        for row in range(word.row1, word.row2+1):
            letter = copy.deepcopy(board[row][col].val)
            letter = str(letter)
            currentstr += letter
        vertwords[i].val = currentstr
    return vertwords



#add accurate wordpools to each horword
def horwordpools(horwords):
    for i, thiswordspace in enumerate(horwords):
        list2 = []
        wordsofar = copy.deepcopy(thiswordspace.val)
        wordsofar = wordsofar.upper()
        wordsofar = list(wordsofar)
        for j, word in enumerate(thiswordspace.wordpool):
            word = copy.deepcopy(word)
            word = list(word)
            if iswordpossible(wordsofar, word):
                word = copy.deepcopy(word)
                word = ''.join(word)
                list2.append(word)
        horwords[i].wordpool = copy.deepcopy(list2)
    return horwords
    
#add accurate wordpools to each vertword
def vertwordpools(vertwords):
    for i, thiswordspace in enumerate(vertwords):
        list2 = []
        wordsofar = copy.deepcopy(thiswordspace.val)
        wordsofar = wordsofar.upper()
        wordsofar = list(wordsofar)
        for j, word in enumerate(thiswordspace.wordpool):
            word = copy.deepcopy(word)
            word = list(word)
            if iswordpossible(wordsofar, word):
                word = copy.deepcopy(word)
                word = ''.join(word)
                list2.append(word)
        vertwords[i].wordpool = copy.deepcopy(list2)
    return vertwords


# In[2]:


for row in selspacelist:
    worklist = []
    for col in row:
        worklist.append(col)
    print(worklist)


# In[3]:


for row in spacelist:
    worklist = []
    for col in row:
        worklist.append(col.val)
    print(worklist)


# In[4]:


for row in horwords:
    print(row.val)


# In[5]:





#functin to add a word to its respective wordspace and either return the updated board or return false
def updateboard(boardinstance, word, wordspacepos):
    
    #get variables
    spacelist = copy.deepcopy(boardinstance.spacelist)
    horwords = copy.deepcopy(boardinstance.horwords)
    vertwords = copy.deepcopy(boardinstance.vertwords)
    wordspacelist = copy.deepcopy(boardinstance.wordspacelist)
    wordspace = copy.deepcopy(wordspacelist[wordspacepos])
    letleft = copy.deepcopy(boardinstance.letleft)

    print('trying')
    print(word)
    
    #add word to board
    
    #get list of letters in word
    word = list(word)
    
    #get positions of spaces in wordspace
    wsrow1 = wordspace.row1
    wsrow2 = wordspace.row2
    wscol1 = wordspace.col1
    wscol2 = wordspace.col2
    
    #var to track which letter of added word i am on
    y = 0
    
    

#     #get spacelist vals from board
#     for row, rowlist in enumerate(spacelist):
#         for col, thisspace in enumerate(rowlist):
#             spacelist[row][col].val = copy.deepcopy(board[row][col])
            
            
    #for loop to add letter of word to each space in wordspace
    templetleft = copy.deepcopy(letleft)
    for row in range(wsrow1, wsrow2+1):
        for col in range(wscol1, wscol2+1):
            letter = copy.deepcopy(word[y])
            letternow = copy.deepcopy(spacelist[row][col].val)
            if letter != letternow and letternow != '1':
                print(1)
                return False
            elif letter == letternow and letternow != '1':
                y += 1
                continue
            else:
                if letter in templetleft:
                    spacelist[row][col].val = copy.deepcopy(letter)
                    templetleft.remove(letter)
                    y += 1
                elif letter != letternow and letternow == '1':
            
                    print(' ')
                    print(templetleft)
                    print(letter)
                    print(letternow)
                    print(2)
                    print(' ')
                    return False

    letleft = copy.deepcopy(templetleft)
                

    
#     after adding word

    #wordspace vals
    horwords = horwordsvals(spacelist, horwords)
    vertwords = vertwordsvals(spacelist, vertwords)
    
    #wordpools
    horwords = horwordpools(horwords)
    vertwords = vertwordpools(vertwords)

    
    
    #clear letterpools so they can be remade
    for row, bob in enumerate(spacelist):
        for col, joe in enumerate(spacelist):
            spacelist[row][col].horletpool = []
            spacelist[row][col].vertletpool = []
            spacelist[row][col].letterpool = []
    
    
    #if already has val, make letterpool that val
    for i, row in enumerate(spacelist):
        for j, thisspace in enumerate(row):
            value = copy.deepcopy(thisspace.val)
            if value == '1' or value == '0':
                continue
            else:
                spacelist[i][j].letterpool.clear()
                spacelist[i][j].horletpool.clear()
                spacelist[i][j].vertletpool.clear()
                spacelist[i][j].letterpool.append(value)
                spacelist[i][j].horletpool.append(value)
                spacelist[i][j].vertletpool.append(value)
                
                

    #hor letterpools
    #loop through wordspaces in horwords
    for thiswordspace in horwords:
        #get coordinates of wordspace
        row = copy.deepcopy(thiswordspace.row1)
        startcol = copy.deepcopy(thiswordspace.col1)
        endcol = copy.deepcopy(thiswordspace.col2)
        #loop thru words in wordpool
        for word in thiswordspace.wordpool:
            word = list(word)
            #loop thru letters in word
            for letpos, letter in enumerate(word):
                #get column for corresponding space
                col = startcol + letpos
                currentlist = []
                #get correspace
                correspace = copy.deepcopy(spacelist[row][col])
                #get ogval
                thisogval = copy.deepcopy(correspace.ogval)
                if thisogval == '1' and letter in letleft:
                    #letter = letter pulled from wordpool word
                    if letter in correspace.horletpool:
                        continue
                    else:
                        spacelist[row][col].horletpool.append(letter)
                    
    
    #vert letterpool
    for thiswordspace in vertwords:
        startrow = copy.deepcopy(thiswordspace.row1)
        endrow = copy.deepcopy(thiswordspace.row2)
        col = copy.deepcopy(thiswordspace.col1)
        for word in thiswordspace.wordpool:
            word = list(word)
            for letpos, letter in enumerate(word):
                row = startrow + letpos
                currentlist = []
                correspace = copy.deepcopy(spacelist[row][col])  
                thisogval = copy.deepcopy(correspace.ogval)
                if thisogval == '1' and letter in letleft:
                    if letter in correspace.vertletpool:
                        continue
                    else:
                        spacelist[row][col].vertletpool.append(letter)
                        

                        
    #combine letterpools                    
    for row, lisp in enumerate(spacelist):
        for col, thisspace in enumerate(lisp):
            horpool = copy.deepcopy(thisspace.horletpool)
            vertpool = copy.deepcopy(thisspace.vertletpool)
            spacelist[row][col].letterpool = []
            let2 = []
            hor2 = []
            vert2 = []
            if len(horpool) > 0 and len(vertpool) > 0:
                for i, letter in enumerate(horpool):
                    if letter in vertpool:
                        hor2.append(letter)
                for i, letter in enumerate(vertpool):
                    if letter in horpool:
                        vert2.append(letter)
                for i, letter in enumerate(hor2):
                    if letter not in spacelist[row][col].letterpool:
                        spacelist[row][col].letterpool.append(letter)
                for i, letter in enumerate(vert2):
                    if letter not in spacelist[row][col].letterpool:
                        spacelist[row][col].letterpool.append(letter) 
                spacelist[row][col].horletpool = copy.deepcopy(hor2)
                spacelist[row][col].vertletpool = copy.deepcopy(vert2)
                
            else:
                spacelist[row][col].letterpool = horpool + vertpool


                
    #if only one letter in letterpool, make val that letter            
    for row, lisp in enumerate(spacelist):
        for col, thisspace in enumerate(lisp):
            letterpool = copy.deepcopy(thisspace.letterpool)
            if len(letterpool) == 1 and spacelist[row][col].val == '1':
                if letterpool[0] in letleft:
                    spacelist[row][col].val = copy.deepcopy(letterpool[0])
                    letleft.remove(letterpool[0])
                else:
                    print(3)
                    return False
                
                


    #update horwordpools based on combined letterpools            
    for i, thiswordspace in enumerate(horwords):
        wordsofar = copy.deepcopy(thiswordspace.val)
        wordsofar = wordsofar.upper()
        wordsofar = list(wordsofar)
        row = copy.deepcopy(thiswordspace.row1)
        startcol = copy.deepcopy(thiswordspace.col1)        
        list2 = []
        #get wordpool
        for j, word in enumerate(thiswordspace.wordpool):
            word = list(word)
            #get letter
            for k, letter in enumerate(word):
                list2 = []
                letterrow = row
                lettercol = startcol + k
                correspace = copy.deepcopy(spacelist[row][lettercol])
                correpool = copy.deepcopy(correspace.letterpool)
                if letter not in correpool and j not in list2:
                    list2.append(j)
                    break
                elif letter not in correpool and j in list2:
                    break
                        
#         for m, lettpos in enumerate(list2):
        for m in range(len(list2)-1,-1,-1):
            lettpos = copy.deepcopy(list2[m])
            try:
                del horwords[i].wordpool[lettpos]
            except IndexError:
                print(4)
                return False
            
    #update vertwordpools based on combined letterpools        
    for i, thiswordspace in enumerate(vertwords):
#         list2 = []
        wordsofar = copy.deepcopy(thiswordspace.val)
        wordsofar = wordsofar.upper()
        wordsofar = list(wordsofar)
        startrow = copy.deepcopy(thiswordspace.row1)
        col = thiswordspace.col1
        #get wordpool
        list2 = []
        for j, word in enumerate(thiswordspace.wordpool):
            word = list(word)
            #get letter
            for k, letter in enumerate(word):
#                 list2 = []
                letterrow = startrow + k
                lettercol = col
                correpool = copy.deepcopy(spacelist[letterrow][lettercol].letterpool)
#                 correpool = copy.deepcopy(correspace.letterpool)
                if letter not in correpool and j not in list2:
                    list2.append(j)
                    break
                elif letter not in correpool and j in list2:
                    break
                        



        for m in range(len(list2)-1,-1,-1):
            lettpos = copy.deepcopy(list2[m])
            try:                
                del vertwords[i].wordpool[lettpos]
            except IndexError:
                print(5)
                return False

    
    
    #see if an unfinished word has nothing in its wordpool and if so, return false
    for i, awordspace in enumerate(horwords):
        awordpool = copy.deepcopy(awordspace.wordpool)
        aval = copy.deepcopy(awordspace.val)
        aval = list(aval)
        if len(awordpool) < 1 and '1' in aval:
            print(6)
            return False
        
        
    #see if an unfinished word has nothing in its wordpool and if so, return false
    for i, awordspace in enumerate(vertwords):
        awordpool = copy.deepcopy(awordspace.wordpool)
        if len(awordpool) == 0:
            print(7)
            return False

            
            
#     #update actual board
#     for row, rowlist in enumerate(spacelist):
#         for col, thisspace in enumerate(rowlist):
#             board[row][col] = copy.deepcopy(spacelist[row][col].val)

    

    #combine wordspace lists
    wordspacelist = horwords + vertwords
    
    boardinstance.wordspacelist = copy.deepcopy(wordspacelist)
    boardinstance.spacelist = copy.deepcopy(spacelist)
    boardinstance.letleft = copy.deepcopy(letleft)
    boardinstance.horwords = copy.deepcopy(horwords)
    boardinstance.vertwords = copy.deepcopy(vertwords)
    
    return boardinstance
    

#function that recursively selects words to try for each wordspace, returning the final board in the end
def doit(lisp):
    #get vars from input
    boardinstance = copy.deepcopy(lisp[-1][0])
    wordspacepos = copy.deepcopy(lisp[-1][1])
    wordpos = copy.deepcopy(lisp[-1][2])
    wordpool1 = copy.deepcopy(boardinstance.wordspacelist[wordspacepos].wordpool)
    wordspacelist = copy.deepcopy(boardinstance.wordspacelist)
    
    print(boardinstance.wordspacelist[wordspacepos].val)
    print(wordspacepos)
    print(wordpool1)

    if wordpos > len(wordpool1) -1:
        for row in spacelist:
            worklist = []
            for col in row:
                worklist.append(col.val)
            print(worklist)
        print(' ')
                

#         print(wordpool1[wordpos])
        del lisp[-1]
        lisp[-1][2] +=1
        return doit(lisp)

    #get val of word
    word = copy.deepcopy(wordpool1[wordpos])
    
    #get updated board class
    newboard = updateboard(boardinstance,word,wordspacepos)
    
    #if updateboard worked
    if newboard:
        print('updateboard worked')
        #see if board is finished
        if wordspacepos == len(wordspacelist) - 1:
            #return final board
            return newboard
        #get pos of next wordspace in wordspacelist
        wordspacepos2 = wordspacepos + 1
        #get next wordpool
        wordpool2 = copy.deepcopy(newboard.wordspacelist[wordspacepos2].wordpool)
        #if there are no words available in wordpool
        if len(wordpool2) == 0:
            #if there is another word available to try
            if wordpos < len(wordpool1) - 1:
                #change the wordpos in input lisp to next word in wordpool
                lisp[-1][2] = lisp[-1][2] + 1
                #run doit with this new input
                return doit(lisp)
            #if this input word was the last word in the wordpool
            elif wordpos == len(wordpool) - 1:
                #remove the last list from lisp
                del lisp[-1]
                #in the list before the list that was just deleted, change wordpos to next word
                lisp[-1][2] +=1
                #run doit with this new input
                return doit(lisp)
        #if there are words available in this new wordpool
        else:
            worklist = []
            worklist = [newboard, wordspacepos+1, 0]
            #append this new list to lisp
            lisp.append(worklist)
            #run doit with updated lisp
            return doit(lisp)
            
    #if updateboard didnt work
    elif newboard == False:
        print('nope')
        #try again with next word
        del lisp[-1]
        lisp.append([boardinstance, wordspacepos, wordpos+1])
        return doit(lisp)    



startinglist = [[firstboard, 0, 0]]

answerr = doit(startinglist)



finalspacelist = answerr.spacelist

# for row in finalspacelist:
#     worklist = []
#     for col in row:
#         if col.val == '0':
#             worklist.append(' ')
#         else:
#             worklist.append(col.val)
#
#
#
# #finish board on unolingo website
# for row, i in enumerate(pagspacelist):
#     for col, j in enumerate(i):
#         #see if letter needs to be added
#         correspace = copy.deepcopy(finalspacelist[9-row][col])
#         ogvalue = correspace.ogval
#         value = correspace.val
#         if ogvalue == '1':
#             pyautogui.click(pagspacelist[row][col].x, pagspacelist[row][col].y)
#             pyautogui.write(str(value))
#




# In[8]:


selspacelist = []
for i in range(100):
    row = int(i/10)
    col = i-(row*10)
    print(i)
    print(row)
    print(col)
    
    print(finalspacelist[row][col].ogval)
    valu = finalspacelist[row][col].val
    print(valu)
    
    workstr = 'p' + str(i)
    workstr = f'"{workstr}"'
    yet = driver.find_element_by_xpath('//*[@id=' + workstr + ']')
    if finalspacelist[row][col].ogval == '1':
        print('ye')
        actions = ActionChains(driver)
        actions.move_to_element(yet).click().perform()
        pyautogui.write(valu)
    print(' ')

