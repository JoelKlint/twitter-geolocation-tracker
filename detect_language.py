from database.database import Database
from langdetect import detect, detect_langs

def detectString():
    db = Database('twitter-geo')
    print ('Got database')
    textsAndIds = db.getAllTweetTextAndIds()
    print ('Got texts, starting detection')
    for text in textsAndIds:
        id = text[0]
        filteredText = filterText(text[1])
        # Checking that the string contains some amount of data to analyse
        if len(filteredText) > 40:
            try:
                guessedLanguage = detect(filteredText)
                db.updateDetectedLanguage(id, guessedLanguage)
            except Exception as ex:
                print ('Got error when detecting Language')

def filterText(text):
    splitString = text.split(' ')
    newText = ''
    for string in splitString:
        if '@' not in string and 'https' not in string:
            newText += ' ' + string
    return newText

detectString()