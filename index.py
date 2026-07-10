#!/usr/bin/python
print('Content-type: text/html\n')

import cgitb
cgitb.enable()
import cgi
from dictcreate import dictionary
text = open('albumdata.csv').read()
template = open('template.html').read()

# returns dict of all entries where s is in d[index]
def filterdict(s, d, index):
    if not s:
        return d
    newd = {}
    for album in d:
        if s.lower() in str(d[album][index]).lower():
            newd[album] = d[album]
    return newd

# make table html from dict and headings
def table(d, txt):
    html = "<table><tr>"
    head = txt.split('\n')[0].split(',')
    for category in head:
        header = category.strip('"')
        html += f'<th>{header}</th>'
    html += "</tr>"
    for album in d:
        html += "<tr>"
        html += f'<th>{album}</th>'
        for info in d[album]:
            html += f'<td>{info}</td>'
        html += "</tr>"
    html += "</table>"
    return html

# make search form + options dropdown html
# modified from https://github.com/mks22-dw/thesource/blob/main/demos/dynaform.py
def makesearchform(currentkeyword='', currenttype='genre'):
    selectedartist = selectedyear = selectedgenre = ''
    if currenttype == 'artist':
        placeholder = 'e.g. Nirvana, Stevie Wonder...'
        selectedartist = 'selected'
    elif currenttype == 'year':
        placeholder = 'e.g. 1970s, 2015...'
        selectedyear = 'selected'
    elif currenttype == 'genre':
        placeholder = 'e.g. rock, rap...'
        selectedgenre = 'selected'
    else:
        placeholder = 'Search...'
    
    html = f'''
    <form action="" method="GET" style="margin-bottom: 20px;">
        <label for="searchtype">Filter by </label>
        <select id="searchtype" name="type" style="margin-right: 5px;">
            <option value="artist" {selectedartist}>Artist</option>
            <option value="year" {selectedyear}>Year/Decade</option>
            <option value="genre" {selectedgenre}>Genre</option>
        </select>
        <input type="text" id="search" name="keyword" value="{currentkeyword}" placeholder="{placeholder}">
        <input type="submit" value="Search">
        <a href="./index.py" style="margin-left: 10px;">Clear</a>
    </form>
    '''
    return html

# generate full html text
def generate_html(title, css, mainh, misch, element, navbar, currentkeyword='', currenttype='genre'):
    html = template
    html = html.replace('CSS_LINK', css)
    
    if not title:
        headingtext = 'Top 500 Albums of All Time'
    elif currenttype == 'year':
        headingtext = f'Top Albums of {title}'
    else:
        headingtext = f'Top {title.title()} Albums of All Time'

    html = html.replace('NAV_BAR', navbar)
    html = html.replace('PAGE_TITLE', headingtext)
    html = html.replace('MAIN_HEADING', headingtext)
    html = html.replace('MISC_HEADING', f'{misch}')
    bodycontent = makesearchform(currentkeyword, currenttype) + table(element, text)
    html = html.replace('ELEMENTS', bodycontent)
    return html

data = cgi.FieldStorage()

indexmapping = {'artist': 0, 'year': 1, 'genre': 4}
navbar = f'''<nav>
      <ul>
        <li><a href="index.html" class="navlink">Home</a></li>
        <li class="current"><a href="index.py" class="navlink">Top 500 Albums Chart</a></li>
        <li><a href="makegraphs.py" class="navlink">Graphing</a></li>
      </ul>
    </nav>'''

alldatafrom = 'All data from <a href="https://rateyourmusic.com/charts/top/album/all-time/">RYM</a>'

# prints generated html based on different arguments
# modified from https://github.com/mks22-dw/thesource/blob/main/demos/dynaform.py
if __name__=='__main__':
    if len(data) != 0 and 'keyword' in data:
        filtername = data['keyword'].value.strip()
    
        if 'type' in data:
            searchtype = data['type'].value.strip()
        else:
            searchtype = 'genre'
        if searchtype in indexmapping:
            searchindex = indexmapping[searchtype]
        else:
            searchindex = 4
    
        cleanfilter = filtername
        if searchtype == 'year' and filtername.lower()[-1] == 's':
            cleanfilter = filtername[:-2]
        filtereddata = filterdict(cleanfilter, dictionary, searchindex)
        if filtername == '':
            print(generate_html('', 'p2styles.css', '', alldatafrom, dictionary, navbar, '', searchtype))
        else:
            print(generate_html(filtername, 'p2styles.css', filtername, alldatafrom, filtereddata, navbar, filtername, searchtype))
    else:
        print(generate_html('', 'p2styles.css', '', alldatafrom, dictionary, navbar, '', 'genre'))