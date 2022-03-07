from bs4 import BeautifulSoup
import requests
import csv

DOMAIN = 'https://nyuad.nyu.edu'
URL = 'https://nyuad.nyu.edu/en/academics/faculty.html'

r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html.parser')
facs = soup.findAll("div", {"class":"faculty-container"})
links = []

# add the description later
header = ['name', 'division', 'title', 'education', 'email', 'Research Areas', 'description', 'image']

for fac in facs:
    links.append(DOMAIN + fac.find("span",{"class":"title"}).find("a")['href'])

counter = 1

rows = []
for link in links[:3]:
    row = []

    f = requests.get(link)
    soup = BeautifulSoup(f.content, 'html.parser')

    #getting the name
    name = soup.find('h1').text.strip()
    print(name, counter)
    counter += 1
    row.append(name)

    # getting the divison info
    aff = soup.find("nav", {"class":"breadcrumbs"})
    ol = aff.find('ol')
    division = ol.contents[7].text
    row.append(division)

    # getting the title
    title = soup.find('span',class_='title').text.replace('"','').strip()
    row.append(title)

    # getting the education info
    last = len(soup.find("p", {"class":"affiliation"}).contents)-1
    ed = soup.find("p", {"class":"affiliation"}).contents[last]
    ed = ed if ed else "NA"
    ed = ed.strip().replace('\"','')
    # ed = '"'+ed+'"'
    # print(type(ed))
    row.append(ed)

    #getting the email
    email = soup.find('a',itemprop = 'email').text
    row.append(email)

    #getting the research areas
    ra = soup.find("div", {"class":"research-areas"})
    ra = ra.contents[-2].text.strip()[16:].replace('"','') if ra else "NA"
    row.append(ra)

    #getting the description
    all_desc = ""
    desc = soup.find('hr').next_siblings
    
    for de in desc:
        print(de.contents)
        if de.name == "p":
            all_desc += de.text.replace('\n','').strip()
        elif de.name =="div":
            break
    # print(all_desc)
    row.append(all_desc.strip())
    print('\n')

    # getting the image link
    img = DOMAIN + soup.find("div", {"class":"responsive-img"}).find("img")['src']
    row.append(img)

    rows.append(row)

with open('all_faculty_data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for row in rows:
        writer.writerow(row)