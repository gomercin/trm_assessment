from abc import ABC, abstractmethod
import typing

from models.dto.asset_information import AssetInformation
from models.dto.option_information import OptionInformation


class BaseDataProvider(ABC):
    """
    Created to abstract data and business logic.
    Creates a list of AssetInformation from the provided source to be used in the portfolio.
    This simplifies testing as we can ignore the excel files for unit tests and use a simpler
    way of providing data instead of creating mock objects in between.
    """

    def __init__(self, data_source):
        """
        Parameters:
            data_source: a reference to the data source to be used
        """
        self.data_source = data_source

    @abstractmethod
    def get_assets(self) -> typing.List[AssetInformation]:
        """
        Parse the data source and return a list of AssetInformation

        Returns:
            a list of AssetInformation
        """

    @abstractmethod
    def get_option_information(self) -> OptionInformation:
        """
        Parse the data source and return the option related information

        Returns:
            Option information
        """
  