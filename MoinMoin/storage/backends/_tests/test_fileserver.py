# Copyright: 2011 MoinMoin:ThomasWaldmann
# License: GNU GPL v2 (or any later version), see LICENSE.txt for details.

"""
MoinMoin - fileserver backend tests
"""


from __future__ import absolute_import, division

import os
import tempfile

from MoinMoin.constants.keys import NAME, MTIME, REVID, ITEMID, HASH_ALGORITHM
from ..fileserver import Backend
from . import BackendTestBase


class TestFileServerBackend(BackendTestBase):
    def setup_method(self, method):
        self.path = path = tempfile.mkdtemp()
        self.be = Backend(path)
        self.be.open()

    def _prepare(self, items):
        expected_result = set()
        for name, meta, data in items:
            fn = os.path.join(self.path, name)
            dn = os.path.dirname(fn)
            try:
                os.makedirs(dn)
            except:
                pass
            with open(fn, 'wb') as f:
                f.write(data)
            meta[NAME] = name
            meta = tuple(sorted(meta.items()))
            expected_result.add((meta, data))
        return expected_result

    def test_iter(self):
        # for the fileserver store, even if the directory is empty,
        # we will get a revid for the root directory:
        contents = list(self.be)
        assert len(contents) == 1
        root_revid = contents[0]
        # revids are like relpath.mtime
        relpath, mtime = root_revid.split('.')
        assert relpath == ''

    def test_files(self):
        # note: as we can only store the data into the file system, meta can
        # only have items that are generated by the fileserver backend:
        items = [  # name,  meta,   data
                 (u'foo.png', dict(size=11, contenttype=u'image/png'), 'png content'),
                 (u'bar.txt', dict(size=12, contenttype=u'text/plain'), 'text content'),
                ]
        expected_result = self._prepare(items)
        dir_meta = tuple(sorted(dict(name=u'', size=0, contenttype=u'text/x.moin.wiki;charset=utf-8').items()))
        dir_data = """\
= Directory contents =
 * [[../]]
 * [[/bar.txt|bar.txt]]
 * [[/foo.png|foo.png]]
""".replace('\n', '\r\n')
        expected_result.add((dir_meta, dir_data))
        result = set()
        for i in self.be:
            meta, data = self.be.retrieve(i)
            # we don't want to check some meta values
            del meta[MTIME]
            del meta[HASH_ALGORITHM]
            del meta[ITEMID]
            del meta[REVID]
            meta = tuple(sorted(meta.items()))
            data = data.read()
            result.add((meta, data))
        assert result == expected_result

    def test_dir(self):
        # note: as we can only store the data into the file system, meta can
        # only have items that are generated by the fileserver backend:
        items = [  # name,  meta,   data
                 (u'dir/foo.png', dict(size=11, contenttype=u'image/png'), 'png content'),
                 (u'dir/bar.txt', dict(size=12, contenttype=u'text/plain'), 'text content'),
                ]
        expected_result = self._prepare(items)
        dir_meta = tuple(sorted(dict(name=u'', size=0, contenttype=u'text/x.moin.wiki;charset=utf-8').items()))
        dir_data = """\
= Directory contents =
 * [[../]]
 * [[/dir|dir/]]
""".replace('\n', '\r\n')
        expected_result.add((dir_meta, dir_data))
        dir_meta = tuple(sorted(dict(name=u'dir', size=0, contenttype=u'text/x.moin.wiki;charset=utf-8').items()))
        dir_data = """\
= Directory contents =
 * [[../]]
 * [[/bar.txt|bar.txt]]
 * [[/foo.png|foo.png]]
""".replace('\n', '\r\n')
        expected_result.add((dir_meta, dir_data))
        result = set()
        for i in self.be:
            meta, data = self.be.retrieve(i)
            # we don't want to check some meta values
            del meta[MTIME]
            del meta[HASH_ALGORITHM]
            del meta[ITEMID]
            del meta[REVID]
            meta = tuple(sorted(meta.items()))
            data = data.read()
            result.add((meta, data))
        assert result == expected_result
