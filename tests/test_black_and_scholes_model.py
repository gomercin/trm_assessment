import os
import unittest
import math
import copy
from assessment_data_provider import AssessmentDataProvider
from models.dto.option_information import OptionInformation
from models.black_and_scholes_model import BlackScholesModel


class TestBlackScholesModel(unittest.TestCase):

    def setUp(self):
        """
        Initialize the model with an example set of option data.
        """

        # Base test data to be used. Its values need to be changed for different cases
        # so it is safer to create copies of the data object for such tests.
        # One other option could be keeping only the values here, and create the DTO
        # in the tests, but picked this approach as it is cleaner for now.
        self.test_option = OptionInformation(S_current_price=100,
                                             K_strike_price=95, 
                                             T_time_to_maturity=1,  # 1 year
                                             r_risk_free_interest_rate=0.05,  # 5% risk free rate
                                             v_volatility=0.2)  # 20% volatility
        

        self.e2e_test_input_file = os.environ.get("TEST_INPUT_FILE", None)
        if self.e2e_test_input_file:
            self.e2e_data_provider = AssessmentDataProvider(self.e2e_test_input_file)
        else:
            self.e2e_data_provider = None


    def test_calculate_d1(self):
        """
        Unit test for the calculate_d1 method.
        """
        model = BlackScholesModel(self.test_option)
        S = self.test_option.S_current_price
        K = self.test_option.K_strike_price
        T = self.test_option.T_time_to_maturity
        r = self.test_option.r_risk_free_interest_rate
        v = self.test_option.v_volatility
        expected_d1 = (math.log(S / K) + T * (r + (v * v / 2))) / (v * math.sqrt(T))
        calculated_d1 = model.calculate_d1()
        self.assertAlmostEqual(calculated_d1, expected_d1, places=6)

    def test_calculate_d2(self):
        """
        Unit test for the calculate_d2 method.
        """
        model = BlackScholesModel(self.test_option)
        T = self.test_option.T_time_to_maturity
        v = self.test_option.v_volatility

        d1 = model.calculate_d1()
        expected_d2 = d1 - (v * math.sqrt(T))
        calculated_d2 = model.calculate_d2()
        self.assertAlmostEqual(calculated_d2, expected_d2, places=6)

    def test_call_option_in_the_money(self):
        """
        Test case for in-the-money call option.
        In-the-money occurs when current price > strike price.
        """
        option_info = copy.copy(self.test_option)
        option_info.S_current_price = option_info.K_strike_price + 10
        model = BlackScholesModel(option_info)

        call_price = model.calculate_call_option_price()
        self.assertGreater(call_price, 0, "In-the-money call option should have a positive price.")

    def test_call_option_at_the_money(self):
        """
        Test case for at-the-money call option.
        At-the-money occurs when current price = strike price.
        """
        option_info = copy.copy(self.test_option)
        option_info.S_current_price = option_info.K_strike_price
        model = BlackScholesModel(option_info)

        call_price = model.calculate_call_option_price()
        self.assertGreater(call_price, 0, "At-the-money call option should have a positive price, though it may be small.")

    def test_call_option_out_of_the_money(self):
        """
        Test case for out-of-the-money call option.
        Out-of-the-money occurs when current price < strike price.
        """
        option_info = copy.copy(self.test_option)
        option_info.S_current_price = option_info.K_strike_price - 10
        model = BlackScholesModel(option_info)
        model = BlackScholesModel(option_info)

        call_price = model.calculate_call_option_price()
        self.assertGreater(call_price, 0, "Out-of-the-money call option should have a small positive price.")

    def test_put_option_in_the_money(self):
        """
        Test case for in-the-money put option.
        In-the-money occurs when current price < strike price.
        """
        option_info = copy.copy(self.test_option)
        option_info.S_current_price = option_info.K_strike_price - 10
        model = BlackScholesModel(option_info)

        put_price = model.calculate_put_option_price()
        self.assertGreater(put_price, 0, "In-the-money put option should have a positive price.")

    def test_put_option_at_the_money(self):
        """
        Test case for at-the-money put option.
        At-the-money occurs when current price = strike price.
        """
        option_info = copy.copy(self.test_option)
        option_info.S_current_price = option_info.K_strike_price
        model = BlackScholesModel(option_info)

        put_price = model.calculate_put_option_price()
        self.assertGreater(put_price, 0, "At-the-money put option should have a positive price, though it may be small.")

    def test_put_option_out_of_the_money(self):
        """
        Test case for out-of-the-money put option.
        Out-of-the-money occurs when current price > strike price.
        """
        option_info = copy.copy(self.test_option)
        option_info.S_current_price = option_info.K_strike_price + 10
        model = BlackScholesModel(option_info)

        put_price = model.calculate_put_option_price()
        self.assertGreater(put_price, 0, "Out-of-the-money put option should have a small positive price.")
    
    def test_end_to_end_call_option(self):
        """
        End-to-end test for calculating the call option price.
        Verifies all underlying calculations for call options.
        """
        assert self.e2e_data_provider, "E2E test data provider is not set. Ensure that TEST_INPUT_FILE environment variable is set to the input file."
        option_info = self.e2e_data_provider.get_option_information()
        model = BlackScholesModel(option_info)

        call_price = model.calculate_call_option_price()
        self.assertAlmostEqual(call_price, option_info.expected_call_price, places=3, msg=f"Value mismatch in E2E call option test. Expected {option_info.expected_call_price}, received {call_price}")

    def test_end_to_end_put_option(self):
        """
        End-to-end test for calculating the put option price.
        Verifies all underlying calculations for put options.
        """
        assert self.e2e_data_provider, "E2E test data provider is not set. Ensure that TEST_INPUT_FILE environment variable is set to the input file."
        option_info = self.e2e_data_provider.get_option_information()
        model = BlackScholesModel(option_info)

        put_price = model.calculate_put_option_price()
        self.assertAlmostEqual(put_price, option_info.expected_put_price, places=3, msg=f"Value mismatch in E2E put option test. Expected {option_info.expected_put_price}, received {put_price}")
