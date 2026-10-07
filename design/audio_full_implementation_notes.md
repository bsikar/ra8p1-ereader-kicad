# Complete audio subsystem: datasheet extraction notes

Working record of primary-source facts used for symbols and sheets. Retrieved
2026-10-06. Each block cites the source; unverified items are marked OPEN.

## XMOS XU316-1024-QF60B-C24 (USB/UAC2 bridge, clock/DSP)

Source: XMOS XU316 Product Series Datasheet v2.0.0,
https://www.xmos.com/documentation/XM-015129-PC/html/rst/XU316-1024.html
(signal tables + QF60B-pinout.svg). QF60B = 3V3 VDDIOL/T/R; VDDIOB18 1V8.

Pin map (QF60B, 0.4 mm QFN-60 + ground paddle):
- VDD 0.9 V: 4,12,19,27,34,42,49,57 (range 0.855-0.945 V)
- VDDIOB18 1.8 V: 17,26; VDDIOL 8; VDDIOR 38; VDDIOT 52 (3.3 V: 2.97-3.63 V)
- PLL_AVDD 22 (0.9 V, ferrite 600R@100MHz DCR<1R + 1 uF suggested)
- USB_VDD33 30 (3.0-3.6 V); USB_VDD18 31 (1.62-1.98 V); USB_DM 28; USB_DP 29
- XOUT 15; XIN 16 (8-30 MHz; 24 MHz typical; refs FA-238 24 MHz 12 pF, Rd 680R, Cl 22 pF)
- TDI 18; TDO 20; RST_N 21 (ST, PU); TMS 23; TCK 24; NC 25; VSS = paddle
- IO: X0D05 1 (4B1), X0D07 2 (4B3), X0D01 3 (1B0), X0D10 5 (1C0), X0D00 6 (1A0),
  X0D11 7 (1D0), X1D00 9 (1A0), X1D01 10 (1B0), X1D09 11 (4A3), X1D10 13 (1C0),
  X1D11 14 (1D0), X1D13 32 (1F0), X1D16 33 (4D0), X1D17 35 (4D1), X1D18 36 (4D2),
  X1D19 37 (4D3), X1D22 39 (1G0), X0D29 40 (4F1), X0D35 41 (1L0), X0D36 43 (1M0),
  X0D37 44 (1N0), X0D38 45 (1O0), X0D40 46 (8D4), X0D39 47 (1P0), X0D42 48 (8D6),
  X0D41 50 (8D5), X0D43 51 (8D7), X1D34 53 (1K0), X0D30 54 (4F2), X0D31 55 (4F3),
  X0D32 56 (4E2), X0D33 58 (4E3), X0D04 59 (4B0), X0D06 60 (4B2)
- IO domain: X0D00-X0D11 and X1D00-X1D11 = IOL; X0D29/35-38 and X1D13-22 = IOR;
  X0D30-33, X0D39-43, X1D34 = IOT.
- Boot: X0D06/X0D05/X0D04 sampled with internal pull-downs; 000 = QSPI flash.
  QSPI: X0D01 SS, X0D04..X0D07 SPIO0..3, X0D10 SCLK (pins fixed in boot ROM).
- Reset: on-chip POR; with multiple supplies RST_N must stay asserted until all
  supplies valid. VDDIO and VDD should ramp within 50 ms. T(RST) >= 5 us.
- IO (3V3): VIH 2.0 V, VIL 0.8 V, VOH >= 2.68 V, VOL <= 0.23 V.
- Ordering codes: XU316-1024-QF60B-C24 / -C32 / -I24 / -I32.
