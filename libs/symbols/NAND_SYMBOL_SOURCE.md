# W25N02KVZEIR schematic symbol

This symbol is a schematic prerequisite for the mandatory NAND addition. It is not yet placed or wired in the design. Existing NOR and microSD circuits are unchanged. No footprint or footprint filter is assigned; package work remains deferred.

Electrical source: Winbond W25N02KVxxIR/U datasheet, Revision G, June 25, 2021, pages 7-8 (pin assignment/description), 60-68 (electrical/timing and package information), 71 (ordering). Exact consulted PDF SHA-256: `3b1ab7e5f738d91539e11c56087d8e8cb974983da2d574200874acb80c682c30`. The ZEIR ordering code denotes the eight-pad WSON option, industrial temperature range.

| Pin | Name | Electrical type |
| --- | --- | --- |
| 1 | /CS | Input |
| 2 | DO / IO1 | Bidirectional |
| 3 | /WP / IO2 | Bidirectional |
| 4 | GND | Power input |
| 5 | DI / IO0 | Bidirectional |
| 6 | CLK | Input |
| 7 | /HOLD / IO3 | Bidirectional |
| 8 | VCC | Power input |

There is no dedicated RESET pin. All four data pins are bidirectional because their direction depends on SPI/Dual/Quad command mode. The exposed central metal pad is not a ninth electrical signal in the datasheet pin assignment.

The candidate is 2 Gbit (256 MiB) raw SLC NAND with internal 8-bit ECC and a 2.7-3.6 V operating supply. Bad-block handling, ECC policy, startup/reset behavior, throughput, shared-rail margin and interface timing remain circuit/firmware qualification requirements. Symbol accuracy does not establish those requirements.

Created through the native KiCad Symbol Editor from the installed KiCad `Memory_Flash:W25Q32JVSS` template, with exact NAND pin names/types and revised geometry. Original KiCad library authors retain attribution. This modified symbol follows the existing KiCad library CC-BY-SA 4.0 license with design exception; see [KICAD_LIBRARY_LICENSE.md](KICAD_LIBRARY_LICENSE.md). Native export confirms readable 50 mil text, 150 mil leads and no overlapping data names.
