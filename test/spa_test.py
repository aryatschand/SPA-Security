import csv
from pathlib import Path
from typing import List
import unittest

from spa.core import SPAException, spa
from spa.ThresholdProperty import ThresholdProperty
from spa.RatioHyperproperty import RatioHyperproperty

from spa.NoiseErrorProperty import NoiseErrorProperty

import pandas as pd
import numpy as np
import spa.alg as alg

prop_1 = str(Path(__file__).parent) + '/data/prop1.csv'
prop_2 = str(Path(__file__).parent) + '/data/prop2.csv'
prop1_incomplete = str(Path(__file__).parent) + '/data/prop1_incomplete.csv'

noise_error_data = str(Path(__file__).parent) + '/data/spectre_data.csv'



def read_data(directory: str) -> List[int]:
    """Reads data from a csv file and returns it as a list of ints"""
    with open(directory, 'r') as file:
        reader = csv.reader(file, dialect='excel')
        string_vals = reader.__next__()

    data = [int(s) for s in string_vals]

    return data

def read_into_df(directory: str) -> pd.DataFrame:
    return pd.read_csv(directory)


def test_basic_threshold():
    # Find data to analyze
    data = read_into_df(prop_1)

    # Should complete successfully
    print(spa(data, ThresholdProperty(threshold=80), prob_threshold=0.9, confidence=0.9))


def test_basic_ratio():
    # Get data
    data = read_into_df(prop_1)

    # Run spa using the RatioHyperproperty (used to find speedup for 2 data sources)
    print(spa(data, RatioHyperproperty(threshold=0.6), prob_threshold=0.5, confidence=0.9))

def test_insufficient_samples():
    # Get too little data to converge to a result
    data = read_into_df(prop1_incomplete)

    with unittest.TestCase.assertRaises(None, SPAException):
        spa(data, ThresholdProperty(threshold=80), prob_threshold=0.9, confidence=0.9, iteration_limit=5)

def test_noise_error_prop():

    for comparison_val in range(40, 65, 5):

        print(comparison_val)
    
        data = read_into_df(noise_error_data)

        true_index = []

        true_data = pd.DataFrame()
        false_data = pd.DataFrame()

        true_error_data = []
        false_error_data = []

        #comparison_val =40
        run_num = 1

        while len(data.query('run == ' + str(run_num) + ' and tag == "Noise_rate"')['value'].tolist())>0:
            noise_val = data.query('run == ' + str(run_num) + ' and tag == "Noise_rate"')['value'].tolist()[0]
            if noise_val < comparison_val:
                true_index.append(run_num)
            run_num+=1

        for x in range(1,run_num):
            if x in true_index:
                true_data = pd.concat([true_data, data.query('run == ' + str(x))], ignore_index=True)
                true_error_data.append(data.query('run == ' + str(x) + ' and tag == "Error_rate"')['value'].tolist()[0])
            else:
                false_data = pd.concat([false_data, data.query('run == ' + str(x))], ignore_index=True)
                false_error_data.append(data.query('run == ' + str(x) + ' and tag == "Error_rate"')['value'].tolist()[0])

        print(len(true_error_data[0:min(len(true_error_data), len(false_error_data))]), len(false_error_data[0:min(len(true_error_data), len(false_error_data))]))

        print(spa(true_data, NoiseErrorProperty(), prob_threshold=0.5, confidence=0.9).confidence_interval)
        print(spa(false_data, NoiseErrorProperty(), prob_threshold=0.5, confidence=0.9).confidence_interval)

        stat = alg.alg1(0.85, 0.5)
        print(stat.stat_test_complete(true_error_data, false_error_data, 0.1))
        print()




# test_basic_threshold()
# test_basic_ratio()
# test_insufficient_samples()

test_noise_error_prop()