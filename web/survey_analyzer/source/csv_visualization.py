import numpy as np
import csv
import matplotlib.pyplot as plt

def read_csv(name_of_file):
    filename = name_of_file + ".csv"

    school = []    
    gender = []
    schoolClass = []
    gotHelp = []
    easyToAsk = []
    easyHelp = []
    assPrepared = []
    mathExciting = []
    goodExplanation = []
    vektorComeBack = []

    # with open(filename) as f:
    #     reader = csv.DictReader(f)
    #     data = [row for row in reader]

    with open(filename) as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            if row[0] == '':
                continue
            # All columns appended to
            school.append(row[0])
            gender.append(row[1])
            schoolClass.append(row[2])
            gotHelp.append(row[3])
            easyToAsk.append(row[4])
            easyHelp.append(row[5])
            assPrepared.append(row[6])
            mathExciting.append(row[7])
            goodExplanation.append(row[8])
            vektorComeBack.append(row[9])

    return school, gender, schoolClass, gotHelp, easyToAsk, easyHelp, \
        assPrepared, mathExciting, goodExplanation, vektorComeBack

def pieChart(strArray):
    agree = strArray.count('Enig')
    semiAgree = strArray.count('Delvis enig')
    neutral = strArray.count('NÃ¸ytral')
    semiDisagree = strArray.count('Delvis uenig')
    disagree = strArray.count('Uenig')

    sizes = [agree, semiAgree, neutral, semiDisagree, disagree]
    labels = 'Enig','Delvis enig','Nøytral','Delvis uenig','Uenig'

    return sizes, labels

def easyToAskChart(strArray):
    sizes, labels = pieChart(strArray)
    plt.pie(sizes, labels=sizes, startangle=90, shadow=True, counterclock=True)
    plt.legend(labels,loc=3)
    plt.axis('equal')
    plt.title('Jeg synes det gikk greit å spørre vektorassistentene om hjelp')
    plt.show()

def easyHelpChart(strArray):
    sizes, labels = pieChart(strArray)
    plt.pie(sizes, labels=sizes, startangle=90, shadow=True, counterclock=True)
    plt.legend(labels,loc=3)
    plt.axis('equal')
    plt.title('Jeg fikk lettere hjelp da assistentene var i timen')
    plt.show()

def assPreparedChart(strArray):
    sizes, labels = pieChart(strArray)
    plt.pie(sizes, labels=sizes, startangle=90, shadow=True, counterclock=True)
    plt.legend(labels,loc=3)
    plt.axis('equal')
    plt.title('Jeg synes assistentene virket godt forberedt')
    plt.show()

def mathExcitingChart(strArray):
    sizes, labels = pieChart(strArray)
    plt.pie(sizes, labels=sizes, startangle=90, shadow=True, counterclock=True)
    plt.legend(labels,loc=3)
    plt.axis('equal')
    plt.title('Jeg synes matte virker mer spennende etter møtet med vektorassistentene')
    plt.show()

def goodExplanationChart(strArray):
    sizes, labels = pieChart(strArray)
    plt.pie(sizes, labels=sizes, startangle=90, shadow=True, counterclock=True)
    plt.legend(labels,loc=3)
    plt.axis('equal')
    plt.title('Jeg synes assistentene forklarte på en forståelig måte')
    plt.show()

def vektorComeBackChart(strArray):
    sizes, labels = pieChart(strArray)
    plt.pie(sizes, labels=sizes, startangle=90, shadow=True, counterclock=True)
    plt.legend(labels,loc=3)
    plt.axis('equal')
    plt.title('Jeg ønsker at vektorassistentene skal komme tilbake')
    plt.show()



# The next Charts need their own "custom" chart plotting code
def genderChart(strArray):
    boyGender = strArray.count("Gutt")
    girlGender = strArray.count("Jente")

    labels ='Gutt','Jente'
    sizes = [boyGender,girlGender]

    plt.pie(sizes, labels=sizes, startangle=90, shadow=True, counterclock=True)
    plt.legend(labels,loc=3)
    plt.axis('equal')
    plt.title('Kjønn')
    plt.show()

def schoolClassChart(strArray):
    classEight = strArray.count('8')
    classNine = strArray.count('9')
    classTen = strArray.count('10')

    labels = '8','9','10'
    sizes = [classEight,classNine,classTen]

    plt.pie(sizes, labels=sizes, startangle=90, shadow=True, counterclock=True)
    plt.legend(labels,loc=3,)
    plt.axis('equal')
    plt.title('Klassetrinn')
    plt.show()

def gotHelpChart(strArray):
    helpYes = strArray.count('Ja')
    helpNo = strArray.count('Nei')

    labels = 'Yes','No'
    sizes = [helpYes, helpNo]

    plt.pie(sizes, labels=sizes, startangle=90, shadow=True, counterclock=True)
    plt.legend(labels,loc=3,)
    plt.axis('equal')
    plt.title('Jeg har fått hjelp av vektorassistentene')
    plt.show()

def schoolChart(strArray):
    schools_dict = {}
    for name in strArray:
        if name in schools_dict:
            schools_dict[name] += 1
        else:
            schools_dict[name] = 1

    schoolNames = schools_dict.keys()
    schoolNumbers = schools_dict.values()
    y_pos = np.arange(len(schoolNames))

    # plt.pie(schoolNumbers, labels=schoolNumbers, startangle=90, shadow=True, counterclock=True)
    # plt.legend(schoolNames,loc=3,)
    # plt.axis('equal')
    # plt.title('Skoler')
    # plt.show()

    plt.barh(y_pos, schoolNumbers, align='center', alpha=0.5)
    plt.yticks(y_pos, schoolNames)
    plt.xlabel('Antall')
    plt.title('Skoler')
    plt.show()

if __name__ == "__main__":
    school, gender, schoolClass, gotHelp, easyToAsk, easyHelp, assPrepared, \
        mathExciting, goodExplanation, vektorComeBack = read_csv("survey_answers")
    # gotHelpChart(gotHelp)
    schoolChart(school)