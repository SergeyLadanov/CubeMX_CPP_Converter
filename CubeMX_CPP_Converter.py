#! python3
# renameFiles - переименовывает все файл в выбранной папке
# Использование:
# Скрипт размещается в каталоге с проектом
# replaceableExtension - заменяемое расширение
# newExtension - подставляемое расширение

import os, sys, time

# Текущий путь приложения
path = os.path.realpath(os.path.dirname(sys.argv[0]))

directTofolderWithFiles = path

replaceableExtension = "no_extension"
newExtension = "no_extension"

# Динамическое определение расширения
for folderName, subfoldersName, fileNames in os.walk(directTofolderWithFiles):
    for fileName in fileNames:
        if (fileName.lower()).endswith("main.c"):
            replaceableExtension = (".c").lower()
            newExtension = (".cpp").lower()
            break
        if (fileName.lower()).endswith("main.cpp"):
            replaceableExtension = (".cpp").lower()
            newExtension = (".c").lower()
            break
        


for folderName, subfoldersName, fileNames in os.walk(directTofolderWithFiles):
    for fileName in fileNames:
        if (fileName.lower()).endswith(replaceableExtension):
            filename1 = "main" + replaceableExtension
            filename2 = "it" + replaceableExtension
            if (fileName.lower()).endswith(filename1) or (fileName.lower()).endswith(filename2):
                source = folderName + '/' + fileName
                os.rename(source, os.path.join(folderName, (fileName[:-(len(replaceableExtension))] + newExtension)))

print('Выполнено')