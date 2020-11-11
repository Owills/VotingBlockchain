from hashlib import sha256
import tkinter as tk
from tkinter.ttk import *
from tkinter import  *
import random
import _pickle as pickle
import re
from datetime import datetime
from itertools import islice

class Block:
    def __init__(self, da, de, ph, i, di):
        self._data = da
        self._date = de
        self._previousHash = ph
        self._index = i
        self._difficulty = di
        self._nonce = 0
    def getDate(self):
        return self._date
    def getData(self):
        return self._data
    def getDifficulty(self):
        return self._difficulty
    def getPreviousHash(self):
        return self._previousHash
    def setPreviousHash(self, ph):
        self._previousHash = ph
    def getIndex(self):
        return self._index
    def getNonce(self):
        return self._nonce
    def setNonce(self, n):
        self._nonce = n
    def setIndex(self, i):
        self._index= i
    def getCanidate(self):
        s = self._data.split(" ", 1)
        return s[1]
    def getUserHash(self):
        s = self._data.split(" ", 1)
        return s[0]
    def printAll(self):
        print("Nonce: "+ str(self._nonce))
        print("Previous Hash: " + self._previousHash)
        print("Index: " + str(self._index))
        print("Difficulty: " + str(self._difficulty))
        print("Data: " +  self._data)
        print("Date: " + self._date)
class BlockChain:
    _chain = []
    def __init__(self):
        self._chain.append(Block("Genisis Block", "0", "Genisis Block", 0, 3))
        self._difficulty = 3
        self.mineBlock(self._chain[0])
    def getDifficulty(self):
        return self._difficulty
    def setDifficulty(self, num):
        self._difficulty = num
    def setIndex(self):
        for i in range(0,self._chain.__len__()):
            self.getBlock(i).setIndex(i)
    def setChain(self, bc):
        self._chain = bc
        self.setDifficulty(self.getBlock(self._chain.__len__()-1).getDifficulty())
    def validateChain(self):
        for b in (self._chain):
            i = b.getIndex()
            if i < self._chain.__len__() - 1:
                if not self.hash(self.getFullData(b)).__eq__(self._chain[i+1].getPreviousHash()):
                    return i
            if i < self._chain.__len__() -1:
                leadingZeros = ""
                for num in range(0, b.getDifficulty()):
                    leadingZeros += "0"
                if not self.hash(self.getFullData(b)).startswith(leadingZeros):
                    return i
        return -1
    def removeBlock(self, i):
        self._chain.pop(i)
        self.setIndex()
        n = self.validateChain()
        self.remineChain(n)
    def remineChain(self, n):
        for num in range(n,self._chain.__len__()):
            if not num == 0:
                self.getBlock(num).setPreviousHash(self.hash(self.getFullData(self.getBlock(num-1))))
            self.getBlock(num).setNonce(0)
            self.mineBlock(self.getBlock(num))
    def mineChain(self, n):
        for num in range(n,self._chain.__len__()):
            self.mineBlock(self.getBlock(num))
    def mineBlock(self, b):
        leadingZeros = ""
        for i in range(0,b.getDifficulty()):
            leadingZeros += "0"
        hashed = self.hash(self.getFullData(b))
        while not(hashed.startswith(leadingZeros)):
            b.setNonce(b.getNonce() + 1)
            hashed = self.hash(self.getFullData(b))
        return "Hash: " + hashed + " Nonce: " + str(b.getNonce()) + " Difficulty: " + str(b.getDifficulty())
    def addBlock(self, b):
        if self.validateChain() == -1:
            self._chain.append(b)
            return "Block Added Successfully"
        return "Chain Invalid"
    def getFullData(self, b):
        return b.getData() + b.getDate() + b.getPreviousHash() + str(b.getNonce())
    def hash(self,s):
        return sha256(s.encode()).hexdigest()
    def getBlock(self,i):
        return self._chain[i]
    def getChain(self):
        return self._chain

