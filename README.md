# TheBest SuperMarket Receipt Analysis

## Project Folder structure

````bash
resources
|-- receipts
|   |--0
|   |  |-- receipt_0.txt
|   |  |-- receipt_1.txt
|   |  ..
|   |  |-- receipt_9999.txt
|   |--1
|   |  |
|   |  ..
|   |  | 
|   `--49
|      |-- receipt_490000.txt
|      |-- receipt_490001.txt
|      ..
|      |
|      `-- receipt_499999.txt
|
|-- explanations
|   |--0
|   |  |-- explanation_0.txt
|   |  |-- explanation_1.txt
|   |  ..
|   |  |-- explanation_9999.txt
|   |--1
|   |  |
|   |  ..
|   |  | 
|   `--49
|      |-- explanation_490000.txt
|      |-- explanation_490001.txt
|      ..
|      |
|      `-- explanation_499999.txt
|
|-- customers_checkpoint
|   |-- NIF_min(nif).csv
|   |
|   ..
|   |-- NIF_max(nif).csv
|
|-- products_checkpoint
|   |--products_0.csv
|   ..
|   |
|   `-- products_49.csv
|       
|
|-- fpgrowth_checkpoint
|   |-- fpgrowth_0.csv
|   ..
|   |
|   `-- fpgrowth_49.csv
|
|-- fpgrowth_final.csv
|
|-- customers_final.json
|
|-- products_final.json
|
|
`-- produtos.txt
| 
src
|-- utils
|   |-- Reader.py
|   |-- Writer.py
|   |-- Parser.py
|   |-- Analyzer.py
|
|-- test.py
````

---

## Input Files Structure

### Products.txt

| Grupo | Nome | Preço | Margem Lucro | Total Prateleiras | Probabilidade Priori |
| :---: | :--- | :---: | :----------: | :---------------: | :------------------: |
| 1 | ARROZ | 2.00 | 10 | 3 | 0.004632 |
| 1 | MASSA | 1.70 | 5 | 3 | 0.008337 |
| ... | ... | ... | ... | ... | ... |
| 24 | TINTA | 20.00 | 16 | 1 | 0.999074 |
| 24 | PINCEIS | 3.00 | 16 | 1 | 1.000000 |

- **Grupo**
  - The product's group or family, an integer.
- **Nome**
  - The product's name, a string.
- **Preço**
  - The product's price, in float.
- **Margem Lucro**
  - The product's margin of profit, an integer (%).
- **Total Prateleiras**
  - The product's available shelfs, an integer.
- **Probabilidade Priori**
  - The product's probability of being in any receipt.

### Receipt_xxxxxx.txt

Receipt files are the core source of information for the supermarket. Receipts hold, in a compact form, information about the customers' spendings.

````bash
+-----------+-------------------+
| NIF       | 123456789         |
| --------- | ----------------- |
| Product 1 | Price(Product 1)  |
| Product 2 | Price(Product 2)  |
|    ...    |        ...        | 
| Product n | Price(Product n)  |
| --------- | ----------------- |
| Total     | Sum(Prices)       |
+-----------+-------------------+
````

Any receipt file can be sectioned in 3:

- **NIF**
  - Representative **unique number** for a customer.
- **Items**
  - Lists every product bought and its' respetive price.
- **Total**
  - The sum of all prices in the product list

### Explanation_xxxxxx.txt

An explanation file holds detailed information about the customers' actions when entering the supermarket. The information is very detailed, but not as compact as in the receipt. Explanation files can be sectioned as in 2:

- **Wish List**:
  - The customers' desired products to obtain from the supermarket.
  - The customers' buying priority starts from the bottom of the wishlist.
- **Customers' thought process**:
  - Looking for $priority\_product$...
  - Nearby there was $non\_priority\_product$ ... I bought.
  - Nearby I looked and liked of $random\_product$. I bought.
  - Found it on (row, col) = $(x,y)$
  - Walking $cell$
  - I bought the product $priority\_product$
  - Walked $steps$. Remaining stamina $remaining\_stamina$
  - I am tired. Enough for me! (stamina $\le$ 0)

## Objectives

- Using a dataset of 500 000 receipts and additional information for each product in an additional file, find supermarket configurations to achieve certain goals - a **configuration is a vector of 222 positions** where **each position** in the vector is the **ID of a product**.
  - Configuration to obtain most profit;
  - Configuration that gets more volume sales.
- Extract support rules for transactions of products. Each receipt is a transaction.
  - Support of 1%;
  - Support of 5%;
  - Support of 10%;
  - Support of 50%.

## Procedures

- [x] Successfully read *products.txt*
- [x] Successfully read *receipts.txt*
- [x] Successfully read *explanations.txt*
- [x] Cross information with products, explanations and receipts
- [x] Created neatly final files
- [x] Query final files
- [x] Do graph out of supermarket
- [x] Get random receipts out of *explanations.txt*
- [x] Get stamina normal distribution
- [ ] Run simulator

### Suggestions

- Try and do a random configuration?
- Insert data in a relational database?
- Create a file for every customer listing receipts?
- List most profitable customers
- List most profitable items
- List most sold products
- Use client routes with explanations
- Heatmap supermarket shelfs, that is, find best shelfs to put items in

### Details to watch out

- Shelfs in the corners of the supermarket are unobtainable.
- Customers have stamina and get tired after walking around the supermarket.

### Rough ideas

```csv
NIF_123456789
receipt_num | total | profit | stamina | wishlist | random | products  |
receipt_123 | 420   | 39     | 240     | [1,4,5]  | [7,8]  | [1,4,5,2] |
```

Possible Client and Product csv?
