import time
import bs4
import requests
import csv

SECONDS_INTERVAL = 3

def get_activities(cuit):
    r = requests.get(f'https://www.cuitonline.com/detalle/{cuit}/')
    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    name = soup.find('span', {'itemprop': 'name'})
    person_data = soup.find('div', class_='persona-data')
    activities = person_data.find('li', {'style': 'list-style: none;'}).text.split('#')
    for elem in enumerate(activities):
        idx = elem[0]
        act = elem[1]
        activities[idx] = activities[idx].strip()

    return name.text, activities[1:5]

f = open('cuits.csv', 'r', newline='')
lines = f.readlines()
data = {}

for row in lines[1:]:
    cuit = row.split(',')[2].strip()

    # Remove floating point part...
    until_float = cuit.find('.0')
    cuit = cuit[:until_float]
    name, acts = get_activities(cuit)

    print(f'{name} listo')
    data[name] = [acts, cuit]

    time.sleep(SECONDS_INTERVAL)

out = open('output.csv', 'w')
writer = csv.writer(out)
writer.writerow(['Empresa', 'Actividades', 'CUIT'])
for comp, acts in data.items():
    writer.writerow([comp, acts[0], acts[1]])

