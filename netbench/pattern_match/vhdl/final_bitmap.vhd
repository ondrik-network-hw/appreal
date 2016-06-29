-- ----------------------------------------------------------------------------
-- Entity for final bitmap representation
-- ----------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity FINAL_BITMAP is
   generic(
      DATA_WIDTH : integer :=  8
   );
   port(
      CLK            : in std_logic;
      RESET          : in std_logic;

      -- input data interface
      SET            : in std_logic_vector(DATA_WIDTH - 1 downto 0);

      -- output data interface
      BITMAP         : out std_logic_vector(DATA_WIDTH - 1 downto 0)
   );

end entity FINAL_BITMAP;

-- ----------------------------------------------------------------------------
--                     Architecture: full
-- ----------------------------------------------------------------------------
architecture full of FINAL_BITMAP is
begin
  gen_reg: for i in 0 to DATA_WIDTH - 1 generate
    reg: process(CLK)
    begin
      if (CLK'event and CLK = '1') then
         if (RESET = '1') then
            BITMAP(i) <= '0';
         else
            if SET(i) = '1' then
               BITMAP(i) <= '1';
            end if;
         end if;
      end if;
    end process reg;
  end generate gen_reg;
end architecture full;


