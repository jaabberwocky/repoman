import unittest
import Repoman as rp
import os

class RepoTest(unittest.TestCase):
    def setUp(self):
        self.repo = rp.Repo()

    def testTopDownloads(self):
        self.assertGreater(len(self.repo.packages), 0)

    def testSetRepoPath(self):
        os.mkdir("test")
        self.repo.setRepoPath("test")
        os.rmdir("test")
        self.assertEqual(self.repo.repopath, "test")
    
    def testReadDownloaded(self):
        q = """test\ndf"""
        f = open("test.txt", "w")
        f.write(q)
        f.close()
        self.repo.readDownloaded("test.txt")
        os.remove("test.txt")
        self.assertEqual(self.repo.downloaded, ["test", "df"])
    
    def testWriteDownloaded(self):
        self.repo.downloaded = ['test' , 'df']
        self.repo.writeDownloaded("test.txt")

        packages = []
        f = open("test.txt", "r")
        for line in f:
            packages.append(line.strip())
        f.close()
        os.remove("test.txt")

        self.assertEqual(packages, ['test','df'])

if __name__ == "__main__":
    unittest.main()