#! python3
# CubeMX+CPP_Converter - заменяет расширения указанных файлов в папке
# Использование:
# Скрипт размещается в каталоге с проектом

import os, sys, time

# Имена/окончания заменяемых файлов (без расширения)
fileList = [
    "main", # Это имя используется в качестве маркера для динамического определения текущего расширения
    "it"
]

# Имя файла на основе которого определяется текущее расширение файлов
fileMarker = fileList[0]

# Массив заменяемых расширений
fileExtensions = [
    ".c",
    ".cpp"
]


# Текущий путь приложения
path = os.path.realpath(os.path.dirname(sys.argv[0]))
# Текущее расширение файлов
currentExtension = "no_extension"
# Новое расширение файлов
newExtension = "no_extension"

# Проверка необходимости замены расширения файла
def IsNeedToChange(filename):
    global currentExtension
    global newExtension
    global fileList

    if not (filename.lower()).endswith(currentExtension):
        return False
    
    for item in fileList:
        if (filename.lower()).endswith(item + currentExtension):
            return True

    return False


# Функция динамического определения текущего расширения файлов
def GetExtensionSettings(project_path):
    global currentExtension
    global newExtension
    global fileMarker

    for folderName, subfoldersName, fileNames in os.walk(project_path):
        for fileName in fileNames:
            ind = 0
            for item in fileExtensions:
                if (fileName.lower()).endswith(fileMarker + item):
                    currentExtension = item
                    newExtension = fileExtensions[(ind + 1) % len(fileExtensions)]
                    return
                ind = ind + 1

def ChangeFileExtensions(project_path):
    global currentExtension
    global newExtension

    for folderName, subfoldersName, fileNames in os.walk(project_path):
        for fileName in fileNames:
            if (IsNeedToChange(fileName)):
                source = folderName + '/' + fileName
                os.rename(source, os.path.join(folderName, (fileName[:-(len(currentExtension))] + newExtension)))

# Выполнение программы
GetExtensionSettings(path)
ChangeFileExtensions(path)

print('Выполнено')