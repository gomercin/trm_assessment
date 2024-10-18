import math
from scipy.stats import norm

from models.dto.option_information import OptionInformation


class BlackScholesModel:
    """
    Manages asset information to calculate Call/Put options for an asset.
    """
    def __init__(self, option_info:OptionInformation):
        self.S_current_price = option_info.S_current_price
        self.K_strike_price = option_info.K_strike_price
        self.T_time_to_maturity = option_info.T_time_to_maturity
        self.r_risk_free_interest_rate = option_info.r_risk_free_interest_rate
        self.v_volatility = option_info.v_volatility

    def calculate_d1(self) -> float:
        """
        Calculates the d1 value using the following formula
        (ln(S/K) + T*(r + (v * v / 2))) / (v * sqrt(t))

        Returns:
            d1 value for the current asset information
        """

        # This method calls multiple times with same parameters in our current flow.
        # Ideally, we can ensure that the parameters do not change between the calls
        # and reuse the calculated d1 value.
        # It doesn't make much of a difference in the assessment context

        assert self.v_volatility, "Volatility is not provided or zero"
        assert self.T_time_to_maturity, "Time to maturity is not provided or zero"

        ln = math.log(self.S_current_price / self.K_strike_price)

        upper_right = self.T_time_to_maturity * (self.r_risk_free_interest_rate + (self.v_volatility * self.v_volatility / 2.0))

        upper = ln + upper_right
        lower = self.v_volatility * math.sqrt(self.T_time_to_maturity)
        
        return upper / lower


    def calculate_d2(self) -> float:
        """
        Calculates d2 value using the following formula
        d1 - (v * sqrt(t))

        Returns:
            d2 value for the current asset information
        """
        d1 = self.calculate_d1()
        return d1 - (self.v_volatility * math.sqrt(self.T_time_to_maturity))


    def calculate_normal_distribution(self, d) -> float:
        """
        Calculates normal distribution for the provided value
        """
        return norm.cdf(d)
    

    def calculate_call_option_price(self) -> float:
        """
        Calculates the call option price using the following formula:
        N(d1)St - N(d2)Keˆ(-rt)

        Returns:
            Call option price for the asset
        """
        d1 = self.calculate_d1()
        d2 = self.calculate_d2()

        norm_d1 = self.calculate_normal_distribution(d1)
        norm_d2 = self.calculate_normal_distribution(d2)

        call_option_price = norm_d1 * self.S_current_price - norm_d2 * self.K_strike_price * math.exp(-1 * self.r_risk_free_interest_rate * self.T_time_to_maturity)

        return call_option_price
    

    def calculate_put_option_price(self) -> float:
        """
        Calculates the put option price using the following formula:
        K*e^(-rt)*N(-d2) - S0*N(-d1)

        Returns:
            Put option price for the asset
        """

        d1 = self.calculate_d1()
        d2 = self.calculate_d2()
        norm_d1 = self.calculate_normal_distribution(-d1)
        norm_d2 = self.calculate_normal_distribution(-d2)

        put_option_price = self.K_strike_price * math.exp(-self.r_risk_free_interest_rate * self.T_time_to_maturity) * norm_d2 - self.S_current_price*norm_d1

        return put_option_price
    
