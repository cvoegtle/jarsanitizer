import unittest
from zipfile import ZipFile
from sanitzier import FileFinder
from sanitzier import Sanitizer

class FileFinderTestCase(unittest.TestCase):
    def test_listfiles(self):
        finder = FileFinder("/Users/cv/.m2/repository")
        files = finder.find()
        print(files)
        self.assertEqual(669, len(files))

    def test_sanitizer(self):
        sanitizer = Sanitizer()
        file_removed = sanitizer.clean('/Users/cv/.m2/repository/ant/ant/1.6.5/ant-1.6.5.jar')
        print(file_removed)

    def test_zip(self):
        zip = ZipFile('/Users/cv/Downloads/asm-7.0.zip')
        print(zip.namelist())



if __name__ == '__main__':
    unittest.main()
