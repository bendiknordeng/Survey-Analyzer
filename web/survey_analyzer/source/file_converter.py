import os
import sys
from pdf2image import convert_from_bytes
import zipfile
import numpy as np
import cv2

class Converter:
    index = 0 # static variable for indexing images

    def __init__(self, file, filename):
        self.files = []
        try:
            if filename.endswith('.jpg') or filename.endswith('.png'):
                self.files.append(np.array(cv2.imread(file, cv2.COLOR_BGR2GRAY)))
            if filename.endswith('.pdf'):
                print(filename)
                self.files.append(np.array(convert_from_bytes(file, grayscale=True)[0]))
            elif filename.endswith('.zip'):
                archive = zipfile.ZipFile(filename, 'r')
                for file in archive.namelist():
                    f = archive.open(file)
                    if file.endswith(".pdf"):
                        self.files.append(np.array(convert_from_bytes(f.read(), grayscale=True)[0]))
        except:
            print("Error:", sys.exc_info()[0])
            raise

    def save(self, location):
        paths = []
        # iterates over all pages and saves them as a new jpg
        for img in self.files:
            path = location+"survey_"+str(Converter.index)+'.jpg'
            cv2.imwrite(path, img)
            paths.append(path)
            Converter.index += 1
        return paths

    def get(self):
        return self.files


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
