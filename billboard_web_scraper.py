from bs4 import BeautifulSoup as bs
import requests

def top_songs():
    '''
    Scrapes Billboard website to gather the top songs of this decade and writes them to csv.
    '''
    year_start = 2010
    
    artist = []
    title=[]
    years=[]
    
    while year_start < 2019:

        url = f"https://www.billboard.com/charts/year-end/{year_start}/hot-r-and-and-b-hip-hop-songs"

        request = requests.get(url).text
        soup = bs(request, 'html.parser')

        # Get all song titles
        song_titles = soup.findAll("div", {"class": "ye-chart-item__title"})
        song_titles = [title.text.strip().replace(",", " ") for title in song_titles]
        title+=song_titles
        
        # Get all artist names
        artist_names = soup.findAll("div", {"class": "ye-chart-item__artist"})
        artist_names = [artist.text.strip().replace(",", " ") for artist in artist_names]
        artist+=artist_names
        
        # Make a list of years to correspond. Makes for better filtering in pandas.
        year=[year_start for i in range(len(artist_names))]
        years+=year

        year_start+=1
        
    with open(f'top_100_hip_hop.csv','w') as f:
        f.write('year,artist,song\n')
        for y,a,t in zip(years,artist,title):
            print(f"Writing {a},{t} to csv for {y}...")
            f.write(f'{y},{a},{t}\n')

if __name__=="__main__":
    top_songs()



        # url = f"https://www.billboard.com/charts/year-end/{year_start}/hot-dance-electronic--songs"
        # url = f"https://www.billboard.com/charts/year-end/{year_start}/hot-100-songs"
        # url = f"https://www.billboard.com/charts/year-end/{year_start}/hot-100-songs"