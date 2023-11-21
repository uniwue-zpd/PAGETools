# Regularization
## Usage
```
Usage: pagetools regularize [OPTIONS] XMLS...

  Regularize the text content of PAGE XML files using custom rulesets.

Options:
  --remove-default [various|quotes|ligatures_consonantal|ligatures_vocal|roman_digits|uvius|punctuation|spaces]
                                  Removes specified default ruleset.
  --add-default [various|quotes|ligatures_consonantal|ligatures_vocal|roman_digits|uvius|punctuation|spaces]
                                  Adds specified default ruleset. Overrides
                                  all other default options.
  -nd, --no-default               Disables all default rulesets.
  -r, --rules PATH                File(s) which contains serialized ruleset.
  -nu, --normalize-unicode [NFC|NFD|NFKC|NFKD]
                                  Normalize unicode for both rules and PAGE
                                  XML tests.
  -s, --safe / -us, --unsafe      Creates backups of original files before
                                  overwriting.
  --help                          Show this message and exit.
```
## Example
::: info
TODO
:::
