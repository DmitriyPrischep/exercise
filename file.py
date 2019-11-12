import os
import io

class FileManager():
  def __init__(self, rootDir = None):
    if rootDir == None:
      rootDir = self._giveWorkDirectory()
    self.rootDir = rootDir

    self._fileCashe = dict()

  # Проверяет есть ли файл в кэше, если есть, то взять от туда, если нет, то закэшировать
  def takeFile(self, url):
    path = self._urlToPath(url)
  #  print("path: ", path)
    casheValue = self._isInCashe(path)
    if not casheValue:
      self._addInCache(path)
      casheValue = self._isInCashe(path)
    # print("casheValue: ", casheValue)
    return casheValue

  def _isInCashe(self, path):
    return self._fileCashe.get(path)

  def _addInCache(self, path):
    with open(path, 'rb') as file:
      self._fileCashe[path] = file.read()

  def _giveWorkDirectory(self):
    return os.getcwd()
  
  def _urlToPath(self, url):
    if url == '':
      path = './index.html'
    else:
      path = url
    return path