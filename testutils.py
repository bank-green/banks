import pandas as pd

from bankreg import BankReg
from sources.banktrack.banktrack import Banktrack
from sources.bocc.bocc import BOCC
from sources.gabv.gabv import Gabv
# from sources.fairfinance.fairfinance import Fairfinance
from sources.switchit.switchit import Switchit
# from sources.marketforces.marketforces import Marketforces
from sources.custombank.custombank import Custombank


bankreg = BankReg()

banktrack1 = Banktrack(bankreg=bankreg,
                       name='aname',
                       tag='atag',
                       description='adescription',
                       update_date='anupdate',
                       banktrack_link='alink',
                       country='Canada',
                       website='awebsite')

banktrack2 = Banktrack(bankreg=bankreg,
                       name='bname',
                       tag='btag',
                       description='bdescription',
                       update_date='bnupdate',
                       banktrack_link='blink',
                       country='Mexico',
                       website='bwebsite')


banktrack3 = Banktrack(bankreg=bankreg,
                       name='Santander',
                       tag='santander',
                       description='bdescription',
                       update_date='bnupdate',
                       banktrack_link='blink',
                       country='Mexico',
                       website='bwebsite')


ran1 = BOCC(bankreg=bankreg,
            name='BOCC ,name ',
            country='ar',
            europe=True,
            asia=False,
            north_america=False,
            canada=False,
            uk=False,
            australia=True,
            percent_assets='20%',
            assets_2020=100,
            coal_score=20,
            og_score=40,
            total_financing=pd.Series(['a', 'b', 'c']),
            arctic_og_financing=pd.Series(['a', 'b', 'c']),
            coal_mining_financing=pd.Series(['a', 'b', 'c']),
            coal_power_financing=pd.Series(['a', 'b', 'c']),
            expansion_financing=pd.Series(['a', 'b', 'c']),
            fracking_financing=pd.Series(['a', 'b', 'c']),
            lng_financing=pd.Series(['a', 'b', 'c']),
            offshore_financing=pd.Series(['a', 'b', 'c']),
            tar_sands_financing=pd.Series(['a', 'b', 'c']))

ran2 = BOCC(bankreg=bankreg,
            name='Bank name',
            country='ar',
            europe=True,
            asia=False,
            north_america=False,
            canada=False,
            uk=False,
            australia=True,
            percent_assets='20%',
            assets_2020=100,
            coal_score=20,
            og_score=40,
            total_financing=pd.Series(['a', 'b', 'c']),
            arctic_og_financing=pd.Series(['a', 'b', 'c']),
            coal_mining_financing=pd.Series(['a', 'b', 'c']),
            coal_power_financing=pd.Series(['a', 'b', 'c']),
            expansion_financing=pd.Series(['a', 'b', 'c']),
            fracking_financing=pd.Series(['a', 'b', 'c']),
            lng_financing=pd.Series(['a', 'b', 'c']),
            offshore_financing=pd.Series(['a', 'b', 'c']),
            tar_sands_financing=pd.Series(['a', 'b', 'c']))

# a BOCC bank with what should be a name similar banktrack 1
ran3 = BOCC(bankreg=bankreg,
            name='aname',
            country='ar',
            europe=True,
            asia=False,
            north_america=False,
            canada=False,
            uk=False,
            australia=True,
            percent_assets='20%',
            assets_2020=100,
            coal_score=20,
            og_score=40,
            total_financing=pd.Series(['a', 'b', 'c']),
            arctic_og_financing=pd.Series(['a', 'b', 'c']),
            coal_mining_financing=pd.Series(['a', 'b', 'c']),
            coal_power_financing=pd.Series(['a', 'b', 'c']),
            expansion_financing=pd.Series(['a', 'b', 'c']),
            fracking_financing=pd.Series(['a', 'b', 'c']),
            lng_financing=pd.Series(['a', 'b', 'c']),
            offshore_financing=pd.Series(['a', 'b', 'c']),
            tar_sands_financing=pd.Series(['a', 'b', 'c']))

# 'Banco Santander': 'santander',
ran4 = BOCC(bankreg=bankreg,
            name='Banco Santander',
            country='ar',
            europe=True,
            asia=False,
            north_america=False,
            canada=False,
            uk=False,
            australia=True,
            percent_assets='20%',
            assets_2020=100,
            coal_score=20,
            og_score=40,
            total_financing=pd.Series(['a', 'b', 'c']),
            arctic_og_financing=pd.Series(['a', 'b', 'c']),
            coal_mining_financing=pd.Series(['a', 'b', 'c']),
            coal_power_financing=pd.Series(['a', 'b', 'c']),
            expansion_financing=pd.Series(['a', 'b', 'c']),
            fracking_financing=pd.Series(['a', 'b', 'c']),
            lng_financing=pd.Series(['a', 'b', 'c']),
            offshore_financing=pd.Series(['a', 'b', 'c']),
            tar_sands_financing=pd.Series(['a', 'b', 'c']))

gabv1 = Gabv(bankreg=bankreg,
             name='Banco Santander',
             is_retail_1no_0yes_blankunk='',
             b_impact='',
             gabv='',
             country='Argentina',
             website='http://gabvSantander.com',
             twitter='',
             description='',
             mission='',
             history='',
             structure='',
             market_focus='',
             overall_score=40,
             impact_area_environment='8',
             state='',
             city='',
             sector_2='',
             size='',
             industry='',
             industry_category='',
             products_and_services='',
             sector='')

gabv2 = Gabv(bankreg=bankreg,
             name='Banco Santander',
             is_retail_1no_0yes_blankunk='',
             b_impact='',
             gabv='',
             country='Mexico',
             website='http://gabvSantander.com',
             twitter='',
             description='',
             mission='',
             history='',
             structure='',
             market_focus='',
             overall_score=40,
             impact_area_environment='8',
             state='',
             city='',
             sector_2='',
             size='',
             industry='',
             industry_category='',
             products_and_services='',
             sector='')

switchit1 = Switchit(bankreg=bankreg,
                     name='HSBC',
                     rating='Terrible')

subsidiary_bank = Custombank(bankreg=bankreg,
                             name='subsidiary_bank',
                             subsidiary_tag='hsbc',
                             bank_tag='')
