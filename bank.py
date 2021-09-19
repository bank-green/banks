import re

import pandas as pd
from sources.banktrack.banktrack import Banktrack
from sources.bocc.bocc import BOCC
from sources.gabv.gabv import Gabv
from sources.fairfinance.fairfinance import Fairfinance
from sources.switchit.switchit import Switchit
from sources.marketforces.marketforces import Marketforces
from sources.custombank.custombank import Custombank
from sources.wikidata.wikidata import Wikidata
from sources.usnic.usnic import USNIC

from maps.preferred_names import preferred_names
from maps.id_map import id_map

class Bank:

    def __init__(self, bankreg, data, tag=None):
        self.tag = tag
        self.bankreg = bankreg
        self.banktrack = None
        self.bocc = None
        self.gabv = None
        self.fairfinance = None
        self.switchit = None
        self.custombank = None
        self.marketforces = None
        self.wikidata = None
        self.usnic = None
        self.set_data_by_source(data=data)

    @property
    def name(self):

        # sometimes a preferred name is specified for a bank.
        # In that case, return the preferred name
        # If there is more than one, just randomly choose one.

        preferred_name = set(self.names).intersection(preferred_names)
        if len(preferred_name) > 0:
            return list(preferred_name)[0]

        # if the name is specified in custombank, use it
        if self.custombank and self.custombank.name:
            return self.custombank.name
        if self.banktrack:
            return self.banktrack.name
        elif self.bocc:
            return self.bocc.name
        elif self.usnic:
            return self.usnic.name
        elif self.wikidata:
            return self.wikidata.name
        elif self.gabv:
            return self.gabv.name
        elif self.marketforces:
            return self.marketforces.name
        elif self.fairfinance:
            return self.fairfinance.name
        elif self.switchit:
            return self.switchit.name
        return 'unk'

    @property
    def names(self):
        '''returns a set of names that the bank was at some point assigned'''
        names = set()
        if self.banktrack:
            names.update([self.banktrack.name])
        if self.bocc:
            names.update([self.bocc.name])
        if self.usnic:
            # USNIC has a aliases
            names.update(self.usnic.aliases)
        if self.wikidata:
            # wikidata has a set of aliases
            names.update(self.wikidata.aliases)
        if self.gabv:
            names.update([self.gabv.name])
        if self.fairfinance:
            names.update([self.fairfinance.name])
        if self.switchit:
            names.update([self.switchit.name])
        if self.marketforces:
            names.update([self.marketforces.name])
        if self.custombank:
            names.update([self.custombank.name])

        names = {re.sub('[^0-9a-zA-Z ]+', '', x.lower().rstrip().lstrip()) for x in names}
        names = {x for x in names if x != ''}
        return sorted(names)

    @property
    def countries(self):
        countries = set()
        if self.banktrack:
            countries.update(self.banktrack.countries)
        if self.wikidata:
            countries.update(self.wikidata.countries)
        if self.bocc:
            countries.update(self.bocc.countries)
        if self.usnic:
            countries.update(self.usnic.countries)
        if self.gabv:
            countries.update(self.gabv.countries)
        if self.fairfinance:
            countries.update(self.fairfinance.countries)
        if self.switchit:
            countries.update(self.switchit.countries)
        if self.marketforces:
            countries.update(self.marketforces.countries)
        if self.custombank:
            countries.update(self.custombank.countries)
        return sorted(countries)

    @property
    def website(self):
        if self.custombank and self.custombank.website:
            return self.custombank.website
        if self.banktrack:
            return self.banktrack.website
        if self.usnic:
            return self.usnic.website
        elif self.gabv:
            return self.gabv.website
        elif self.wikidata:
            return self.wikidata.website

    @property
    def rating_reason(self):

        # custom overrides always come first
        if self.custombank and self.custombank.rating != '':
            return self.custombank.rating.lower(), self.custombank.reason

        # in case of subsidiary relationships, return the parent. Check for recursion
        if self.custombank and self.custombank.subsidiary_tag and self.custombank.subsidiary_tag != self.tag:
            rating, reason = self.bankreg.reg[self.custombank.subsidiary_tag].rating_reason
            reason = self.name + 'is owned and/or operated by ' + self.custombank.subsidiary_tag + '. ' + reason

            return rating.lower(), reason

        if self.bocc:
            return self.bocc.rating

        if self.switchit:
            return self.switchit.rating, 'This rating was determined by the switchit.money team.'
        if self.marketforces and self.marketforces.ff_financing == 0:
            reason = "This rating is based on the marketforces.org.au verification that " + self.name + " does not invest in fossl fuels." # noqa
            return 'great', reason

        if self.gabv and self.gabv.gabv is not None and self.gabv.gabv != '':
            reason = "This rating was based on " + self.name + "'s membership in the Global Alliance of Banking Values. The bank.green team has not been able to verify that the bank does not invest in fossil fuels, but believes that the bank is generally making a positive impact on the world." # noqa
            return 'ok', reason
        if self.gabv and self.gabv.b_impact:

            reason = "This rating was based on " + self.name + "'s certification as a b-impact corporation or non-profit. The bank.green team has not been able to verify that the bank does not invest in fossil fuels, but believes that the bank is generally making a positive impact on the world." # noqa
            return 'ok', reason

        if self.fairfinance:
            if self.fairfinance.rating >= 80:
                reason = self.name + " has a fairfinance guide rating of greater than 80 on the fair finance guide. It may be making a positive impact on the world." # noqa
                return 'ok', reason
            else:
                return 'unk', 'We do not have enough information to rate this bank'

        if self.wikidata and self.subsidiary_tag and self.subsidiary_tag != self.tag:
            rating, reason = self.bankreg.reg[self.subsidiary_tag].rating_reason
            reason = self.name + 'is owned and/or operated by ' + self.subsidiary_tag + '. ' + reason
            return rating.lower(), reason

        return 'unk', 'We do not have enough information to rate this bank'

    @property
    def data_sources(self):
        """returns a comma seperated string with data sources"""
        data_sources = []
        if self.banktrack:
            data_sources.append('banktrack')
        if self.bocc:
            data_sources.append('bocc')
        if self.usnic:
            data_sources.append('usnic')
        if self.wikidata:
            data_sources.append('wikidata')
        if self.gabv and not pd.isna(self.gabv.gabv):
            data_sources.append('gabv')
        if self.gabv and not pd.isna(self.gabv.b_impact):
            data_sources.append('bimpact')
        if self.fairfinance:
            data_sources.append('fairfinance')
        if self.switchit:
            data_sources.append('switchit')
        if self.marketforces:
            data_sources.append('marketforces')
        if self.custombank:
            data_sources.append('custombank')
        return sorted(data_sources)

    @property
    def subsidiary_tag(self):
        # import pdb; pdb.set_trace()
        if self.custombank and self.custombank.subsidiary_tag:
            return self.custombank.subsidiary_tag
        if self.usnic and self.usnic.subsidiary_tag:
            return self.usnic.subsidiary_tag
        if self.wikidata and self.wikidata.subsidiary_tag:
            return self.wikidata.subsidiary_tag
        return None

    @property
    def financing_of_fossil_fuels(self):
        rank_total, total_usd, total_eur, total_gbp, total_aud, total_cad = None, None, None, None, None, None

        if self.bocc:
            rank_total = self.bocc.rank
            total_usd = float(
                self.bocc.financing['fff']['FFF - 2016-2020'].replace(
                    ',', '').replace('$', '')) / 1000000000
            total_eur = self.bocc.total_financing(currency='eur')
            total_gbp = self.bocc.total_financing(currency='gbp')
            total_aud = self.bocc.total_financing(currency='aud')
            total_cad = self.bocc.total_financing(currency='cad')

        return {'rank_total': rank_total,
                'total_usd': total_usd,
                'total_eur': total_eur,
                'total_gbp': total_gbp,
                'total_aud': total_aud,
                'total_cad': total_cad}

    @property
    def permid(self):
        if self.wikidata:
            return self.wikidata.permid

    @property
    def isin(self):
        if self.wikidata:
            return self.wikidata.isin

    @property
    def viafid(self):
        if self.wikidata:
            return self.wikidata.viafid

    @property
    def rssd(self):
        if self.usnic:
            return self.usnic.rssd

    @property
    def lei(self):
        if self.wikidata and self.wikidata.lei:
            return self.wikidata.lei
        elif self.usnic and self.usnic.lei:
            return self.usnic.lei

    @property
    def googleid(self):
        if self.wikidata:
            return self.wikidata.googleid

    @property
    def wikiid(self):
        if self.wikidata:
            return self.wikidata.wikiid

    def set_data_by_source(self, data, source=None):
        '''Set bank data from a single source (e.g., just BOCC data)'''
        datatype = type(data)

        # note: Equality can have unexpected results when using autoreload.
        # if things that should be equal do not appear so, disable autoreload
        # in jupyter notebook
        if datatype == Banktrack:
            self.banktrack = data
        elif datatype == BOCC:
            self.bocc = data
        elif datatype == USNIC:
            self.usnic = data
        # case in which gabv is being overwritten
        elif datatype == Gabv and self.gabv is not None:
            self.gabv.add_new_country(data.countries)
        elif datatype == Gabv:
            self.gabv = data
        elif datatype == Fairfinance:
            self.fairfinance = data
        elif datatype == Switchit:
            self.switchit = data
        elif datatype == Marketforces:
            self.marketforces = data
        elif datatype == Custombank:
            self.custombank = data
        elif datatype == Wikidata:
            self.wikidata = data

    def __str__(self):
        return self.tag + ": " + str(self.names) + " | " + str(self.countries)

    def __repr__(self):
        type_ = type(self)
        module = type_.__module__
        qualname = type_.__qualname__
        return f"<{self.tag} {type(self)} with {', '.join(self.data_sources)}>"
