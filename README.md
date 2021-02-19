# PAGETools - WIP
Small collection of [PAGE XML](https://github.com/PRImA-Research-Lab/PAGE-XML) related Python scripts.

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

### Extraction
```
Usage: pagetools extract [OPTIONS] XMLS...

  Extract elements as image (optionally with text) files.

Options:
  --include [TextRegion|ImageRegion|LineDrawingRegion|GraphicRegion|TableRegion|ChartRegion|MapRegion|SeparatorRegion|MathsRegion|ChemRegion|MusicRegion|AdvertRegion|NoiseRegion|NoiseRegion|UnknownRegion|CustomRegion|TextLine|*]
                                  PAGE XML element types to extract (highest
                                  priority).

  --exclude [TextRegion|ImageRegion|LineDrawingRegion|GraphicRegion|TableRegion|ChartRegion|MapRegion|SeparatorRegion|MathsRegion|ChemRegion|MusicRegion|AdvertRegion|NoiseRegion|NoiseRegion|UnknownRegion|CustomRegion|TextLine|*]
                                  PAGE XML element types to exclude from
                                  extraction (lowest priority)

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

### 

### Regularization
```
Usage: pagetools regularize [OPTIONS] XMLS...

  Regularize the text content of PAGE XML files using custom rulesets.

Options:
  -r, --rules PATH            File(s) which contains serialized ruleset.
  -s, --safe / -us, --unsafe  Creates backups of original files before
                              overwriting.

  --help                      Show this message and exit.

```
