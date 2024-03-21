"""
The following algorithms are Algorithm 1 and Algorithm 2, based on the paper
https://arxiv.org/abs/2008.01135
"""
import numpy as np
from statsmodels.distributions.empirical_distribution import ECDF

class alg1:

    def __init__(self,alpha_d, c, k1=1, k2=1):
        '''
        Algorithm 1 answers Equation (11) seen in the above paper.

        Parameters
        ----------
        alpha_d : float
            Desired confidence level. The higher the confidence level, the
            closer you are to the true underlying probability. This value is
            within (0,1], not including zero.

        c : float
            Approximate equality. This is a measure of how close you want two
            underlying distributions to be to each other. The lower the value,
            the closer the two distributions are to each other. This value must
            be greater than zero.

        k1 : integer
            This is the number of samples to draw from underlying distribution
            #1. Default is 1, which means the algorithm will draw one sample
            from the distribution each loop.

        k2 : integer
            This is the number of samples to draw from underlying distribution
            #1. Default is 1, which means the algorithm will draw one sample
            from the distribution each loop.
        '''
        self.alpha_d = alpha_d
        self.c = c
        self.k1 = k1
        self.k2 = k2

        # Initialize empty 1D numpy float arrays to hold data. This will be
        # used later.
        self.Xdata = np.array([])
        self.Ydata = np.array([])


    # def ECDF(self, samples, x):
    #     '''
    #     This function is based on Equation (9) and it calculates the fraction
    #     of sample data that is less than a threshold 'x'. As the threshold
    #     increases, the fraction increases until it reaches one. This is the
    #     empirical cumulative distribution function.

    #     According to the equation in the above paper,
    #     'n' is the total number of samples taken from the system 'M'.
    #     'X^(i)' is the value of the sample data 'i'.
    #     'x' is a threshold that will vary from smallest to largest data value.
    #     More details about 'x' will be seen in the deltaXY function below.
    #     'I' is an indicator function (outputs true/false).

    #     Parameters
    #     ----------
    #     samples : 1D numpy float array
    #         These are the samples taken from system 'M'. Arrange in a 1D
    #         numpy array.

    #     x : float
    #         A threshold value to compare with the sample data.

    #     Returns
    #     -------
    #     F_X : float
    #         This is the fraction of sample data that is less than the
    #         threshold x.

    #     '''
    #     # Check which elements are less than the threshold.
    #     less_than = samples < x

    #     # Calculate the fraction.
    #     F_X = np.sum(less_than) / len(less_than)

    #     return F_X

    def deltaXY(self, sampleX, sampleY, ecdf_intervals=1000):
        '''
        This function is based on Equation (10) in the above paper and it
        calculates the largest difference between two empirical cumulative
        distribution functions (ECDF).

        Parameters
        ----------
        sampleX : 1D numpy float array
            Sample data taken from model 1.

        sampleY : 1D numpy float array
            Sample data taken from model 2.

        ecdf_intervals : Integer
            When calculating the difference between two ECDF, we need to
            calculate in equal intervals between the smallest and the largest
            value. Default value is 1000 intervals.

        Returns
        -------
        difference : float
            The largest difference between the two ECDF.

        '''
        # Initialize the empirical cumulative distribution functions (ECDF) for
        # both sample data.
        Xecdf = ECDF(sampleX)
        Yecdf = ECDF(sampleY)

        # Assuming that the two samples are from similar underlying
        # distributions, then we can take the smallest and largest values
        # seen in sampleX or sampleY.
        minData = np.min([np.min(sampleX), np.min(sampleY)])
        maxData = np.max([np.max(sampleX), np.max(sampleY)])

        # Calculate the ECDF for both sample data at equal intervals.
        points = np.linspace(minData, maxData, ecdf_intervals)

        Xecdf_val = Xecdf(points)
        Yecdf_val = Yecdf(points)

        # Calculate the largest difference between the two distributions. It
        # is also called an l-infinity norm.
        difference = np.linalg.norm(Xecdf_val - Yecdf_val, ord=np.inf)
        return difference

    def confidence_level(self, m, n, lamb):
        '''
        This function calcualtes the confidence level alpha, as seen in
        Equation (19) in the above paper.

        Parameters
        ----------
        m : integer
            The number of samples in model 1.

        n : integer
            The number of samples in model 2.

        lamb : float
            Some value different from c? We need to figure out what is lambda.

        Returns
        -------
        alpha : float
            The confidence level

        '''
        # Calculate the value inside the parenthesis in Equation (19).
        val = abs(lamb - self.c) * np.sqrt(m*n / (m+n))

        # Use Equation (14) to calculate the confidence level.
        alpha = 1 - 2*np.exp(-2*val**2)

        return alpha

    def stat_test(self, new_Xdata, new_Ydata, lamb):
        '''
        This function will only handle lines 4-6 of Algorithm 1
        because the drawn data sample comes from outside the Algorithm.

        Parameters
        ----------
        new_Xdata : 1D numpy float array
            An array of data taken from model 1.

        new_Ydata : 1D numpy float array
            An array of data taken from model 2.

        lamb : float
            Some value different from c? We need to figure out what is lambda.

        Returns
        -------
        n : integer
            number of data taken from model 1.

        m : integer
            number of data taken from model 2.

        difference : float
            the difference between the two models' ECDF.

        alpha : float
            confidence level.

        '''
        # If this function will be incorporated into a while loop outside of
        # this class, then we will need to concatenate data into Xdata and
        # Ydata, which were initialized in the __init__ section.
        self.Xdata = np.concatenate((self.Xdata, new_Xdata))
        self.Ydata = np.concatenate((self.Ydata, new_Ydata))

        # Calculate the number of data points for each array.
        n = len(self.Xdata)
        m = len(self.Ydata)

        # Calculate the difference in the two models' ECDF.
        difference = self.deltaXY(self.Xdata, self.Ydata)

        # Calculate the confidence level.
        alpha = self.confidence_level(m, n, lamb)

        return n, m, difference, alpha

    def stat_test_complete(self, full_Xdata, full_Ydata, lamb):
        '''
        This function will handle the whole Algorithm 1, including the
        while loop. Note that this function assumes you have collected so much
        data that the number exceeds what you need for the desired confidence
        level. I highly doubt you will be able to do that because we do not
        know beforehand how many samples we need to achieve the desired
        confidence level. But here is the whole algorithm if you think you do.


        Parameters
        ----------
        full_Xdata : 1D numpy float array
            An array of data taken from model 1. Must be the full data set.

        full_Ydata : 1D numpy float array
            An array of data taken from model 1. Must be the full data set.

        lamb : float
            Some value different from c? We need to figure out what is lambda.

        Returns
        -------
        n : integer
            number of data taken from model 1.

        m : integer
            number of data taken from model 2.

        difference : float
            the difference between the two models' ECDF.

        alpha : float
            confidence level.

        assertion : boolean
            The equation for the assertion can be seen in Equation (11).
            The output is 0 if the difference is less than c.
            The output is 1 if the difference is greater than or equal to c.

        '''
        # Initialize values to enter the while loop.
        n = 0
        m = 0
        alpha = 0

        while alpha < self.alpha_d:
            # Extract the nth through (n+k1)th data from X data set.
            # Extract the mth through (m+k2)th data from Y data set.
            extractX = full_Xdata[n : (n + self.k1)]
            extractY = full_Ydata[m : (m + self.k2)]

            # Feed the extracted data into the (incomplete) stat_test function.
            n, m, difference, alpha = self.stat_test(extractX, extractY, lamb)

        # Calculate the assertion.
        if difference < self.c:
            assertion = 0
        else:
            assertion = 1

        return n, m, difference, alpha, assertion