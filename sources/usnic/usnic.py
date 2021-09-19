import pandas as pd

from sources.source import Source, URIs
from sources.pycountry_util import find_country


class USNIC(Source):
    """
    Data from the US National Information Center. This must be manually downloaded, and contains data on
    Banks operating in the US and their owners. The data is quite accurate, but can contain banks that are shut down
    or no longer accept deposits. It also only tracks legal entities, but not brands, creating many entities for what
    most people think of as a single entity. For example, "Bank of America Maryland, vs Bank of America"
    """

    def __init__(self, bankreg, name, aliases, country, rssd, rssd_hd, lei,
                 cusip, thrift, thrift_hc, aba_prim, fdic_cert, ncua, occ, ein,
                 website, subsidiary_tag=None):
        self.name = name.rstrip().lstrip()
        self.aliases = set([x.rstrip().lstrip() for x in aliases])
        self.website = website

        # LEI default is 0, but should be None
        if int(float('0.0')) == 0:
            lei = None

        super(USNIC, self).__init__(bankreg=bankreg,
                                    name=self.name,
                                    countries=set([country]),
                                    rssd=rssd,
                                    rssd_hd=rssd_hd,
                                    lei=lei,
                                    cusip=cusip,
                                    thrift=thrift,
                                    thrift_hc=thrift_hc,
                                    aba_prim=aba_prim,
                                    fdic_cert=fdic_cert,
                                    ncua=ncua,
                                    occ=occ,
                                    ein=ein,
                                    subsidiary_tag=subsidiary_tag)

    @property
    def tag(self):
        return super(USNIC, self).tag

    @classmethod
    def instantiate_banks(cls, bankreg):
        """
        Populate the initial us_nic banks
        """
        df = pd.read_csv(URIs.USNIC_ACTIVE.value)
        bank = None

        for (i, row) in df.iterrows():
            bank = USNIC(
                bankreg=bankreg,
                name=row['NM_SHORT'],
                aliases=[row['NM_SHORT'], row['NM_LGL']],  # TODO: include long names.
                country=find_country('United States')[1],
                rssd=str(row['#ID_RSSD']),
                rssd_hd=str(row['ID_RSSD_HD_OFF']),
                lei=str(row['ID_LEI']),
                cusip=str(row['ID_CUSIP']),
                thrift=str(row['ID_THRIFT']),
                thrift_hc=str(row['ID_THRIFT_HC']),
                aba_prim=str(row['ID_ABA_PRIM']),
                fdic_cert=str(row['ID_FDIC_CERT']),
                ncua=str(row['ID_NCUA']),
                occ=str(row['ID_OCC']),
                ein=str(row['ID_TAX']),
                website=row['URL'],
                subsidiary_tag=None)
            bankreg.create_or_update_bank(source=bank)

        return bank

    @classmethod
    def link_parents(cls, bankreg):
        # cycle through banks again, this time adding parent relationships

        df = pd.read_csv(URIs.USNIC_RELATIONSHIPS.value)
        for (i, row) in df.iterrows():
            parent_tag = bankreg.id_tag_dict['rssd'].get(str(row['#ID_RSSD_PARENT']))
            offspring_tag = bankreg.id_tag_dict['rssd'].get(str(row['ID_RSSD_OFFSPRING']))
            offspring = bankreg.reg.get(offspring_tag)

            ongoing = '12/31/9999' in row['D_DT_END']
            pct_equity = int(row['PCT_EQUITY'])

            if parent_tag and offspring_tag and offspring and ongoing and pct_equity >= 20:
                offspring.usnic.subsidiary_tag = parent_tag

    @classmethod
    def load_and_create(cls, bankreg):

        cls.instantiate_banks(bankreg)
        cls.link_parents(bankreg)
