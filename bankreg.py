import pandas as pd
from bank import Bank
from maps.name_tag_map import name_tag_map
from maps.id_map import id_map


class BankReg:
    __instance__ = None

    def __init__(self):
        """ Constructor.
        """
        if BankReg.__instance__ is None:
            BankReg.__instance__ = self
            self.reg = {}

            # maps bank names to their tags. Used for determining bank tags.
            self.name_tag_dict = name_tag_map

            # maps bank unique identifiers (permid, LEI, etc) to bank tags.
            # Used by some data sources to denote subsidiary relationships.
            self.id_tag_dict = {'permid': {}, 'isin': {}, 'viafid': {},
                                'lei': {}, 'googleid': {}, 'wikiid': {},
                                'rssd': {}}
            for tag, v in id_map.items():
                permid, isin, viafid = v.get('permid'), v.get('isin'), v.get('viafid')
                lei, googleid, wikiid = v.get('lei'), v.get('googleid'), v.get('wikiid')
                rssd = v.get('rssd')

                if permid:
                    self.id_tag_dict['permid'][permid] = tag
                if isin:
                    self.id_tag_dict['isin'][isin] = tag
                if viafid:
                    self.id_tag_dict['viafid'][viafid] = tag
                if lei:
                    self.id_tag_dict['lei'][lei] = tag
                if googleid:
                    self.id_tag_dict['googleid'][googleid] = tag
                if wikiid:
                    self.id_tag_dict['wikiid'][wikiid] = tag
                if rssd:
                    self.id_tag_dict['rssd'][wikiid] = tag

        else:
            return BankReg.__instance__

    def update_id_tag_dict(self, source):
        # for wikidata, also the id map. this is hacky because
        # id_map is a seperate source for source already existing
        # inside of banks... It only exists because the the bank data is slow to extract
        # and would cause wikidata imports to become O(n^2).

        # cast to string
        tag = str(source.tag)
        if source.permid:
            self.id_tag_dict['permid'][source.permid] = tag
        if source.isin:
            self.id_tag_dict['isin'][source.isin] = tag
        if source.viafid:
            self.id_tag_dict['viafid'][source.viafid] = tag
        if source.lei:
            self.id_tag_dict['lei'][source.lei] = tag
        if source.googleid:
            self.id_tag_dict['googleid'][source.googleid] = tag
        if source.wikiid:
            self.id_tag_dict['wikiid'][source.wikiid] = tag
        if source.rssd:
            self.id_tag_dict['rssd'][source.rssd] = tag

    def return_tag_from_id_tag_dict(
            self, permid=None, isin=None, viafid=None,
            lei=None, googleid=None, wikiid=None, rssd=None):
        '''
        given a unique identifier of one sort or another,
        query the id_tag_dict and return the tag of the intended bank,
        or None if no tag can be found.
        '''

        permid_tag = self.id_tag_dict['permid'].get(str(permid))
        if permid_tag:
            return permid_tag

        isin_tag = self.id_tag_dict['isin'].get(str(isin))
        if isin_tag:
            return isin_tag

        viafid_tag = self.id_tag_dict['viafid'].get(str(viafid))
        if viafid_tag:
            return viafid_tag

        rssd_tag = self.id_tag_dict['rssd'].get(str(rssd))
        if rssd_tag:
            return rssd_tag
        lei_tag = self.id_tag_dict['lei'].get(str(lei))
        if lei_tag:
            return lei_tag

        googleid_tag = self.id_tag_dict['googleid'].get(str(googleid))
        if googleid_tag:
            return googleid_tag

        wikiid_tag = self.id_tag_dict['wikiid'].get(str(wikiid))
        if wikiid_tag:
            return wikiid_tag

        return None

    def create_or_update_bank(self, source):
        # If there is a preexisting Bank instance, update the instance with
        # the source's data. Otherwise register a new Bank instance.
        preexisting_bank = self.reg.get(source.tag, None)

        # update dictionaries
        self.name_tag_dict[source.name] = source.tag
        self.update_id_tag_dict(source)

        if preexisting_bank:
            # update and return
            preexisting_bank.set_data_by_source(data=source)
            return preexisting_bank
        else:
            # create, register, and return
            new_bank = Bank(bankreg=self, tag=source.tag, data=source)
            self.reg[source.tag] = new_bank
            return new_bank

    def return_registry_as_df(self, allowed_ratings=['great', 'ok', 'bad', 'worst']):
        rows = []

        for tag, bank in self.reg.items():

            rating, reason = bank.rating_reason
            if rating in allowed_ratings:

                financing_of_fossil_fuels = bank.financing_of_fossil_fuels
                row = {'tag': tag,
                       'name': bank.name,
                       'aliases': ','.join(bank.names),
                       'country': ','.join(bank.countries),
                       'data_sources': ','.join(bank.data_sources),
                       'website': bank.website,
                       'rating': rating.lower(),
                       'reason': reason,
                       'subsidiary_of': bank.subsidiary_tag,
                       'Rank - Total': financing_of_fossil_fuels['rank_total'],
                       'total-USD': financing_of_fossil_fuels['total_usd'],
                       'total-EUR': financing_of_fossil_fuels['total_eur'],
                       'total-GBP': financing_of_fossil_fuels['total_gbp'],
                       'total-AUD': financing_of_fossil_fuels['total_aud'],
                       'total-CAD': financing_of_fossil_fuels['total_cad'],
                       'permid': bank.permid,
                       'isin': bank.isin,
                       'viafid': bank.viafid,
                       'lei': bank.lei,
                       'rssd': bank.rssd,
                       'googleid': bank.googleid,
                       'wikiid': bank.wikiid}

                rows.append(row)

        return pd.DataFrame.from_dict(rows)
