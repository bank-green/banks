import os
from datetime import datetime
import pandas as pd

from airtable import airtable
from dotenv import load_dotenv
load_dotenv()


class BankGreenAirtable:

    def __init__(self, table_name, local_df, preservation_columns=[]):
        self.connection = airtable.Airtable(os.getenv("base_key"), table_name, api_key=os.getenv("api_key"))
        self.connection.API_LIMIT = 0.2

        self.table_name = table_name

        self.local_df = local_df
        self.local_tags = [x for x in self.local_df['tag']]
        # columns where user data will not be overwritten
        self.preservation_columns = preservation_columns
        self.refresh()

    def refresh(self):
        self.records = self.connection.get_all()
        self.df = pd.DataFrame([record['fields'] for record in self.records],
                               index=[record['id'] for record in self.records])

        # deletion candidates marked preserve are not deletable.
        # Must be != True, not "is not True"
        deletion_candidates_tags = self.df[self.df.preserve != True].tag  # noqa

        # delete_tags are are bank tags. delete_ids are airtable row ids
        self.delete_tags = set(deletion_candidates_tags) - set(self.local_tags)
        self.delete_ids = self.list_airtable_ids_for_tags(self.delete_tags)

        self.update_tags = set(self.local_tags).intersection(set(self.df.tag))
        self.update_ids = self.list_airtable_ids_for_tags(self.update_tags)

        self.insert_tags = set(self.local_tags) - set(self.df.tag)

    def airtable_backup(self):
        now = datetime.now()
        dt_string = now.strftime("%Y.%d.%m %H.%M.%S")
        filepath = './airtable_backups/' + dt_string + ' ' + self.table_name + '.pkl'
        self.df.to_pickle(filepath)
        return filepath

    def list_airtable_ids_for_tags(self, tag_list):
        ids = [index for index, row in self.df.iterrows()
               if row['tag'] in tag_list]
        return ids

    def airtable_flush(self):
        ''' batch delete unnecessary ids'''
        deleted_data = self.df.loc[self.delete_ids]
        self.connection.batch_delete(self.delete_ids)
        return deleted_data

    def airtable_insert(self):
        '''batch insert data into airtable'''

        # filter out unnecessary to insert tags and convert to a dictionary
        insertion_dict = self.local_df.loc[
            lambda d: d['tag'].isin(self.insert_tags)].to_dict(orient='records')

        # filter out blank/nan/None values
        insertion_dict = [{k: v for k, v in item.items() if not self.true_if_empty_ish(v)}
                          for item in insertion_dict]

        # insert and return result
        return self.connection.batch_insert(insertion_dict, typecast=True)

    def airtable_update(self):

        # filter to only records that need updating
        update_records = [x for x in self.records if x['id'] in self.update_ids]
        to_be_updated = []

        # filter to only the columns tha tneed updating
        for remote_row in update_records:
            new_record = {}
            new_record['id'] = remote_row['id']
            new_record['fields'] = {}

            tag = remote_row['fields']['tag']

            local_row_dict = self.local_df[self.local_df.tag == tag].to_dict(orient='records')[0]

            for column in local_row_dict.keys():

                # get the remote and local values and determine if they are empty
                remote_value = remote_row['fields'].get(column)

                # check for value type, since airtable returns inconsistenty
                if isinstance(remote_value, list) and len(remote_value) > 0:
                    remote_value = remote_value[0]
                if isinstance(remote_value, list) and len(remote_value) == 0:
                    remote_value = None

                empty_remote = self.true_if_empty_ish(remote_value)
                local_value = local_row_dict.get(column)
                empty_local = self.true_if_empty_ish(local_value)

                # convert local nan to None, since airtable falls over with nans
                # important! None Values will not be written, since they are flagged in empty_local
                if pd.isna(local_value):
                    local_value = None

                # update the non-special columns with local results
                if column not in self.preservation_columns and not empty_local:
                    new_record['fields'][column] = local_value
                # allow some columns to be overridden if they are not empty
                elif empty_remote:
                    new_record['fields'][column] = local_value

            to_be_updated.append(new_record)
        # return to_be_updated 

        return self.connection.batch_update(to_be_updated, typecast=True)

        # single row update loop is here for debugging purposes. Batch update's errors are unhelpful.
        # for record in to_be_updated:
        #     try:
        #         self.connection.update(record['id'], record['fields'], typecast=True)
        #     except Exception as e:
        #         print(record['fields']['tag'])
        #         import pdb; pdb.set_trace()
        #         print(e)

    def true_if_empty_ish(self, str_or_other_obj):
        if str_or_other_obj is None:
            return True
        if str_or_other_obj is 'None':
            return True
        if str_or_other_obj == 'nan':
            return True
        if pd.isna(str_or_other_obj):
            return True
        if isinstance(str_or_other_obj, str) and str_or_other_obj.rstrip().lstrip() == '':
            return True
        if str_or_other_obj == '-':
            return True
        return False
