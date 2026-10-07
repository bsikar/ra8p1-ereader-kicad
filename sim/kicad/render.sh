#!/bin/sh
# Export the SPICE netlist and an SVG drawing for one study project: ./render.sh quiet_chain
K=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
cd "$(dirname "$0")" || exit 1
"$K" sch export netlist --format spice -o "$1/$1.cir" "$1/$1.kicad_sch" && "$K" sch export svg -o "$1/" "$1/$1.kicad_sch" | tail -1
