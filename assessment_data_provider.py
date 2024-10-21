
import pandas as pd
from models.dto.base_data_provider import BaseDataProvider
from models.dto.option_information import OptionInformation
from models.var_calculation import AssetInformation


  
class AssessmentDataProvider(BaseDataProvider):
    """
    DataProvider specific to the excel file in the assessment
    """
    def get_assets(self):
        """
        Parse the provided excel file to fetch the required data.
        """

        # This reads the same excel file twice. Not computatinally efficient but good enough for the use case
        historical_data_df = pd.read_excel(self.data_source, header=5, sheet_name="VaR Calculation")
        spot_data_df = pd.read_excel(self.data_source, header=1, sheet_name="VaR Calculation")

        ccy1_spot_value = spot_data_df["SPOT Portfolio value"].iloc[0]
        ccy2_spot_value = spot_data_df["SPOT Portfolio value"].iloc[1]

        # For more complex data, using dataframes would probably be a wiser choice to simplify the operations.
        ccy1_historical_data = historical_data_df['market rate'].tolist()
        ccy2_historical_data = historical_data_df['market rate.1'].tolist()

        ccy1_asset_info = AssetInformation("ccy1", ccy1_spot_value, ccy1_historical_data)
        ccy2_asset_info = AssetInformation("ccy2", ccy2_spot_value, ccy2_historical_data)

        return [ccy1_asset_info, ccy2_asset_info]


    def get_option_information(self) -> OptionInformation:
        def get_value_for_parameter(df, param_name, index = 0):
            return float(df.loc[df['European Vanilla Call'] == param_name, 'base case'].values[index])
        
        option_df = pd.read_excel(self.data_source, header=2, sheet_name="Option")
        s0 = get_value_for_parameter(option_df, "S0")
        k = get_value_for_parameter(option_df, "K (strike)")
        t = get_value_for_parameter(option_df, "Time to Expiry")
        r = get_value_for_parameter(option_df, "r")
        v = get_value_for_parameter(option_df, "Vol")

        call_price = get_value_for_parameter(option_df, "Call", 1)  # Using the second result for Spot call price
        put_price = get_value_for_parameter(option_df, "Put", 0)  # Using the result for Put option with forward price
                                                       # as Spot/Put price was not provided.
                                                       # Checked manually to see if the values are close enough for our purpose.

        return OptionInformation(s0, k, t, r, v, call_price, put_price)