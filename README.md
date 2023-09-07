<div align="center"><img style="width: 50%" src="assets/logo.png" alt="logo"></div>

---
[![Python package](https://github.com/uniwue-zpd/PAGETools/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/uniwue-zpd/PAGETools/actions/workflows/python-package.yml) [![Upload Python Package](https://github.com/uniwue-zpd/PAGETools/actions/workflows/python-publish.yml/badge.svg?branch=main)](https://github.com/uniwue-zpd/PAGETools/actions/workflows/python-publish.yml)

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
python -m venv VENV_NAME
source VENV_NAME/bin/activate
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
                                  [default: .png]
  -o, --output TEXT               Path where generated files will get saved.
  -e, --enumerate-output          Enumerates output file names instead of
                                  using original names.
  -z, --zip-output                Add generated output to zip archive.
  -bg, --background-color INTEGER...
                                  RGB color code used to fill up background.
                                  Used when padding and / or deskewing.
                                  [default: 255, 255, 255]
  --background-mode [median|mean|dominant]
                                  Color calc mode to fill up background
                                  (overwrites -bg / --background-color).
  -p, --padding INTEGER...        Padding in pixels around the line image
                                  cutout (top, bottom, left, right).
                                  [default: 0, 0, 0, 0]
  -ad, --auto-deskew              Automatically deskew extracted line images
                                  using a custom algorithm (Experimental!).
  -d, --deskew FLOAT              Angle for manual clockwise rotation of the
                                  line images.  [default: 0.0]
  -gt, --gt-index INTEGER         Index of the TextEquiv elements containing
                                  ground truth.  [default: 0]
  -pred, --pred-index INTEGER     Index of the TextEquiv elements containing
                                  predicted text.  [default: 1]
  --help                          Show this message and exit.
```

##### Examples
Only extract `TextLine` elements:
```
pagetools extract <Path/to/xml/files>/*.xml -ie <img_extension> -o <Path/to/output/dir> --include TextLine --exclude "*"
```

Pay in mind that --include / --exclude currently work different from e.g. the same arguments in `rsync` (due to limitations with the `click` library). Inclusion of certain element types always trumps exclusion of the same type, regardless of the order in the call.

#### line2page
Merges line images with corresponding text-files in page-images and page-xml

```
Usage: pagetools line2page [OPTIONS]

  Merges line images and line texts into combined images and XML files

Options:
  -c, --creator TEXT              Creator tag for PAGE XML  [default:
                                  PAGETools]
  -s, --source-folder TEXT        Path to images and GT  [required]
  -i, --image-folder TEXT         Path to images  [default: ]
  -gt, --gt-folder TEXT           Path to GT  [default: ]
  -d, --dest-folder TEXT          Path where output gets stored  [default:
                                  /home/ocr4all/merged]
  -e, --ext TEXT                  Image extension  [default: .bin.png]
  -p, --pred                      Sets flag to also include .pred.txt
                                  [default: False]
  -l, --lines INTEGER RANGE       Lines per page  [default: 20;x>=0]
  -ls, --line-spacing INTEGER RANGE
                                  Spacing between lines (in pixel)  [default:
                                  5;x>=0]
  -b, --border INTEGER RANGE...   Border (in pixel): TOP BOTTOM LEFT RIGHT
                                  [default: 10, 10, 10, 10;x>=0]
  --debug [10|20|30|40|50]        Sets the level of feedback to receive:
                                  DEBUG=10, INFO=20, WARNING=30, ERROR=40,
                                  CRITICAL=50  [default: 20]
  --threads INTEGER RANGE         Thread count to be used  [default: 16;x>=1]
  --xml-schema [2017|2019]        Sets the year of the xml-Schema to be used
                                  [default: 2019]
  --help                          Show this message and exit.
```

Please note that each image file has to have the same name as its Ground Truth file.
```
foo.nrm.png -> foo.gt.txt (& foo.pred.txt)
bar.bin.png -> bar.gt.txt (& bar.pred.txt)
```

#### Regularization
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
#### Change index
```
Usage: pagetools change-index [OPTIONS] XMLS... SOURCE TARGET

  Change index on TextEquiv elements.

Options:
  -s, --safe / -us, --unsafe  Creates backups of original files before
                              overwriting.
  --help                      Show this message and exit.
```
### Analytics
#### Get Codec
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
### Get text count
```
Usage: pagetools get-text-count [OPTIONS] FILES...

  Returns the amount of text equiv elements in certain elements for certain
  indices.

Options:
  -e, --element [TextRegion|TextLine|Word]
  -i, --index TEXT                [required]
  -so, --stats-out TEXT           Output directory for detailed stats csv
                                  file.
  --help                          Show this message and exit.

```
