import os
import sys
from pdf2image import convert_from_path, convert_from_bytes
import zipfile
import numpy as np
import cv2

class Converter:
    index = 0 # static variable for indexing images

    def __init__(self, filename):
        self.__files = []
        try:
            if filename.endswith('.jpg') or filename.endswith('.png'):
                self.__files.append(np.array(cv2.imread(filename, cv2.COLOR_BGR2GRAY)))
            if filename.endswith('.pdf'):
                print(filename)
                self.__files.append(np.array(convert_from_path(filename, grayscale=True)[0]))
            elif filename.endswith('.zip'):
                archive = zipfile.ZipFile(filename, 'r')
                for file in archive.namelist():
                    f = archive.open(file)
                    if file.endswith(".pdf"):
                        self.__files.append(np.array(convert_from_bytes(f.read(), grayscale=True)[0]))
            elif filename.endswith('/'):
                for file in os.listdir(filename):
                    self.__files.append(np.array(convert_from_path(filename+file, grayscale=True)[0]))
        except:
            print("Error:", sys.exc_info()[0])
            raise

    def save(self, location):
        # iterates over all pages and saves them as a new jpg
        for img in self.__files:
            cv2.imwrite(location+"survey_"+str(Converter.index)+'.jpg', img)
            Converter.index += 1

    def get(self):
        return self.__files


if __name__ == '__main__':
    filename = 'Survey.pdf'
    c = Converter(filename)
    print(c.get())

    # iterates over all files in the given directory
    #directory = os.fsencode('survey_pdfs')
    #for file in os.listdir(directory):
    #     filename = os.fsdecode(file)
    #     if filename.endswith(".pdf"):
    #         Converter('survey_data/'+filename).save()
