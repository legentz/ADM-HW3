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

Here you can download the generated [.tsv](https://drive.google.com/file/d/1T0Wku_IY0qVWo21s3J2fghfsBMj0gJPz/view?usp=sharing).

## Save/Load
The CSV2Dict class is able to load previously generated data stored in store folder (store.pkl) to speed up the execution. Only for the first run, due to the significant amount of tsv files, you'd need to download the tsv.zip and extract the content in the data/tsv folder. That should be done in order to 'load':

```python
# wrapper for csv processing

# 1. dataset => is the dataset we're using
# 2. quotechar and delimiter are two csv reader prefs
# 3. splittsv => if None, any .tsv will be created; otherwise, for each line of the .csv a .tsv file will be 
#    created in the provided folder (tsv_dir)
# 4. topickle => is a tuple containing the method (load or save) and the folder where to store/read a pickle file

csv2dict = CSV2Dict(dataset, delimiter=',', quotechar='"', splittsv=tsv_dir, topickle=('load', pickle_location))
data = csv2dict.init()
``` 

If you whish to proceed from scratch (save option):

```python
# wrapper for csv processing
# ...

csv2dict = CSV2Dict(dataset, delimiter=',', quotechar='"', splittsv=tsv_dir, topickle=('save', pickle_location))
data = csv2dict.init()
``` 

The new store.pkl will be store under data/store/ and all tsv files will be generated under data/tsv/, so you won't need to download them. 
