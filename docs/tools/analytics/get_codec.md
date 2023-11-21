# Get Codec
## Usage
```
Usage: pagetools get-codec [OPTIONS] FILES...

  Retrieves codec of PAGE XML files.

Options:
  -l, --level [region|line|word|glyph]
                                  [default: line]
  -idx, --index INTEGER           Considers only text from TextEquiv elements
                                  with a certain index.
  -mc, --most-common INTEGER      Only prints n most common entries. Shows all
                                  by default.
  -o, --output TEXT               File to which results are written.
  -rw, --remove-whitespace
  -of, --output-format [json|csv|txt]
                                  Available result formats.
  -freq, --frequencies            Outputs character frequencies.
  -nu, --normalize-unicode [NFC|NFD|NFKC|NFKD]
                                  Normalize unicode for both rules and PAGE
                                  XML tests.
  --text-output-newline           Inserts new line after every character in
                                  txt output. Only applies when frequencies
                                  aren't output.
  --verbose / --silent            Choose between verbose or silent output.
  --help                          Show this message and exit.
```

## Example
::: info
TODO
:::