import os
import unittest
from assessment_data_provider import AssessmentDataProvider
from models.black_and_scholes_model import BlackScholesModel


class TestE2EBlackScholesModel(unittest.TestCase):

    def setUp(self):
        """
        Initialize the model with the external data source.
        """

        self.e2e_test_input_file = os.environ.get("TEST_INPUT_FILE", None)
        assert self.e2e_test_input_file, "For E2E tests TEST_INPUT_FILE environment variable must be set to point to the input file."
        self.e2e_data_provider = AssessmentDataProvider(self.e2e_test_input_file)
    
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
