-- ----------------------------------------------------------------------------
-- Pattern match control FSM
-- ----------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;
use work.math_pack.all;

-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity CONTROL_FSM is
   port(
    CLK         : in  std_logic;
    RESET       : in  std_logic;
    
    -- input interface
    EOF         : in  std_logic;
    SRC_RDY     : in  std_logic;
    DST_RDY     : out std_logic;

    -- output interface
    WE          : out std_logic;
    LOCAL_RESET : out std_logic;

    -- inner interface
    VLD         : out std_logic;
    ACK         : in  std_logic

   );
end entity CONTROL_FSM;

-- ----------------------------------------------------------------------------
--                      Architecture declaration
-- ----------------------------------------------------------------------------
architecture CONTROL_FSM_ARCH of CONTROL_FSM is
    type tstates is (READY, FINISH, VALID, PREPARE);
    signal current_state             : tstates;
    signal next_state                : tstates;
begin
    -- FSM state register
    state_register: process (RESET, CLK)
    begin
        if CLK'event and CLK = '1' then
            if RESET = '1' then
                current_state <= READY;
            else
                current_state <= next_state;
            end if;
        end if;
    end process state_register;

    -- transitions in FSM
    transitions_FSM: process (current_state, EOF, SRC_RDY, ACK)
    begin
        next_state <= current_state;
      
        case current_state is
            when READY =>
                if (EOF = '1' and SRC_RDY = '1') then
                    next_state <= FINISH;
                end if;
            when FINISH =>
                next_state <= VALID;
            when VALID =>
                if (ACK = '1') then
                    next_state <= PREPARE;
                end if;
            when PREPARE =>
                next_state <= READY;
            when others =>
        end case;
    end process;
   
    -- outputs of FSM
    outputs_FSM: process (current_state,  EOF, SRC_RDY, ACK)
    begin
        case current_state is
            when READY =>
                DST_RDY <= '1';
                VLD <= '0';
                LOCAL_RESET <= '0';
                WE <= SRC_RDY;
            when FINISH =>
                DST_RDY <= '0';
                VLD <= '0';
                LOCAL_RESET <= '0';
                WE <= '0';
            when VALID =>
                DST_RDY <= '0';
                VLD <= '1';
                LOCAL_RESET <= '0';
                WE <= '0';
            when PREPARE =>
                DST_RDY <= '0';
                VLD <= '0';
                LOCAL_RESET <= '1';
                WE <= '0';
            when others =>
        end case;
    end process;

end architecture CONTROL_FSM_ARCH;