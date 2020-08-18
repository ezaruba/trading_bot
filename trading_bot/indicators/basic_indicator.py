"""All basic indicators classes.

This file allows developer to use any basic financial indicator contains in this file.

All basic indicator classes must inherit from the `BasicIndicator` class to standardize all used basic indicators.

This script requires that `pandas` and `numpy` be installed within the Python 
environment you are running this script in.

This file can also be imported as a module and contains of the following 
classes and functions:

    * HighestHigh - class used to reprensent "Highest High" indicator
    * LowestLow - class used to reprensent "Lowest Low" indicator
    * MedianPrice - class used to reprensent "Median price" indicator
    * TypicalPrice - class used to reprensent "Typical price" indicator
    * AverageTrueRange - class used to reprensent "Average True Range" or "ATR" indicator
"""

import abc
import numpy as np
import pandas as pd

from trading_bot.indicators.base_indicator import Indicator
from trading_bot.indicators.utils import wwma


class BasicIndicator(Indicator, metaclass=abc.ABCMeta):
    """
    An abstract class used to reprensent the base of each basic indicator that we will use.

    Attributes
    ----------
    period : int
        number of ticks that indicator is based to calculate

    Methods
    -------
    get_column_name()
        Return the column name associated at this indicator.

    calculate(df)
        Calculate the indicator for the given data.

    calculate_in_place(df)
        Calculate the indicator for the given data and put this directly in 
        the dataframe.
    """

    def __init__(self, column_name: str, period: int) -> None:
        """
        Initializer and constructor of the class.

        Parameters
        ----------
        column_name : str
            indicator name to put in the pandas dataframe
        period : int
            number of ticks that indicator is based to calculate
        """
        Indicator.__init__(self, column_name, period)


