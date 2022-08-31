import os
import requests
import gzip
import shutil

# Downloads data sets from IMDB
# NOTE: Data needs to be cleansed before passing on
def downloadDataSet(files):
    blank_url='https://datasets.imdbws.com/'
    for file in files:
        url = blank_url + file + '.tsv.gz'
        r = requests.get(url,stream=True)
        with open(file+'.tsv.gz','wb') as f:
            for chunk in r.raw.stream(1024,decode_content=False):
                if chunk:
                    f.write(chunk)
        with gzip.open(file+'.tsv.gz','rb') as fin:
            with open(file+'.tsv','wb') as fout:
                shutil.copyfileobj(fin,fout)
        os.remove(file+'.tsv.gz')

# Reads original files previously downloaded from IMDB
# Parses files during cleanse
def readOriginalFile(file,data):
    myDict = {}
    approvedTypes = ['Comedy', 'Romance', 'Animation', 'Drama', 'Fantasy', 'Horror', 'Biography', 'Music', 'War',
                     'Crime', 'Western', 'Family', 'Adventure', 'Action', 'History', 'Mystery', 'Sci-Fi', 'Musical',
                     'Thriller', 'Film-Noir']
    print('Reading '+file)
    f = open(file,'r',encoding='utf-8')
    f.readline()
    while True:
        line = f.readline().strip()
        if not line: break
        spl = line.split('\t')
        if file=='title.akas.tsv':
            if spl[3]=='US':
                myDict[spl[0]]=''
        elif file=='title.basics.tsv':
            # Us Only, movie or tv movie that is not a porn
            if spl[0] in data.keys() and (spl[1]=='movie' or spl[1]=='tvMovie') and spl[4]=='0':
                strYr = spl[5]
                try:
                    yr = int(strYr)
                except:
                    yr = 1900
                if yr>=1980:
                    temp = spl[8].split(',')
                    remove_title = False
                    for t in temp:
                        # checks if all categories listed are approved types of categories
                        if t not in approvedTypes:
                            remove_title=True
                    if not remove_title:
                        myDict[spl[0]]=spl[2]+'\t'+spl[5]+'\t'+spl[7]+'\t'+spl[8]
        elif file=='name.basics.tsv':
            myDict[spl[0]]=spl[1]+'\t'+spl[2]+'\t'+spl[3]
    f.close()
    return myDict

# Used prior to actual development to confirm what categories there are
# Output: File with all types of categories.  Narrowed down for data cleanse
def getAllTypes():
    types = {}
    f = open('title.basics.tsv','r',encoding='utf-8')
    f.readline()
    while True:
        line = f.readline().strip()
        if not line: break
        spl = line.split('\t')
        temp = spl[8].split(',')
        for t in temp:
            if t not in types.keys():
                types[t]=t
    f.close()
    return types

def cleanseNames():
    names = readOriginalFile('name.basics.tsv',{})
    writeDictionaryToFile(names,'actors.tsv')

# Once titles cleansed to us only after 1979, non-porn, of particular categories
# Writes these movies to movies.tsv OR
# Once names are cleansed, writes to actors.tsv
def writeDictionaryToFile(myDict,file):
    print('Writing '+file)
    f = open(file,'w',encoding='utf-8')
    for k,v in myDict.items():
        f.write(k+'\t'+v+'\n')
    f.close()

# Cleanses title.akas.tsv and title.basics.tsv into one file
# simply called movies
def titleCleanse():
    usOnly = readOriginalFile('title.akas.tsv',{})
    movies = readOriginalFile('title.basics.tsv',usOnly)
    writeDictionaryToFile(movies,'movies.tsv')

def main():
    if not os.path.isfile('name.basics.tsv') or not os.path.isfile('title.akas.tsv') or not os.path.isfile('title.basics.tsv'):
        downloadDataSet(['name.basics','title.basics','title.akas'])
    titleCleanse()
    cleanseNames()

if __name__=='__main__':
    main()