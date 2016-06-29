library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- pragma translate_off
library unisim;
use unisim.vcomponents.all;
-- pragma translate_on

-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity DFSM_MEMORY%$% is
   generic(
      MEMORY_TARGET_WIDTH : integer := %$%;
      MEMORY_SYMBOL_WIDTH : integer := %$%;
      MEMORY_ADDR_WIDTH   : integer := %$%
   );
   port(
      -- common signals
      CLK            : in  std_logic;
      RESET          : in  std_logic;
      
      -- memory interface
      MEMORY_ADDR    : in  std_logic_vector(MEMORY_ADDR_WIDTH - 1 downto 0);
      MEMORY_RQ      : in  std_logic;
      TARGET         : out std_logic_vector(MEMORY_TARGET_WIDTH - 1 downto 0);
      SYMBOL         : out std_logic_vector(MEMORY_SYMBOL_WIDTH - 1 downto 0);
      N              : out std_logic;
      F              : out std_logic;
      V              : out std_logic
      
   );
end entity DFSM_MEMORY%$%;

architecture full of DFSM_MEMORY%$% is
%$%
begin
%$%
end architecture full;