class voterRegistry:
    def __init__(self):
        self._votersList = {}
    def addVoter(self, v):
        self._votersList[v.getUsername()] = v
    def uniqueUsernameCheck(self, u):
        # if u.find(',')!=-1:
        #     return "Username Must Not Contains Commas"
        if len(u) < 7:
            return "Username Must Be At Least Seven Characters"
        if len(self._votersList) >0:
            if u in self._votersList:
                return "Username Already Exists"
        return True
    def passwordStrengthCheck(self,p, cp):
        print(p)
        if not p == cp:
            return "Passwords Must Match"
        if len(p) < 7:
            return "Password Must Be At Least Seven Characters"
        if not re.search(r"[A-Z]",p):
            return "Password Must Contain Capital Letters"
        if not re.search("[a-z]", p):
            return "Password Must Contain Lowercase Letters"
        if not re.search("[0-9]", p):
            return "Password Must Contain Numbers"
        return True
    def checkName(self, n):
        if len(n) == 0:
            return "Please Enter Your Full Name"
        return True
    def hash(self,s):
        return sha256(s.encode()).hexdigest()
    def getSalt(self):
        ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chars = []
        for i in range(16):
            chars.append(random.choice(ALPHABET))
        return "".join(chars)
    def getRegistry(self):
        return self._votersList
    def setRegistry(self, r):
        self._votersList = r
class Voter:
    def __init__(self, u, hp, s, n):
        self._username = u
        self._hashedPassword = hp
        self._salt = s
        self._name = n
        self.hasVotedBoolean = False
    def getUsername(self):
        return self._username
    def getHashedPassword(self):
        return self._hashedPassword
    def getSalt(self):
        return self._salt
    def getName(self):
        return self._name
    def printAll(self):
        print ("Username: " + self._username)
        print("Hash: " + self._hashedPassword)
        print("Salt: " + self._salt)
        print("Name: " + self._name)
    def hasVoted(self):
        return self.hasVotedBoolean
    def makeVote(self, t): #Typically always true
        self.hasVotedBoolean = t

def readFile(f):
    with open(f, 'rb') as input:
        return pickle.load(input)
def writeFile(f, l):
    with open(f, "wb") as output:
        pickle.dump(l, output, 5)
#Data, Nonce, Difficulty, PreviousHash
#Username, HP, salt, name, hasVoted
def writeTextFile(f, l, type):
    file = open(f,"w")
    if type == 'BC':
        for b in l:
            file.write(b.getData() + "\n" + b.getDate() + "\n" + b.getPreviousHash() + "\n" + str(b.getIndex()) + "\n" + str(b.getDifficulty())+ "\n" + str(b.getNonce()) + "\n")
            file.write("\n")
    elif type == "VR":
        for k , v in l.items():
            file.write(v.getUsername() + "\n" + v.getHashedPassword() + "\n" + v.getSalt() + "\n" + v.getName() + "\n")
            if(v.hasVoted()):
                file.write("True\n")
            else:
                file.write("False\n")
            file.write("\n")
def readTextFile(f, type):
    file = open(f, "r")
    if type == 'BC':
        bc = []
        while(True):
            blocks = list(islice(file, 7))
            for i in range(0, blocks.__len__()):
                blocks[i] = blocks[i].replace('\n', '')
            if not blocks:
                break
            b = Block(blocks[0],blocks[1],blocks[2],int(blocks[3]),int(blocks[4]))
            b.setNonce(int(blocks[5]))
            bc.append(b)
        return bc
    elif type == "VR":
        pass

def getValidTextFile():
    file = open('blockchain.text', "r")
    data = file.read().replace('\n', '')
    data = sha256(data.encode()).hexdigest()

    file = open('blockchain1.text', "r")
    data1 = file.read().replace('\n', '')
    data1 = sha256(data1.encode()).hexdigest()

    file = open('blockchain2.text', "r")
    data2 = file.read().replace('\n', '')
    data2 = sha256(data2.encode()).hexdigest()

    file = open('blockchain3.text', "r")
    data3 = file.read().replace('\n', '')
    data3 = sha256(data3.encode()).hexdigest()

    file = open('blockchain4.text', "r")
    data4 = file.read().replace('\n', '')
    data4 = sha256(data4.encode()).hexdigest()

    datas = [data, data1, data2, data3, data4]
    uniqueDatas = set(datas)
    num = 0
    bestNum = 0
    bestData = data
    for d in uniqueDatas:
        for d2 in datas:
            if d == d2:
                num += 1
        if num > bestNum:
            bestNum = num
            bestData = d
        num = 0
    if bestData == data:
        return 'blockchain.text'
    if bestData == data1:
        return 'blockchain1.text'
    if bestData == data2:
        return 'blockchain2.text'
    if bestData == data3:
        return 'blockchain3.text'
    if bestData == data4:
        return 'blockchain4.text'
