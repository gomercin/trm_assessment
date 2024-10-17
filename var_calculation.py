import math
import typing
import pandas as pd

class HistoricalVarCalculationModel:
    def __init__(self, spot_value, market_rates, asset_name = None):
        self.spot_value = spot_value
        self.market_rates = market_rates
        self.asset_name = asset_name


    def __calculate_1day_shift(self, day_index):
        assert day_index < len(self.market_rates) # TODO: raise appropriate error

        return math.exp(math.log(self.market_rates[day_index] / self.market_rates[day_index + 1])) - 1


    def calculate_pnl_vector(self):
        daily_shift_vector = [self.__calculate_1day_shift(day_index) for day_index in range(len(self.market_rates) - 1)]

        return [self.spot_value * daily_shift for daily_shift in daily_shift_vector]


class AssetInformation:
    def __init__(self, asset_name, spot_value, historical_data):
        self.asset_name = asset_name
        self.spot_value = spot_value
        self.historical_data = historical_data


class PortfolioVarModel:
    def __init__(self):
        self.assets : typing.List[AssetInformation] = []
        self.var_models = []

    def add_asset(self, asset_info: AssetInformation):
        self.assets.append(asset_info)

    def get_total_pnl(self):
        pnls = []
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


    def calculate_var(self):
        total_pnls = self.get_total_pnl()
        sorted_pnls = sorted(total_pnls)

        return 0.4 * sorted_pnls[1] + 0.6 * sorted_pnls[2]
        

# ccy1_model = HistoricalVarCalculationModel(ccy1_spot_value, ccy1_historical_data, "ccy1")
# ccy2_model = HistoricalVarCalculationModel(ccy2_spot_value, ccy2_historical_data, "ccy2")

# ccy1_pnl = ccy1_model.calculate_pnl_vector()
# ccy2_pnl = ccy2_model.calculate_pnl_vector()

# print(ccy1_pnl)
# print(ccy2_pnl)




#DataProvider

historical_data_df = pd.read_excel("/Users/karaduman/Projects/ING/TRM/assessment/TRM Engineering_Interview_Option_VaR_.xlsx", header=5, sheet_name="VaR Calculation")
spot_data_df = pd.read_excel("/Users/karaduman/Projects/ING/TRM/assessment/TRM Engineering_Interview_Option_VaR_.xlsx", header=1, sheet_name="VaR Calculation")

print(historical_data_df)
print(spot_data_df)

ccy1_spot_value = spot_data_df["SPOT Portfolio value"].iloc[0]
ccy2_spot_value = spot_data_df["SPOT Portfolio value"].iloc[1]

ccy1_historical_data = historical_data_df['market rate'].tolist()
ccy2_historical_data = historical_data_df['market rate.1'].tolist()

print(ccy1_spot_value)
print(ccy2_spot_value)

print(ccy1_historical_data)
print(ccy2_historical_data)

ccy1_asset_info = AssetInformation("ccy1", ccy1_spot_value, ccy1_historical_data)
ccy2_asset_info = AssetInformation("ccy2", ccy2_spot_value, ccy2_historical_data)

portfolio_manager = PortfolioVarModel()
portfolio_manager.add_asset(ccy1_asset_info)
portfolio_manager.add_asset(ccy2_asset_info)

total_var = portfolio_manager.calculate_var()
print(total_var)