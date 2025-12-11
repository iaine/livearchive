from rdflib import Graph

g = Graph()

g.parse('nin.n3')

link_nin = """
SELECT DISTINCT ?taper ?tour
WHERE {
    ?a ns1:taper ?b .
    ?a ns1:year ?year .
    ?a ns1:month ?month .
    ?a ns1:day ?day .
    ?b foaf:name ?taper .
    ?a ns1:lineage ?literal .
    ?a ns1:tour ?c .
    ?c ns1:tourname ?tour .
    filter contains(?literal,"ninlive") .
    
} ORDER BY ?year ?month ?day"""

qres = g.query(link_nin)
for row in qres:
    print(f"{row.taper} -> {row.tour}")

gear_nin = """
SELECT ?tour ?microphone ?country
WHERE {
    ?a ns1:taper ?b .
    ?a ns1:microphone ?d .
    ?d ns1:microphonename ?microphone .
    ?a ns1:tour ?c .
    ?c ns1:tourname ?tour .
    ?a ns1:country ?country
} GROUP BY ?microphone
ORDER BY ?country ?tour """

qres = g.query(gear_nin)
for row in qres:
    print(f"{row.tour} ({row.country}) ->  : {row.microphone}")

print("----------------------------")
#query by kit, gig, 
nin = " SELECT ?tour ?taper ?venue \
WHERE {{ \
    ?a ns1:taper ?c . \
    ?c foaf:name ?taper . \
    ?a ns1:microphone ?d . \
    ?d ns1:microphonename \"{}\" . \
    ?a ns1:tour ?b . \
    ?b ns1:tourname ?tour . \
    ?a ns1:venue ?e . \
    ?e ns1:venuename ?venue . \
}} GROUP BY ?tour ?venue ".format("DPA 4060s")

qres = g.query(nin)
for row in qres:
    print(f"{row.tour} ({row.taper}) {row.venue}")

    print("----------------------------")
#query by kit, gig, 
nin = """ SELECT (COUNT(?a) as ?event) ?year ?month \
WHERE { \
    ?a ns1:year ?year .
    ?a ns1:month ?month .
} GROUP BY ?year ?month 
ORDER BY ?year ?month"""

qres = g.query(nin)
with open("viz/dates.csv", "w") as fh:
    for row in qres:
        fh.write(f"{row.year}-{row.month}, {row.event}\n")