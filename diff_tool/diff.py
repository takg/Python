import argparse

'''
This file shall pick two csv sources and show the differences between them.
'''

import json
import pandas as pd


def read_config(config):
    '''
    :param config: json config path for running the test case
    :return: json data
    '''
    with open(config, mode="r") as file:
        json_data = json.load(file)

        print("test case {}: {}".format(json_data["test_case_id"], json_data["test_case_name"]))
        print("data_type: {}".format(json_data["data_type"]))
        print("lhs: {}".format(json_data["lhs"]))
        print("rhs: {}".format(json_data["rhs"]))

    return json_data


def get_df(data_type, file_name):
    '''
    Returns panda's data frame from file
    :param data_type: csv / other types
    :param file_name: input file name
    :return: data frame
    '''
    if data_type == "csv":
        data_frame = pd.read_csv(file_name)

    return data_frame


def run_diff(lhs_df, rhs_df, keys):
    '''

    :param lhs_df: lhs data frame
    :param rhs_df: lhs data frame
    :return:
    '''
    merged_df = lhs_df.merge(rhs_df, indicator=True, how='outer', on=keys)
    print(merged_df[merged_df['_merge'] != 'both'])

def main():
    '''
    The main function
    :return: None
    '''
    config_list = ["config/test_case_1.json", "config/test_case_2.json"]

    for config in config_list:
        json_data = read_config(config)
        lhs_df = get_df(json_data["data_type"], json_data["lhs"])
        rhs_df = get_df(json_data["data_type"], json_data["rhs"])
        run_diff(lhs_df, rhs_df, json_data["key"].split(','))


main()
