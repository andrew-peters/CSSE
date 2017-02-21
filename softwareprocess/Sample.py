import math
class Sample(object):

# outward facing methods
    def __init__(self, n=None):
        functionName = "Sample.__init__: "
        if(n == None):
            raise ValueError(functionName + "invalid n")
        if(not(isinstance(n, int))):
            raise ValueError(functionName + "invalid n")
        if((n < 2) or (n >= 30)):
            raise ValueError(functionName + "invalid n")
        self.n = n

    def getN(self):
        return self.n

    
    def p(self, t=None, tails=1):
        functionName = "Sample.p: "
        if(t == None):
            raise ValueError(functionName + "missing t")
        if(not(isinstance(t, float))):
            raise ValueError(functionName + "invalid t")
        if(t < 0.0):
            raise ValueError(functionName + "invalid t")
        
        if(not(isinstance(tails, int))):
            raise ValueError(functionName + "invalid tails")
        if((tails != 1) & (tails != 2)):
            raise ValueError(functionName + "invalid tails")
        
        constant = self.calculateConstant(self.n)
        integration = self.integrate(0, t, self.n, self.f)
        if(tails == 1):
            result = constant * integration + 0.5
        else:
            result = constant * integration * 2
            
        if(result > 1.0):
            raise ValueError(functionName + "result > 1.0")
        
        return result
        
# internal methods
    def gamma(self, x):
        if(x == 1):
            return 1
        if(x == 0.5):
            return math.sqrt(math.pi)
        return (x - 1) * self.gamma(x - 1)
    
    def calculateConstant(self, n):
        n = float(n)
        numerator = self.gamma((n + 1.0) / 2.0)
        denominator = self.gamma(n / 2.0) * math.sqrt(n * math.pi)
        result = numerator / denominator
        return result
    
    def f(self, u, n):
        n = float(n)
        base = (1 + (u ** 2) / n)
        exponent = -(n + 1.0) / 2
        result = base ** exponent
        return result
    
    # def integrate(self, lowBound, highBound, n, f):
    #     epsilon = 0.001
    #     simpsonOld = 0.0
    #     simpsonNew = epsilon
    #     s = 4
    #     coefficient = 0
    #     temp = 0.0
    #     while (abs((simpsonNew - simpsonOld) / simpsonNew) > epsilon):
    #         simpsonOld = simpsonNew
    #         w = (highBound - lowBound) / s
    #         for i in range(0, s):
    #             if i % 2 == 0:
    #                 coefficient = 4
    #             if i % 2 == 1:
    #                 coefficient = 2
    #             if i == 0 or i == s:
    #                 coefficient = 1
    #
    #             temp += coefficient * f(lowBound + (w*i), n)
    #
    #         simpsonNew = (w/3) * temp
    #         s = s * 2
    #
    #     return simpsonNew



    def integrate(self, lowBound, highBound, n, f):
        """
        integrate returns the integral of f  with n degrees of freedom from lowBound to highBound.
        :param lowBound: The lower bound of the integration. Typically 0.
        :param highBound: t, the upper bound of the integration. >= 0.
        :param n: The number of degrees of freedom the distribution has.
        :param f: The function to integrate over, with u and n.
        :return: The area under f between lowBound and highBound, approximated with Simpson's rule.
        """
        epsilon = 0.0001
        simpsonOld = 0.0
        simpsonNew = epsilon
        s = 4
        while abs(simpsonNew - simpsonOld) / simpsonNew > epsilon:
            simpsonOld = simpsonNew
            simpsonNew = self.calculateSimpson(lowBound, highBound, n, f, s)
            s *= 2
        return simpsonNew

    def calculateSimpson(self, lowBound, highBound, n, f, s):
        """
        calculateSimpson returns the integral of f with n degrees of freedom from lowBound to highBound, broken
        into s partitions.
        :param lowBound:    numeric mandatory validated
        :param highBound:   numeric .GE. lowBound mandatory validated
        :param n:           numeric .GE. 2 and .LT. 30 mandatory validated
        :param f:           function(self, float, integer) -> float mandatory validated
        :param s:           integer .GE. 1 mandatory validated
        :return: float, the integral of f, on s partitions
        """
        w = (highBound - lowBound) / s
        total = 0.0
        for i in range(0, s+1):
            total += self.getCoefficient(i, s) * f(lowBound + w * i, n)

        return (w / 3) * total

    def getCoefficient(self, index, numPartitions):
        """
        getCoefficient returns the coefficient for the indexth element of the partitions.
        If this is the first or last coefficient, this is 1. Otherwise, it alternates between 2 and 4.
        :param index: Which element of the partitions to calculate the coefficient for, from 0 (the first partition)
        up to numPartitions (inclusive).
        :param numPartitions: The number of partitions to break the function into.
        :return: An integer, one of 1, 2, or 4, the appropriate coefficient for this partition.
        """

        # Special handling for the boundaries.
        if index == 0 or index == numPartitions:
            return 1

        # Otherwise, every-other has coefficient 2, starting with index 1 (odd indices)
        if index % 2 == 1:
            return 2
        # With all other coefficients (even indices) are 4.
        else:
            return 4

        
        
    
        
            
        
