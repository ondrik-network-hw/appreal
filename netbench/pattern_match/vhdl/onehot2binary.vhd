-- ----------------------------------------------------------------------------
-- Entity for conversion from one hot encoding to binary encoding
-- ----------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity ONEHOT2BINARY is
   generic(
      INPUT_DATA_WIDTH   : integer := 16;
      OUTPUT_DATA_WIDTH  : integer :=  4
   );
   port(
      -- input data interface
      INPUT          :  in std_logic_vector(INPUT_DATA_WIDTH - 1 downto 0);

      -- output data interface
      OUTPUT         : out std_logic_vector(OUTPUT_DATA_WIDTH - 1 downto 0);
      VLD            : out std_logic
   );

end entity ONEHOT2BINARY;

-- ----------------------------------------------------------------------------
--                     Architecture: full
-- ----------------------------------------------------------------------------
architecture full of ONEHOT2BINARY is
begin
    one_hot_2_binary: process(INPUT)
        variable bin : std_logic_vector(OUTPUT_DATA_WIDTH - 1 downto 0);
    begin
        bin:= (others => '0');
    
        for i in INPUT_DATA_WIDTH-1 downto 0 loop
            if (INPUT(i) = '1') then
                bin := conv_std_logic_vector(i, 32);
            end if;
        end loop;
    
        OUTPUT <= bin;
    end process one_hot_2_binary;
    
    generic_or: process(INPUT)
    begin
        if (INPUT = conv_std_logic_vector(0, INPUT_DATA_WIDTH)) then
            VLD <= '0';
        else
            VLD <= '1';
        end if;
    end process generic_or;
    
end architecture full;