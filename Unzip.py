from zipfile import ZipFile
import os
import googletrans
from deep_translator import GoogleTranslator
from googletrans import Translator
import shutil

def unzip(file):
    with ZipFile (file, 'r') as zipObj:
        zipObj.extractall('Text')
        #print ('File is unzipped in Text folder')


def translate(path, languageInput, languageOutput):
    data =[]
    print()
    print(path)
    print()
    # print(len(list(os.walk(database))[0]))
    database= os.path.join(path, 'Text')
    for root, folders, files in os.walk(database):
        for file in files:
            print(file)
            path = os.path.join(root, file)
            with open(path) as inf:
                print(path)
                text = inf.read()
                translator = Translator()
            translated = GoogleTranslator(source=languageInput , target=languageOutput).translate_file(path)
            print(translated)
            with open(path, 'w') as f:
                    f.write(translated)
                    print(translated)
                    f.write("\n")


def zip(outputName, file):
    shutil.make_archive( outputName, 'zip', file)


def translateFile(path, languageInput, languageOutput):
    translated = GoogleTranslator(source=languageInput, target=languageOutput).translate_file(path)


if __name__ == '__main__':
    file='text2.zip'
    unzip(file)
    os.getcwd()
    # database = os.path.join(os.getcwd(), 'Text')
    database = os.path.join(os.getcwd())
    languageInput = input("Please introduce the language of the source: \n")
    languageOutput = input("Plase introduce the language to translate: \n")
    translate(database, languageInput, languageOutput)
    outputName ='outputFiles'
    file = 'Text'
    zip(outputName, file)
    # print(texts)
    # traducere(languageInput, languageOutput)