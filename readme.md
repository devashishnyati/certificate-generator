Install Python
https://docs.anaconda.com/anaconda/install/

pip install -r requirements.txt


python create_cert.py

- Award.csv should be present in the directory where create_cert.py is present
- image name should be exactly same as the employee name in the csv file + .jpeg
- All the fields in recognition text are coming from Awards.csv file

`rec_text = 'Performer of the year 2019-20 ' + j['CATEGORY'] + ' ' + j['Product'] + ' as ' + j['DESIGNATION'] + ' under category of ' + j['TROPHY TYPE']`



# Format for the file Award.csv: 
`S.NO,EMPLOYEE NAME,DESIGNATION,TROPHY TYPE,CATEGORY,Product`

`1,XYZ,Relationship Manager,CMD,B2C Sales,Life Insurrance`

`2,ABC,Relationship Manager,Director,B2C Sales,Life Insurrance `

