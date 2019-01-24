from bs4 import BeautifulSoup as bs
import requests

def billboard_top_songs(genre,endpoint):
    '''
    Scrapes Billboard website to gather the top songs of this decade and writes them to csv.
    '''
    start_year = 2010
    
    artist = []
    title=[]
    years=[]
    
    while start_year < 2019:

        url = f"https://www.billboard.com/charts/year-end/{start_year}/{endpoint}"

        request = requests.get(url)

        if request:
            soup = bs(request.text, 'html.parser')

            # Get all song titles
            song_titles = soup.findAll("div", {"class": "ye-chart-item__title"})
            song_titles = [title.text.strip().replace(",", " ") for title in song_titles]
            title+=song_titles
            
            # Get all artist names
            artist_names = soup.findAll("div", {"class": "ye-chart-item__artist"})
            artist_names = [artist.text.strip().replace(",", " ") for artist in artist_names]
            artist+=artist_names
            
            # Make a list of years to correspond. Makes for better filtering in pandas.
            year=[start_year for i in range(len(artist_names))]
            years+=year

            start_year+=1
        else:
            # Account for invalid inputs.
            request.raise_for_status()
    
    # Refactoring to include genre.
    with open(f'top_100_{genre}.csv','w') as f:
        f.write('year,artist,song\n')
        for y,a,t in zip(years,artist,title):
            print(f"Writing {a},{t} to csv for {y}...")
            f.write(f'{y},{a},{t}\n')

if __name__=="__main__":
    billboard_top_songs('test','dfdlffd')

        # url = f"https://www.billboard.com/charts/year-end/{year}/hot-dance-electronic--songs"
        # url = f"https://www.billboard.com/charts/year-end/{year}/hot-100-songs"
        # url = f"https://www.billboard.com/charts/year-end/{year}/hot-100-songs"