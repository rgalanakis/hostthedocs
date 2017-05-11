import mock
import os
import random
import shutil
import tempfile
import unittest
import natsort

from hostthedocs import filekeeper as fk
from tests import DOCFILESDIR, THISDIR

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


class TestInsertLatest(unittest.TestCase):
    def test_inserts(self):
        result = fk.parse_docfiles(DOCFILESDIR, 'static')
        fk.insert_link_to_latest(result, '%(project)s/blah')
        for projinfo in result:
            gotlink = projinfo['versions'][-1]['link']
            ideallink = '%s/blah' % projinfo['name']
            self.assertEqual(gotlink, ideallink)

    def test_does_not_overwrite_existing_latest(self):
        projs = [{'name': 'Project', 'versions': [{'version': 'latest', 'link': 'SPAM'}]}]
        fk.insert_link_to_latest(projs, 'EGGS/%(project)s')
        self.assertEqual(len(projs[0]['versions']), 1)
        self.assertEqual(projs[0]['versions'][-1]['link'], 'SPAM')


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


@mock.patch('shutil.rmtree')
class DeleteFilesTests(unittest.TestCase):

    def test_noop_if_not_exist(self, rmtree):
        fk.delete_files('foo', '1.1.1', 'blah')
        self.assertFalse(rmtree.call_count)

    def test_rm_version(self, rmtree):
        fk.delete_files('Project2', '2.0.3', DOCFILESDIR)
        realpath = os.path.join(DOCFILESDIR, 'Project2', '2.0.3')
        rmtree.assert_called_once_with(realpath)

    def test_rm_all(self, rmtree):
        fk.delete_files('Project2', None, DOCFILESDIR, True)
        realpath = os.path.join(DOCFILESDIR, 'Project2')
        rmtree.assert_called_once_with(realpath)


class SortByVersionTests(unittest.TestCase):

    def test_sorts(self):
        vers = [
            '1.1', '1.2alpha', '1.2beta1', '1.2beta2',
            '1.2rc1', '1.2', '1.2.1', '1.3'
        ]
        vers = [dict(version=v) for v in vers]
        randvers = list(vers)
        random.shuffle(randvers)
        self.assertNotEqual(vers, randvers)
        randvers = natsort.natsorted(randvers, key=fk.sort_by_version)
        self.assertEqual(vers, randvers)

    def test_sorts_with_nonnumeric(self):
        pass


class ValidationTests(unittest.TestCase):

    def test_name(self):
        valid = lambda s: self.assertTrue(fk.valid_name(s))
        valid('hello there')
        valid('1 hello - _ there')
        invalid = lambda s: self.assertFalse(fk.valid_name(s))
        invalid('hel |')
        invalid('% hi')
        invalid('; hi')
        invalid('/foo')

    def test_version(self):
        valid = lambda s: self.assertTrue(fk.valid_version(s))
        valid('1.2.3')
        valid('4.rc.1')
        invalid = lambda s: self.assertFalse(fk.valid_version(s))
        invalid(' 1.2')
        invalid('1.2 ')
        invalid('1.2-')
        invalid('1.2_')
