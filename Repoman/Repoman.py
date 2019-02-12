import requests
import json
import os

class Repo:
    '''
    Implements repository with top 5000 packages python downloads.

    '''
    def __init__(self):
        self.packages = self.__getTopDownloads()
        self.downloaded = []
        self.repopath = None

    # private method
    def __getTopDownloads(self, url = 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.json'):
        '''
            Gets the top 5000 PyPi download packages. Expects JSON object from hugovk's github.

            Returns a list of packages.
        '''
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("HTTP response is not 200!")

        try: 
            j = json.loads(r.text)
        except json.decoder.JSONDecodeError:
            raise Exception("JSON not found!")

        packages = []
        # download stats are stored in 'rows' variable
        for row in j['rows']:
            packages.append(row['project'])
        return packages
    
    def setRepoPath(self, repopath):
        '''
            Sets repository path.
        '''
        if os.path.isdir(repopath):
            self.repopath = repopath
        else:
            raise TypeError("Repo path provided is not a directory!")

    def readDownloaded(self, filepath):
        '''
            Reads in from text file. Assumes that file packages are written line by line.
        '''
        try:
            # overwrite previous packages
            self.downloaded = []
            f = open(os.path.join(os.getcwd(), filepath), 'r')
            for line in f:
                if len(line) > 0:
                    self.downloaded.append(line.replace(" ", "").strip())
            f.close()
        except FileNotFoundError:
            raise Exception("File not found!")
        return None
    
    def writeDownloaded(self, filepath):
        '''
            Writes downloaded packages to text file with one package per line.
        '''
        f = open(filepath, "w")
        for p in self.downloaded:
            f.write(p+"\n")
        f.close()
        return None

    def downloadPackages(self):
        '''
            Downloads packages using Basket to target repository path
        '''
        
        
    