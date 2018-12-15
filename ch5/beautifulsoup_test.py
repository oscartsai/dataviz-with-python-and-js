from bs4 import BeautifulSoup
import requests
import requests_cache

requests_cache.install_cache()

BASE_URL = 'http://en.wikipedia.org'

# Wikipedia will reject our request unless we add
# a 'User-Agent' attribute to our http header.
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_Nobel_soup():
    """ Return a parsed tag tree of our Nobel prize page """

    # Make a request to the Nobel page, setting valid headers
    response = requests.get(
    BASE_URL + '/wiki/List_of_Nobel_laureates', headers=HEADERS)

    # Return the content of the response parsed by BeautifulSoup
    return BeautifulSoup(response.content, 'html.parser')

soup = get_Nobel_soup()
soup.title.string
wikitable = soup.select_one('table.sortable.wikitable')

def get_column_titles(table):
    """ Get the Nobel categories from the table header """

    cols = []
    for th in table.select_one('tr').select('th')[1:]:
        link = th.select_one('a')
        # Store the category name and any Wikipedia link it has
        if link:
            cols.append({
                'name': link.text,
                'href': link.attrs['href']
                })
        else:
            cols.append({'name': th.text, 'href': None})
    return cols

get_column_titles(wikitable)

def get_Nobel_winners(table):
    cols = get_column_titles(table)
    winners = []
    for row in table.select('tr')[1:-1]:
        year = int(row.select_one('td').contents[0])  # Gets 1st <td>
        for i, td in enumerate(row.select('td')[1:]):
            for winner in td.select('a'):
                href = winner.attrs['href']
                if not href.startswith('#endnote'):
                    winners.append({
                        'year': year,
                        'category': cols[i]['name'],
                        'name': winner.text,
                        'link': winner.attrs['href']
                    })
    return winners

winners = get_Nobel_winners(wikitable)

def get_winner_nationality(w):
    """ scrape biographic data from the winner's wikipedia page """
    data = requests.get('http://en.wikipedia.org' + w['link'])
    soup = BeautifulSoup(data.content, 'html.parser')
    person_data = {'name': w['name']}
    attr_rows = soup.select('table.infobox tr')
    for tr in attr_rows:
        try:
            attribute = tr.select_one('th').text
            if attribute == 'Nationality':
                person_data[attribute] = tr.select_one('td').text
        except AttributeError:
            pass
    return person_data

wdata = []
# test first 50 winners
for w in winners[:50]:
    wdata.append(get_winner_nationality(w))

missing_nationality = []
for w in wdata:
    # if missing 'Nationality' add to list
    if not w.get('Nationality'):
        missing_nationality.append(w)
# output list
print(missing_nationality)