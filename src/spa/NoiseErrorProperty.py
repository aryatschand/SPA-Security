import numpy as np
from typing import Any, List, Tuple, Union
import pandas as pd
from spa.properties import GenericProperty, GenericThreshold, OutOfDataException

_T_NUMBER = Union[int, float]

class NoiseErrorProperty(GenericThreshold, GenericProperty):

    @staticmethod
    def start_point_estimate(data: pd.DataFrame, proportion: float) -> float:

        data = data.query("System == 1 and tag == 'Error_rate'")["value"].tolist()
        return np.quantile(data, 1 - proportion)

    def extract_value(self, data: pd.DataFrame) -> Tuple[_T_NUMBER, List[_T_NUMBER]]:
        """Extract the value from the input data. Meant to be used in conjunction with :function check_sample_satisfy:
        For this property, return only first value of both systems from the dataframe. Returns the value and the remaining data.
        :param data: The data to extract from.
        :return: The extracted value(s).
        """

        while True:
            if len(data) < 3:
                raise OutOfDataException

            # Get the data from only the top run
            run_number = int(data.iloc[0]['run'])
            run_data = data.query('run == ' + str(run_number))
            if not len(run_data) > 0:
                raise OutOfDataException

            # Get and return the latency for request 1 and request 2
            noise_val = data.query('run == ' + str(run_number) + ' and tag == "Noise_rate"')['value'].tolist()[0]
            error_val = data.query('run == ' + str(run_number) + ' and tag == "Error_rate"')['value'].tolist()[0]
            time_val = data.query('run == ' + str(run_number) + ' and tag == "Time"')['value'].tolist()[0]

            data = data.iloc[3: , :]
            
            # if noise_val < 5 and time_val < 2:
                
            #     return error_val,data
            return error_val,data

        return OutOfDataException

    def check_sample_satisfy(self, value: _T_NUMBER) -> bool:
        """Check if the property is satisfied or not satisfied by the given value. Meant to be used with the
        :function extract_value: method.
        In this case, the property is satisfied if the value comparison against the threshold is True.
        :param value: The value(s) to check.
        :return: True if the property is satisfied, False otherwise.
        """

        # First ensure that the property is set
        if not (isinstance(self.threshold, int) or isinstance(self.threshold, float)):
            raise TypeError('Threshold must be an integer or float')
        # Use the comparison operator defined in the constructor to check the value against the threshold
        return self._comparison(value, self.threshold)