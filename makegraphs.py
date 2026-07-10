#!/usr/bin/python
import matplotlib.pyplot as plt
from index import filterdict
template= open('template.html').read()
from dictcreate import dictionary
import cgi
import io
import base64
import cgitb
cgitb.enable
years=['195','196','197','198','199','200','201']
decades=['1950s','1960s','1970s','1980s','1990s','2000s','2010s']
def make_img():
    buffer=io.BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_code=base64.b64encode(buffer.read()).decode('utf-8')
    html=f'<img src="data:image/png;base64,{image_code}">'
    return html
def makesearchform(currentkeyword='', currenttype='genre'):
    selectedyear = selectedgenre = ''
    if currenttype == 'year':
        selectedyear = 'selected'
    else:
        selectedgenre = 'selected'
    
    html = f'''
    <form action="makegraphs.py" method="GET" style="margin-bottom: 20px;">
        <label for="searchtype">Sort Data by Graphing </label>
        <select id="searchtype" name="type" style="margin-right: 5px;">
            <option value="year" {selectedyear}>Year/Decade</option>
            <option value="genre" {selectedgenre}>Genre</option>
        </select>
        <input type="submit" name="cho`ose" value="Choose">
    </form>
    '''
    if currenttype == 'genre':
        html+=f'''
        <form action="makegraphs.py" method="GET" style="margin-bottom: 20px;">
            <input type="hidden" name="type" value="genre">
            <label for="search"> Compare distributions of genres: </label>
            <input type="text" id="search" name="keyword" value="{currentkeyword}" placeholder="e.g. rock,rap...">
            <input type="submit" value="Search">
        </form>'''
        html+='''
         <a href="./makegraphs.py" style="margin-left: 10px;">Clear</a>'''
    return html
def plotdata (g,d,index):
    numbs=[]
    for value in g:
        numbs.append(len(filterdict(value,d,index)))
    return numbs
def generate_html(title, css, mainh, misch,graph_html, navbar, currentkeyword='', currenttype='genre'):
    html = template
    html = html.replace('CSS_LINK', css)
    
    if not title:
        headingtext = 'Top 500 Albums of All Time Graphed'
    elif currenttype == 'year':
        headingtext = 'Top 500 Albums of All Time by Decade'
    else:
        headingtext = 'Top 500 Albums Sorted by Genre'
    
    html = html.replace('NAV_BAR', navbar)
    html = html.replace('PAGE_TITLE', headingtext)
    html = html.replace('MAIN_HEADING', headingtext)
    html = html.replace('MISC_HEADING', f'{misch}')
    bodycontent = makesearchform(currentkeyword, currenttype) + graph_html
    html = html.replace('ELEMENTS', bodycontent)
    return html

#making the graphs
data=cgi.FieldStorage()
current_type=data.getfirst('type','genre')
keyword=data.getfirst('keyword','').strip().lower()
if current_type =='genre':
    genres_input=[]
    for g in keyword.split(','):
        g=g.strip()
        if g !='':
            genres_input.append(g)
    if not genres_input:
        graph_html='<p> Please enter a list of genres like: "rock, jazz, pop"</p>'
    else:
        counts=[]
        plt.figure()
        for g in genres_input:
            counts.append(len(filterdict(g,dictionary,4)))
        plt.bar(genres_input,counts)
        plt.xlabel('Genres')
        plt.ylabel('Number of Albums')
        plt.title(f'The Top 500 Albums sorted by Genre')
        graph_html=make_img()
        plt.close()
else:
    ydata=plotdata(years,dictionary,1)
    plt.figure()
    plt.bar(decades,ydata)
    plt.xlabel('Decade')
    plt.ylabel('Number of Albums')
    plt.title('Top 500 Albums by Decade')
    graph_html=make_img()
    plt.close()

navbar = f'''<nav>
      <ul>
        <li><a href="index.html" class="navlink">Home</a></li>
        <li><a href="index.py" class="navlink">Top 500 Albums Chart</a></li>
        <li class="current"><a href="makegraphs.py" class="navlink">Graphing</a></li>
      </ul>
    </nav>'''


html=generate_html('','p2styles.css','','Distribution of Albums',graph_html,navbar,keyword,current_type)
print(html)