def writeToAllTextFiles(mainChain,type):
    if type == 'BC':
        writeFile('blockchain.pickle', mainChain.getChain())

        writeTextFile('blockchain.text', mainChain.getChain(), type)
        writeTextFile('blockchain1.text', mainChain.getChain(), type)
        writeTextFile('blockchain2.text', mainChain.getChain(), type)
        writeTextFile('blockchain3.text', mainChain.getChain(), type)
        writeTextFile('blockchain4.text', mainChain.getChain(), type)

class Window:
    def __init__(self, title):
        self.root = Tk()
        self.root.geometry("700x500")
        self.root.title(title)
        self.root.resizable(False, False)
        self.labels = []
        self.labelTexts = []
        self.buttons = []
        self.entrys = []
        self.entryText = []
    def addLabel(self, t, x, y):
        text = StringVar()
        text.set(t)
        self.labels.append(Label(self.root,textvariable=text).place(x=x-125, y=y, width=550))
        self.labelTexts.append(text)
        self.setLabelText(self.labelTexts.__len__()-1, t)
    def addButton(self,t,x,y,c):
        btn = Button(self.root, text=t, command=c)
        btn.place(x=x, y=y, width=120)
        self.buttons.append(btn)
    def addEntry(self, x, y):
        t = tk.StringVar()
        tempEntry = Entry(self.root, width=15, textvariable=t)
        tempEntry.place(x=x, y=y, width=120)
        self.entryText.append(t)
        self.entrys.append(tempEntry)
    def hideWidget(self, w):
        w.place_forget()
    def getButton(self, i):
        return self.buttons[i]
    def getButtons(self):
        return self.buttons
    def getEntryText(self, i):
        return self.entryText[i].get()
    def getRoot(self):
        return self.root
    def run(self):
        self.root.mainloop()
    def clearEntrys(self):
         for u in self.entryText:
             u.set("")
    def setLabelText(self, i, t):
        self.labelTexts[i].set(t)
    def giveIndex(self, i):
        self.index = i
    def getIndex(self):
        return self.index

def main():
    mainChain = BlockChain()
    f = getValidTextFile()
    mainChain.setChain(readTextFile(f, 'BC'))

    writeToAllTextFiles(mainChain, 'BC')


    voters = voterRegistry()
    voters.setRegistry(readFile("voters.pickle"))

    writeFile("voters.pickle", voters.getRegistry())
    writeTextFile('voters.text', voters.getRegistry(), 'VR')

    #voters.getRegistry()["Username"].printAll() Username, Username1, Username2, Username3, Username 4, Password123

    startWindow(voters, mainChain)
def startWindow(voters, mainChain):
    startingWindow = Window("Voting Blockchain")
    startingWindow.addButton('View Public Chain', 290, 100,lambda: viewPublicChainWindow(startingWindow,voters, mainChain))
    startingWindow.addButton('Register to Vote', 290, 150,lambda: registerToVoteWindow(startingWindow,voters, mainChain))
    startingWindow.addButton('Login', 290, 200,lambda: loginWindow(startingWindow,voters, mainChain, "account"))
    startingWindow.run()

def registerToVoteWindow(startWindow, voters, mainChain):
    startWindow.getRoot().destroy()
    del startWindow

    rtvWindow = Window("Register To Vote")
    rtvWindow.addButton('Return Home',290,100,lambda: returnHome(rtvWindow, voters, mainChain))

    rtvWindow.addLabel("Username: ", 200, 130)
    rtvWindow.addEntry(290,147)

    rtvWindow.addLabel("Full Name: ", 200, 180)
    rtvWindow.addEntry(290,197)

    rtvWindow.addLabel("Password: ", 200, 230)
    rtvWindow.addEntry(290,247)

    rtvWindow.addLabel("Confirm Password:", 200, 280)
    rtvWindow.addEntry(290,297)

    rtvWindow.addLabel(" ", 200, 350)
    rtvWindow.addButton("Create Account", 420, 297,lambda: createAccount(rtvWindow, voters))
    rtvWindow.run()
