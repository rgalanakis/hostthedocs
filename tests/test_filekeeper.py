import os
import shutil
import tempfile
import unittest

from hostthedocs import filekeeper as fk


THISDIR = os.path.dirname(__file__)
DOCFILESDIR = os.path.join(THISDIR, 'docfiles')
ZIPFILE = os.path.join(THISDIR, 'project.zip')


class TestParseDocfiles(unittest.TestCase):
    def test_parses(self):
        result = fk.parse_docfiles(DOCFILESDIR, 'static')
        ideal = [
            {
                'name': 'project1',
                'description': 'Project description.',
                'versions': [
                    {'version': '1.0.1',
                     'link': 'static/project1/1.0.1/index.html'},
                    {'version': '1.2.0',
                     'link': 'static/project1/1.2.0/index.html'}
                ]
            },
            {
                # Caps to test sorting
                'name': 'Project2',
                'description': fk.DEFAULT_PROJECT_DESCRIPTION,
                'versions': [
                    {'version': '2.0.3',
                     'link': 'static/Project2/2.0.3/index.html'},
                ]
            },
            {
                'name': 'project3',
                'description': fk.DEFAULT_PROJECT_DESCRIPTION,
                'versions': [
                    {'version': '3.3.3',
                     'link': 'static/project3/3.3.3/index.html'},
                ]
            }
        ]
        self.assertEqual(result, ideal)

    def test_not_existing_dir(self):
        self.assertEqual(fk.parse_docfiles('balh blah blah', 'static'), {})


class TestUnpackProject(unittest.TestCase):
    def test_unpacks(self):
        tempd = tempfile.mkdtemp('hostthedocs_tests')
        self.addCleanup(shutil.rmtree, tempd)
        metad = {'name': 'proj', 'version': '1.1', 'description': 'descr'}
        fk.unpack_project(ZIPFILE, metad, tempd)

        def assert_exists(tail, exists=os.path.isdir):
            path = os.path.join(tempd, tail)
            self.assertTrue(exists(path), '%s does not exist' % path)

        assert_exists('proj')
        assert_exists('proj/1.1')
        assert_exists('proj/1.1/index.html', os.path.isfile)
        assert_exists('proj/description.txt', os.path.isfile)
