import unittest

from bankreg import BankReg
from testutils import banktrack3, ran4, switchit1, subsidiary_bank


class TestPreferredName(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        BankReg.__instance__ = None
        cls.bankreg = BankReg()
        cls.bankreg.create_or_update_bank(source=banktrack3)
        cls.bankreg.create_or_update_bank(source=ran4)

    def test_preferred_name(self):
        self.assertEqual(self.bankreg.reg['santander'].name, 'Santander')


class TestRatingSubsidiaries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        BankReg.__instance__ = None
        cls.bankreg = BankReg()


#         cls.parent = cls.bankreg.create_or_update_bank(
#             bank=switchit1)

#         cls.subsidiary = cls.bankreg.create_or_update_bank(
#             bank=subsidiary_bank)

#    def test_subsidiary_relationship_represented(self):
#        # child should have the same rating as its parent
#        self.assertEqual(self.parent.rating_reason, self.subsidiary.rating_reason)

