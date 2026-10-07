# Saved MCU connection audit

MCU: R7KA8P1KFLCAC#UC0; 289 unique pins and 199 GPIO ball names
match the checked-in BGA289 pinout derived from Renesas Table 1.17.
This comparison checks the cached symbol against that reference; it does
not independently qualify the reference generator or peripheral functions.

Netlist SHA256: `ac67e94f1c7e1b6dcaeeb00654eec400e6ae8adbeacd1e27f8082a47d2457d9b`.
Counts: {'connected': 111, 'open': 77, 'named singleton': 11}.

Open means no exported electrical peer, not available for reassignment.
Named singletons retain their intended ownership even without a receiver.
The netlist does not prove whether an open pin has a no-connect marker.
Reservations below are incomplete and must be reconciled with all subsystem
contracts before assigning audio enable/status, DAC control or protection.
SSI1_B cannot carry PCM768 in 64-bit stereo frames: 49.152 MHz exceeds
the currently documented 12.5 MHz SSI limit. Keep XU316 transport work open.

Reservation authorities: [radio SDIO](radio_sdio_migration.md),
[camera/storage interfaces](camera_storage_interfaces.md), and
[audio platform](audio_platform_study.md). These records distinguish
future reservations from saved native wiring. Re-run after CAD changes:

`python scripts/report_mcu_connections.py NETLIST.xml --output design/mcu_connection_audit.md`

