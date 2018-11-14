# ADM-HW3
#3 Homework of ADM within the MSc in Data Science @ La Sapienza University

## Data
As being said by the professor, multiple .tsv files have to be created from the dataset 'Airbnb_Texas_Rentals.csv'.

* Dealing with different files it's an important task in Data Mining. For this purpose, create a `.tsv` file for each record of the dataset. The content of the file should be the following:

    ```
    average_rate_per_night \t  bedrooms_count \t city \t date_of_listing \t description \t latitude\t longitude \t title \t url
    ```
   
    __Example__:
  
    ```
    20$      4       Humble     May 2016        stylish and beautiful apartment etc etc..      40.2        17.02       River house        www.airbnb.com/19281 
    ```
   
__Note__ that in a .tsv file, each column is separated by the `tab`.
* Store the documents in a directory with inside one file per house review. You should name each file as `doc_i.tsv` where `i` is the dataframe index the document.

We can achieve this task through this Python script:

```python
with open('Airbnb_Texas_Rentals.csv', 'r') as csv:
    for i, line in enumerate(csv):
    
        # skip the first line as we're dealing with a .csv
        if i == 0: continue
        
        # parsing data and taking the index that has to be part of filenames
        elems = list(map(lambda x: x.replace('"', ''), line.rstrip('\n').split(',')))
        index = elems[0]
        
        # put .tsv files into 'tsv' folder (that already has to exist)
        with open('tsv/doc_' + index + '.tsv', 'w') as doc_out:
            doc_out.write('\t'.join(elems[1:]))
```

Here you can download the generated [.tsv](https://drive.google.com/file/d/1T0Wku_IY0qVWo21s3J2fghfsBMj0gJPz/view?usp=sharing).
*Please, do not share with anyone.*
