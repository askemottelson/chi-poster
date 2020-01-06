Tested with Python 2.7.16

# before you begin
`pip install -r requirements`

You will need to have a database with all (CHI) papers at your disposal; unfortunately I cannot provide this. A dummy implementation is shown in `proceedings.py` that fetches data from a database and pickles it into binary files. Specifically, you will need to implement `get_proceedings` to return a list of `MockPaper` objects, representing your sample's papers.

# make poster
```
python poster.py
```