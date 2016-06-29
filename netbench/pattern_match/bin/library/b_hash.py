import sys
class b_hash:
    """ This is a base class for implementation of the hashing function. It defines the basic interface that every hash function in the pattern_match module has to implement """

    def __init__(self):
        self.seed = None
        self.lowbound = -sys.maxint-1
        self.highbound = sys.maxint
   
    def get_seed(self):
        """ The function returns seed. The format of the returned data depends on the implemented method """
        return self.seed

    def set_seed(self, seed):
        """ The function allows to set the seed for the hash function. The format is specific for every method. """
        self.seed = seed
        

    def generate_seed(self):
        """ The function generate and set random seed for the hash function. This is only correct way how the seed should be generate. """

    def hash(self,key):
        """ This function coputes hash value for the given key. """
    
    def get_size(self):
        """ The size of the computed hash can differ. This function is able to return the size of the interval to which function hashes the data. The returned interval is in the form of two tuple (lower bound, high bound) """
        return (self.lowbound,self.highbound)

    def set_size(self,bounds):
        """ This function is used for the settings of the size of the output interval of the hash function. The bounds has to be specified as a two tuple (low bound, high bound). However not every method has to support all possible ranges. If the hash function do not support selected interval, set_size returns fail and the interval is not set. """
        return False;

class NoData(Exception):
    """This exceptipon is called if the hash function requires data, which was not set (for example if PHF is generated without setting set of keys"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

