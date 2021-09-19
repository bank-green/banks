import pandas as pd
from sources.source import Source, URIs
from sources.pycountry_util import find_country


class Custombank(Source):
    """
    Custom Banks are banks sourced by staff at Bank.Green. Bank.Green staff sometimes rate
    banks based on their policies, add countries of operation, or add new banks that have been frequently
    requested via the contact box on the Bank.Green website. Noteworthy: Ratings that
    Bank.Green staff give a bank currently override other ratings.
    """
    def __init__(self, bankreg, name="", bank_tag=None, countries="", subsidiary_tag=None,
                 rating=None, reason=None, website=None):

        if countries != "":
            countries = set([x.rstrip().lstrip() for x in countries.split(",")])
            countries = [find_country(x)[1] for x in countries]
            countries = set(countries)
        else:
            countries = set()

        self.bank_tag = bank_tag
        if self.bank_tag:
            self.bank_tag = bank_tag.lower()

        self.website = website
        if website:
            self.website = website.rstrip().lstrip().lower()

        self.rating = rating
        if rating:
            self.rating = rating.rstrip().lstrip().lower()

        self.reason = reason
        if reason:
            self.reason = reason.rstrip().lstrip()

        super(Custombank, self).__init__(
            bankreg=bankreg,
            name=name,
            countries=countries,
            subsidiary_tag=subsidiary_tag.lower().lstrip().rstrip())

    @property
    def tag(self):
        if self.bank_tag:
            return self.bank_tag

        # search for a tag if one is not provided
        return super(Custombank, self).tag

    @classmethod
    def load_and_create(cls, bankreg, load_from_api=True):

        df = None
        if not load_from_api:
            df = pd.read_csv('./sources/custombank/custombank.csv').fillna('')
        else:
            df = pd.read_csv(URIs.CUSTOM_BANK.value).fillna('')
            df.to_csv('./sources/custombank/custombank.csv')

        for (i, row) in df.iterrows():
            bank = Custombank(
                bankreg=bankreg,
                name=row['Preferred Bank Name'],
                bank_tag=row['Bank Tag'],
                countries=row['Country'],
                subsidiary_tag=row['Subsidiary Of Tag'],
                rating=row['Rating'],
                reason=row['Rating Reason'],
                website=row['Website'])

            bankreg.create_or_update_bank(source=bank)
