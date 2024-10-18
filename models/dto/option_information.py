class OptionInformation:
    """
    DTO to store option related information
    """
    def __init__(self, S_current_price,
                        K_strike_price,
                        T_time_to_maturity,
                        r_risk_free_interest_rate,
                        v_volatility):
        self.S_current_price = S_current_price
        self.K_strike_price = K_strike_price
        self.T_time_to_maturity = T_time_to_maturity
        self.r_risk_free_interest_rate = r_risk_free_interest_rate
        self.v_volatility = v_volatility
