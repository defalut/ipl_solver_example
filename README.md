IPL solver written in Python

## Run server

    export FLASK_APP=solver_app.py
    python -m flask run


## Query server

By opening test [page](http://127.0.0.1:5000/solve) with default data.

Or by posting your own data in json format:

    python post_json.py [FILENAME]

## Sample JSON input

```json
{
  "offers": ["A", "B", "C", "D", "E"],
  "customers": ["1", "2", "3"],
  "matrix": [
    [10, 20, 30, 4, 7],
    [25, 15, 5, 23, 6],
    [10, 9, 9, 2, 5]
  ],
  "constraints": {
    "max_offer_per_customer": 2,
    "max_total_offers": 5,
    "min_offers": {"C": 1, "E": 2},
    "max_offers": {"A": 2},
    "conflicts": [["A", "B"], ["C", "E"], ["C", "B"]]
  }
}
```