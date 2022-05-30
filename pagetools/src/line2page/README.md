# line2page
Merges line images with corresponding textfiles to page images and pagexml

# Usage

```
# pagetools line2page --help

Usage: pagetools line2page [OPTIONS]

  Merges line images and text to a combined image with a corresponding XML-
  File

Options:
  -c, --creator TEXT              Creator tag for PAGE XML
  -s, --source-folder TEXT        Path to images and GT  [required]
  -i, --image-folder TEXT         Path to images
  -gt, --gt-folder TEXT           Path to GT
  -d, --dest-folder TEXT          Path to merge objects
  -e, --ext TEXT                  Image extension
  -p, --pred BOOLEAN              Set flag to also store .pred.txt
  -l, --lines INTEGER RANGE       Lines per page
  -ls, --line-spacing INTEGER RANGE
                                  Spacing between lines in pixel
  -b, --border INTEGER RANGE...   Border in pixel: top bottom left right
  --debug [10|20|30|40|50]        Sets the level of feedback to receive:
                                  DEBUG=10, INFO=20, WARNING=30, ERROR=40,
                                  CRITICAL=50
  --threads INTEGER RANGE         Thread count to be used
  --xml-schema [17|19]            Sets the year of the xml-Schema to be used
  --help                          Show this message and exit.

```

#### File Names
Please note that each image file has to have the same name as its Ground Truth file.
```
foo.nrm.png --> foo.gt.txt (& foo.pred.txt)
bar.bin.png --> bar.gt.txt (& bar.pred.txt)
```

# ZPD
Developed at [Zentrum für Philologie und Digitalität](https://www.uni-wuerzburg.de/en/zpd/startseite/) at the [Julius-Maximilians-Universität of Würzburg](https://www.uni-wuerzburg.de/en/home/)
