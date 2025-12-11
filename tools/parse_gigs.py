import os
from bs4 import BeautifulSoup

from hashlib import md5
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import FOAF

EX = Namespace("http://example.org/")

files = os.listdir('gigs')

tapes = set()
mics = set()
vs = set()
tour = set()
for file in files:
    with open(f"gigs/{file}", "r") as fh:
        soup = BeautifulSoup(fh.read(), "html.parser")
        for link in soup.find_all('a', href=True):
            if link['href'].startswith("/recordings?microphone_type"):
                mics.add(link.text.strip())
            elif link['href'].startswith("/recordings?taper_name"):
                tapes.add(link.text.strip())
            elif link['href'].startswith("/artists/nin/venues/"):
                vs.add(link.text.strip())
            elif link['href'].startswith("/artists/nin/tours/"):
                tour.add(link.text.strip())


g = Graph()

tapers = {}
for t in tapes:
    turl = md5(t.encode('utf-8')).hexdigest()
    tapers[t] = turl
    g.add( (URIRef(turl), FOAF.name, Literal(t)) )

microphones = {}
for t in mics:
    murl = md5(t.encode('utf-8')).hexdigest()
    microphones[t] = murl
    g.add( (URIRef(murl), EX.microphonename, Literal(t)) )

venues = {}
for t in vs:
    murl = md5(t.encode('utf-8')).hexdigest()
    venues[t] = murl
    g.add( (URIRef(murl), EX.venuename, Literal(t)) )    

tours = {}
for t in tour:
    murl = md5(t.encode('utf-8')).hexdigest()
    tours[t] = murl
    g.add( (URIRef(murl), EX.tourname, Literal(t)) ) 

ninlive = set()
for file in files:
    url = md5(file.encode('utf-8')).hexdigest()
    dates = file.split("-")
    print(dates)
    g.add( (URIRef(url), EX.year, Literal(dates[0])) )
    g.add( (URIRef(url), EX.month, Literal(dates[1])) )
    g.add( (URIRef(url), EX.day, Literal(dates[2])) )

    with open(f"gigs/{file}", "r") as fh:
        soup = BeautifulSoup(fh.read(), "html.parser")
        for link in soup.find_all('a', href=True):
            if link['href'].startswith("/recordings?microphone_type"):
                g.add( (URIRef(url), EX.microphone, URIRef(microphones[link.text.strip()])) )
            elif link['href'].startswith("/recordings?taper_name"):
                g.add( (URIRef(url), EX.taper, URIRef(tapers[link.text.strip()])) )
            elif link['href'].startswith("/artists/nin/tours/"):
                g.add( (URIRef(url), EX.tour, URIRef(tours[link.text.strip()])) )
            elif link['href'].startswith("/artists/nin/venues/"):
                g.add( (URIRef(url), EX.venue, URIRef(venues[link.text.strip()])) )
            elif link['href'].startswith("/artists/nin/countries/"):
                g.add( (URIRef(url), EX.country, Literal(link.text.strip())) )

        for link in soup.find_all('li', {"class": "mb-2"}):
            textlink = link.text.strip()
            if textlink.startswith("Lineage"):
                g.add( (URIRef(url), EX.lineage, Literal(link.text.strip().split("Lineage:")[1].strip())) )
                if "ninlive Traveling Rig" in link.text:
                    ninlive.add( link.text.strip().split("Lineage:")[1].strip() )
            elif textlink.startswith("Length"):
                g.add( (URIRef(url), EX.length, Literal(link.text.strip().split("Length:")[1].strip())) )

g.serialize(destination="nin.n3", format="turtle")
