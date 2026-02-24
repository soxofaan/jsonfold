
# JSON Fold

Indented JSON, but with folded whitespace to have more data on a single line.

JSON serialization has two popular approaches:
- put everything on a single line: most compact, but not handy for human consumption
- spread out everything (each array item, each object property) on its own line
  with appropriate indentation: easier for humans to parse visually
  (often even referred to as "prettifying" or "beautifying"),
  but it's very space-inefficient because of all the repeated indentation.

JSON Fold allows to find a better compromise:
only make arrays or objects multi-line if they would exceed a given line length.