class HighestHigh(BasicIndicator):
    """
    A class used to reprensent "Highest High" indicator.
    This statistical indicator makes a line with the highest "High" n-period ticks indicator.

    Attributes
    ----------
    period : int
        number of ticks that indicator is based to calculate

    Methods
    -------
    get_column_name()
        Return the column name associated at this indicator.

    calculate(df)
        Calculate the indicator for the given data.

    calculate_in_place(df)
        Calculate the indicator for the given data and put this directly in 
        the dataframe.
    """

    def __init__(self, period: int = 14) -> None:
        """
        Initializer and constructor of the class.

        Parameters
        ----------
        period : int, optional
            number of ticks that indicator is based to calculate (default = 14)
        """
        BasicIndicator.__init__(self, "Highest High", period)

    def calculate(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate the indicator for the given data.

        Parameters
        ----------
        df : pd.DataFrame
            data used to calculate the indicator

        Returns
        -------
        pd.DataFrame
            the DataFrame containing the calculated data

        Raises
        ------
        KeyError
            If the dataframe is not sdandardize yet
        """
        highest_high = df['High'].copy()
        if self.period <= len(highest_high):
            for i in range(0, len(highest_high)):
                subframe = df['High'][i-self.period+1:i+1]
                highest_high[i] = subframe.max(skipna=True)
        return highest_high


class LowestLow(BasicIndicator):
    """
    A class used to reprensent "Lowest Low" indicator.
    This statistical indicator makes a line with the Lowest "Low" n-period ticks indicator.

    Attributes
    ----------
    period : int
        number of ticks that indicator is based to calculate

    Methods
    -------
    get_column_name()
        Return the column name associated at this indicator.

    calculate(df)
        Calculate the indicator for the given data.

    calculate_in_place(df)
        Calculate the indicator for the given data and put this directly in 
        the dataframe.
    """

    def __init__(self, period: int = 14) -> None:
        """
        Initializer and constructor of the class.

        Parameters
        ----------
        period : int, optional
            number of ticks that indicator is based to calculate (default = 14)
        """
        BasicIndicator.__init__(self, "Lowest Low", period)

    def calculate(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate the indicator for the given data.

        Parameters
        ----------
        df : pd.DataFrame
            data used to calculate the indicator

        Returns
        -------
        pd.DataFrame
            the DataFrame containing the calculated data

        Raises
        ------
        KeyError
            If the dataframe is not sdandardize yet
        """
        lowest_low = df['Low'].copy()
        if self.period <= len(lowest_low):
            for i in range(0, len(lowest_low)):
                subframe = df['Low'][i-self.period+1:i+1]
                lowest_low[i] = subframe.min(skipna=True)
        return lowest_low


class MedianPrice(BasicIndicator):
    """
    A class used to reprensent "Median price" indicator.
    This statistical indicator makes a line with the average of the "High" and "Low" prices.

    Attributes
    ----------
    period : int
        number of ticks that indicator is based to calculate

    Methods
    -------
    get_column_name()
        Return the column name associated at this indicator.

    calculate(df)
        Calculate the indicator for the given data.

    calculate_in_place(df)
        Calculate the indicator for the given data and put this directly in 
        the dataframe.
    """

    def __init__(self) -> None:
        """
        Initializer and constructor of the class.
        """
        BasicIndicator.__init__(self, "Median Price", 0)

    def calculate(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate the indicator for the given data.

        Parameters
        ----------
        df : pd.DataFrame
            data used to calculate the indicator

        Returns
        -------
        pd.DataFrame
            the DataFrame containing the calculated data

        Raises
        ------
        KeyError
            If the dataframe is not sdandardize yet
        """
        return np.mean(np.stack((df['High'], df['Low'])), axis=0)


class TypicalPrice(BasicIndicator):
    """
    A class used to reprensent "Typical price" indicator.
    This statistical indicator makes a line with the average of the "High", "Low" and "Close" prices.

    Attributes
    ----------
    period : int
        number of ticks that indicator is based to calculate

    Methods
    -------
    get_column_name()
        Return the column name associated at this indicator.

    calculate(df)
        Calculate the indicator for the given data.

    calculate_in_place(df)
        Calculate the indicator for the given data and put this directly in 
        the dataframe.
    """

    def __init__(self) -> None:
        """
        Initializer and constructor of the class.
        """
        BasicIndicator.__init__(self, "Typical Price", None)

    def calculate(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate the indicator for the given data.

        Parameters
        ----------
        df : pd.DataFrame
            data used to calculate the indicator

        Returns
        -------
        pd.DataFrame
            the DataFrame containing the calculated data

        Raises
        ------
        KeyError
            If the dataframe is not sdandardize yet
        """
        return np.mean(np.stack((df['High'], df['Low'], df['Close'])), axis=0)


class AverageTrueRange(BasicIndicator):
    """
    A class used to reprensent "Average True Range" or "ATR" indicator.
    This volatility indicator makes a line with the average of the "High", "Low" and "Close" prices.

    Attributes
    ----------
    period : int
        number of ticks that indicator is based to calculate

    Methods
    -------
    get_column_name()
        Return the column name associated at this indicator.

    calculate(df)
        Calculate the indicator for the given data.

    calculate_in_place(df)
        Calculate the indicator for the given data and put this directly in 
        the dataframe.
    """

    def __init__(self, period: int = 14) -> None:
        """
        Initializer and constructor of the class.

        Parameters
        ----------
        period : int, optional
            number of ticks that indicator is based to calculate (default = 14)
        """
        super().__init__("Average True Range", period)

    def calculate(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate the indicator for the given data.

        Parameters
        ----------
        df : pd.DataFrame
            data used to calculate the indicator

        Returns
        -------
        pd.DataFrame
            the DataFrame containing the calculated data

        Raises
        ------
        KeyError
            If the dataframe is not sdandardize yet
        """
        tr0 = abs(df['High'] - df['Low'])
        tr1 = abs(df['High'] - df['Close'].shift(1))
        tr2 = abs(df['Low'] - df['Close'].shift(1))
        tr = np.stack((tr0, tr1, tr2)).max(axis=1)
        atr = wwma(tr, self.period)
        return atr
