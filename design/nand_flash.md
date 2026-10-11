# Buffered NAND storage schematic

The additional storage is U39, Winbond W25N02KVZEIR: 2 Gbit (256 MiB) SLC NAND with 8-bit on-die ECC. It uses a dedicated SCI4_C single-SPI interface. Existing microSD and octal NOR remain present.

| Signal | MCU ball / port | Circuit |
|---|---|---|
| NAND_SCK | R14 / P514 | R126 33 ohm to U39 CLK, pin 6; R132 47k to ground |
| NAND_MOSI | N14 / P714 | R127 33 ohm to U39 DI, pin 5 |
| NAND_MISO | T15 / P715 | U39 DO, pin 2, to U40 A; U40 Y through R128 33 ohm to MCU |
| NAND_CS_N | P14 / P413 | GPIO chip select to U39 pin 1; R129 10k to supply |

U39 WP (pin 3) and HOLD (pin 7) each have a 10k pull-up, R130 and R131. R133 is a 47k pull-down at U40 A. U39 VCC/GND are pins 8/4. U40 is Nexperia 74AUP1T34GW,125; VCCA, A, GND, Y, VCCY are pins 1, 2, 3, 4, 5 respectively. Both buffer supply pins, NAND and MCU use the same +3V3_MCU rail and ground. C144/C145 are the NAND's 100n/1u bypass pair with a common drawn return; C146 is the buffer's 100n bypass.

## Why the buffer is required

Winbond guarantees DO VOH of 2.4 V at 400 uA. RA8P1's peripheral VIH is 0.8 times VCC, reaching 2.88 V at 3.6 V. A direct DO-to-MCU connection therefore lacks a guaranteed high-level margin. U40's Schmitt input has VIH 2.0 V and VIL 0.9 V across 3.0–3.6 V; its output guarantees VCCY minus 0.1 V / 0.1 V at 20 uA. The static loads in this circuit fit those guarantees. MCU outputs must use the standard drive condition (VOH >= VCC minus 0.5 V at 1 mA), with MISO pulls disabled.

## Supported schematic envelope

- Shared supply 3.0–3.6 V; operating temperature -40 to +85 C.
- SCI4_C, single-SPI mode 0, at most 10 MHz; actual SCK duty 45–55%. The generic RA8 AC minimum of 0.4 cycle does not by itself meet Winbond's 45% requirement.
- U40 output load at most 10 pF. RA8's other-pin input capacitance limit is 8 pF at 25 C; remaining load and full-temperature behavior require later physical verification. NAND DO must meet the 30 pF datasheet timing load and edge conditions.
- A conditional 5 ns combined path/edge allowance gives 25.2 ns buffered read setup and 36.2 ns hold margins using guaranteed device delays. These are timing screens, contingent on actual divider/sample phase, duty, loading and edges; 33 ohm is an initial series value, not a proven termination.
- Allocate 40 mA steady-state branch current provisionally: NAND's 35 mA active-current basis plus pulls and headroom. Full power budgeting must include loaded NAND/buffer static and switching current. Added MLCC upper initial/tolerance/temperature capacitance is 1.518 uF; <=6 mA inrush assumes a rail rise of at least 1 ms. Neither estimate proves the full rail budget.

## Startup and firmware contract

CS must track VCC during startup. Initialize its data high before enabling GPIO output; leave clock low on reset and idle. Do not infer permission for independently powered domains. Wait at least 200 us after VCC reaches 2.7 V before ordinary access and at least 1 ms before writing/programming. Observe busy/failure status, maximum reset/busy timing, and 1.5 ms release from deep power-down. The datasheet's below-0.7 V, 1 ms power-down interval is characterized, not a universal brownout guarantee.

Firmware must handle ECC status, factory/runtime bad blocks, wear management, atomic metadata and power-loss recovery. FTL and power-loss tests are future work. At 10 MHz the raw ceiling is 1.25 MB/s; a conditional 2048-byte page plus 60 us ECC read screen is about 1.20 MB/s. NAND is not promised to sustain 192/768 kHz uncompressed PCM playback; microSD remains available.

## Parts and primary evidence

R126–R128: Vishay CRCW060333R0FKEA. R129–R131: CRCW060310K0FKEA. R132–R133: CRCW060347K0FKEA. These are 1%, 100 ppm/K parts; calculations use a conservative 1.75% initial/temperature corner. C144/C146: KEMET C0603C104K5RACTU, 100n, 50 V, 10%, X7R. C145: C0603C105K8RACTU, 1u, 10 V, 10%, X7R. Candidate ordering/availability fields are in the native BOM; inventory must be rechecked before purchase. Footprint selection is deferred.

- [RA8P1 datasheet](https://www.renesas.com/en/document/dst/ra8p1-group-datasheet): Rev 1.30, electrical tables 2.5/2.7, ball and alternate-function mapping.
- [Nexperia buffer datasheet](https://assets.nexperia.com/documents/data-sheet/74AUP1T34.pdf): Rev 10, pinning p3, DC p6–7, 10 pF timing p10.
- [Winbond product documentation](https://www.winbond.com/hq/product/code-storage-flash-memory/qspinand-flash/?__locale=en&partNo=W25N02KV): W25N02KV Rev G, June 25 2021, pinout printed p7, startup p59, DC p60, AC p62–63.
- [Vishay resistor datasheet](https://www.vishay.com/docs/20035/dcrcwe3.pdf): Rev April 14 2026, ratings and ordering code.
- [KEMET 100n exact part specification](https://search.kemet.com/component-documentation/download/specsheet/C0603C104K5RACTU) and [1u exact part specification](https://search.kemet.com/component-documentation/download/specsheet/C0603C105K8RACTU).

The source-qualified schematic is complete within this envelope. Actual loading, clock phase/duty, edge behavior, full supply/current behavior and firmware qualification remain separate future gates. The inherited project still has ERC findings; this addition removes four open MCU pins and introduces no new ERC violations. No complete-design release qualification is claimed.
