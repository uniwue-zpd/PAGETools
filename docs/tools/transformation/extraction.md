# Extraction
## Usage
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

## Example
Only extract `TextLine` elements:
```
pagetools extract <Path/to/xml/files>/*.xml -ie <img_extension> -o <Path/to/output/dir> --include TextLine --exclude "*"
```

## Info
Pay in mind that --include / --exclude currently work different from e.g. the same arguments in `rsync` (due to limitations with the `click` library). Inclusion of certain element types always trumps exclusion of the same type, regardless of the order in the call.