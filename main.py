import re

import pandas as pd


def main():
    wos_data = pd.read_excel("WoS2020.xlsx")
    scopus_data = pd.read_csv("data_scopus.csv")
    wos_data_filter = wos_data.filter(items=['Article Title'])
    scopus_data_filter = scopus_data.filter(items=[' Title'])
    wos_data_filter['KEY'] = wos_data_filter.apply(
        lambda x: re.compile('\W').sub('', x.get("Article Title")).upper(), axis=1)
    scopus_data_filter['KEY'] = scopus_data_filter.apply(
        lambda x: re.compile('\W').sub('', x.get(" Title")).upper(), axis=1)
    wos_data_filter_key = wos_data_filter.filter(items=['KEY'])
    scopus_data_filter_key = scopus_data_filter.filter(items=['KEY'])
    result_wos_scopus = pd.concat([wos_data_filter_key, scopus_data_filter_key])
    result_wos_scopus = result_wos_scopus.loc[result_wos_scopus.duplicated(keep=False), :]

    concat_data = pd.concat([wos_data_filter_key, result_wos_scopus])
    result_data_key = concat_data.drop_duplicates(keep=False)

    result_data_key_title = pd.merge(left=result_data_key, right=wos_data_filter, left_on="KEY", right_on="KEY")
    result_full_data = pd.merge(left=result_data_key_title, right=wos_data, left_on="Article Title",
                                right_on="Article Title")

    result_full_data.to_excel("result_data_wos.xlsx", index=False)