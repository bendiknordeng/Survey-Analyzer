import os, io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
import numpy as np
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ServiceAccountToken.json'

class TextReader:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def read(self, filename):
        with io.open(filename, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = self.client.document_text_detection(image=image)
        os.remove(filename)
        #print(response.full_text_annotation.text)
        """
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                print('\nBlock confidence: {}\n'.format(block.confidence))

                for paragraph in block.paragraphs:
                    print('Paragraph confidence: {}'.format(paragraph.confidence))

                    for word in paragraph.words:
                        word_text = ''.join([symbol.text for symbol in word.symbols])
                        print('Word text: {} (confidence: {})'.format(word_text, word.confidence))

                        for symbol in word.symbols:
                            print('\tSymbol: {} (confidence: {})'.format(symbol.text, symbol.confidence))

        if response.error.message:
            raise Exception('{}'.format(response.error.message))
        """
        return response.full_text_annotation.text

if __name__ == "__main__":
    reader = TextReader()

    reader.read("text_recog_test.jpg")
