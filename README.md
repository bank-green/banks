# Bank Green Data Pipeline and Social Harvesting Code

The Bank.Green pipeline is a tool for extract bank data from various sources, transforming them into `Bank` (`bank.py`) objects, and them loading them into an airtable for deployment on the bank.green website. The primary purposes of the pipeline are to identify banks, rate them, and to provide data on those banks for ingestion in the website.

## Running

Install dependencies and open Jupyter-Lab
`cd pipeline`
`python -m pip install -r requirements.txt`
`jupyter-lab`

The `pipeline.ipynb` notebook is used to extract data from various sources, transform it into the pipeline `Bank` format, and to load it to airtable. With proper credentials notebook can be run from top to bottom.

Without credentials, it is sometimes not possible to access remote data and is not possible to to upload to airtable. However, you still should be able to run the notebook with local data which will not differ greatly from remote.


## Repo Structure and main files
`bankreg.py`, `bank.py`, and `sources.py` provide the primary files for data transformation. `airtable.py` contains code for the (very complicated and messy) merge and upload process to airtable. The `maps` directory contains various hand-populated maps which are mostly used to match banks frou different data sources.

### bankreg.py
The `BankReg` is a singleton containing a registry of banks. As new banks are ingested, they are added to the registry.

### sources.py
`Source` is an abstract class that other sub sources (i.e. `banktrack.py`, '`gabv.py`, `wikidata.py`) inherit from. Attributes in class `Source` appear frequently across different datasets.

### bank.py
`Bank` is used to combine various sources into a single "bank" legal entity. A `Bank` instance contains one or more sources, while various `@property` tags determine which data from a `Bank`'s sources will be preferred, or combined.


## Data Sources
Bank.Green accesses data from multiple websites and sources. 

### BankTrack
`sources/banktrack/banktrack.py`
`Accessed by:` Private API or Local CSV
BankTrack supplies rich data on banks, the country that their headquarters is in, and data on what companies and projects the bank has financed.

`TODO:` BankTrack has rich data on the fossil fuel investments of various banks, but this data is currently unused to generate bank ratings. This data could be used data to generate ratings.

## BOCC (Banking on Climate Change Report, formerly known as Rainforest Action Network or RAN)
`sources/bocc/bocc.py`
`Accessed by:` Local CSV
The Banking on Climate Change report tracks fossil fuel investments of the 60 largest banks, worldwide. The report releases yearly, and bank.green uses this data to assign ratings.

`TODO:` Update this data after the release of the 2022 report

## Wikidata
`sources/wikidata/wikidata.py`
`Accessed by:` Public API or local CSV
Wikidata provides data on banks, bank names, and importantly, subsidiary information, which helps Bank.Green rate smaller banks based on their parent organization's rating. Wikidata can be messy, because some wikidatians add tag bank buildings (the physical structures) as banks (the legal entities)

`TODO:` Filter out bank buildings using a better SPARQL query


### GABV (Global Aliance on Banking Values) and B-Impact
`sources/gabv/gabv.py`
`Accessed by:` Local CSV
The Global Alliance on Banking Values and B-Impact lists were manually combined, resulting in a local CSV. These banks are generally thought to do good in the world, but do not necessarily have ratings assigned to them yet.

`TODO:` Seperate this into GABV and B-Impact data sources. B-Impact, in particular, can be accessed via the https://data.world api.


### Custom Banks
`sources/custombank/custombank.py`
`accessed by:` Google Sheets API or Local CSV
The Custom Bank spreadsheet is a private bank.green sheet used to specify preferred bank names, manually add countries to banks, manually assign subsidiary relationships, and to manually assign them ratings based on Bank.green research.

`TODO:` The functionality of this sheet may eventually be migrated to an admin dashboard type system.

### Fair Finance
`sources/fairfinance/fairfinance.py`
`accessed by:` Local CSV
The Fair Finance guide rates banks on their fossil fuel investment _policies_ (not, not on their actual investments). The data here is mostly used to identify _bad_ banks with bad policies. Banks often do not follow through on their _good_ policies are often not followed-through on.

`TODO:` Periodically manually update data

### SWITCHIT
`sources/fairfinance/fairfinance.py`
`accessed by:` Local CSV
The https://Switchit.money guide researches banks fossil fuel financing investments. https://Bank.Green trusts the switchit.money ratings, and generally transforms them directly into its own ratings.

`TODO:` Periodically manually update data

### MarketForces
`sources/marketforces/marketforces.py`
`accessed by:` Local CSV
The US National Information Center which provides CSV's of bank data. This is a very rich and accurate data source, but its fidelity is greater than the project anticipates.

`TODO:` Improve ingestion of banks, including ingesting additional bank details and work on matching USNIC banks to existing banks.


### USNIC
`sources/usnic/usnic.py`
`accessed by:` Local CSV
The Marketforces.org.au website researches Australian bank investments in fossil fuels. https://Bank.Green trusts MarketForces's research and uses it to guide ratings.

`TODO:` Periodically manually update data

## Testing
Some tests are written for the pipeline. Test using `python3 -m unittest *_test.py` Debug using `import pdb; pdb.set_trace()`.

## Future Development
There are a number of tasks for future development:
- Convert the pipeline into a Django project, adding ORM mappings for sources, developing an admin dashboard, and migrating away from airtable
- Create a new source for US-based banks and ingest from the [treasury.gov website](https://www.occ.treas.gov/topics/charters-and-licensing/financial-institution-lists/index-financial-institution-lists.html)
- Ratings in `bank.py` are currently a mess. Re-Architect this
- Ingestion of Open Courporates dataset, which should provide more subsidiary relationships and data on particular banks.


# Contact

We're friendly!

Open an issue or email albert@bank.green to ask questions about the code, the product roadmap, etc.

We welcome pull requests.

# Product Roadmap

This codebase is intended to eventually become a django application, facilitating manual cleanup of the available data.

In the meantime, there are many small TO DO's (especially regarding the USNIC data) and integrations of additional data sources.
