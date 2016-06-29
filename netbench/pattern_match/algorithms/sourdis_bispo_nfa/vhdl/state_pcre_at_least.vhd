-- ----------------------------------------------------------------------------
-- Entity for implementation of exactly N 
-- ----------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity STATE_PCRE_AT_LEAST is
   generic(
      M              : integer
   );
   port(
      CLK            : in std_logic;
      RESET          : in std_logic;

      -- input data interface
      INPUT          :  in std_logic;
      SYMBOL         :  in std_logic;
      WE             :  in std_logic;

      -- output data interface
      OUTPUT         : out std_logic
   );

end entity STATE_PCRE_AT_LEAST;

-- ----------------------------------------------------------------------------
--                     Architecture: full
-- ----------------------------------------------------------------------------
architecture full of STATE_PCRE_AT_LEAST is
    signal value : std_logic_vector(11 downto 0);
    signal local_reset : std_logic;
begin
    local_reset <= RESET or not SYMBOL;

    cnt_symbols: process(RESET, CLK)
    begin
        if (CLK'event and CLK = '1') then
            if (local_reset = '1') then
                value <= (others => '0');
            else
                if (we = '1') then
                    if ((value > 0) or (INPUT = '1')) then
                        value <= value + 1;
                    end if;
                end if;
            end if;
        end if;
    end process;

   OUTPUT <= '1' when (value >= M) else '0';
   
end architecture full;
