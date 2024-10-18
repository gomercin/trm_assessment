import math
import typing

from models.dto.asset_information import AssetInformation

class HistoricalVarCalculationModel:
    """
    Calculates the PnL for the provided asset using the historical data method.
    """
    def __init__(self, spot_value, market_rates, asset_name = None):
        """
        Create the model for an asset to calculate historical VaR.
        """
        self.spot_value = spot_value
        self.market_rates = market_rates
        self.asset_name = asset_name


    def __calculate_1day_shift(self, day_index) -> float:
        """
        Calculate 1 day shift for the provided asset.
        It assumes that the data is sorted from recent to old. 
        Returns:
            1 day shift value for the given day.
        """
        assert day_index < len(self.market_rates), f"Provided day index ({day_index}) is out of bounds."

        return math.exp(math.log(self.market_rates[day_index] / self.market_rates[day_index + 1])) - 1


    def calculate_pnl_vector(self) -> typing.List[float]:
        """
        Calculate the PnL vector for the asset using the spot value and the historical rates.
        """
        daily_shift_vector = [self.__calculate_1day_shift(day_index) for day_index in range(len(self.market_rates) - 1)]

        return [self.spot_value * daily_shift for daily_shift in daily_shift_vector]
    

    def calculate_asset_var(self, confidence_level=0.99) -> float:
        """
        Calculates the VaR for the current asset
        Parameters:
            confidence_level (float): desired confidence level
        Returns:
            VaR for the current asset
        """
        return HistoricalVarCalculationModel.calculate_asset_var(self.calculate_pnl_vector(), confidence_level)


    @staticmethod
    def calculate_external_var(pnl_values: typing.List[float], confidence_level=0.99) -> float:
        """
        Calculates the VaR for the provided pnl values.
        Parameters:
            confidence_level (float): desired confidence level. Note that it is ignored and hardcoded values are used in the assignment
        Returns:
            VaR for the provided PnL values (and confidence level).
        """
        sorted_pnls = sorted(pnl_values)

        return 0.4 * sorted_pnls[1] + 0.6 * sorted_pnls[2]


class PortfolioVarModel:
    """
    Basic porfolio model to store different assets and manage aggregated calculations.
    """
    def __init__(self):
        self.assets : typing.List[AssetInformation] = []
        self.var_models = []


    def add_asset(self, asset_info: AssetInformation):
        """
        Adds the provided asset to the portfolio
        """
        self.assets.append(asset_info)

    def get_aggregated_pnl(self):
        """
        Creates an aggregated PnL vector for the current porfolio.
        Ideally, we can have a smarter porfolio manager where the correlation between the assets, or
        the differences in the historical data is handled properly.
        For the sake of the assessment, the problem is in a narrow scope, so current implementation
        should be good enough.

        Note that we are assuming all assets have the same amount of historical data. Otherwise, we
        would need a better way to align the data for missing values.

        Returns:
            Aggregated PnL vector for the entire portfolio
        """
        pnls = []

        # we can separately calculate the PnL for each asset as they are not dependent.
        for asset in self.assets:
            asset_model = HistoricalVarCalculationModel(asset.spot_value, asset.historical_data, asset.asset_name)
            pnls.append(asset_model.calculate_pnl_vector())

        total_pnls = []
        for i in range(len(pnls[0])):
            total_pnl = 0
            for pnl in pnls:
                total_pnl += pnl[i]

            total_pnls.append(total_pnl)

        return total_pnls


    def calculate_var(self, confidence_level=0.99) -> float:
        """
        Calculate the combined VaR using HistoricalVarCalculationModel and the aggregated PnL vector

        Returns:
            the aggregated VaR for the portfolio
        """
        return HistoricalVarCalculationModel.calculate_external_var(self.get_aggregated_pnl(), confidence_level)
        