def createAccount(rtvWindow, voters):
    #rtvWindow.getEntryText(0),rtvWindow.getEntryText(1),rtvWindow.getEntryText(2), rtvWindow.getEntryText(3)
    #user, name, pass, conpass
    userReturn = voters.uniqueUsernameCheck(rtvWindow.getEntryText(0))
    if not userReturn == True:
         rtvWindow.setLabelText(4, userReturn)
         rtvWindow.clearEntrys()
         return
    nameReturn = voters.checkName(rtvWindow.getEntryText(1))
    if not nameReturn == True:
        rtvWindow.setLabelText(4, nameReturn)
        rtvWindow.clearEntrys()
        return
    passReturn = voters.passwordStrengthCheck(rtvWindow.getEntryText(2), rtvWindow.getEntryText(3))
    if not passReturn == True:
        rtvWindow.setLabelText(4,passReturn)
        rtvWindow.clearEntrys()
        return
    s = voters.getSalt()
    hp = voters.hash(rtvWindow.getEntryText(2) + s)
    v = Voter(rtvWindow.getEntryText(0), hp, s,rtvWindow.getEntryText(1))
    voters.addVoter(v)
    writeFile("voters.pickle", voters.getRegistry())
    rtvWindow.setLabelText(4, "Account Created")
    rtvWindow.clearEntrys()

def makeVoteWindow(lWindow, voters, mainChain, v):
    lWindow.getRoot().destroy()
    del lWindow

    mvWindow = Window("Make Vote")
    mvWindow.addButton('Return Home', 290, 100, lambda: returnHome(mvWindow, voters, mainChain))

    mvWindow.addButton("Canidate 1", 290, 237, lambda: makeVote(mvWindow, voters, mainChain, "Canidate 1", v))
    mvWindow.addButton("Canidate 2", 290, 287, lambda: makeVote(mvWindow, voters, mainChain, "Canidate 2", v))
    mvWindow.addButton("Canidate 3", 290, 337, lambda: makeVote(mvWindow, voters, mainChain, "Canidate 3", v))
    mvWindow.addLabel(" ", 200, 370)
    mvWindow.run()
def makeVote(mvWindow, voters, mainChain, nominee, v):
    if (v.hasVoted()):
        mvWindow.setLabelText(0, "User Has Already Voted")
        return
    v.makeVote(True)
    i = mainChain.getChain().__len__()
    de = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    ph = mainChain.hash(mainChain.getFullData(mainChain.getBlock(i-1)))
    di = mainChain.getDifficulty()
    b = Block(voters.hash(v.getUsername()) + " " + nominee,de,ph,i,di)
    mainChain.mineBlock(b)
    mainChain.addBlock(b)


    writeFile("voters.pickle", voters.getRegistry())
    writeToAllTextFiles(mainChain, 'BC')

    mvWindow.setLabelText(0, "Vote Recorded for: " + nominee)

def loginWindow(window, voters, mainChain, command):
    window.getRoot().destroy()
    del window

    lWindow = Window("Login")
    lWindow.addButton('Return Home',290,190,lambda: returnHome(lWindow, voters, mainChain))

    lWindow.addLabel("Username: ", 200, 230)
    lWindow.addEntry(290, 247)

    lWindow.addLabel("Password: ", 200, 280)
    lWindow.addEntry(290, 297)

    lWindow.addButton("Login", 420, 297, lambda: login(lWindow, voters, mainChain, command))
    lWindow.addLabel(" ", 200, 350)
    lWindow.run()
def login(lWindow, voters, mainChain, command):
    userReturn = voters.uniqueUsernameCheck(lWindow.getEntryText(0))
    if userReturn == True or len(lWindow.getEntryText(0)) < 7:
        lWindow.setLabelText(2, "Username or Password is Incorrect")
        lWindow.clearEntrys()
        return
    v = voters.getRegistry()[lWindow.getEntryText(0)]
    s = v.getSalt()
    hp = voters.hash(lWindow.getEntryText(1) + s)
    if hp == v.getHashedPassword():
        lWindow.setLabelText(2, "Login Good")
        lWindow.clearEntrys()
        if command == "account":
            accountWindow(lWindow, voters, mainChain, v)
        if command == "private":
            viewPrivateChainWindow(lWindow, voters, mainChain, v)
        return
    lWindow.setLabelText(2, "Username or Password is Incorrect")
    lWindow.clearEntrys()
    return

def accountWindow(lWindow, voters, mainChain, v):
    lWindow.getRoot().destroy()
    del lWindow
    aWindow = Window("Welcome " + v.getName())

    aWindow.addButton('Return Home', 290, 100, lambda: returnHome(aWindow, voters, mainChain))
    aWindow.addButton('Make Vote', 290, 200, lambda: makeVoteWindow(aWindow, voters, mainChain, v))
    aWindow.addButton('View Chain', 290, 300, lambda: viewPrivateChainWindow(aWindow, voters, mainChain, v))
    aWindow.run()

