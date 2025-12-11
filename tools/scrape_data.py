from  urllib.request import urlopen
from bs4 import BeautifulSoup


base_url = "https://ninlive.com/artists/nin/concerts?year="

gigs=set()

for year in range(1988, 2026):
    print(year)

    html = None
    with urlopen(base_url + str(year)) as response:
        html = response.read()

        soup = BeautifulSoup(html, "html.parser")

        
        for link in soup.find_all('a', href=True):
            lnk = link['href']
            if lnk.startswith("/artists/nin/concerts/"):
                if '#' in lnk: lnk = lnk.split("#")[0]
                gigs.add(lnk.replace("/artists/nin/concerts/", ""))
with open("links.txt", "w+") as fh:       
    for gig in gigs:
        fh.write(f"{gig}\n")
            #    g = gig.replace("/artists/nin/concerts/", "")
            #    with open(f"./gigs/{g}.html", "w") as fh:
            #        with urlopen(f"https://ninlive.com/{gig}", timeout=30) as response:
            #            fh.write(response.read().decode('utf-8'))
      
      