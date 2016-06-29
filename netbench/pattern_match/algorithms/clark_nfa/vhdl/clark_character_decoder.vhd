-- ----------------------------------------------------------------------------
-- Entity for implementation of Clark Strided NFA
-- ----------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity CLARK_CHARACTER_DECODER is
   generic(
      DATA_WIDTH : integer := %$%
   );
   port(
      DATA : in std_logic_vector(DATA_WIDTH - 1 downto 0);
%$%
   );

end entity CLARK_CHARACTER_DECODER;

-- ----------------------------------------------------------------------------
--                     Architecture: LUT
-- ----------------------------------------------------------------------------
architecture LUT of CLARK_CHARACTER_DECODER is
%$%
begin
%$%
end architecture LUT;
