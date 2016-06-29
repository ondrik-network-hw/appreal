library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity sh_reg is
   generic(
      NUM_BITS    : integer   
   );
   port(
      CLK      : in  std_logic;

      DIN      : in  std_logic;
      CE       : in  std_logic;
      DOUT     : out std_logic
   );
end entity sh_reg;

-- ----------------------------------------------------------------------------
--                      Architecture declaration
-- ----------------------------------------------------------------------------
architecture full of sh_reg is
signal reg_value : std_logic_vector(NUM_BITS-1 downto 0);
begin

    process (CLK)
    begin
    if CLK'event and CLK='1' then  
--         if CE = '1' then 
            reg_value <= reg_value(NUM_BITS-2 downto 0) & DIN;
--         end if; 
    end if;
    end process;
    DOUT <= reg_value(NUM_BITS-1);

end architecture full;
