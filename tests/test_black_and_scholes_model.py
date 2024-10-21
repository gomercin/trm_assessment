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
        self.assertGreater(call_price, 0, "At-the-money call option should have a positive price.")


    def test_call_option_out_of_the_money(self):
        """
        Test case for out-of-the-money call option.
        Out-of-the-money occurs when current price < strike price.
        """
        option_info = copy.copy(self.test_option)
        option_info.S_current_price = option_info.K_strike_price - 10
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
        self.assertGreater(put_price, 0, "At-the-money put option should have a positive price.")


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


    def test_zero_time_to_maturity_call(self):
        """
        Test calculation when Time To Maturity is 0.
        For the current implementation, I took it as an invalid case, thus verifying if correct assertion is being thrown.
        In a real implementation, we might rather want to check the intrinsic value.
        """
        option_info = copy.copy(self.test_option)
        option_info.T_time_to_maturity = 0
        model = BlackScholesModel(option_info)
        self.assertRaises(AssertionError, model.calculate_call_option_price)


    def test_zero_volatility_call(self):
        """
        Test the behavior with 0 volatility.
        Similar to time to maturity, 0 volatility causes an exception in the current code.
        """
        option_info = copy.copy(self.test_option)
        option_info.v_volatility = 0
        
        intrinsic_val = 10
        option_info.S_current_price = option_info.K_strike_price + intrinsic_val
        
        model = BlackScholesModel(option_info)
        self.assertRaises(AssertionError, model.calculate_call_option_price)


    def test_high_volatility_call(self):
        """
        Test if call option is close to the current price when there is high volatility.
        """
        option_info = copy.copy(self.test_option)
        option_info.v_volatility = 1000
        model = BlackScholesModel(option_info)
        self.assertAlmostEqual(model.calculate_call_option_price(), option_info.S_current_price, delta=1)


    def test_high_volatility_put(self):
        """
        Test if put option is close to strike price (adjusted for duration and risk-free rate) when there is high volatility
        """
        option_info = copy.copy(self.test_option)
        option_info.v_volatility = 1000
        model = BlackScholesModel(option_info)
        self.assertAlmostEqual(model.calculate_put_option_price(), option_info.K_strike_price * math.exp(-0.05 * 1), delta=1)


    def test_zero_interest_rate_call(self):
        """
        Test the behavior with 0 interest rate.
        We are mainly checking if this is handled differently from volatility and time to maturity.
        i.e. no exceptions thrown, and a positive value is calculated
        """
        option_info = copy.copy(self.test_option)
        option_info.r_risk_free_interest_rate = 0
        model = BlackScholesModel(option_info)
        self.assertGreater(model.calculate_call_option_price(), 0)


    def test_zero_interest_rate_put(self):
        """
        Test the behavior with 0 interest rate.
        We are mainly checking if this is handled differently from volatility and time to maturity.
        i.e. no exceptions thrown, and a positive value is calculated
        """
        option_info = copy.copy(self.test_option)
        option_info.r_risk_free_interest_rate = 0
        model = BlackScholesModel(option_info)
        self.assertGreater(model.calculate_put_option_price(), 0)


    def test_negative_interest_rate_call(self):
        """
        Test if negative interest rate doesn't break anything in the model for call options.
        """
        option_info = copy.copy(self.test_option)
        option_info.r_risk_free_interest_rate = -0.01
        model = BlackScholesModel(option_info)
        self.assertGreater(model.calculate_call_option_price(), 0)


    def test_negative_interest_rate_put(self):
        """
        Test if negative interest rate doesn't break anything in the model for put options.
        """
        option_info = copy.copy(self.test_option)
        option_info.r_risk_free_interest_rate = -0.01
        model = BlackScholesModel(option_info)
        self.assertGreater(model.calculate_put_option_price(), 0)