def viewPublicChainWindow(startWindow, voters, mainChain):
    startWindow.getRoot().destroy()
    del startWindow

    vpcWindow = Window("Public Chain")
    vpcWindow.addLabel(" ", 200, 370)

    vpcWindow.addButton('Return Home', 75, 440, lambda: returnHome(vpcWindow, voters, mainChain))
    vpcWindow.addButton('Validate Chain', 225, 440, lambda: validateChainW(vpcWindow, mainChain))
    vpcWindow.addButton('View Private Info', 375, 440, lambda: loginWindow(vpcWindow, voters, mainChain, "private"))
    vpcWindow.addButton('Get Vote Tally', 525, 440, lambda: getVoteTally(vpcWindow, mainChain))

    vpcWindow.addLabel(" ", 200, 50)
    #defualts to latest block
    vpcWindow.giveIndex(mainChain.getChain().__len__() - 1)
    getBlockString(vpcWindow,mainChain, vpcWindow.getIndex())
    vpcWindow.addButton('Last Block', 100, 340, lambda: lastBlock(vpcWindow, vpcWindow.getIndex(), mainChain))
    vpcWindow.addButton('Next Block', 500, 340, lambda: nextBlock(vpcWindow, vpcWindow.getIndex(), mainChain))
    vpcWindow.run()
def getVoteTally(vpcWindow, mainChain):
    chain = mainChain.getChain()
    cd1 = 0
    cd2 = 0
    cd3 = 0
    for u in chain:
        if u.getData().endswith("Canidate 3"):
            cd3 += 1
        elif u.getData().endswith("Canidate 2"):
            cd2 +=1
        elif u.getData().endswith("Canidate 1"):
            cd1 +=1
    vpcWindow.setLabelText(0, " Canidate 1: " +str(cd1) + "\n Canidate 2: " + str(cd2) + "\n Canidate 3: " + str(cd3))

def viewPrivateChainWindow(lWindow, voters, mainChain, v):
    lWindow.getRoot().destroy()
    del lWindow

    vprcWindow = Window("Private Chain")
    vprcWindow.addLabel(" ", 200, 370)

    vprcWindow.addButton('Return Home', 50, 440, lambda: returnHome(vprcWindow, voters, mainChain))
    vprcWindow.addButton('Validate Chain', 170, 440, lambda: validateChainW(vprcWindow, mainChain))
    vprcWindow.addButton('Search For Vote', 290, 440, lambda: searchForUsersVote(vprcWindow, voters, mainChain, v))
    vprcWindow.addButton('Raise Difficulty', 410, 440, lambda: raiseDifficulty(vprcWindow, mainChain))
    vprcWindow.addButton('Get Vote Tally', 530, 440, lambda: getVoteTally(vprcWindow, mainChain))

    vprcWindow.addLabel("Block", 200, 50)
    vprcWindow.giveIndex(mainChain.getChain().__len__() - 1)
    getBlockString(vprcWindow, mainChain, vprcWindow.getIndex())
    vprcWindow.addButton('Last Block', 100, 340, lambda: lastBlock(vprcWindow, vprcWindow.getIndex(), mainChain))
    vprcWindow.addButton('Next Block', 500, 340, lambda: nextBlock(vprcWindow, vprcWindow.getIndex(), mainChain))

    vprcWindow.addButton('Delete Vote', 500, 30, lambda: deleteBlock(vprcWindow, mainChain, v, voters))
    vprcWindow.hideWidget(vprcWindow.getButton(7))
    vprcWindow.run()
def searchForUsersVote(vprcWindow, voters, mainChain, v):
    user = v.getUsername()
    for u in mainChain.getChain():
        if u.getData().startswith(voters.hash(user)):
            getBlockString(vprcWindow,mainChain,u.getIndex())
            vprcWindow.setLabelText(0, "Vote Found")
            vprcWindow.getButton(7).place(x=520, y=30)
            return
    vprcWindow.setLabelText(0, "Vote Not Found")
def raiseDifficulty(vprcWindow, mainChain):
    chain = mainChain.getChain()
    d = mainChain.getDifficulty()
    for b in chain:
        if b.getDifficulty() == d:
            mainChain.setDifficulty(d+1)
            vprcWindow.setLabelText(0, "Difficulty Raised to: " + str(mainChain.getDifficulty()))
            writeToAllTextFiles(mainChain, 'BC')
            return
    vprcWindow.setLabelText(0, "Must Mine At Least One Block At Currenty Difficulty: "  + str(mainChain.getDifficulty()))
