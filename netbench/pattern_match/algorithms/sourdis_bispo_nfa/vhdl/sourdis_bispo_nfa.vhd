-- ----------------------------------------------------------------------------
-- Entity for implementation of Sourdis_Bispo NFA
-- ----------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity SOURDIS_BISPO_NFA is
   generic(
      DATA_WIDTH : integer := %$%;
      RULES      : integer := %$%
   );
   port(
      CLK            : in std_logic;
      RESET          : in std_logic;

      -- input data interface
      DATA           :  in std_logic_vector(DATA_WIDTH - 1 downto 0);
      SOF            :  in std_logic;
      EOF            :  in std_logic;
      SRC_RDY        :  in std_logic;
      DST_RDY        : out std_logic;

      -- output data interface
      BITMAP         : out std_logic_vector(RULES - 1 downto 0);
      VLD            : out std_logic;
      ACK            :  in std_logic
   );

end entity SOURDIS_BISPO_NFA;

-- ----------------------------------------------------------------------------
--                     Architecture: full
-- ----------------------------------------------------------------------------
architecture full of SOURDIS_BISPO_NFA is
    signal local_reset : std_logic;
    signal local_reset_fsm : std_logic;
    signal we : std_logic;
--     signal rdy : std_logic;
--     signal vld_internal : std_logic;
--     signal set : std_logic;
%$%
begin

    local_reset <= RESET or local_reset_fsm;
    
    ctrl_fsm: entity work.CONTROL_FSM
    port map(
    CLK         => CLK,
    RESET       => RESET,
    
    -- input interface
    EOF         => EOF,
    SRC_RDY     => SRC_RDY,
    DST_RDY     => DST_RDY,

    -- output interface
    WE          => we,
    LOCAL_RESET => local_reset_fsm,

    -- inner interface
    VLD         => VLD,
    ACK         => ACK
   );
   
--     local_reset <= RESET or ACK;
--     we <= SRC_RDY and rdy;
--     DST_RDY <= rdy;
--     VLD <= vld_internal;
--     set <= SRC_RDY and EOF and rdy;
--     rdy <= not vld_internal;
--     
--     end_reg: process(CLK)
--     begin
--         if (CLK'event and CLK = '1') then
--             if (local_reset = '1') then
--                 vld_internal <= '0';
--             else
--                 if set = '1' then
--                     vld_internal <= '1';
--                 end if;
--             end if;
--         end if;
--     end process end_reg;
    
%$%
    final_bitmap_u: entity work.FINAL_BITMAP
    generic map(
      DATA_WIDTH => RULES
    )
    port map(
        CLK            => CLK,
        RESET          => local_reset,

        -- input data interface
        SET            => bitmap_in,

        -- output data interface
        BITMAP         => BITMAP
    );
end architecture full;
