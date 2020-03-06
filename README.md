# nlp-categorize
nlp-categorize is using a natural language analyzer to categorize loose texts
with the help keyword(-chains) into 3 levels of categories.

## Keyword-file-structure

The keyword file-structure must be a CSV file (export for LibreOffice for example):
With the following strucutre:

```CSV
category-level1, category-level2, category-level3, keyword(s), keyword(s), ..., keyword(s)
```

E.g.:

```CSV
Technology,IT,Web Programming,php,js,javascript
Technology,IT,Low-Level C Programming,c compiler,linux kernel
Technology,IT,Programmer,programmer,compiler,programming
```

(*Note*: Here "c compiler" (or linux kernel) is a keyword-chain. As match only
count if both words are present and the natural-language analyzer sees them in
a direct relation)

The file must stored as `keywords.csv` in the directory where the script is run.

## Data input structure

As a CSV-file as well. Just one column per line, containing the text to be analyzed.

```CSV
"I like programming, C++ and C. I love the Linux Kernel.
```

Would match the 'Technology -> IT -> Low-Level C Programming' and 'Technology
IT Programmer' categories.

## Output structure

For the moment a simple output, again in a CSV format, is generated:

```CSV
Orignal Text, Match_CAT0, Match_CAT1, ..., CATN, detail cat, ...
```

The aggregated first column of the keywords-file is considered the _main_ column. The
above example would produce:

```CSV
text,Technology
"I like programming, C++ and C. I love the Linux Kernel.",1,IT - Low-Level C Programming, IT - Programmer
```
## Languages

By default a French language package is used (`fr_core_news_sm`).

Keywords must be in their infinitif and masculin-form. For exmaple, *permis
conduire* becomes *permettre conduire* or *realisatrice* has to be stored (and
will be referenced) as *realisateur*. When using the output, be careful to get back
the raw text to check the original gender.

## Step-by-step install and first run

You need a working python3 environment on your PC/MAC.

On MAC, refer to (this guide)[https://docs.python-guide.org/starting/install3/osx/]. The section
*Doing it right* should be enough. You need `git` as well: `brew install git`

Then git clone this repository to your PC:

```Bash
cd place/to/store/project
git clone https://github.com/pboettch/nlp-categorize.git
```

Install the dependencies:

```Bash
cd nlp-categorize
pip3 install -r requirements.txt
```

Install Spacy's language package
```Bash
python3 -m spacy download fr_core_news_sm
```

Create a `keywords.csv` and an `input.csv` as described above. Then run the script:

```Bash
./nlp-categorize.py
```

It'll take some time and with no furthur printed output, a `output.csv`-file
should have been generated.
