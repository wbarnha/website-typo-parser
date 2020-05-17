from HTMLParser import HTMLParser
from enchant.checker import SpellChecker
import os
import enchant
import sys
import wget
import shutil
import requests
from urlparse import urlparse
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QGridLayout
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QTextEdit
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QScrollArea
from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QSizePolicy
from PySide2.QtWidgets import QProgressBar
from PySide2.QtCore import Slot, Qt

###### THIS PROGRAM IS DESIGNED TO RUN ON UNIX AND UNIX-LIKE SYSTEMS WITH PYTHON 2 ######
#Some components require features from UNIX in order to gain full functionality of this program.

#Since there are missing words from the local dictionary, they have to be manually added
dictionary = enchant.Dict("en_US") #Declares dictionary and assigns to a variable
new_words = []
displaytext = []

##TODO: Add a button for adding words to the dictionary by allowing for the textbox to be edited and read
#Add a word to the list in order to update the dictionary.

for word in new_words:
    dictionary.add(word)

lang = SpellChecker("en_US") #Selects dictionary for a language

#checklist = []
spell_errors = 0 #Used for counting number of spelling errors indicated by the program
#evaluate = False
part = 0 #Used for tracking examples only
#report = open("typos.txt","w+") #Creates a .txt file containing the typos
section =  0 #Used for tracking parts of a lecture  
period = 1 #This is going to be used globally for counting periods.
ques = 1 #Used for identifying questions in exercises
letter = 1 #Used for tracking letters in an exercise question
temporary = []

class MyHTMLParser(HTMLParser): #THIS ONLY WORKS IN PYTHON 2
    global spell_errors,report,period,temporary,displaytext
    def handle_data(self, data):
        global period,section,period,part
        temporary = [] #Used to hold parsed words to be processed by NLTK
        lang.set_text(data) #Handles each word individually
        temporary.append(data) #Adds parsed language to list in order to search for grammatical issues
        for misspell in lang: #Searches for possible spelling errors
            global spell_errors,report,section,part
            if len(dictionary.suggest(misspell.word)) > 0: #This is a way of removing gibberish    
                #print("Misspelled: "+str(misspell.word)) #For displaying errors to terminal
                #print("Suggestions: "+str(dictionary.suggest(misspell.word))+"\n")
                displaytext.append("\nMisspelled: "+str(misspell.word)+"\n") #For displaying errors to terminal
                displaytext.append("Suggestions: "+str(dictionary.suggest(misspell.word))+"\n")
                spell_errors += 1
        if "." in data and data.isdigit() == False: #General case for a word with a period at the end or enumeration
            if len(data) > 2: #Used in case of individual letter listing
                period += 1

    def handle_starttag(self, tag, attrs):
        global part,section,period,ques,letter
        if tag == "p":
            if len(attrs) >= 1: #Added in case there are no attributes
                if attrs[0][0] == "class":
                    if attrs[0][1] == "example-FirstPara":
                        part += 1
                        period = 1
                    if attrs[0][1] == "SubHead1":
                        section += 1
                        period = 1
        if tag == "ol":
            ques += letter 
    def handle_endtag(self,tag):
        global letter
        if tag == "/li":
            letter = 1

#TODO: Update QLabel ability to display text and continually update
#TODO: Remove os.system usage and replace with Python methods for portability
class TypoWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Typo Parser")
        self.layout = QGridLayout(self)
        self.text = QTextEdit("")
        self.clear = QPushButton("Clear")
        self.save = QPushButton("Save")
        self.update = QPushButton("Add to Dictionary")
        self.run = QPushButton("Run")
        self.run.setCheckable(True)
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.url = QLineEdit("math.cos.gmu.edu/~sap/ode/index.html")
        self.user = QLineEdit("")
        self.password = QLineEdit("")
        self.text.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
        self.text.setReadOnly(False)
        self.layout.addWidget(self.url, 0, 1, 1, 3)
        self.layout.addWidget(QLabel("URL:"), 0,0)
        self.layout.addWidget(self.user, 1, 1)
        self.layout.addWidget(QLabel("Username:"), 1,0)
        self.layout.addWidget(self.password, 1, 3)
        self.layout.addWidget(QLabel("Password:"), 1,2)
        self.layout.addWidget(self.run,2,0)
        self.layout.addWidget(self.save,2,1,1,1)
        self.layout.addWidget(self.clear,2,2)
        self.layout.addWidget(self.update,2,3,1,1)
        self.layout.addWidget(self.progress,3,0,1,4)
        self.layout.addWidget(self.text,4,0,4,4)
        self.clear.clicked.connect(self.cleartext)
        self.save.clicked.connect(self.savefile)
        self.run.clicked.connect(self.parse)
        self.update.clicked.connect(self.update_dict)

    @Slot()
    def savefile(self):
        f = open("report.txt",'w')
        f.write(self.text.text())
        f.close()

    @Slot()
    def cleartext(self):
        self.text.clear()
        self.progress.setValue(0)

    #Since there are missing words from the local dictionary, they have to be manually added
    @Slot()
    def update_dict(self):
        new_words = self.text.toPlainText()
        for word in new_words.split():
            dictionary.add(str(word))

    @Slot()
    def parse(self):
        self.progress.setValue(0)
        url = self.url.text()
        username = self.user.text()
        password = self.password.text()
        path = os.path.dirname(urlparse(url).path)
        if path in os.path.dirname(os.path.realpath(__file__)):
            shutil.rmtree(path)
        #if not(self.run.isChecked()):
        os.system("bash -c 'wget -rL -R jpg,gif,png,pdf,mp4,css --http-password=%s --http-user=%s %s'" % (password,username,url))
        #self.run.setChecked(True)
        #TODO: Get rid of wget
        #TODO: Set up program to ease file location search
        parser = MyHTMLParser() #Required to be declared in order to feed data, does not work in Python 3
        formats = "xhthtmlhtm" #Used for storing suffixes of file types
        dirsize = 0
        xhtfiles = 0
        for p, d, files in os.walk(os.getcwd()):
            for filename in files:
                if filename.endswith(".xht"):
                    xhtfiles += 1
                    dirsize += os.path.getsize(p+os.sep+filename)
        for tuples in os.walk(path): #Identifies potential typos
            if self.run.isChecked():
                for contents in tuples[2]: #This loop iterates over every single file in a directory, add functions below
                    if "xht" in contents[-6:]:# or "htm" in contents[-6:]: #Controls type of files read (HTML and its derivatives only), comment this out to go crazy
                        displaytext.append("\n########## "+path+tuples[0].replace(path,"")+os.sep+str(contents)+" ##########\n") #Provides a header for each section
                        self.text.setText(''.join([str(t) for t in displaytext if t is not None]))
                        f = open(tuples[0]+os.sep+contents,"r")
                        info = f.read()
                        displaytext.append(parser.feed(info))
                        self.text.setText(''.join([str(t) for t in displaytext if t is not None]))
                        self.progress.setValue(int(100*((self.progress.value())/100.0+(1/(1.0*xhtfiles)))))
                    part = 0
                    section = 0
                    period = 1
                    ques = 1
                    letter = 1
                    temporary = [] #Resets list
            else:
                break

            displaytext.append("\n%d spelling errors detected.\n" % (spell_errors))
        displaytext.append("\nThere are currently %d locally-added items in the dictionary." % (len(new_words)))
        self.text.setText(''.join([str(t) for t in displaytext if t is not None]))
        self.run.setChecked(False)
        self.progress.setValue(100)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = TypoWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())

