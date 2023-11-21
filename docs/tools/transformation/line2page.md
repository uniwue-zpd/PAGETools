# Line2Page
## Usage
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

## Example 
::: info
TODO
:::

## Info
Please note that each image file has to have the same name as its Ground Truth file.
```
foo.nrm.png -> foo.gt.txt (& foo.pred.txt)
bar.bin.png -> bar.gt.txt (& bar.pred.txt)
```