# phrase-craze

Source: https://wortschatz.uni-leipzig.de/en/download/Dutch

Generate database with the following command:
```
python3 manage.py import_question quiz/data/sentences.csv
python3 manage.py near_matches
```