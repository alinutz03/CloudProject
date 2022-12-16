from zipfile import ZipFile
import os


def unzip(file):
    with ZipFile (file, 'r') as zipObj:
        zipObj.extractall('Text')
        #print ('File is unzipped in Text folder')


def readText(path):
    data =[]
    # print(len(list(os.walk(database))[0]))
    for root, folders, files in os.walk(database):
        for file in files:
            path = os.path.join(root, file)
            with open(path) as inf:
                data.append(inf.read())
                # print(inf.read())

    # print(data)
    # print(len(data))





if __name__ == '__main__':
    file='file.zip'
    unzip(file)
    os.getcwd()
    database = os.path.join(os.getcwd(), 'Text')
    readText(database)