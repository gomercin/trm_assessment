from assessment_data_provider import AssessmentDataProvider
from models.black_and_scholes_model import BlackScholesModel
from models.dto.option_information import OptionInformation
from models.var_calculation import PortfolioVarModel


data_provider = AssessmentDataProvider("/Users/karaduman/Projects/ING/TRM/assessment/TRM Engineering_Interview_Option_VaR_.xlsx")

bm = BlackScholesModel(data_provider.get_option_information())

cp = bm.calculate_call_option_price()
print(cp)

pp = bm.calculate_put_option_price()
print(pp)


portfolio_manager = PortfolioVarModel()
for asset in data_provider.get_assets():
    portfolio_manager.add_asset(asset)

total_var = portfolio_manager.calculate_var()
print(total_var)