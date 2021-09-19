import unidecode

import pycountry
import pandas as pd

from ..source import Source, URIs


class BOCC(Source):
    """
    BOCC = The Banking on Climate Change Annual Report, published with help of the
    Rainforest action network (RAN).
    BOCC, unlike other data sources, provides detailed financing breakdowns for each
    of the banks it tracks. Since BOCC tracks the n largest banks in the world (60 banks in 2021),
    many smaller banks in other datasets end up being owned by one of the banks here.
    """

    def __init__(self, bankreg, name, country,
                 europe, asia, north_america, canada, uk, australia,
                 percent_assets, assets_2020,
                 coal_score, og_score,
                 total_financing, arctic_og_financing, coal_mining_financing,
                 coal_power_financing, expansion_financing, fracking_financing,
                 lng_financing, offshore_financing, tar_sands_financing):
        # country = pycountry.countries.get(alpha_2=country).name
        # self.name = name
        # self.countries = set([country])
        self.regions = {'europe': europe,
                        'asia': asia,
                        'north america': north_america,
                        'canada': canada,
                        'uk': uk,
                        'australia': australia}
        self.assets = {'percent_assets_loaned_since_2016': float(percent_assets.replace('%', '')),
                       '2020_assets': assets_2020}
        self.policy_score = {'coal': coal_score, 'og': og_score}

        self.financing = {
            'fff': total_financing,
            'aog': arctic_og_financing,
            'cm': coal_mining_financing,
            'cp': coal_power_financing,
            'e': expansion_financing,
            'fog': fracking_financing,
            'lng': lng_financing,
            'oog': offshore_financing,
            'ts': tar_sands_financing}


        super(BOCC, self).__init__(bankreg=bankreg,
                                   name=name,
                                   countries=set([pycountry.countries.get(alpha_2=country).name]))


    @classmethod
    def load_and_create(cls, bankreg):
        df = pd.read_csv(URIs.BOCC.value)

        for i, row in df.iterrows():
            bank = BOCC(
                bankreg=bankreg,
                name=row['Bank'],
                country=row['Country'],
                europe=row['Europe'],
                asia=row['Asia'],
                north_america=row['North America'],
                canada=row['Canada'],
                uk=row['UK'],
                australia=row['Australia'],

                percent_assets=row['Cum % of Assets Loaned since 2016'],
                assets_2020=row['2020 Assets (Billions)'],

                coal_score=row['Policy - Total Coal (0/80)'],
                og_score=row['Policy - Total O&G (0/120)'],

                total_financing=row[['FFF - total rank', 'FFF - European Rank', 'FFF - Asian Rank', 'FFF - North American Rank', 'FFF - Canadian Rank',
                                     'FFF - UK Rank', 'FFF - 2016', 'FFF - 2017', 'FFF - 2018', 'FFF - 2019', 'FFF - 2020', 'FFF - 2016-2020', 'FFF - Compared To 2016']],
                arctic_og_financing=row[['AOG - Rank', 'AOG - European Rank', 'AOG - Asian Rank', 'AOG - North American Rank', 'AOG - Canadian Rank',
                                         'AOG - UK Rank', 'AOG - 2016', 'AOG - 2017', 'AOG - 2018', 'AOG - 2019', 'AOG - 2020', 'AOG - Total', 'AOG - Compared To 2016']],
                coal_mining_financing=row[['CM - Rank', 'CM - European Rank', 'CM - Asian Rank', 'CM - North American Rank', 'CM - Canadian Rank',
                                           'CM - UK Rank', 'CM - 2016', 'CM - 2017', 'CM - 2018', 'CM - 2019', 'CM - 2020', 'CM - Total', 'CM - Compared To 2016']],
                coal_power_financing=row[['CP - Rank', 'CP - European Rank', 'CP - Asian Rank', 'CP - North American Rank', 'CP - Canadian Rank',
                                          'CP - UK Rank', 'CP - 2016', 'CP - 2017', 'CP - 2018', 'CP - 2019', 'CP - 2020', 'CP - Total', 'CP - Compared To 2016']],
                expansion_financing=row[['FFE - Rank', 'FFE - European Rank', 'FFE - Asian Rank', 'FFE - North American Rank', 'FFE - Canadian Rank',
                                         'FFE - UK Rank', 'FFE - 2016', 'FFE - 2017', 'FFE - 2018', 'FFE - 2019', 'FFE - 2020', 'FFE - Total', 'FFE - Compared To 2016']],
                fracking_financing=row[['FOG - Rank', 'FOG - European Rank', 'FOG - Asian Rank', 'FOG - North American Rank', 'FOG - Canadian Rank',
                                        'FOG - UK Rank', 'FOG - 2016', 'FOG - 2017', 'FOG - 2018', 'FOG - 2019', 'FOG - 2020', 'FOG - Total', 'FOG - Compared To 2016']],
                lng_financing=row[['LNG - Rank', 'LNG - European Rank', 'LNG - Asian Rank', 'LNG - North American Rank', 'LNG - Canadian Rank',
                                   'LNG - UK Rank', 'LNG - 2016', 'LNG - 2017', 'LNG - 2018', 'LNG - 2019', 'LNG - 2020', 'LNG - Total', 'LNG - Compared To 2016']],
                offshore_financing=row[['OOG - Rank', 'OOG - European Rank', 'OOG - Asian Rank', 'OOG - North American Rank', 'OOG - Canadian Rank',
                                        'OOG - UK Rank', 'OOG - 2016', 'OOG - 2017', 'OOG - 2018', 'OOG - 2019', 'OOG - 2020', 'OOG - Total', 'OOG - Compared To 2016']],
                tar_sands_financing=row[['TS - Rank', 'TS - European Rank', 'TS - Asian Rank', 'TS - North American Rank', 'TS - Canadian Rank',
                                         'TS - UK Rank', 'TS - 2016', 'TS - 2017', 'TS - 2018', 'TS - 2019', 'TS - 2020', 'TS - Total', 'TS - Compared To 2016']]
            )

            bankreg.create_or_update_bank(source=bank)


    @classmethod
    def number_in_billions(cls, number):
        altered_number = str(number).replace(',', '').replace('$', '')
        altered_number = float(altered_number) / 1000000000

        return altered_number

    @property
    def rank(self):
        rank_total = int(self.financing['fff']['FFF - total rank'])
        return rank_total

    @property
    def rating(self):
        ff_asset_percent = self.assets['percent_assets_loaned_since_2016']

        reason = str(ff_asset_percent) + "% of " + self.name + "'s assets in have been invested in fossil fuels between 2016 and 2020.\n"  # noqa
        ################################################
        # if a bank is a top 5 financer, rate it worst #
        ################################################
        financing = self.financing
        financing_ranks = [financing['fff']['FFF - total rank'],
                           financing['aog']['AOG - Rank'],
                           financing['cm']['CM - Rank'],
                           financing['cp']['CP - Rank'],
                           financing['e']['FFE - Rank'],
                           financing['fog']['FOG - Rank'],
                           financing['lng']['LNG - Rank'],
                           financing['oog']['OOG - Rank'],
                           financing['ts']['TS - Rank']]
        financing_ranks = [x for x in financing_ranks if x <= 5]

        financial_tuples = [('all fossil fuel infrastructure (Total)', financing['fff']['FFF - total rank']),
                            ('arctic oil and gas', financing['aog']['AOG - Rank']),
                            ('coal mining', financing['cm']['CM - Rank']),
                            ('coal power', financing['cp']['CP - Rank']),
                            ('expansion of existing fossil fuel infrastructure', financing['e']['FFE - Rank']),
                            ('fracked oil and gas', financing['fog']['FOG - Rank']),
                            ('liquid natural gas', financing['lng']['LNG - Rank']),
                            ('offshore oil and gas', financing['oog']['OOG - Rank']),
                            ('tar sands', financing['ts']['TS - Rank'])]
        financial_tuples = [x for x in financial_tuples if str(x[1]).isdigit() and int(x[1]) <= 10]
        financial_tuples.sort(key=lambda tup: tup[1])

        reason += self.name + " is one of the top funders of fossil fuel infrastructure worldwide:\n"

        for pairs in financial_tuples:
            reason += '# ' + str(pairs[1]) + ' funder of ' + pairs[0] + "\n"

        if len(financing_ranks) > 0:
            return (
                'worst',
                reason)

        #########################################################
        # if a bank did not finance fossil fuels, rate it ok #
        #########################################################

        finances_2020 = [financing['fff']['FFF - 2020'],
                         financing['aog']['AOG - 2020'],
                         financing['cm']['CM - 2020'],
                         financing['cp']['CP - 2020'],
                         financing['e']['FFE - 2020'],
                         financing['fog']['FOG - 2020'],
                         financing['lng']['LNG - 2020'],
                         financing['oog']['OOG - 2020'],
                         financing['ts']['TS - 2020']]
        finances_2020 = sum([
            float(x.replace(',', '').replace('$', '')) for x in finances_2020])

        if finances_2020 == 0:
            return(
                'ok',
                "ran. This bank does not finance fossil fuels.")

        #############################################################
        # if a bank did not fall into those categories, rate it bad #
        #############################################################

        return ('bad', 'this bank has not divested from fossil fuels')

    def convert(self, year, amount, currency_from, currency_to='USD'):

        currency_from, currency_to = currency_from.upper(), currency_to.upper()

        currency_dict = {
            2016: {'USD': 1, 'EUR': 1.11, 'GBP': 1.35, 'AUD': 0.74, 'CAD': 0.7553},
            2017: {'USD': 1, 'EUR': 1.13, 'GBP': 1.29, 'AUD': 0.77, 'CAD': 0.7713},
            2018: {'USD': 1, 'EUR': 1.18, 'GBP': 1.33, 'AUD': 0.75, 'CAD': 0.7717},
            2019: {'USD': 1, 'EUR': 1.12, 'GBP': 1.28, 'AUD': 0.70, 'CAD': 0.7538},
            2020: {'USD': 1, 'EUR': 1.14, 'GBP': 1.28, 'AUD': 0.69, 'CAD': 0.7462}
        }

        usd = amount * currency_dict[year][currency_from]
        total = usd / currency_dict[year][currency_to]

        return total

    def total_financing(self, currency, financing_type='fff',
                        years=[2016, 2017, 2018, 2019, 2020]):
        financing_type = financing_type.upper()

        year_array = [financing_type + " - " + str(year) for year in years]

        convereted_amounts = []
        for year in years:
            amount_in_dollars = self.financing[
                financing_type.lower()][financing_type.upper() + " - " + str(year)]
            amount_in_dollars = self.number_in_billions(amount_in_dollars)

            amount_converted = self.convert(
                year, amount_in_dollars, currency_from='USD', currency_to=currency)
            convereted_amounts.append(amount_converted)

        return sum(convereted_amounts)
