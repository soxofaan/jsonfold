
Some rough ideas for future work:

- [x] CLI tool
- leverage streaming "iterencode" of json.JSONEncoder
- integration with different (non-stdlib) JSON libraries
- also support Python `repr`?
- improve documentation
- compatibility with Windows-style line endings?
- project structure with src folder?
- test compatibility with tab indentation, or even space+tab mixing
- smarter flushing: see test_fold_iter_flushing_nested