def deleteBlock(vprcWindow, mainChain, v, voters):
    user = v.getUsername()
    for u in mainChain.getChain():
        if u.getData().startswith(voters.hash(user)):
            vprcWindow.setLabelText(0, "Vote Found")
            confirmBlockDeleteWindow(vprcWindow, mainChain, v, voters)
            return
    vprcWindow.setLabelText(0, "Vote Not Found")

def confirmBlockDeleteWindow(vprcWindow, mainChain, v, voters):
    cbdWindow = tk.Toplevel()
    cbdWindow.geometry("400x200")
    cbdWindow.resizable(False,False)
    l = tk.Label(cbdWindow, text="Are You Sure You Want to Delete This Block?\n You Will Not Be Allowed To Revote")
    l.grid(column=0, row=0)

    ExitYes = tk.Button(cbdWindow, text="Delete Block", command= lambda: confirmBlockDelete(vprcWindow,mainChain,cbdWindow,v,voters))
    ExitYes.grid(column=0, row=2)

    NoYes = tk.Button(cbdWindow, text="Exit", command= lambda: removeDeleteBlockWindow(cbdWindow))
    NoYes.grid(column=2, row=2)
def confirmBlockDelete(vprcWindow, mainChain, cbdWindow, v, voters):
    user = v.getUsername()
    for u in mainChain.getChain():
        if u.getData().startswith(voters.hash(user)):
            mainChain.removeBlock(u.getIndex())
    removeDeleteBlockWindow(cbdWindow)
    writeToAllTextFiles(mainChain, 'BC')
    viewPrivateChainWindow(vprcWindow,voters,mainChain,v)
def removeDeleteBlockWindow(cbdWindow) :
    cbdWindow.destroy()
    del cbdWindow

def validateChainW(vcWindow, mainChain):
    val = mainChain.validateChain()
    if val == -1:
        vcWindow.setLabelText(0, "Chain Valid")
        return
    vcWindow.setLabelText(0,"Chain Invalid At Current Block")
    vcWindow.addButton('Remine Chain', 500, 30, lambda: remineChain(vcWindow, mainChain, val))
    getBlockString(vcWindow,mainChain, val)
def remineChain(vcWindow, mainChain, val):
    mainChain.remineChain(val)
    writeToAllTextFiles(mainChain, 'BC')
    btns = vcWindow.getButtons()
    for i in range(0, btns.__len__()):
        t = vcWindow.getButton(i).cget('text')
        if t == 'Remine Chain':
            vcWindow.hideWidget(vcWindow.getButton(i))
            btns.pop(i)
    vcWindow.setLabelText(0, "Chain Remined")

def getBlockString(vcWindow,mainChain, i):
    b = mainChain.getBlock(i)
    s = "User Hash: \n" + b.getUserHash() + "\n \nVoted For: \n " + b.getCanidate() + "\n \n Date Of Vote: \n" + b.getDate() + "\n \n Previous Hash: \n" + b.getPreviousHash() +"\n \n Dificulty: \n" + str(b.getDifficulty())+ "\n \n Nonce: \n" + str(b.getNonce())
    vcWindow.setLabelText(1,s)
    vcWindow.giveIndex(i)
def lastBlock(vcWindow, index, mainChain):
    if index == 0:
        vcWindow.setLabelText(0, "No More Last Blocks")
        return
    getBlockString(vcWindow, mainChain, index-1)
    vcWindow.setLabelText(0, "")
    vcWindow.giveIndex(index -1)
    try:
        vcWindow.hideWidget(vcWindow.getButton(7))
    except IndexError as e:
        pass
def nextBlock(vcWindow, index, mainChain):
    if index == (mainChain.getChain().__len__() - 1):
        vcWindow.setLabelText(0, "No More Next Blocks")
        return
    getBlockString(vcWindow, mainChain, index + 1)
    vcWindow.setLabelText(0, "")
    vcWindow.giveIndex(index +1)
    try:
        vcWindow.hideWidget(vcWindow.getButton(7))
    except IndexError as e:
        pass

def returnHome(frame, voters, mainChain):
    frame.getRoot().destroy()
    del frame
    startWindow(voters, mainChain)

main()
