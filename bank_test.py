import unittest
from testutils import banktrack1, banktrack2, banktrack3, ran1, ran4, switchit1, gabv1, gabv2
from bank import Bank
from bankreg import BankReg

class TestBanktrack(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bank = Bank(bankreg=None,
                        tag='atag',
                        data=banktrack1)

    def test_name(self):
        self.assertEqual('aname', self.bank.name)

    def test_names(self):
        self.assertEqual(['aname'], self.bank.names)

    def test_tag(self):
        self.assertEqual('atag', self.bank.tag)

    def test_countries(self):
        self.assertEqual(['Canada'], self.bank.countries)


class TestBOCC(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bank = Bank(bankreg=None,
                        data=ran1)

    def test_name(self):
        self.assertEqual('BOCC ,name', self.bank.name)

    def test_names(self):
        self.assertEqual(['bocc name'], self.bank.names)

    def test_tag(self):
        # should not have a tag unless assigned by the registry
        self.assertEqual(None, self.bank.tag)

    def test_countries(self):
        self.assertEqual(['Argentina'], self.bank.countries)


class TestSwitchIt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bank = Bank(bankreg=None,
                        data=switchit1)

    def test_name(self):
        self.assertEqual('HSBC', self.bank.name)

    def test_names(self):
        self.assertEqual(['hsbc'], self.bank.names)

    def test_countries(self):
        self.assertEqual(['United Kingdom'], self.bank.countries)

    def test_tag(self):
        # should not have a tag unless assigned by the registry
        self.assertEqual(None, self.bank.tag)

    def test_rating(self):
        self.assertEqual('Terrible', self.bank.switchit.rating)

class TestCountriesAreAlphabetised(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        BankReg.__instance__ = None
        cls.bankreg = BankReg()
        cls.bankreg.create_or_update_bank(source=banktrack3)
        cls.bankreg.create_or_update_bank(source=ran4)

    def test_alphabetised(self):
        self.assertEqual(self.bankreg.reg['santander'].countries, ['Argentina', 'Mexico'] )

if __name__ == '__main__':
    unittest.main()
