# PAGETools - WIP
Small collection of [PAGE XML](https://github.com/PRImA-Research-Lab/PAGE-XML) related Python scripts.

## Installing
### pip
```bash
python -m venv VENV_NAME
source VENV_NAME/bin/activate
pip install pagetools
```

```bash
pip install pagetools
```

### Install from source
```bash
python setup.py install
```

## Usage

### Line extraction
```
Usage: pagetools-extract-lines [OPTIONS] [XMLS]...

Options:
  -ie, --image-extension TEXT     Extension of image files (must be in the
                                  same directory as XML files to be
                                  considered).

  -o, --output TEXT               Path where generated files will get stored.
  -e, --enumerate-output          Enumerates output file names instead of
                                  using original names.

  -z, --zip-output                Add output to zip archive.
  -bg, --background-color INTEGER...
                                  RGB color code used to fill up background.
                                  Used when padding and / or deskewing.

  --background-mode [median|mean|dominant]
                                  Color calc mode to fill up background
                                  (overwrites -bg / --background-color).

  -p, --padding INTEGER...        Padding in pixels around the line image
                                  cutout (top, bottom, left, right).

  -ad, --auto-deskew              Autodeskew extracted line images
                                  (Experimental!).

  -d, --deskew FLOAT              Angle for manuel clockwise rotation of the
                                  line images.

  -gt, --gt-index INTEGER         Index of the TextEquiv elements containing
                                  ground truth.

  -pred, --pred-index INTEGER     Index of the TextEquiv elements containing
                                  predicted text.

  --help                          Show this message and exit.

```
