from enum import Enum
import re
import unidecode


class URIs(Enum):
    BANK_TRACK = 'https://www.banktrack.org/service/sections/Bankprofile/financedata'
    BOCC = './sources/bocc/ran_complete_2021.csv'
    GABV = './sources/gabv/gabv_bimpact_banks.csv'
    FAIR_FINANCE = './sources/fairfinance/fairfinance.csv'
    SWITCHIT = './sources/switchit/switchit.csv'
    MARKETFORCES = './sources/marketforces/marketforces.csv'
    CUSTOM_BANK = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS83tz2TOX3T50O4QR7SEaG2-8o-uLGbic9PAhqqWQ8JcWs_V2v_-XTqtzUG_PxzBk1fLU5YEGyqYJ1/pub?output=csv' # noqa
    WIKIDATA = './sources/wikidata/query.sparql'
    USNIC_ACTIVE = './sources/USNIC/CSV_ATTRIBUTES_ACTIVE.CSV'
    USNIC_RELATIONSHIPS = './sources/USNIC/CSV_RELATIONSHIPS.CSV'
    USNIC_TRANSFORMATIONS = './sources/USNIC/CSV_TRANSFORMATIONS.CSV'


class Source:
    def __init__(self, bankreg, name, countries,
                 permid=None, isin=None, viafid=None, lei=None, googleid=None, wikiid=None, rssd=None,
                 rssd_hd=None, cusip=None, thrift=None, thrift_hc=None, aba_prim=None, fdic_cert=None, ncua=None,
                 occ=None, ein=None, subsidiary_tag=None):
        self.bankreg = bankreg
        self.name = name.rstrip().lstrip()
        self.countries = countries
        self.permid = permid
        self.isin = isin
        self.viafid = viafid
        self.lei = lei
        self.googleid = googleid
        self.wikiid = wikiid
        self.rssd = rssd
        self.rssd_hd = rssd_hd
        self.cusip = cusip
        self.thrift = thrift
        self.thrift_hc = thrift_hc
        self.aba_prim = aba_prim
        self.ncua = ncua
        self.fdic_cert = fdic_cert
        self.occ = occ
        self.ein = ein

        # subsidiary tags must be lowercased to prevent bad lookups
        if subsidiary_tag:
            subsidiary_tag = subsidiary_tag.lower().lstrip().rstrip()

        self.subsidiary_tag = subsidiary_tag

    def autogenerate_tag(self):
        """ using the bank name replace spaces with underscores.
            convert accented characters to non accented. Remove special characters."""
        mystr = unidecode.unidecode(self.name).lower(
        ).rstrip().lstrip().replace(' ', '_')
        mystr = re.sub('[\W]', '', mystr) # noqa
        return mystr

    @property
    def tag(self):
        # Check the id_tag_dict for entries. If there are entries there, return them.
        lookup_tag = self.bankreg.return_tag_from_id_tag_dict(
            permid=self.permid, isin=self.isin, viafid=self.viafid, lei=self.lei,
            googleid=self.googleid, wikiid=self.wikiid, rssd=self.rssd)
        if lookup_tag:
            return lookup_tag.lower()

        # check the name_tag_dict. If there is an entry there, return it.
        name_tag_dict = self.bankreg.name_tag_dict
        if name_tag_dict.get(self.name):
            return name_tag_dict.get(self.name).lower()

        # check the name_tag_dict for unidecoded names. If there is an entry there, return it.
        unidecoded_name = unidecode.unidecode(self.name)
        if name_tag_dict.get(unidecoded_name):
            return name_tag_dict.get(unidecoded_name).lower()

        # if all else fails, autogenerate a tag
        return self.autogenerate_tag().lower()
