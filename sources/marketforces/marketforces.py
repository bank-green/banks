import pycountry

import pandas as pd
from sources.source import Source, URIs


class Marketforces(Source):
    """
    Marketforces an international group tracking banks' fossil fuel policies.
    Data is manually collected from the Marketforces Australian website, where
    the group is most active.
    """
    def __init__(self, bankreg, name, ff_financing, statement):
        self.name = name.rstrip().lstrip()
        self.ff_financing = ff_financing
        self.statement = statement

        country = pycountry.countries.get(alpha_2='au').name

        super(Marketforces, self).__init__(bankreg=bankreg,
                                           name=name.rstrip().lstrip(),
                                           countries=set([country]))

    @classmethod
    def load_and_create(cls, bankreg):
        df = pd.read_csv(URIs.MARKETFORCES.value)
        for (i, row) in df.iterrows():
            bank = Marketforces(
                bankreg=bankreg,
                name=str(row.Name),
                ff_financing=row['Amount Invested'],
                statement=row['Position'])
            bankreg.create_or_update_bank(source=bank)