| Port | Ball | Cached type | Electrical state | Net | Other package pins | Documented reservation |
| --- | --- | --- | --- | --- | --- | --- |
| P609 | A1 | bidirectional | connected | /SDRAM_DQ7 | U14.13 | - |
| P113 | A2 | bidirectional | connected | /SDRAM_DQ4 | U14.8 | - |
| P115 | A3 | bidirectional | connected | /SDRAM_DQ6 | U14.11 | - |
| P112 | A4 | bidirectional | connected | /SDRAM_DQ3 | U14.7 | - |
| P302 | A5 | bidirectional | connected | /SDRAM_DQ0 | U14.2 | - |
| P915 | A6 | bidirectional | open | unconnected-(U1F-P915-PadA6) | - | - |
| P309 | A12 | bidirectional | connected | /Page and volume buttons/PAGE_PREV_N | C58.1, R23.2, R27.2 | - |
| P906 | A13 | bidirectional | named singleton | /RA8P1 IO allocation/CEU_D5 | - | - |
| P905 | A14 | bidirectional | named singleton | /RA8P1 IO allocation/CEU_D6 | - | - |
| P907 | A15 | bidirectional | named singleton | /RA8P1 IO allocation/CEU_D4 | - | - |
| P904 | A16 | bidirectional | connected | /AUDIO_AUX_PG | R118.2, U36.2 | AUDIO_AUX_PG GPIO input, polling; not headphone protection |
| P207 | A17 | bidirectional | open | unconnected-(U1C-P207-PadA17) | - | - |
| P813 | B1 | output | connected | /SDRAM_CS_N | R49.2, U14.20 | - |
| PA12 | B2 | bidirectional | connected | /SDRAM_DQ9 | U14.76 | - |
| P114 | B3 | bidirectional | connected | /SDRAM_DQ5 | U14.10 | - |
| PA11 | B4 | bidirectional | connected | /SDRAM_DQ8 | U14.74 | - |
| P300 | B5 | bidirectional | connected | /SDRAM_DQ2 | U14.5 | - |
| P303 | B6 | bidirectional | connected | /Power button and source control/POWER_BUTTON_N | R20.2, U9.5 | - |
| P311 | B12 | bidirectional | connected | /Page and volume buttons/VOL_DOWN_N | C60.1, R25.2, R29.2 | - |
| P908 | B13 | bidirectional | named singleton | /RA8P1 IO allocation/CEU_D3 | - | - |
| P909 | B14 | bidirectional | named singleton | /RA8P1 IO allocation/CEU_D2 | - | - |
| P206 | B15 | bidirectional | named singleton | /RA8P1 IO allocation/CEU_D0 | - | - |
| PD01 | B16 | bidirectional | open | unconnected-(U1H-PD01-PadB16) | - | RADIO-024 SDHI0_C DAT2 |
| PD02 | B17 | bidirectional | open | unconnected-(U1H-PD02-PadB17) | - | RADIO-024 SDHI0_C DAT1 |
| PA06 | C1 | output | connected | /SDRAM_CKE | R44.2, U14.67 | - |
| P613 | C2 | bidirectional | connected | /SDRAM_DQ15 | U14.85 | - |
| PA13 | C3 | bidirectional | connected | /SDRAM_DQ10 | U14.77 | - |
| P301 | C4 | bidirectional | connected | /SDRAM_DQ1 | U14.4 | - |
| P200 | C5 | input | open | unconnected-(U1C-P200-PadC5) | - | - |
| P210 | C6 | bidirectional | connected | /RA8P1 clocks, reset and debug/DBG_SWDIO | J1.2, R3.2 | - |
| P208 | C7 | input | connected | /RA8P1 clocks, reset and debug/DBG_TDI | J1.8, R5.2 | - |
| P110 | C8 | bidirectional | open | unconnected-(U1B-P110-PadC8) | - | Historical optional MMC DAT4; expansion unresolved, not automatically free |
| P308 | C9 | bidirectional | open | unconnected-(U1C-P308-PadC9) | - | - |
| P305 | C10 | bidirectional | open | unconnected-(U1C-P305-PadC10) | - | - |
| P307 | C11 | bidirectional | connected | /Page and volume buttons/VOL_UP_N | C61.1, R26.2, R30.2 | - |
| P911 | C12 | bidirectional | open | unconnected-(U1F-P911-PadC12) | - | - |
| P312 | C13 | bidirectional | open | unconnected-(U1C-P312-PadC13) | - | - |
| PD04 | C14 | bidirectional | open | unconnected-(U1H-PD04-PadC14) | - | RADIO-024 SDHI0_C CMD |
| PD03 | C15 | bidirectional | open | unconnected-(U1H-PD03-PadC15) | - | RADIO-024 SDHI0_C DAT0 |
| PD05 | C16 | bidirectional | open | unconnected-(U1H-PD05-PadC16) | - | RADIO-024 SDHI0_C CLK |
| PD06 | C17 | bidirectional | open | unconnected-(U1H-PD06-PadC17) | - | RADIO-024 USBHS_OVRCURA candidate |
| PA04 | D1 | output | connected | /SDRAM_DQM3 | R48.2, U14.59 | - |
| P611 | D2 | bidirectional | connected | /SDRAM_DQ13 | U14.82 | - |
| P610 | D3 | bidirectional | connected | /SDRAM_DQ12 | U14.80 | - |
| PA14 | D4 | bidirectional | connected | /SDRAM_DQ11 | U14.79 | - |
| P211 | D6 | input | connected | /RA8P1 clocks, reset and debug/DBG_SWCLK | J1.4, R4.2 | - |
| P109 | D7 | bidirectional | open | unconnected-(U1B-P109-PadD7) | - | Historical optional MMC DAT5; expansion unresolved, not automatically free |
| P108 | D8 | bidirectional | open | unconnected-(U1B-P108-PadD8) | - | Historical optional MMC DAT6; expansion unresolved, not automatically free |
| P903 | D9 | bidirectional | connected | /Power button and source control/POWER_KILL_N | Q1.3, R21.2, R22.1, U9.8 | - |
| P304 | D10 | bidirectional | open | unconnected-(U1C-P304-PadD10) | - | - |
| P306 | D11 | bidirectional | connected | /SENS_INT1 | U26.12 | - |
| P912 | D12 | bidirectional | open | unconnected-(U1F-P912-PadD12) | - | - |
| PB04 | D13 | bidirectional | named singleton | /RA8P1 IO allocation/CEU_PCLK | - | - |
| PB07 | D14 | bidirectional | open | unconnected-(U1G-PB07-PadD14) | - | - |
| PB05 | D15 | bidirectional | open | unconnected-(U1G-PB05-PadD15) | - | - |
| PB03 | D16 | bidirectional | named singleton | /RA8P1 IO allocation/CEU_HREF | - | - |
| PB01 | D17 | bidirectional | open | unconnected-(U1G-PB01-PadD17) | - | - |
| PA15 | E1 | output | connected | /RA8P1 IO allocation/SDRAM_CLK_SRC | R43.2 | - |
| P615 | E2 | output | connected | /SDRAM_DQM2 | R47.2, U14.28 | - |
| P614 | E3 | output | connected | /SDRAM_DQM0 | R45.2, U14.16 | - |
| P612 | E4 | bidirectional | connected | /SDRAM_DQ14 | U14.83 | - |
| P914 | E5 | bidirectional | open | unconnected-(U1F-P914-PadE5) | - | - |
| P201 | E6 | input | connected | /RA8P1 clocks, reset and debug/MCU_BOOT_MD | R2.2, TP2.1 | - |
| P209 | E7 | output | connected | /RA8P1 clocks, reset and debug/DBG_TDO_SWO | J1.6 | - |
| P111 | E8 | bidirectional | open | unconnected-(U1B-P111-PadE8) | - | RADIO-024 SDHI0_C DAT3 |
| P902 | E9 | bidirectional | named singleton | /RA8P1 IO allocation/CEU_D1 | - | - |
| P310 | E10 | bidirectional | connected | /Page and volume buttons/PAGE_NEXT_N | C59.1, R24.2, R28.2 | - |
| P910 | E11 | bidirectional | open | unconnected-(U1F-P910-PadE11) | - | - |
| P913 | E12 | bidirectional | open | unconnected-(U1F-P913-PadE12) | - | - |
| PB02 | E13 | bidirectional | named singleton | /RA8P1 IO allocation/CEU_VSYNC | - | - |
| PB06 | E14 | bidirectional | open | unconnected-(U1G-PB06-PadE14) | - | - |
| PD07 | E15 | bidirectional | open | unconnected-(U1H-PD07-PadE15) | - | - |
| PB00 | E16 | bidirectional | open | unconnected-(U1G-PB00-PadE16) | - | - |
| P706 | E17 | bidirectional | connected | /ESP32-C6 radio/RADIO_RESET_REQ_N | R14.1, U7.6 | - |
| PA02 | F1 | output | connected | /SDRAM_A1 | U14.26 | - |
| PA10 | F2 | output | connected | /SDRAM_RAS_N | R50.2, U14.19 | - |
| PA08 | F3 | output | connected | /SDRAM_WE_N | R52.2, U14.17 | - |
| PA09 | F4 | output | connected | /SDRAM_CAS_N | R51.2, U14.18 | - |
| PC14 | F5 | bidirectional | connected | /SDRAM_DQ16 | U14.31 | - |
| P700 | F12 | bidirectional | open | unconnected-(U1E-P700-PadF12) | - | SSI1_B TX; high-rate transport must be reconciled |
| P702 | F13 | bidirectional | open | unconnected-(U1E-P702-PadF13) | - | SSI1_B BCLK; high-rate transport must be reconciled |
| P406 | F14 | input | connected | /SD_CD_N | R73.2 | - |
| P701 | F15 | bidirectional | open | unconnected-(U1E-P701-PadF15) | - | SSI1_B LRCLK; high-rate transport must be reconciled |
| P707 | F16 | bidirectional | connected | /ESP32-C6 radio/RADIO_PWR_EN | U28.1, U8.6 | - |
| P705 | F17 | bidirectional | connected | /ESP32-C6 radio/RADIO_HANDSHAKE | R101.1, U25.1 | - |
| PA00 | G1 | output | connected | /SDRAM_A3 | U14.60 | - |
| PA03 | G2 | output | connected | /SDRAM_A0 | U14.25 | - |
| PA05 | G3 | output | connected | /SDRAM_DQM1 | R46.2, U14.71 | - |
| PA07 | G4 | bidirectional | open | unconnected-(U1G-PA07-PadG4) | - | - |
| PC12 | G5 | bidirectional | connected | /SDRAM_DQ18 | U14.34 | - |
| P405 | G12 | bidirectional | connected | /SD_DAT3 | R85.1 | - |
| P704 | G13 | bidirectional | connected | /ESP32-C6 radio/RADIO_DATA_READY | R100.2, U25.8 | - |
| P703 | G14 | bidirectional | named singleton | /RA8P1 IO allocation/CEU_D7 | - | - |
| P504 | H1 | output | connected | /SDRAM_A5 | U14.62 | - |
| P503 | H2 | output | connected | /SDRAM_A4 | U14.61 | - |
| P505 | H3 | output | connected | /SDRAM_A6 | U14.63 | - |
| PA01 | H4 | output | connected | /SDRAM_A2 | U14.27 | - |
| PC11 | H5 | bidirectional | connected | /SDRAM_DQ19 | U14.36 | - |
| P403 | H13 | bidirectional | connected | /SD_DAT1 | R87.1 | - |
| P506 | J1 | output | connected | /SDRAM_A7 | U14.64 | - |
| P507 | J2 | output | connected | /SDRAM_A8 | U14.65 | - |
| P508 | J3 | output | connected | /SDRAM_A9 | U14.66 | - |
| P509 | J4 | output | connected | /SDRAM_A10 | U14.24 | - |
| PC13 | J5 | bidirectional | connected | /SDRAM_DQ17 | U14.33 | - |
| P404 | J13 | bidirectional | connected | /SD_DAT2 | R86.1 | - |
| PC15 | K1 | output | connected | /SDRAM_BA1 | U14.23 | - |
| P608 | K2 | output | connected | /SDRAM_A12 | U14.69 | - |
| P510 | K3 | output | connected | /SDRAM_A11 | U14.21 | - |
| PD00 | K4 | output | connected | /SDRAM_BA0 | U14.22 | - |
| PC07 | K5 | bidirectional | connected | /SDRAM_DQ23 | U14.42 | - |
| P410 | K13 | bidirectional | connected | /SENS_SCL | R102.2, U26.1, U32.5 | - |
| P213 | K16 | output | connected | /RA8P1 clocks, reset and debug/OSC_XTAL | C36.1, Y1.3 | - |
| P212 | K17 | input | connected | /RA8P1 clocks, reset and debug/OSC_EXTAL | C35.1, Y1.1 | - |
| PC03 | L1 | bidirectional | connected | /SDRAM_DQ27 | U14.50 | - |
| PC02 | L2 | bidirectional | connected | /SDRAM_DQ28 | U14.51 | - |
| PC04 | L3 | bidirectional | connected | /SDRAM_DQ26 | U14.48 | - |
| PC09 | L4 | bidirectional | connected | /SDRAM_DQ21 | U14.39 | - |
| PC05 | L5 | bidirectional | connected | /SDRAM_DQ25 | U14.47 | - |
| P414 | L13 | bidirectional | open | unconnected-(U1D-P414-PadL13) | - | - |
| P402 | L14 | bidirectional | connected | /SD_DAT0 | R88.1 | - |
| P214 | L16 | output | connected | /RA8P1 clocks, reset and debug/RTC_XCOUT | C38.1, Y2.2 | - |
| P215 | L17 | input | connected | /RA8P1 clocks, reset and debug/RTC_XCIN | C37.1, Y2.1 | - |
| PC00 | M1 | bidirectional | connected | /SDRAM_DQ30 | U14.54 | - |
| P607 | M2 | bidirectional | connected | /SDRAM_DQ31 | U14.56 | - |
| PC01 | M3 | bidirectional | connected | /SDRAM_DQ29 | U14.53 | - |
| PC08 | M4 | bidirectional | connected | /SDRAM_DQ22 | U14.40 | - |
| PC10 | M5 | bidirectional | connected | /SDRAM_DQ20 | U14.37 | - |
| P104 | M6 | output | connected | /NOR_CS_N | R64.2, U15.C2 | - |
| P810 | M9 | bidirectional | open | unconnected-(U1F-P810-PadM9) | - | - |
| P412 | M12 | bidirectional | connected | COVER_INT_N | U33.2 | - |
| P710 | M13 | bidirectional | open | unconnected-(U1E-P710-PadM13) | - | - |
| P411 | M14 | bidirectional | open | unconnected-(U1D-P411-PadM14) | - | - |
| P408 | M15 | bidirectional | open | unconnected-(U1D-P408-PadM15) | - | - |
| P605 | N1 | bidirectional | open | unconnected-(U1E-P605-PadN1) | - | - |
| P604 | N2 | bidirectional | connected | /ESP32-C6 radio/RADIO_CS_N | U5.4 | - |
| P606 | N3 | bidirectional | open | unconnected-(U1E-P606-PadN3) | - | - |
| PC06 | N4 | bidirectional | connected | /SDRAM_DQ24 | U14.45 | - |
| P107 | N5 | bidirectional | connected | /AUDIO_AUX_REQ | R122.1, U37.1 | AUDIO_AUX_REQ GPIO output to U37 request gate; permission and U38 clamp are hardware |
| P106 | N6 | bidirectional | connected | /SD_PWR_REQ | R78.1, U19.3 | Implemented SD_PWR_REQ; not free (microSD power interface) |
| P105 | N7 | input | connected | /NOR_INT_N | R65.2, U15.A5 | - |
| P811 | N8 | bidirectional | open | unconnected-(U1F-P811-PadN8) | - | - |
| P013 | N9 | bidirectional | open | unconnected-(U1B-P013-PadN9) | - | - |
| P011 | N10 | bidirectional | open | unconnected-(U1B-P011-PadN10) | - | - |
| P807 | N11 | bidirectional | open | unconnected-(U1F-P807-PadN11) | - | - |
| P708 | N12 | bidirectional | connected | /SD_IO_REQ | R79.1, U20.3 | - |
| P712 | N13 | bidirectional | open | unconnected-(U1E-P712-PadN13) | - | - |
| P714 | N14 | bidirectional | open | unconnected-(U1E-P714-PadN14) | - | - |
| P711 | N15 | bidirectional | open | unconnected-(U1E-P711-PadN15) | - | - |
| P713 | N16 | bidirectional | open | unconnected-(U1E-P713-PadN16) | - | - |
| P401 | N17 | bidirectional | connected | /SD_CMD | R84.1 | - |
| P603 | P1 | bidirectional | connected | /ESP32-C6 radio/RADIO_COPI | U5.3 | - |
| P602 | P2 | bidirectional | connected | /ESP32-C6 radio/RADIO_CIPO | U5.5 | - |
| P600 | P3 | bidirectional | open | unconnected-(U1E-P600-PadP3) | - | - |
| P601 | P4 | bidirectional | connected | /ESP32-C6 radio/RADIO_SCLK | U5.2 | - |
| P102 | P5 | bidirectional | connected | /NOR_DQ_HOST4 | R58.1 | - |
| P801 | P6 | input | connected | /NOR_DS_HOST | R63.1 | - |
| P803 | P7 | bidirectional | connected | /NOR_DQ_HOST1 | R55.1 | - |
| P812 | P8 | bidirectional | open | unconnected-(U1F-P812-PadP8) | - | - |
| P012 | P9 | bidirectional | open | unconnected-(U1B-P012-PadP9) | - | - |
| P010 | P10 | bidirectional | open | unconnected-(U1B-P010-PadP10) | - | - |
| P009 | P11 | bidirectional | open | unconnected-(U1B-P009-PadP11) | - | - |
| P805 | P12 | bidirectional | open | unconnected-(U1F-P805-PadP12) | - | - |
| P512 | P13 | bidirectional | connected | /CAM_SCL | J3.13, R98.1 | - |
| P413 | P14 | bidirectional | open | unconnected-(U1D-P413-PadP14) | - | - |
| P515 | P15 | bidirectional | open | unconnected-(U1D-P515-PadP15) | - | - |
| P709 | P16 | bidirectional | connected | /CAM_PWR_REQ | R96.1, U24.3 | - |
| P400 | P17 | bidirectional | connected | /SD_CLK | R83.1 | - |
| P103 | R4 | bidirectional | connected | /NOR_DQ_HOST2 | R56.1 | - |
| P101 | R5 | bidirectional | connected | /NOR_DQ_HOST3 | R57.1 | - |
| P802 | R6 | bidirectional | connected | /NOR_DQ_HOST6 | R60.1 | - |
| P804 | R7 | bidirectional | connected | /NOR_DQ_HOST7 | R61.1 | - |
| P501 | R8 | bidirectional | open | unconnected-(U1D-P501-PadR8) | - | - |
| P005 | R11 | bidirectional | open | unconnected-(U1B-P005-PadR11) | - | - |
| P003 | R12 | bidirectional | open | unconnected-(U1B-P003-PadR12) | - | - |
| P513 | R13 | bidirectional | open | unconnected-(U1D-P513-PadR13) | - | - |
| P514 | R14 | bidirectional | open | unconnected-(U1D-P514-PadR14) | - | - |
| P415 | R15 | bidirectional | open | unconnected-(U1D-P415-PadR15) | - | - |
| P409 | R16 | bidirectional | connected | /SENS_SDA | R103.2, U26.4, U32.8 | - |
| P407 | R17 | bidirectional | connected | /SD_READY | R81.2, U17.6, U18.1, U20.6 | - |
| P809 | T5 | bidirectional | open | unconnected-(U1F-P809-PadT5) | - | - |
| P800 | T6 | bidirectional | connected | /NOR_DQ_HOST5 | R59.1 | - |
| P502 | T7 | bidirectional | open | unconnected-(U1D-P502-PadT7) | - | - |
| P014 | T8 | bidirectional | open | unconnected-(U1B-P014-PadT8) | - | - |
| P004 | T11 | bidirectional | open | unconnected-(U1B-P004-PadT11) | - | - |
| P007 | T12 | bidirectional | open | unconnected-(U1B-P007-PadT12) | - | - |
| P001 | T13 | bidirectional | open | unconnected-(U1B-P001-PadT13) | - | - |
| P806 | T14 | bidirectional | open | unconnected-(U1F-P806-PadT14) | - | - |
| P715 | T15 | bidirectional | open | unconnected-(U1E-P715-PadT15) | - | - |
| P815 | T16 | bidirectional | open | unconnected-(U1M-P815/USB_DM-PadT16) | - | USB FS DM/DP pair; USB ownership pending |
| P808 | U5 | output | connected | /NOR_CK_HOST | R62.1 | - |
| P100 | U6 | bidirectional | connected | /NOR_DQ_HOST0 | R54.1 | - |
| P500 | U7 | bidirectional | open | unconnected-(U1D-P500-PadU7) | - | - |
| P015 | U8 | bidirectional | open | unconnected-(U1B-P015-PadU8) | - | - |
| P008 | U11 | bidirectional | open | unconnected-(U1B-P008-PadU11) | - | - |
| P006 | U12 | bidirectional | open | unconnected-(U1B-P006-PadU12) | - | - |
| P000 | U13 | bidirectional | open | unconnected-(U1B-P000-PadU13) | - | - |
| P002 | U14 | bidirectional | open | unconnected-(U1B-P002-PadU14) | - | - |
| P511 | U15 | bidirectional | connected | /CAM_SDA | J3.14, R99.1 | - |
| P814 | U16 | bidirectional | open | unconnected-(U1M-P814/USB_DP-PadU16) | - | USB FS DM/DP pair; USB ownership pending |
