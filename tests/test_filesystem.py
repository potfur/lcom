from src.filesystem import FileSystem


class TestFileSystem(object):
    def setup_method(self):
        self.fs = FileSystem()

    def test_find_scans_directory(self):
        result = self.fs.find('src/')
        result = {repr(ref) for ref in result}

        assert result == {
            'src/__init__.py',
            'src/filesystem.py',
            'src/lcom.py',
            'src/reflection.py'
        }

    def test_find_can_filter_by_file_name(self):
        result = self.fs.find('src/', 'filesystem.py')
        result = {repr(ref) for ref in result}

        assert result == {
            'src/filesystem.py',
        }
