import os
import sys
from assessment_data_provider import AssessmentDataProvider
from models.black_and_scholes_model import BlackScholesModel
from models.var_calculation import PortfolioVarModel


if __name__ == "__main__":
    # It is usually a better option to use argparse, but would be an overkill for this purpose

    if len(sys.argv) != 2:
        print("Usage: python main.py <path to input excel file>")
        exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"Provided parameter is not a valid file: {input_file}")
        exit(1)

    data_provider = AssessmentDataProvider(input_file)

    bm = BlackScholesModel(data_provider.get_option_information())

    call_price = bm.calculate_call_option_price()
    print("Call option price with Spot price calculation: " + str(call_price))

    put_price = bm.calculate_put_option_price()
    print("Put option price with Spot price calculation: " + str(put_price.real))


    portfolio_manager = PortfolioVarModel()
    for asset in data_provider.get_assets():
        portfolio_manager.add_asset(asset)

    total_var = portfolio_manager.calculate_var()
    print("VaR 1D 0.99 calculation result: " + str(total_var.real))