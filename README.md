# PAGETools - WIP
Small collection of [PAGE XML](https://github.com/PRImA-Research-Lab/PAGE-XML) related Python scripts used at the
[Centre for Philology and Digitality (ZPD), University of Würzburg](https://github.com/uniwue-zpd).

## Installing
### Installation using pip
The suggested method is to install `pagetools` into a virtual environment using pip:
```bash
python -m venv VENV_NAME
source VENV_NAME/bin/activate
pip install pagetools
```
To install the package from source, clone this repository and run inside the project directory
```bash
pip install .
```

## Usage

### Transformations 
#### Extraction
```
Usage: pagetools extract [OPTIONS] XMLS...

  Extract elements as image (optionally with text) files.

Options:
  --include [TextRegion|ImageRegion|LineDrawingRegion|GraphicRegion|TableRegion|ChartRegion|MapRegion|SeparatorRegion|MathsRegion|ChemRegion|MusicRegion|AdvertRegion|NoiseRegion|NoiseRegion|UnknownRegion|CustomRegion|TextLine|*]
                                  PAGE XML element types to extract (highest
                                  priority).

  --exclude [TextRegion|ImageRegion|LineDrawingRegion|GraphicRegion|TableRegion|ChartRegion|MapRegion|SeparatorRegion|MathsRegion|ChemRegion|MusicRegion|AdvertRegion|NoiseRegion|NoiseRegion|UnknownRegion|CustomRegion|TextLine|*]
                                  PAGE XML element types to exclude from
                                  extraction (lowest priority).

  --no-text                       Suppresses text extraction.
  -ie, --image-extension TEXT     Extension of image files. Must be in the
                                  same directory as corresponding XML file.

  -o, --output TEXT               Path where generated files will get saved.
  -e, --enumerate-output          Enumerates output file names instead of
                                  using original names.

  -z, --zip-output                Add generated output to zip archive.
  -bg, --background-color INTEGER...
                                  RGB color code used to fill up background.
                                  Used when padding and / or deskewing.

  --background-mode [median|mean|dominant]
                                  Color calc mode to fill up background
                                  (overwrites -bg / --background-color).

  -p, --padding INTEGER...        Padding in pixels around the line image
                                  cutout (top, bottom, left, right).

  -ad, --auto-deskew              Automatically deskew extracted line images
                                  (Experimental!).

  -d, --deskew FLOAT              Angle for manual clockwise rotation of the
                                  line images.

  -gt, --gt-index INTEGER         Index of the TextEquiv elements containing
                                  ground truth.

  -pred, --pred-index INTEGER     Index of the TextEquiv elements containing
                                  predicted text.

  --help                          Show this message and exit.
```

##### Examples
Only extract `TextLine` elements:
```
pagetools extract <Path/to/xml/files>/*.xml -ie <img_extension> -o <Path/to/output/dir> --include TextLine --exclude "*"
```

Pay in mind that --include / --exclude currently work different from e.g. the same arguments in `rsync` (due to limitations with the `click` library). Inclusion of certain element types always trumps exclusion of the same type, regardless of the order in the call.

#### Regularization
```
Usage: pagetools regularize [OPTIONS] XMLS...

  Regularize the text content of PAGE XML files using custom rulesets.

Options:
  --remove-default [default|ligatures_consonantal|ligatures_vocal|punctuation|quotes|roman_digits|spaces|uvius|various]
                                  Removes specified default ruleset.
  --add-default [default|ligatures_consonantal|ligatures_vocal|punctuation|quotes|roman_digits|spaces|uvius|various]
                                  Adds specified default ruleset. Overrides
                                  all other default options.

  -nd, --no-default               Disables all default rulesets.
  -r, --rules PATH                File(s) which contains serialized ruleset.
  -s, --safe / -us, --unsafe      Creates backups of original files before
                                  overwriting.

  --help                          Show this message and exit.
```

### Analytics
#### Get Codec
```
Usage: pagetools get_codec [OPTIONS] FILES...

  Retrieves codec of PAGE XML files.

Options:
  -l, --level [region|line|word|glyph]
  -idx, --index INTEGER           Considers only text from TextEquiv elements
                                  with a certain index.

  -mc, --most-common INTEGER      Only prints n most common entries. Shows all
                                  by default.

  -o, --output TEXT               File to which results are written.
  -rw, --remove-whitespace
  -of, --output-format [json|csv|txt]
                                  Available result formats.
  -freq, --frequencies            Outputs character frequencies.
  --text-output-newline           Inserts new line after every character in
                                  txt output. Only applies when frequencies
                                  aren't output.

  --verbose / --silent            Choose between verbose or silent output.
  --help                          Show this message and exit.

```