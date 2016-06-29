from b_hash import b_hash
import random
from bitstring import BitStream, BitArray

class h3_hash(b_hash):
    """Fast hash in hardware. This hash uses only XOR and AND operation"""

    def set_bitsize(self,size):
        """this function sets the number of bits required for output"""
        self.bit_size = size

    def get_size(self):
        """This function returns bitsize of the output"""
        return self.bit_size

    def set_input_size(self,size):
        """This function sets in number of input bits"""
        self.input_size = size

    def get_input_size(self):
        """This function returns the number of bit in the key."""
        return self.input_size

    def generate_seed(self):
        """This function generates the new h3 hash function"""
        self.seed = [None] *self.bit_size
        for out_bit in range(0,self.bit_size):
            self.seed[out_bit] = BitArray(uint = random.getrandbits(self.input_size),length = self.input_size)
        
    def hash(self,key):
        """This function computes hash values for the given key according to the H3 function family. The result is returned as an integer value on 32 bits. However if the hash function generates lower number of bits, higher positions are set to 0"""
        value = BitArray()
        key_val = BitArray(bytes=key, length = self.input_size)
        for i in range(0,self.bit_size):
            bit = [key_val[j] and self.seed[i][j] for j in range(0,self.input_size)]
            bit_v = bit[0]
            for j in range(1,self.input_size):
                bit_v = bit_v ^ bit[j]
            if bit_v:
                value.append('0b1')
            else:
                value.append('0b0') 
            #print(key_val.bin,self.seed[i].bin,bit,bit_v)
        #print(value.uint,value.bin)
        return value.uint
               
                 
