import requests
import json

import pandas as pd
from ..source import Source, URIs
from sources.pycountry_util import find_country

from .secret import PASSWORD as password


class Banktrack(Source):
    """
    Data from BankTrack.org, a nonprofit that tracks questionable bank financing.
    The BankTrack.org project also provides unique ID's for each of the ~220 banks
    in its dataset, which this project uses.
    Because of this, BankTrack data must be imported before other data sources.
    """
    def __init__(self, bankreg, name, tag, update_date,
                 banktrack_link, country, website, description=''):

        # in the case of banktrack, a source_id is supplied by
        # the original data provider
        self.source_id = tag

        self.name = name.rstrip().lstrip()
        self.description = description
        self.update_date = update_date
        self.banktrack_link = banktrack_link
        self.countries = set([find_country(country)[1]])
        self.website = website

        super(Banktrack, self).__init__(bankreg=bankreg,
                                        name=name,
                                        countries=set([find_country(country)[1]]))

    @property
    def tag(self):
        '''overwrites parent property. Must be lowercased and stripped to match pipeline expectations'''
        return self.source_id.lower().rstrip().lstrip()

    @classmethod
    def load_and_create(cls, bankreg, load_from_api=False):

        # load from api or from local disk.
        # this is here because we don't have permission to publish one column of the data in this table
        # and definitely don't have permission for opening up BankTrack's api.
        df = None
        if not load_from_api:
            df = pd.read_csv('./sources/banktrack/bankprofiles.csv')
        else:
            r = requests.post(URIs.BANK_TRACK.value, data={'pass': password})
            res = json.loads(r.text)
            df = pd.DataFrame(res['bankprofiles'])
            df = df.drop(columns=['general_comment'])
            df.to_csv('bankprofiles.csv')

        for i, row in df.iterrows():
            bank = Banktrack(bankreg=bankreg,
                             name=row.title,
                             tag=row.tag,
                             description=row.general_comment if 'general_comment' in row.values else '',
                             update_date=row.updated_at,
                             banktrack_link=row.link,
                             country=row.country,
                             website=row.website)
            bankreg.create_or_update_bank(source=bank)
        return bankreg
