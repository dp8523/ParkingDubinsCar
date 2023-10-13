import constants


class Control:
    """
    stores Gray code representations of the control variables
    """

    def __init__(self, gamma, beta):
        self.gamma = gamma
        self.beta = beta

    @staticmethod
    def get_gray(n):
        """
        adapted from https://www.geeksforgeeks.org/generate-n-bit-gray-codes/
        """
        val = (n ^ (n >> 1))
        s = bin(val)[2::]
        return s.zfill(constants.chromosome_length)

    @staticmethod
    def get_decimal(n):
        """
        from https://rosettacode.org/wiki/Gray_code#Python
        """
        int_n = int(n, 2)
        m = int_n >> 1
        while m:
            int_n ^= m
            m >>= 1
        return int_n

    def get_actual_gamma(self):
        decimal_gamma = Control.get_decimal(self.gamma)
        actual = (decimal_gamma / (2 ** constants.chromosome_length - 1)) * 1.048 - 0.524
        return actual

    def get_actual_beta(self):
        decimal_beta = Control.get_decimal(self.beta)
        actual = (decimal_beta / (2 ** constants.chromosome_length - 1)) * 10 - 5
        return actual
