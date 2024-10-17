import math
from scipy.stats import norm


class BlackScholesModel:
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

    def calculate_d1(self):
        """
        (ln(S/K) + T*(r + (v * v / 2))) / (v * sqrt(t))
        """

        ln = math.log(self.S_current_price / self.K_strike_price)

        upper_right = self.T_time_to_maturity * (self.r_risk_free_interest_rate + (self.v_volatility * self.v_volatility / 2.0))

        upper = ln + upper_right
        lower = self.v_volatility * math.sqrt(self.T_time_to_maturity)
        
        return upper / lower
    
    def calculate_d2(self):
        """
        d1 - (v * sqrt(t))
        """
        d1 = self.calculate_d1()
        return d1 - (self.v_volatility * math.sqrt(self.T_time_to_maturity))


    def calculate_normal_distribution(self, d):
        return norm.cdf(d)
    

    def calculate_call_option_price(self):
        """
        N(d1)St - N(d2)Keˆ(-rt)
        """
        d1 = self.calculate_d1()
        d2 = self.calculate_d2()

        norm_d1 = self.calculate_normal_distribution(d1)
        norm_d2 = self.calculate_normal_distribution(d2)

        call_option_price = norm_d1 * self.S_current_price - norm_d2 * self.K_strike_price * math.exp(-1 * self.r_risk_free_interest_rate * self.T_time_to_maturity)

        return call_option_price
    

    def calculate_put_option_price(self):
        """
        K*e^(-rt)*N(-d2) - S0*N(-d1)
        """

        d1 = self.calculate_d1()
        d2 = self.calculate_d2()
        norm_d1 = self.calculate_normal_distribution(-d1)
        norm_d2 = self.calculate_normal_distribution(-d2)

        put_option_price = self.K_strike_price * math.exp(-self.r_risk_free_interest_rate * self.T_time_to_maturity) * norm_d2 - self.S_current_price*norm_d1

        return put_option_price
    
S = 19.0
K = 17.0
T = 0.460
r = 0.005
v = 0.3

bm = BlackScholesModel(S, K, T, r, v)

St = S * math.exp(r * T)
print(St)

d1 = bm.calculate_d1()
print(d1)
cp = bm.calculate_call_option_price()
print(cp)

pp = bm.calculate_put_option_price()
print(pp)


def spot_call(S_current_price,
              K_strike_price,
              T_time_to_expiry,
              r_risk_free_interest_rate,
              v_volatility):
    pass