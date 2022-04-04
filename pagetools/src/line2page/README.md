# line2page
Merges line images with corresponding textfiles to page images and pagexml

# Usage

```
# python3 line2page.py -h

usage: line2page.py [-h] [-s SOURCE_PATH] [-i IMAGE_PATH] [-gt GT_PATH] [-d DEST_PATH] [-e IMG_EXT] [-p] [-l LINES]
                    [-ls SPACING] [-b BORDER] [--debug]

python script to merge GT lines to page images and xml

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE_PATH, --source-folder SOURCE_PATH
                        Path to images and GT
  -i IMAGE_PATH, --images-folder IMAGE_PATH
                        Path to images
  -gt GT_PATH, --gt-folder GT_PATH
                        Path to GT
  -d DEST_PATH, --dest-folder DEST_PATH
                        Path to merge objects
  -e IMG_EXT, --ext IMG_EXT
                        image extension
  -p, --pred            Set Flag to also store .pred.txt
  -l LINES, --lines LINES
                        lines per page
  -ls SPACING, --line-spacing SPACING
                        line spacing
  -b BORDER, --border BORDER
                        border in px
  --debug               prints debug xml
```

#### File Names
Please note that each image file has to have the same name as its Ground Truth file.
```
foo.nrm.png --> foo.gt.txt (& foo.pred.txt)
bar.bin.png --> bar.gt.txt (& bar.pred.txt)
```

# ZPD
Developed at [Zentrum für Philologie und Digitalität](https://www.uni-wuerzburg.de/en/zpd/startseite/) at the [Julius-Maximilians-Universität of Würzburg](https://www.uni-wuerzburg.de/en/home/)
