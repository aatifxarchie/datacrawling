import pandas as pd
from bs4 import BeautifulSoup
import requests

# getting the url
url = 'https://openaccess.thecvf.com/ICCV2023?day=all'

# use requests to handle the url request
page = requests.get(url)

# parsing the html using Beautiful Soup
soup = BeautifulSoup(page.text, 'html')

# initiating empty list for titles, pdfs and names
paper_titles = []
pdfs = []
names = []

# the titles are stored in 'dt' tags in the actual webpage
tle = soup.find_all('dt')

for t in tle:
  paper_titles.append(t.text)


# the author names are present inside forms in 'dd' tags in webpage
dd_elements = soup.find_all('dd')

for dd_ele in dd_elements:
  form_elements = dd_ele.find_all('form')
  if form_elements is not None:
    name = []
    for form_ele in form_elements:
      a_element = form_ele.find('a')
      if a_element is not None:
        name.append(a_element.text)
    names.append(name)


author_names = []
for n in names:
  if len(n) > 0:
    author_names.append(n)

new_author_names = []

# concatenating all author names for a particular paper with commas and creating a list
for a_name in author_names:
  all_author = ''
  for a in a_name:
    all_author = all_author + a + ','
  all_author_new = all_author[:len(all_author) - 1]
  new_author_names.append(all_author_new)


# whenever the 'a' tag has text as pdf, it is stored in the pdf list
for dd_ele in dd_elements:
  a_elements = dd_ele.find_all('a')
  if a_elements is not None:
    for a_ele in a_elements:
      if a_ele.text == 'pdf':
        pdf = 'https://openaccess.thecvf.com/' + a_ele['href']
        pdfs.append(pdf)

# creating a DataFrame with the three lists
df = pd.DataFrame({
    'Author Names' : new_author_names,
    'Paper Title' : paper_titles,
    'Paper PDF' : pdfs
})

# Finally saving the DataFrame with a desired name
df.to_csv('iccv23openaccess.csv')

