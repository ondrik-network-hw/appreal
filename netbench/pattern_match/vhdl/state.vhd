-- ----------------------------------------------------------------------------
-- Entity for state representation of Clark NFA
-- ----------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity STATE is
   generic(
      DEFAULT : std_logic :=  '0'
   );
   port(
      CLK            : in std_logic;
      RESET          : in std_logic;

      -- input data interface
      INPUT          :  in std_logic;
      WE             :  in std_logic;

      -- output data interface
      OUTPUT         : out std_logic
   );

end entity STATE;

-- ----------------------------------------------------------------------------
--                     Architecture: full
-- ----------------------------------------------------------------------------
architecture full of STATE is
begin
   reg: process(CLK)
   begin
      if (CLK'event and CLK = '1') then
         if (RESET = '1') then
            OUTPUT <= DEFAULT;
         else
            if WE = '1' then
               OUTPUT <= INPUT;
            end if;
         end if;
      end if;
   end process reg;
end architecture full;


