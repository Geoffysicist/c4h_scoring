"""directory_tree prints the directory tree as a text file.

use the exclude key word argument to exclude unwanted files.
For example exclude="." excludes all files starting with .
exclude='._' excludes all files starting with . or _
exclude='foo' excludes all files starting with f, or o.

  Typical usage example:

  paths = DisplayablePath.make_tree(Path('relative_path'), exclude='._')
  for path in paths:
    print(path.displayable())

TODO add .gitignore to criteria
"""
from pathlib import Path

class DisplayablePath(object):
    display_filename_prefix_middle = '├──'
    display_filename_prefix_last = '└──'
    display_parent_prefix_middle = '    '
    display_parent_prefix_last = '│   '

    def __init__(self, path, parent_path, is_last):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name

    @classmethod
    def make_tree(cls, root, parent=None, is_last=False, exclude=None):
        root = Path(str(root))
        # criteria = criteria or cls._default_criteria
        exclude = exclude

        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        children = sorted(list(path
                               for path in root.iterdir()
                               if cls.check_criteria(path, exclude=exclude)),
                          key=lambda s: str(s).lower())
        count = 1
        for path in children:
            is_last = count == len(children)
            if path.is_dir():
                yield from cls.make_tree(path,
                                         parent=displayable_root,
                                         is_last=is_last,
                                         exclude=exclude)
            else:
                yield cls(path, displayable_root, is_last)
            count += 1

    # @classmethod
    # def _default_criteria(cls, path):
    #     return True

    @classmethod
    def check_criteria(cls, path, exclude):
        # exclude = exclude
        sub_path = path.__str__().split('\\')[-1]
        # print(sub_path)
        if sub_path[0] in exclude:
            # print(f'ignored path {path}')
            return False
        else:
            # print(path)

            return True

            

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name

    def displayable(self):
        if self.parent is None:
            return self.displayname

        _filename_prefix = (self.display_filename_prefix_last
                            if self.is_last
                            else self.display_filename_prefix_middle)

        parts = ['{!s} {!s}'.format(_filename_prefix,
                                    self.displayname)]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(self.display_parent_prefix_middle
                         if parent.is_last
                         else self.display_parent_prefix_last)
            parent = parent.parent

        return ''.join(reversed(parts))

if __name__ == "__main__":
    paths = DisplayablePath.make_tree(Path('C4HScore'), exclude='._')
    for path in paths:
        print(path.displayable())