from HTMLParser import HTMLParser
from enchant.checker import SpellChecker
import os
import enchant
import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QGridLayout
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QScrollArea
from PySide2.QtWidgets import QFileDialog
from PySide2.QtCore import Slot, Qt

class TypoWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Typo Parser")
        self.layout = QGridLayout(self)
        self.text = QLabel("test")
        self.clear = QPushButton("Clear")
        self.save = QPushButton("Save")
        self.run = QPushButton("Run")

        self.layout.addWidget(QLineEdit(), 0, 1, 1, 3)
        self.layout.addWidget(QLabel("URL:"), 0,0)
        self.layout.addWidget(QLineEdit(), 1, 1,)
        self.layout.addWidget(QLabel("Username:"), 1,0)
        self.layout.addWidget(QLineEdit(), 1, 3,)
        self.layout.addWidget(QLabel("Password:"), 1,2)
        self.layout.addWidget(self.run,2,0)
        self.layout.addWidget(self.save,2,1,1,1)
        self.layout.addWidget(self.clear,2,2)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.text)
        self.layout.addWidget(self.scrollArea,3,0,4,4)

        self.clear.clicked.connect(self.cleartext)
        self.save.clicked.connect(self.savefile)
        self.run.clicked.connect(self.parse)


###### THIS PROGRAM IS DESIGNED TO RUN ON UNIX AND UNIX-LIKE SYSTEMS WITH PYTHON 2 ######
#For those who want further details, Python 3 is very poor for processing information from the
#internet at the moment. There are plenty of resources available in Python 2 to get the job done.
#Additionally, some features require features from UNIX in order to gain the full potential of this
#program.

path = "math.cos.gmu.edu/~sap/ode/index.html" #This may have to be configured by the end-user
## Left blank for obvious reasons
username=""
password=""

#If you do choose to run this, please know that I do not take any liability whatsoever for the
#damage caused to your storage device. This program is run at the risk of the end-user.
#Interestingly enough, this can get into some FTP systems without any authentication.
#In order to speed things up, the program does not download some files.
os.system("bash -c 'rm -rf ~/%s'" % path)
os.system("bash -c 'wget -rL -R jpg,gif,png,pdf,mp4,css --http-password=%s --http-user=%s %s'" % (password,username,path))

#Since there are missing words from the native dictionary, they have to be manually added
#TODO: Consult statistician to determine how to go about evaluating typo probability to increase versatility
#TODO: Implement typo probability determination
dictionary = enchant.Dict("en_US") #Declares dictionary and assigns to a variable
new_words = []

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
    global spell_errors,report,period,temporary
    def handle_data(self, data):
        global period,section,period,part
        temporary = [] #Used to hold parsed words to be processed by NLTK
        lang.set_text(data) #Handles each word individually
        temporary.append(data) #Adds parsed language to list in order to search for grammatical issues
        for misspell in lang: #Searches for possible spelling errors
            global spell_errors,report,section,part
            if len(dictionary.suggest(misspell.word)) > 0: #This is a way of removing gibberish    
                print("Misspelled: "+str(misspell.word)) #For displaying errors to terminal
                print("Suggestions: "+str(dictionary.suggest(misspell.word))+"\n")
                #report.write("Misspelled: "+str(misspell.word)+"\n") #For displaying errors to text file
                #report.write("Suggestions: "+str(dictionary.suggest(misspell.word))+"\n\n")
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
                        #print("## With reference from the beginning of Example %d ##\n" % (part))
                        #report.write("## With reference from the beginning of Example %d ##\n" % (part))
                        period = 1
                    if attrs[0][1] == "SubHead1":
                        section += 1
                        #print("## With reference from the beginning of Section %d ##\n" % (section))
                        #report.write("## With reference from the beginning of Section %d ##\n" % (section))
                        period = 1
        if tag == "ol":
            ques += letter 
    def handle_endtag(self,tag):
        global letter
        if tag == "/li":
            letter = 1

path = "math.cos.gmu.edu/" #This may have to be configured by the end-user
#TODO: Set up program to ease file location search
parser = MyHTMLParser() #Required to be declared in order to feed data, does not work in Python 3

#Iterates over contents of Saperstone's folders downloaded from Math Department
#If desired, it could look over the entire department... 
#TODO: ADD GRAMMAR CHECKING
#TODO: ADD MATH CHECKING
formats = "xhthtmlhtm" #Used for storing suffixes of file types
for tuples in os.walk(path): #Identifies potential typos
    for contents in tuples[2]: #This loop iterates over every single file in a directory, add functions below
        if "xht" in contents[-6:]:# or "htm" in contents[-6:]: #Controls type of files read (HTML and its derivatives only), comment this out to go crazy
            print("########## "+path+tuples[0].replace(path,"")+"/"+str(contents)+" ##########\n") #Provides a header for each section
            #report.write("########## "+path+tuples[0].replace(path,"")+"/"+str(contents)+" ##########\n") #Provides a header file
            f = open(tuples[0]+"/"+contents,"r")
            info = f.read()
            parser.feed(info)
        part = 0
        section = 0
        period = 1
        ques = 1
        letter = 1
        temporary = [] #Resets list to empty contents and save memory...

print("\nThere are currently %d non-native items in the dictionary." % (len(new_words)))
#This section is reserved for printing the number of errors by type
print("\n%d spelling errors detected.\n" % (spell_errors))
#report.write("\n%d spelling errors detected." % (spell_errors))

#report.close() #Writing to file is complete

class TypoWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Typo Parser")
        self.layout = QGridLayout(self)
        self.text = QLabel("test")
        self.clear = QPushButton("Clear")
        self.save = QPushButton("Save")
        self.run = QPushButton("Run")

        self.layout.addWidget(QLineEdit(), 0, 1, 1, 3)
        self.layout.addWidget(QLabel("URL:"), 0,0)
        self.layout.addWidget(QLineEdit(), 1, 1,)
        self.layout.addWidget(QLabel("Username:"), 1,0)
        self.layout.addWidget(QLineEdit(), 1, 3,)
        self.layout.addWidget(QLabel("Password:"), 1,2)
        self.layout.addWidget(self.run,2,0)
        self.layout.addWidget(self.save,2,1,1,1)
        self.layout.addWidget(self.clear,2,2)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.text)
        self.layout.addWidget(self.scrollArea,3,0,4,4)

        self.clear.clicked.connect(self.cleartext)
        self.save.clicked.connect(self.savefile)
        self.run.clicked.connect(self.parse)

    @Slot()
    def savefile(self):
        filename, filter = QFileDialog.getSaveFileName(parent=self, caption='Open file', dir='.', filter='Text files (*.txt)')

        if filename:
            self.inputFileLineEdit.setText(filename)

    @Slot()
    def cleartext(self):
        self.text.clear()

    @Slot()
    def parse(self):
        self.text.setText("poooooooooooooop")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = TypoWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())

