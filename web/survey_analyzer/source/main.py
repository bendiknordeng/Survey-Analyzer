from file_converter import Converter
from box_detection import box_detection
from rectangleselect import MarkRects
from detect_box_content import box_content_detection
from text_recognition import TextReader
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import cv2
import csv
import pickle

def main(filename):
    path = filedialog.askopenfilename()
    rect_crops = [tuple(map(int, x)) for x in MarkRects(path).get()]
    handwritten_crops = [tuple(map(int, x)) for x in MarkRects(path).get()]

    headlines = ["Skole","Kjønn:","Trinn:","Jeg har fått hjelp av vektorassistentene.","Jeg synes det gikk greit å spørre vektorassistentene om hjelp.","Jeg fikk lettere hjelp da assistentene var i timen.","Jeg synes assistentene virket godt forberedt.","Jeg synes matte virker mer spennende etter møtet med vektorassistentene.","Jeg synes assistentene forklarte på en forståelig måte.","Jeg ønsker at vektorassistentene skal komme tilbake.","Har du noen kommentarer til vektorprogrammet, eventuelt noe vi kunne gjort bedre? (valgfritt)"]

    surveys = Converter(filename).get()

    with open('survey_results.csv', 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter = ';')
        writer.writerow(headlines)
        out = []

        for survey in surveys:
            for c in rect_crops:
                boxes = box_detection(survey[c[1]:c[3],c[0]:c[2]])
                answer, confidence = box_content_detection(boxes)
                print("Answer:",answer,"Confidence:",confidence)
                out.append(answer)

            for c in handwritten_crops:
                filename = "text.jpg"
                cv2.imwrite(filename,survey[c[1]:c[3],c[0]:c[2]])
                text = TextReader().read(filename)
                print("Text:",text.strip())
                out.append(text.strip())

            writer.writerow(out)

if __name__ == '__main__':
    main('Survey.pdf')
