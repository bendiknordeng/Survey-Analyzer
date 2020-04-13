import os
import sys
from pdf2image import convert_from_path, convert_from_bytes
import zipfile
import numpy as np
import cv2

class Converter:
    global_index = 0  # static variable for unique filepaths

    def __init__(self, filename):
        self.__files = []
        try:
            if filename.endswith('.jpg') or filename.endswith('.png'):
                self.__files.append(np.array(cv2.imread(filename, cv2.COLOR_BGR2GRAY)))
            elif filename.endswith('.pdf'):
                images = convert_from_path(filename, grayscale=True)
                for img in images:
                    self.__files.append(np.array(img))
            elif filename.endswith('.zip'):
                archive = zipfile.ZipFile(filename)
                for file in archive.namelist():
                    f = archive.open(file)
                    if file.endswith('.jpg') or file.endswith('.png'):
                        image = np.asarray(bytearray(f.read()), dtype="uint8")
                        self.__files.append(np.array(cv2.imdecode(image, cv2.COLOR_BGR2GRAY)))
                    elif file.endswith('.pdf'):
                        images = convert_from_bytes(f.read(), grayscale=True)
                        for img in images:
                            self.__files.append(np.array(img))
            elif filename.endswith('/'):
                for file in os.listdir(filename):
                    images = convert_from_path(filename+file, grayscale=True)
                    for img in images:
                        self.__files.append(np.array(img))
        except:
            print("Error:", sys.exc_info()[0])
            raise

    def save(self, location):
        paths = []
        # iterates over all pages and saves them as a new jpg
        for i, img in enumerate(self.__files, start=Converter.global_index):
            path = location+"survey_"+str(i)+'.jpg'
            cv2.imwrite(path, img)
            paths.append(path)
            Converter.global_index += 1
        return paths

    def get(self):
        return self.__files


if __name__ == '__main__':
    filename = 'Survey.pdf'
    c = Converter(filename)
    print(c.get())

    # iterates over all __files in the given directory
    #directory = os.fsencode('survey_pdfs')
    #for file in os.listdir(directory):
    #     filename = os.fsdecode(file)
    #     if filename.endswith(".pdf"):
    #         Converter('survey_data/'+filename).save()
