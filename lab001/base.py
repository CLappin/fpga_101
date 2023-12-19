#!/usr/bin/env python3

from migen import *

from litex.build.generic_platform import *
from litex.build.microsemi import MicrosemiPlatform

# IOs ----------------------------------------------------------------------------------------------

_io = [
    ("user_led",  0, Pins("D6"), IOStandard("LVCMOS33")),

    ("user_sw",  0, Pins("E14"), IOStandard("LVCMOS33")),

    ("user_btn", 0, Pins("E13"), IOStandard("LVCMOS33")),

    ("clk100", 0, Pins("R1"), IOStandard("LVCMOS33")),

    ("cpu_reset", 0, Pins("F5"), IOStandard("LVCMOS33")),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(MicrosemiPlatform):
    default_clk_name   = "clk100"
    default_clk_period = 1e9/100e6

    def __init__(self):
        MicrosemiPlatform.__init__(self, "MPF300TS-FCG484-1", _io, toolchain="libero_soc_polarfire")

# Design -------------------------------------------------------------------------------------------

# Create our platform (fpga interface)
platform = Platform()
led = platform.request("user_led")

# Create our module (fpga description)
module = Module()

# Create a counter and blink a led
counter = Signal(26)
module.comb += led.eq(counter[25])
module.sync += counter.eq(counter + 1)

# Build --------------------------------------------------------------------------------------------

platform.build(module)