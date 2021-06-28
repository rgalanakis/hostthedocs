import os

from hostthedocs import filekeeper as fk
from hostthedocs import util
from tests import THISDIR

from .test_filekeeper import make_uploaded_file, BaseTestUnpackProject

ZIPFILE_SUB = os.path.join(THISDIR, 'project_sub.zip')
TARFILE_SUB = os.path.join(THISDIR, 'project_sub.tar')
TARGZFILE_SUB = os.path.join(THISDIR, 'project_sub.tar.gz')
TARBZ2FILE_SUB = os.path.join(THISDIR, 'project_sub.tar.bz2')


class TestUnpackProjectFileSub(BaseTestUnpackProject):
    def find_root(self, uploaded_file):
        with util.FileExpander(uploaded_file) as compressed_file:
            root_dir = fk.find_root_dir(compressed_file)
        
            assert(root_dir == "project")

    def test_find_root_zip(self):
        uploaded_file = make_uploaded_file(ZIPFILE_SUB)
        self.find_root(uploaded_file)
        
    def test_find_root_tar(self):
        uploaded_file = make_uploaded_file(TARFILE_SUB)
        self.find_root(uploaded_file)
        
    def test_find_root_tar_gz(self):
        uploaded_file = make_uploaded_file(TARGZFILE_SUB)
        self.find_root(uploaded_file)
        
    def test_find_root_tar_bz2(self):
        uploaded_file = make_uploaded_file(TARBZ2FILE_SUB)
        self.find_root(uploaded_file)
        
    def do_unpacks(self, uploaded_file):
        tempd = self.make_temp_dir()
        metad = {'name': 'proj', 'version': '1.1', 'description': 'descr'}
        fk.unpack_project(uploaded_file, metad, tempd)

        self.assert_exists('proj')
        self.assert_exists('proj/1.1')
        self.assert_exists('proj/1.1/index.html', exists=os.path.isfile)
        self.assert_exists('proj/description.txt', exists=os.path.isfile)

    def test_unpack_zip(self):
        uploaded_file = make_uploaded_file(ZIPFILE_SUB)
        self.do_unpacks(uploaded_file)

    def test_unpack_tar(self):
        uploaded_file = make_uploaded_file(TARFILE_SUB)
        self.do_unpacks(uploaded_file)

    def test_unpack_tar_gz(self):
        uploaded_file = make_uploaded_file(TARGZFILE_SUB)
        self.do_unpacks(uploaded_file)

    def test_unpack_tar_bz(self):
        uploaded_file = make_uploaded_file(TARBZ2FILE_SUB)
        self.do_unpacks(uploaded_file)
