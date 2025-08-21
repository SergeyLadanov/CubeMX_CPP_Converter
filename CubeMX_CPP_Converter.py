#! python3
# CubeMX+CPP_Converter - заменяет расширения указанных файлов в папке
# Использование:
# Скрипт размещается в каталоге с проектом

import os, sys, time
import re

# Имена/окончания заменяемых файлов (без расширения)
fileList = [
    "main", # Это имя используется в качестве маркера для динамического определения текущего расширения
    "*it"
]

# Массив заменяемых расширений
fileExtensions = [
    ".c",
    ".cpp"
]

# Путь к файлу со списком исходниов (для изменения расширения указанных файлов в списке)
sourceListFile = ""

# Текущий путь приложения
path = os.path.realpath(os.path.dirname(sys.argv[0]))


class ExtensionConverter(object):
    """Класс конвертера расширения файлов"""

    # Текущее расширение файлов
    __CurrentExtension = "no_extension"
    # Новое расширение файлов
    __NewExtension = "no_extension"

    # Файл со списком исходников
    __SourceListFile = ""

    def __init__(self, fileList, extensionList, directory, listfile):
        """ Конструктор класса """
        # Список файлов
        self.__FileList = fileList
        # Список расширений
        self.__ExtensionList = extensionList
        # Имя файла-маркера
        self.__MarkerName = self.__FileList[0].replace("*", ".*").lower()
        # Директория
        self.__Directory = directory

        self.__SourceListFile = listfile

    def __IsNeedToChange(self, filename):
        """ Метод проверки необходимости изменения расширения для текущего файла """
        if not (filename.lower()).endswith(self.__CurrentExtension):
            return False
        
        for item in self.__FileList:
            pattern = fr'{item.replace("*", ".*").lower()}{self.__CurrentExtension}$'

            if re.search(pattern, filename.lower()):
                return True
        return False

    def __GetExtensionSettings(self, project_path):
        """ Метод автоматического определения настроек конвертации """
        for folderName, subfoldersName, fileNames in os.walk(project_path):
            for fileName in fileNames:
                ind = 0
                fileName = folderName + '/' + fileName
                fileName = fileName.replace('\\', '/')
                for item in self.__ExtensionList:
                    pattern = fr'{self.__MarkerName}{item}$'
                    if re.search(pattern, fileName.lower()):
                        self.__CurrentExtension = item
                        self.__NewExtension = self.__ExtensionList[(ind + 1) % len(self.__ExtensionList)]
                    ind = ind + 1


    def __ChangeFileExtensions(self, project_path):
        """ Метод замены расширений файлов """
        for folderName, subfoldersName, fileNames in os.walk(project_path):
            for fileName in fileNames:
                source = folderName + '/' + fileName
                source = source.replace('\\', '/')
                if (self.__IsNeedToChange(source)):
                    if self.__SourceListFile != "":
                        self.__SourceListFile = os.path.join(path, self.__SourceListFile)
                        current_name = fileName
                        new_name = (fileName[:-(len(self.__CurrentExtension))] + self.__NewExtension)
                        head, tail = os.path.split(folderName)

                        with open (self.__SourceListFile, 'r') as f:
                            old_data = f.read()

                        new_data = old_data.replace(f'{tail}/{current_name}\n', f'{tail}/{new_name}\n')

                        with open (self.__SourceListFile, 'w') as f:
                            f.write(new_data)

                    os.rename(source, os.path.join(folderName, (fileName[:-(len(self.__CurrentExtension))] + self.__NewExtension)))

    def Process(self):
        """ Метод обработки файлов """
        self.__GetExtensionSettings(self.__Directory)
        self.__ChangeFileExtensions(self.__Directory)


# Выполнение программы
if __name__ == '__main__':
    # Экземпляр класса
    converter = ExtensionConverter(fileList, fileExtensions, path, sourceListFile)
    converter.Process()
    print('Выполнено')