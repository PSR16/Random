from bs4 import BeautifulSoup
import os

def open_file(html_file):
    """
    opens HTML file using Beautiful Soup

    :param html_file: input HTML file
    :return: parsed HTML
    """
    soup = BeautifulSoup(open(html_file), "lxml")
    return soup

def getAnswers(html_file, answer):
    """

    :param html_file:
    :param answer:
    :return:
    """
    answers = []
    for ans in answer[1]:
        answers.append(ans)
    #Inserts all questions into a list

    spec_char = ['=', '<', '>', '#', '&']
    question = []
    for li in html_file.findAll('li'):
        quest = li.get_text().strip()
        for ch in spec_char:
            if ch in quest:
                quest = quest.replace(ch, "\\"+ch)
        question.append(quest)

    questAns = []
    listQA = []
    for index, q in enumerate(question):
        questAns.append(question[index])
        questAns.append(answers[index])
        listQA.append(questAns[0])
        listQA.append(questAns[1])
        questAns = []

def toGIFT(html_file, outFile, quizName):
    heading = html_file.find('h3').text.split("Key: ")
    title = heading[0]
    answers = []
    for ans in heading[1]:
        answers.append(ans)
    getAnswers(html_file, heading)

    spec_char = ['=', '#', '&']
    index = 0
    for li in html_file.findAll('li'):
        name = li.get_text().strip()
        outFile.write( "::" + quizName + "::" + name.encode('utf-8'))
        outFile.write("{\n")
        for ans in li.findAll('asp:listitem', {'text': True, 'value': True}):
            quest = ans['text']
            for ch in spec_char:
                if ch in quest:
                    quest = quest.replace(ch, "\\" + ch)
            if ans['value'] == answers[index]:
                outFile.write("=" + quest.encode('utf-8') + "\n")
            else:
                outFile.write("~" + quest.encode('utf-8') + "\n")
        outFile.write("} \n\n")
        index = index + 1

count = 0
for file in os.listdir("C:\Users\Pegah\OneDrive\Programming\Work\Quizzes"):
    if file.endswith(".html"):
        print(file)
        name= file.split(".")
        outFileName = name[0]
        htmlFile = open_file("C:\Users\Pegah\OneDrive\Programming\Work\Quizzes\\" + file)
        moodleFile = open('C:\Users\Pegah\OneDrive\Programming\Work\outputQuizNew\\' + outFileName + '.txt', 'w')
        quizName = file.split(".")
        quizN = quizName[0]
        quizN = quizN.encode('utf-8')
        toGIFT(htmlFile, moodleFile, quizName[0])
        moodleFile.close()
        count += 1

print(count)


