import math
import numpy as np
import pandas as pd

from ..source import Source, URIs


class Fairfinance(Source):
    """
    Fair Finance Guides internationally track bank _policies_. They do not track how well banks follow
    their policies. The data here was manually collected from various international fair finance guides
    sometime around April 2021.
    """
    def __init__(self, bankreg, name, countries, sweden, netherlands,
                 japan, norway, brazil,
                 belgium, indonesia, germany, thailand, india):

        # individual country name attrs are used to denote data provinance
        self.sweden = sweden
        self.netherlands = netherlands
        self.japan = japan
        self.norway = norway
        self.brazil = brazil
        self.belgium = belgium
        self.indonesia = indonesia
        self.germany = germany
        self.thailand = thailand
        self.india = india

        # for the fair finance guide, assume that the countries are correctly specified
        # and do not require standardization
        super(Fairfinance, self).__init__(bankreg=bankreg,
                                          name=name,
                                          countries=set([countries]))

    @property
    def rating(self):
        scores = [self.sweden, self.netherlands, self.japan, self.norway, self.brazil,
                  self.belgium, self.indonesia, self.germany, self.thailand, self.india]

        numerator = np.nansum(scores)
        divisor = len([x for x in scores if not math.isnan(x)])

        return numerator / divisor

    @classmethod
    def load_and_create(cls, bankreg):

        df = pd.read_csv(URIs.FAIR_FINANCE.value)
        for (i, row) in df.iterrows():
            bank = Fairfinance(bankreg=bankreg,
                               name=row['Bank'],
                               countries=row['Countries'],
                               sweden=row['Sweden - fairfinanceguide.se'],
                               netherlands=row['Netherlands - https://eerlijkegeldwijzer.nl/bankwijzer/'],
                               japan=row['Japan - https://fairfinance.jp/'],
                               norway=row['Norway - https://etiskbankguide.no/'],
                               brazil=row['Brazil - https://guiadosbancosresponsaveis.org.br/'],
                               belgium=row['Belgium - https://bankwijzer.be/nl'],
                               indonesia=row['Indonesia - https://responsibank.id/'],
                               germany=row['Germany - https://www.fairfinanceguide.de/'],
                               thailand=row['Thailand - https://fairfinancethailand.org/'],
                               india=row['India - https://fairfinanceindia.org/media/495381/fair-finance-india-report_1311_final.pdf'] # noqa
                               )
            bankreg.create_or_update_bank(source=bank)
