import pandas as pd

from ..source import Source, URIs
from sources.pycountry_util import find_country

class Gabv(Source):
    """
    GABV: The Global Alliance on Banking Values. These banks have agreed to some
    ethically stringent standards that often include divesting from fossil fuels.

    This dataset contains both GABV banks and B-Impact banks. The datasets were manually
    merged early in Bank.Green project, though it would be better to have a seperate
    B-Impact source and merge automatically.
    """

    def __init__(self, bankreg, name, is_retail_1no_0yes_blankunk, b_impact,
                 gabv, country, website, twitter, description, mission,
                 history, structure, market_focus, overall_score,
                 impact_area_environment, state, city, sector_2,
                 size, industry, industry_category,
                 products_and_services, sector):

        if pd.isna(gabv):
            gabv = None
        if pd.isna(b_impact):
            b_impact = None

        country = find_country(country)[1]

        self.is_retail_1no_0yes_blankunk = is_retail_1no_0yes_blankunk
        self.b_impact = b_impact
        self.gabv = gabv
        self.website = website
        self.twitter = twitter
        self.description = description
        self.mission = mission
        self.history = history
        self.structure = structure
        self.market_focus = market_focus
        self.overall_score = overall_score
        self.impact_area_environment = float(impact_area_environment)
        self.state = state
        self.city = city
        self.sector_2 = sector_2
        self.size = size
        self.industry = industry
        self.industry_category = industry_category
        self.products_and_services = products_and_services
        self.sector = sector

        super(Gabv, self).__init__(bankreg=bankreg,
                                   name=name,
                                   countries=set([country]))

    def add_new_country(self, countries):
        ''' gabv banks are sometimes represented multiple times in
            the same dataset. This is a bit of a hack to make
            multiple countries possible, although not all data
            is preserved when more than one gabv bank is in the dataset
        '''
        new_countries = [find_country(x)[1] for x in countries]
        self.countries.update(set(new_countries))

    @classmethod
    def load_and_create(cls, bankreg):
        df = pd.read_csv(URIs.GABV.value)

        for (i, row) in df.iterrows():
            bank = Gabv(bankreg=bankreg,
                        name=row['company_name'],
                        is_retail_1no_0yes_blankunk=row['No Retail Banking? 1 = No, 0 = Yes, Blank = Unknown'],
                        b_impact=row['b-impact'],
                        gabv=row['GABV'],
                        country=row['country'],
                        website=row['website'],
                        twitter=row['twitter'],
                        description=row['description'],
                        mission=row['Mission'],
                        history=row['History'],
                        structure=row['Structure'],
                        market_focus=row['Market Focus'],
                        overall_score=row['overall_score'],
                        impact_area_environment=row['impact_area_environment'],
                        state=row['state'],
                        city=row['city'],
                        sector_2=row['sector_2'],
                        size=row['size'],
                        industry=row['industry'],
                        industry_category=row['industry_category'],
                        products_and_services=row['products_and_services'],
                        sector=row['sector'])

            bankreg.create_or_update_bank(source=bank)
        len(bankreg.reg)
