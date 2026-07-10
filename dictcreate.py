text = open('albumdata.csv').read()

def sortdata(txt):
    d = {}
    albums = txt.split('\n')[1:]
    for music in albums:
        if music.strip(): 
            x = music.split(',')
            album = x[0].strip('"')
            info = []
            for item in x[1:5]:
                info.append(item.strip('"'))
            genrestring = ''
            for item in x[5:]:
                genrestring += f'{item.lower()}, '
            genrestring = genrestring[:-2].strip('"')
            info.append(genrestring)
            d[album] = info
    return d

dictionary = sortdata(text)
