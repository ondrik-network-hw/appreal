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
entity STATE_PCRE_EXACT is
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

end entity STATE_PCRE_EXACT;

-- ----------------------------------------------------------------------------
--                     Architecture: full
-- ----------------------------------------------------------------------------
architecture full of STATE_PCRE_EXACT is
    signal local_reset : std_logic;
    signal local_reset_out: std_logic;
    signal cnt_reset: std_logic;
    signal sh_out : std_logic;
    signal sh_in : std_logic;
    signal value : std_logic_vector(11 downto 0);
begin
    local_reset <= RESET or not SYMBOL;
    local_reset_out <= RESET or cnt_reset;
    
    input_reg: process(CLK, RESET)
    begin
        if (clk'event and CLK='1') then
            if (local_reset = '1') then
                sh_in <= '0';
            else
                sh_in <= INPUT;
            end if;
        end if;
    end process;

    gen_shift: if M > 2 generate
        shift_reg: entity work.sh_reg
        generic map(
            NUM_BITS  => M - 2
        )
        port map(
            CLK      => CLK,

            DIN      => sh_in,
            CE       => WE,
            DOUT     => sh_out
        );
    end generate;
    gen_2: if M = 2 generate
        sh_out <= sh_in;
    end generate;
    gen_1: if M = 1 generate
        sh_out <= INPUT;
    end generate;

    output_reg: process(CLK, RESET)
    begin
        if (clk'event and CLK='1') then
            if (local_reset_out = '1') then
                OUTPUT <= '0';
            else
                OUTPUT <= sh_out;
            end if;
        end if;
    end process;
    
    cnt_reset_u: process(CLK, RESET)
    begin
        if (CLK'event and CLK = '1') then
            if (local_reset = '1') then
                value <= (others => '0');
            else
                if (we = '1') then
                    if ((cnt_reset = '1')) then
                        value <= value + 1;
                    end if;
                end if;
            end if;
        end if;
    end process;
    
    cnt_reset <= '1' when (value > 0 and value <= M) else '0';
    
end architecture full;
