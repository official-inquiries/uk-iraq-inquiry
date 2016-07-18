To extract the text, we did the following:

1. Installed pdfminer
2. Ran the following:

  ```
  pdf2txt.py -o executive-summary.txt "the-report-of-the-iraq-inquiry_executive-summary.pdf"
  ```
  
To tidy up text for markdown run the following command from main direcotory:

  ```
  python scripts/process.py -i <inputfile> -o <outputfile>
  
  # e.g.
  python scripts/process.py -i test/data/executive-summary.txt -o test/data/test.md
  ```
