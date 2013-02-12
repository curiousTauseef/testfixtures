from __future__ import with_statement
# Copyright (c) 2011-2013 Simplistix Ltd
# See license.txt for license details.

from nose.plugins.skip import SkipTest

try:
    from testfixtures.components import TestComponents
except ImportError:  # pragma: no cover
    raise SkipTest('zope.component is not available')

from mock import Mock, call
from testfixtures import Replacer, compare
from testfixtures.compat import PY3
from unittest import TestCase

from .compat import catch_warnings

class ComponentsTests(TestCase):

    def test_atexit(self):
        m = Mock()
        with Replacer() as r:
            r.replace('atexit.register', m.register)
                
            c = TestComponents()

            expected = [call.register(c.atexit)]

            compare(expected, m.mock_calls)

            with catch_warnings(record=True) as w:
                c.atexit()
                self.assertTrue(len(w), 1)
                compare(str(w[0].message), (
                    "TestComponents instances not uninstalled by shutdown!"
                    ))
                
            c.uninstall()

            compare(expected, m.mock_calls)
            
            # check re-running has no ill effects
            c.atexit()
            
            compare(expected, m.mock_calls)
