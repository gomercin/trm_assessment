class OptionInformation:
    """
    DTO to store option related information
    """
    def __init__(self, S_current_price,
                        K_strike_price,
                        T_time_to_maturity,
                        r_risk_free_interest_rate,
                        v_volatility,
                        expected_call_price = None,
                        expected_put_price = None):
        self.S_current_price = S_current_price
        self.K_strike_price = K_strike_price
        self.T_time_to_maturity = T_time_to_maturity
        self.r_risk_free_interest_rate = r_risk_free_interest_rate
        self.v_volatility = v_volatility

        # these values are retrieved for testing
        self.expected_call_price = expected_call_price
        self.expected_put_price = expected_put_price
