import requests
import json
import os

class Repo:
    '''
    Implements repository with top 5000 packages python downloads.

    '''
    def __init__(self):
        self.packages = set(self.__getTopDownloads())
        self.downloaded = None
        self.repopath = None
        self.toDownload = None

    # private method
    def __getTopDownloads(self, url = 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.json'):
        '''
            Gets the top 5000 PyPi download packages. Expects JSON object from hugovk's github.

            Returns a list of packages.
        '''
        # retry 5 times
        # TODO: store a cache and read off that instead

        ctr = 0
        while ctr < 5:
            if ctr == 5:
                return [None]
            try:
                r = requests.get(url)
            except:
                print("Unable to get URL!")
            ctr += 1

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
            self.downloaded = set()
            f = open(os.path.join(os.getcwd(), filepath), 'r')
            for line in f:
                if len(line) > 0:
                    self.downloaded.add(line.replace(" ", "").strip())
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
            Downloads packages using Basket to target repository path. Checks first for things already downloaded.
        '''
        # set exclusion
        self.toDownload = self.packages - self.downloaded
        return None
        
    