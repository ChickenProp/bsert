import unittest
import traceback
import sys

class _Bsert(object):
    def __or__(self, other):
        return _Wrapped(other)

    def __call__(self, other):
        if not other:
            try:
                raise AssertionError
            except AssertionError:
                f = sys.exc_info()[2].tb_frame.f_back
            stck = traceback.extract_stack(f)
            tc = unittest.case.TestCase('__init__')
            tc.assert_(False, stck[-1][-1])
            
class _Wrapped(unittest.TestCase):
    def __init__(self, obj):
        # TestCase needs to be passed the name of one of its methods. I'm not
        # really sure why.
        super(_Wrapped, self).__init__('__init__')
        self.wrapped = obj

    def __eq__(self, other):
        self.assertEqual(self.wrapped, other)
        return True

    def __ne__(self, other):
        self.assertNotEqual(self.wrapped, other)
        return True

    def __le__(self, other):
        self.assertLessEqual(self.wrapped, other)
        return True

    def __ge__(self, other):
        self.assertGreaterEqual(self.wrapped, other)
        return True

    def __lt__(self, other):
        self.assertLess(self.wrapped, other)
        return True

    def __gt__(self, other):
        self.assertGreater(self.wrapped, other)
        return True

    def __or__(self, other):
        return _Wrapped(self.wrapped | other)

bsert = _Bsert()
