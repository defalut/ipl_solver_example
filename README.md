IPL solver written in Python

## Run server

    export FLASK_APP=solver_app.py
    python -m flask run


## Query server

By opening test [page](http://127.0.0.1:5000/solve) with default data.

Or by posting your own data in json format:

    python post_json.py [file.json]

## Sample JSON input ...

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

## ... the LP recipe generated by PuLP ...
```
 \* chicken *\
Maximize
cost: 10 x_1_A + 20 x_1_B + 30 x_1_C + 4 x_1_D + 7 x_1_E + 25 x_2_A + 15 x_2_B
 + 5 x_2_C + 23 x_2_D + 6 x_2_E + 10 x_3_A + 9 x_3_B + 9 x_3_C + 2 x_3_D
 + 5 x_3_E
Subject To
A_conflicts_with_B_at_customer_1: x_1_A + x_1_B <= 1
A_conflicts_with_B_at_customer_2: x_2_A + x_2_B <= 1
A_conflicts_with_B_at_customer_3: x_3_A + x_3_B <= 1
B_conflicts_with_C_at_customer_1: x_1_B + x_1_C <= 1
B_conflicts_with_C_at_customer_2: x_2_B + x_2_C <= 1
B_conflicts_with_C_at_customer_3: x_3_B + x_3_C <= 1
C_conflicts_with_E_at_customer_1: x_1_C + x_1_E <= 1
C_conflicts_with_E_at_customer_2: x_2_C + x_2_E <= 1
C_conflicts_with_E_at_customer_3: x_3_C + x_3_E <= 1
max_offer_per_customer_1: x_1_A + x_1_B + x_1_C + x_1_D + x_1_E <= 2
max_offer_per_customer_2: x_2_A + x_2_B + x_2_C + x_2_D + x_2_E <= 2
max_offer_per_customer_3: x_3_A + x_3_B + x_3_C + x_3_D + x_3_E <= 2
max_offers_A: x_1_A + x_2_A + x_3_A <= 2
max_total_offers: x_1_A + x_1_B + x_1_C + x_1_D + x_1_E + x_2_A + x_2_B
 + x_2_C + x_2_D + x_2_E + x_3_A + x_3_B + x_3_C + x_3_D + x_3_E <= 5
min_offers_C: x_1_C + x_2_C + x_3_C >= 1
min_offers_E: x_1_E + x_2_E + x_3_E >= 2
Binaries
x_1_A
x_1_B
x_1_C
x_1_D
x_1_E
x_2_A
x_2_B
x_2_C
x_2_D
x_2_E
x_3_A
x_3_B
x_3_C
x_3_D
x_3_E
End
```

## ... and finally the output!


Result: Optimal!

30.00 + 25.00 + 6.00 + 10.00 + 5.00 = 76.00

<table class="empty">

<thead>

<tr>

<th>°</th>

<th>A</th>

<th>B</th>

<th>C</th>

<th>D</th>

<th>E</th>

</tr>

</thead>

<tbody>

<tr>

<th>1</th>

<td class="empty">10</td>

<td class="empty">20</td>

<th class="empty">30</th>

<td class="empty">4</td>

<td class="empty">7</td>

</tr>

<tr>

<th>2</th>

<th class="empty">25</th>

<td class="empty">15</td>

<td class="empty">5</td>

<td class="empty">23</td>

<th class="empty">6</th>

</tr>

<tr>

<th>3</th>

<th class="empty">10</th>

<td class="empty">9</td>

<td class="empty">9</td>

<td class="empty">2</td>

<th class="empty">5</th>

</tr>

</tbody>

</table>
