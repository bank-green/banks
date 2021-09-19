from qwikidata.sparql import return_sparql_query_results

import pandas as pd
import np

from sources.source import Source, URIs
from sources.pycountry_util import find_country


class Wikidata(Source):
    """
    Wikidata has a community sourced dataset of banks, various unique identifiers, and their countries of operation.
    Data is collected via the Wikidata.org api. The API sometimes times out when hit too often, so be sure not to
    do that.

    The most important things we collect from wikidata are subsidiary information and unique bank ids including
    - Legal Entity Identifier,
    - Permanent ID

    These ID's are used for de-duplication of banks.
    """

    def __init__(self, bankreg, name, language, websites, countries, bank_types, twitters, description, aliases,
                 permid, isin, viafid, lei, googleid, wikiid, subsidiary_tag=None):
        self.name = name.rstrip().lstrip()
        self.language = language
        self.websites = websites
        self.bank_types = bank_types
        self.twitters = twitters
        self.description = description
        self.aliases = aliases

        super(Wikidata, self).__init__(bankreg=bankreg,
                                       name=name,
                                       countries=set(countries),
                                       permid=permid,
                                       isin=isin,
                                       viafid=viafid,
                                       lei=lei,
                                       googleid=googleid,
                                       wikiid=wikiid,
                                       subsidiary_tag=subsidiary_tag)

    @property
    def tag(self):
        return super(Wikidata, self).tag

    @property
    def website(self):
        websites = sorted(self.websites)
        if len(websites) > 0:
            return websites[0]

    @classmethod
    def discard_nan_and_return_first_value(cls, aset):
        """given a set of values, discard nan.
           Return either the first item of the set or None if the set is empty"""
        aset = {x for x in aset if x == x}

        res = None
        if len(aset) > 0:
            res = list(aset)[0]
        return res

    @classmethod
    def instantiate_bank(cls, bankreg, df):
        """
        Parse a dataframe looking for the bank uri. Extract values from it and instantiate a bank
        if the bank is probably a modern one.
        """
        # get a single name for the bank
        labels = set(df['bankLabel.value'])
        labels = {x for x in labels if x == x}
        name = cls.discard_nan_and_return_first_value(labels)

        # get the languages of the name
        language = cls.discard_nan_and_return_first_value(
            set(df['bankLabel.xml:lang']))

        # get aliases and combine with labels
        aliases = set(df['bankAltLabel.value'])
        aliases = {x for x in aliases if x == x}
        aliases = aliases.union(labels)

        websites = set(df['website.value'])
        websites = {x for x in websites if x == x}

        countries = set(df['countryLabel.value'])
        countries = {x for x in countries if x == x}

        bank_types = set(df['instanceLabel.value'])
        bank_types = {x for x in bank_types if x == x}

        twitters = set(df['twitter.value'])
        twitters = {x for x in twitters if x == x}

        # get the identifiers
        permid = cls.discard_nan_and_return_first_value(set(df['permid.value']))
        isin = cls.discard_nan_and_return_first_value(set(df['isin.value']))
        viafid = cls.discard_nan_and_return_first_value(set(df['viafid.value']))
        lei = cls.discard_nan_and_return_first_value(set(df['lei.value']))
        # unclear why, but qwikidata falls over when using ?googleid as a parm. use gid instead.
        googleid = cls.discard_nan_and_return_first_value(set(df['gid.value']))
        wikiid = cls.discard_nan_and_return_first_value(set(df['bank.value']))

        # get the first description
        description = cls.discard_nan_and_return_first_value(
            set(df['bankDescription.value']))

        # used only for excluding banks that have been closed
        # discard nan, using fact that nan != nan
        closing_year = set(df['deathyear.value'])
        closing_year = {x for x in closing_year if x == x}

        # is the bank's country current or historical?
        # if its a historical country, don't add to the dataset
        country_tuples = [find_country(x) for x in countries]

        modern_country = True
        for mytup in country_tuples:
            if mytup[0] == 'failure':
                modern_country = False

        countries = [x[1] for x in country_tuples]

        # if the country is modern, its closing year does not exist, it has a language, and it has a name
        # add to the dataset
        bank = None
        if modern_country and len(closing_year) < 1 and language and name is not None:
            bank = Wikidata(
                bankreg=bankreg,
                name=name,
                language=language,
                websites=websites,
                countries=countries,
                bank_types=bank_types,
                twitters=twitters,
                description=description,
                aliases=aliases,
                permid=permid,
                isin=isin,
                viafid=viafid,
                lei=lei,
                googleid=googleid,
                wikiid=wikiid)
            bankreg.create_or_update_bank(source=bank)

        return bank

    @classmethod
    def load_and_create(cls, bankreg, load_from_api=True):

        # query wikidata and convert into dataframe
        # TODO: Use a wikidata endpoint directly and parse results instead of relying on 
        # qwikidata
        df = None
        if not load_from_api:
            df = pd.read_csv('./sources/wikidata/wikidata.csv')
        else:
            with open(URIs.WIKIDATA.value) as query_file:
                myquery = query_file.read()
            res = return_sparql_query_results(myquery)
            df = pd.json_normalize(res['results']['bindings'])
            df.to_csv('./sources/wikidata/wikidata.csv')

        # do some string replacement for easier manipulation of parent/subsidiary relationships
        df['bank.value'] = df['bank.value'].str.replace('https*\:\/\/w+\.wikidata\.org\/[a-zA-Z]+\/', '', regex=True)  # noqa
        df['parent.value'] = df['parent.value'].str.replace('https*\:\/\/w+\.wikidata\.org\/[a-zA-Z]+\/', '')  # noqa

        # remove all parent/subsidiary_of relationships that are not banks.
        bank_values = set(df['bank.value'])

        def only_allowed(val):
            if val in bank_values:
                return val
            return np.nan
        df['parent.value'] = df['parent.value'].apply(only_allowed)

        # cycle through banks and add them, temporarily ignoring parent relationships
        bank_values = set(df['bank.value'])
        for bank_value in bank_values:
            bank_df = df[df['bank.value'] == bank_value]
            bank = cls.instantiate_bank(bankreg, bank_df)

        # cycle through banks again, this time adding parent relationships
        for bank_value in bank_values:

            # not all banks are entered in the db, so not all will be found
            tag = bankreg.id_tag_dict['wikiid'].get(bank_value)
            bank_df = df[df['bank.value'] == bank_value]

            if tag:

                bank = bankreg.reg[tag]

                parent = cls.discard_nan_and_return_first_value(
                    set(bank_df['parent.value']))

                if parent and bank.wikidata:
                    bank.wikidata.subsidiary_tag = bankreg.id_tag_dict['wikiid'].get(parent).lower().rstrip().lstrip()
