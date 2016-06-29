vlib work
vdel -all
vlib work

# BASE setting and Modules.tcl inclusion
set ENTITY_BASE "."
source "Modules.tcl"

# FPGA Design modules compilation
foreach i $MOD {
   vcom -93 -O0 -explicit -work work $i
}

# Addition simulation modules compilation
vcom -93 -explicit -O0 -work work testbench.vhd

# Starting simulation
vsim -novopt -t 1ps -L xilinxcorelib -lib work testbench

# Suppress warnings from arithm library
puts "Std Arith Warnings - Disabled"
set  StdArithNoWarnings 1

# -------------------------------------------------------------------------
#                       Waveform Definition 
# -------------------------------------------------------------------------
add wave -label reset /testbench/uut/reset
add wave -label clk   /testbench/uut/clk

# input sinals
add wave -divider "FL in"
add wave -hex -label rx_data /testbench/uut/RX_DATA
add wave -label rx_sof_n /testbench/uut/RX_SOF_N
add wave -label rx_sop_n /testbench/uut/RX_SOP_N
add wave -label rx_eop_n /testbench/uut/RX_EOP_N
add wave -label rx_eof_n /testbench/uut/RX_EOF_N
add wave -label rx_src_rdy_n /testbench/uut/RX_SRC_RDY_N
add wave -label rx_dst_rdy_n /testbench/uut/RX_DST_RDY_N

add wave -divider "FL out"
add wave -hex -label tx_data /testbench/uut/TX_DATA
add wave -label tx_sof_n /testbench/uut/TX_SOF_N
add wave -label tx_sop_n /testbench/uut/TX_SOP_N
add wave -label tx_eop_n /testbench/uut/TX_EOP_N
add wave -label tx_eof_n /testbench/uut/TX_EOF_N
add wave -label tx_src_rdy_n /testbench/uut/TX_SRC_RDY_N
add wave -label tx_dst_rdy_n /testbench/uut/TX_DST_RDY_N

# User defined signals ----------------------------------------------
add wave -divider "Inner Signals"
# INSERT HERE : User defined signals
add wave -hex -label bitmap /testbench/uut/bitmap
add wave -label vld /testbench/uut/vld
add wave -label ack /testbench/uut/ack

# add wave -divider "Monitor Signals"
# add wave -divider "Fifo in"
# add wave -hex -label rx_data /testbench/MONITOR_I/RX_DATA
# add wave -label rx_sof_n /testbench/MONITOR_I/RX_SOF_N
# add wave -label rx_sop_n /testbench/MONITOR_I/RX_SOP_N
# add wave -label rx_eop_n /testbench/MONITOR_I/RX_EOP_N
# add wave -label rx_eof_n /testbench/MONITOR_I/RX_EOF_N
# add wave -label rdy_n /testbench/MONITOR_I/RDY_N
# add wave -label fifo_rdy_n /testbench/MONITOR_I/FIFO_RDY_N
# 
# add wave -divider "Fifo out"
# add wave -hex -label inbus_data /testbench/MONITOR_I/INBUS_DATA
# add wave -label inbus_sof_n /testbench/MONITOR_I/INBUS_SOF_N
# add wave -label inbus_sop_n /testbench/MONITOR_I/INBUS_SOP_N
# add wave -label inbus_eop_n /testbench/MONITOR_I/INBUS_EOP_N
# add wave -label inbus_eof_n /testbench/MONITOR_I/INBUS_EOF_N
# add wave -label inbus_src_rdy_n /testbench/MONITOR_I/INBUS_SRC_RDY_N
# add wave -label inbus_dst_rdy_n /testbench/MONITOR_I/INBUS_DST_RDY_N
# 
# add wave -divider "Fifo out"
# add wave -hex -label aux_fl_bus /testbench/MONITOR_I/AUX_FL_BUS
# 
# add wave -divider "Other"
# add wave -label DST_RDY_N /testbench/MONITOR_I/DST_RDY_N
# add wave -label FIFO_RDY_N /testbench/MONITOR_I/FIFO_RDY_N
# add wave -label sig_full /testbench/MONITOR_I/input_fifo/FL_FIFO_LOG/sig_full
# add wave -label RESET /testbench/MONITOR_I/input_fifo/FL_FIFO_LOG/RESET

# add wave -divider "Testbench Signals"
#add wave -hex -label FL_bus /testbench/FL_bus
#add wave -hex -label FL_bus2 /testbench/FL_bus2

# add wave -hex -label FL_bus_data /testbench/FL_bus_DATA
# add wave -label FL_bus_sof_n /testbench/FL_bus_SOF_N
# add wave -label FL_bus_sop_n /testbench/FL_bus_SOP_N
# add wave -label FL_bus_eop_n /testbench/FL_bus_EOP_N
# add wave -label FL_bus_eof_n /testbench/FL_bus_EOF_N
# add wave -label FL_bus_src_rdy_n /testbench/FL_bus_SRC_RDY_N
# add wave -label FL_bus_dst_rdy_n /testbench/FL_bus_DST_RDY_N
# 
# add wave -hex -label FL_bus2_data /testbench/FL_bus2_DATA
# add wave -label FL_bus2_sof_n /testbench/FL_bus2_SOF_N
# add wave -label FL_bus2_sop_n /testbench/FL_bus2_SOP_N
# add wave -label FL_bus2_eop_n /testbench/FL_bus2_EOP_N
# add wave -label FL_bus2_eof_n /testbench/FL_bus2_EOF_N
# add wave -label FL_bus2_src_rdy_n /testbench/FL_bus2_SRC_RDY_N
# add wave -label FL_bus2_dst_rdy_n /testbench/FL_bus2_DST_RDY_N


# add wave -divider "Clark unit"
# add wave -label clk  /testbench/uut/unit/clk   
# add wave -divider "Unit signals"
# add wave -label local_reset  /testbench/uut/unit/local_reset   
# add wave -label we           /testbench/uut/unit/we            
# 
# add wave -divider "Generated Logic"
# add wave -label char_97      /testbench/uut/unit/char_97     
# add wave -label char_98      /testbench/uut/unit/char_98     
# add wave -label symbol_0     /testbench/uut/unit/symbol_0    
# add wave -label symbol_1     /testbench/uut/unit/symbol_1    
# add wave -label state_in_0   /testbench/uut/unit/state_in_0  
# add wave -label state_out_0  /testbench/uut/unit/state_out_0 
# add wave -label state_in_2   /testbench/uut/unit/state_in_2  
# add wave -label state_out_2  /testbench/uut/unit/state_out_2 
# add wave -label state_in_5   /testbench/uut/unit/state_in_5  
# add wave -label state_out_5  /testbench/uut/unit/state_out_5 
# add wave -label bitmap_in    /testbench/uut/unit/bitmap_in   
# add wave -label final_0      /testbench/uut/unit/final_0     
run 3 us

