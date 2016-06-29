-- ----------------------------------------------------------------------------
-- Entity for value decoding (N->1)
-- ----------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity VALUE_DECODER is
   generic(
      DATA_WIDTH : integer := 8;
      VALUE      : integer := 0
   );
   port(
      -- input data interface
      INPUT      :  in std_logic_vector(DATA_WIDTH - 1 downto 0);

      -- output data interface
      OUTPUT     : out std_logic
   );

end entity VALUE_DECODER;

-- ----------------------------------------------------------------------------
--                     Architecture: full
-- ----------------------------------------------------------------------------
architecture full of VALUE_DECODER is
begin
    dec: process(INPUT)
    begin
        if (INPUT = conv_std_logic_vector(VALUE, DATA_WIDTH)) then
            OUTPUT <= '1';
        else
            OUTPUT <= '0';
        end if;
    end process dec;
end architecture full;