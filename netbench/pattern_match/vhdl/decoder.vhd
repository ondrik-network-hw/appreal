-- ----------------------------------------------------------------------------
-- Entity for conversion from binary state encoding to one hot encoding 
-- ----------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity DECODER%$% is
   generic(
      INPUT_DATA_WIDTH   : integer := %$%;
      OUTPUT_DATA_WIDTH  : integer := %$%
   );
   port(
      -- input data interface
      INPUT          :  in std_logic_vector(INPUT_DATA_WIDTH - 1 downto 0);

      -- output data interface
      OUTPUT         : out std_logic_vector(OUTPUT_DATA_WIDTH - 1 downto 0)
   );

end entity DECODER%$%;

-- ----------------------------------------------------------------------------
--                     Architecture: full
-- ----------------------------------------------------------------------------
architecture full of DECODER%$% is
    signal bin : std_logic_vector(OUTPUT_DATA_WIDTH - 1 downto 0);
%$%
begin
%$%
end architecture full;