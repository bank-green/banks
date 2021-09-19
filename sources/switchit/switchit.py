import pandas as pd

from sources.source import Source, URIs


class Switchit(Source):
    """
    Switchit is a UK-Based group rating banks, energy providers, and pension funds
    based on their fossil fuel policies.
    """
    def __init__(self, bankreg, name, rating):
        self.name = name.rstrip().lstrip()
        self.rating = rating

        super(Switchit, self).__init__(bankreg=bankreg,
                                       name=name,
                                       countries=set(['United Kingdom']))

    @classmethod
    def load_and_create(cls, bankreg):
        df = pd.read_csv(URIs.SWITCHIT.value)
        for (i, row) in df.iterrows():
            bank = Switchit(
                bankreg=bankreg,
                name=row.company_name,
                rating=row.rating)
            bankreg.create_or_update_bank(source=bank)
