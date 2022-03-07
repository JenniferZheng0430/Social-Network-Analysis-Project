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
header = ['name', 'division', 'title', 'education', 'email', 'Research Areas', 'image']

for fac in facs:
    links.append(DOMAIN + fac.find("span",{"class":"title"}).find("a")['href'])

rows = []
for link in links:
    row = []

    f = requests.get(link)
    soup = BeautifulSoup(f.content, 'html.parser')

    #getting the name
    name = soup.find('h1').text.strip()
    print(name)
    row.append(name)

    # getting the divison info
    aff = soup.find("nav", {"class":"breadcrumbs"})
    ol = aff.find('ol')
    division = ol.contents[7].text
    row.append(division)

    # getting the title
    title = soup.find('span',class_='title').text.replace('"','').strip()
    row.append(title)
    print(title)

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
    # row.append("descrtihsdfsdfih")

    # getting the image link
    img = DOMAIN + soup.find("div", {"class":"responsive-img"}).find("img")['src']
    row.append(img)

    rows.append(row)

with open('faculty.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for row in rows:
        writer.writerow(row)


    

    

    
    
    
    # research_areas = faculty_detail[-3].text[16:]
    # detail = faculty_detail[-2].text+faculty_detail[-1].text
    # print(name)
    # print('')
    # print(division)
    # print('')
    # print(education)
    # print('')
    # print(title)
    # print('')
    # print(email)
    # print('')
    # print(research_areas)
    # print('')
    # print(img)

# for each in faculty_detail:
#     print(each.text)
#     print('---')

# for faculty in faculty_detail:
   
#     research = faculty.find_all('p')[-1].text

#     print(f"name : {name.strip()}")
#     print(f"job_title : {job_title.strip()}")
#     print(f"email : {email.strip()}")
#     print(f"{research.strip()}")
#     print('')