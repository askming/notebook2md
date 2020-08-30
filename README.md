# notebook2md

Python script to clean up new vocabulary saved from online reading using [Saladdict](https://github.com/crimx/ext-saladict) and export to a markdown file.

## Usage
- Put the `notebook.json` file exported from Saladict and the `notebook2md.py` file under the same directory.
- `cd` to the directory where files are saved
- Run the script 
```python
notebook2md.py
```

### Output
1. A markdown file with file name as `YYYY-MM-DD.md`, which is the date the file is generated
2. A `JSON` file with name `notebook_cleaned.json`, which contains four variables from the original `notebook.json` file: `date`, `text`, `trans`, `context` where the `trans` variable has been simplified by removing the translation for `context`. 