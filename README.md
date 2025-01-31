# phrase-craze

Source of Dutch sentences: https://wortschatz.uni-leipzig.de/en/download/Dutch

Load initial data:
```
rm db.sqlite3 && python manage.py migrate && python manage.py loaddata quiz/fixtures/initial.yaml
```

Load sentences and generate near matches:
```
python3 manage.py import_question quiz/data/sentences.csv
python3 manage.py near_matches
```