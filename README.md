# RA8P1 e-reader electronics

Open `ereader/ereader_rev1.kicad_pro` in KiCad 10.0.5 or a compatible newer
version. The project includes its schematic, board, project configuration,
project-local library tables, symbols, footprints, and STEP models. Library
paths resolve relative to the project; standard `Device` and `power` symbols
use the bundled KiCad 10 libraries through `${KICAD10_SYMBOL_DIR}`. No custom
global library installation is needed.

The schematic has a root index and separate processor interface, core-power,
I/O-supply, and clock/reset/debug sheets. The power circuits are drafts with passive qualification
still open; the processor interfaces and remaining subsystems are unfinished.
The PCB is empty.
Neither is a manufacturing release. Imported component models still require
electrical and package qualification before use in a finished design.

## Clone and open

Install Git LFS before cloning, or run `git lfs pull` after cloning. The large
manufacturer reference-design ZIP uses LFS. The editable KiCad project and
component libraries are ordinary Git files. Manufacturer reference files retain
their original notices and are reference material, not this board's design.

Open the project from its checked-out location. Do not add absolute model paths
or depend on a user's global symbol/footprint tables. KiCad lock files, personal
view settings, and editor history are excluded from commits.

## Review and export

`exports/ereader_rev1.pdf` contains every schematic sheet and is refreshed for
each design commit. It represents the design at that commit, including any
explicitly incomplete sections. It is not a fabrication drawing of the PCB.

From the repository root, regenerate it with:

```sh
./scripts/export_design.sh
```

The script also works when called by absolute path from another directory.
It finds `kicad-cli` on PATH or in the standard macOS KiCad app bundle. Set
`KICAD_CLI` to select another executable. An optional schematic path exports
that project's complete hierarchy to `exports/<schematic-name>.pdf`.

The script exports saved files, including all child sheets, and replaces the
previous PDF only after KiCad succeeds and produces a nonempty PDF. It does
not save unsaved editor changes. `--help` shows the available arguments.

Before each commit, save all sheets, export the complete PDF, inspect every
page, and run ERC. During circuit development, record unresolved findings;
do not hide unconnected pins merely to obtain a clean report. Before pushing,
run `python scripts/check_clock_calculations.py`, review the relevant
calculation checks in `design/`, and run `git diff --check`. Follow
`.agents/AGENTS.md` and `LIBRARY_STANDARDS.md`; the former firmware checkout's
parent-relative `CLAUDE.md` is not present in this standalone repository.

## Design references

- [Hardware requirements](design/ereader_requirements.md)
- [Library conventions](LIBRARY_STANDARDS.md)
- [Imported parts inventory](PARTS-CHECKLIST.md)
- [Hardware epic and section issues](https://github.com/bsikar/ra8p1-ereader-kicad/issues/21)

The Gaggia controller is a separate future board. Shared components belong in
the functional libraries under `libs/`; board-specific sheets belong in their
own project directory.

## Related repositories

This board is a separate product that uses the same Renesas RA8 part as the
firmware monorepo, so the electronics live here and the software stays there.
Both are wired in as submodules for context:

- `firmware/` -- [bsikar/ra8-firmware](https://github.com/bsikar/ra8-firmware),
  the RA8 firmware monorepo this project was split out of.
- `emulator/` -- [bsikar/ra8-emulator](https://github.com/bsikar/ra8-emulator),
  the host-side RA8 emulator used for EIL runs.

Clone with `git clone --recurse-submodules`, or run
`git submodule update --init --depth 1` in an existing clone. Both submodules
are registered shallow; nothing in this repository builds against them.
