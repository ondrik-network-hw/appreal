-- ----------------------------------------------------------------------------
-- Entity for conversion from one hot encoding to binary state encoding
-- ----------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity ENCODER%$% is
   generic(
      INPUT_DATA_WIDTH   : integer := %$%;
      OUTPUT_DATA_WIDTH  : integer := %$%
   );
   port(
      -- input data interface
      INPUT          :  in std_logic_vector(INPUT_DATA_WIDTH - 1 downto 0);

      -- output data interface
      OUTPUT         : out std_logic_vector(OUTPUT_DATA_WIDTH - 1 downto 0);
      VLD            : out std_logic
   );

end entity ENCODER%$%;

-- ----------------------------------------------------------------------------
--                     Architecture: full
-- ----------------------------------------------------------------------------
architecture full of ENCODER%$% is
    signal bin : std_logic_vector(OUTPUT_DATA_WIDTH - 1 downto 0);
begin
%$%    
    OUTPUT <= bin;
    
    generic_or: process(INPUT)
    begin
        if (INPUT = conv_std_logic_vector(0, INPUT_DATA_WIDTH)) then
            VLD <= '0';
        else
            VLD <= '1';
        end if;
    end process generic_or;
    
end architecture full;