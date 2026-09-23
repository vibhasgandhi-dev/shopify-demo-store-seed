import json,sys,urllib.request,time
import os
KEY=os.environ['GRAPHIQL_KEY']  # from `shopify app dev` output: GraphiQL URL (Admin API) ...?key=<KEY>
LOC=os.environ["LOCATION_ID"]            # gid://shopify/Location/...
PUB_ONLINE=os.environ["PUBLICATION_ONLINE"]  # gid://shopify/Publication/... (Online Store)
PUB_SHOP=os.environ.get("PUBLICATION_SHOP",PUB_ONLINE)
def gql(q,v=None):
    req=urllib.request.Request(f"http://localhost:3457/graphiql/graphql.json?api_version=2026-07&key={KEY}",data=json.dumps({"query":q,"variables":v or {}}).encode(),headers={"Content-Type":"application/json"})
    r=json.load(urllib.request.urlopen(req,timeout=120))
    if 'errors' in r: print("GQL ERRORS",json.dumps(r['errors'])[:800])
    return r.get('data',{})
U=lambda i,w=1600,h=2000:f"https://images.unsplash.com/photo-{i}?w={w}&h={h}&fit=crop&q=82&fm=jpg"  # uniform 4:5 crop so the grid stays even
V="Ember & Bean"
COLLECTIONS={"brewers":("Brewers","Pour-over, French press, moka and cold brew: everything that turns grounds into a cup.","brewers"),
 "espresso":("Espresso & Grinders","Machines, burr grinders and the tools that make a proper shot.","espresso"),
 "beans":("Coffee Beans","Freshly roasted single origins and blends, shipped within 48 hours of roasting.","beans"),
 "accessories":("Accessories","Scales, kettles, mugs and the small things that make brewing better.","accessories")}
P=[
 dict(h="ceramic-pour-over-dripper",t="Ceramic Pour-Over Dripper",type="Brewer",tags=["brewers","pour-over"],price=34,cmp=None,sku="EB-DRIP-01",imgs=["1638202518327-956c496a5240","1582768772255-7fb8066357ce"],
  d="A conical ceramic dripper with a single large hole for a clean, bright cup. Holds heat evenly, fits standard #2 filters and sits on any mug or server. Dishwasher safe."),
 dict(h="pour-over-starter-set",t="Pour-Over Starter Set",type="Brewer",tags=["brewers","pour-over","gift"],price=79,cmp=95,sku="EB-SET-01",imgs=["1442512595331-e89e73853f31","1638202518327-956c496a5240"],
  d="Dripper, 600 ml glass server, 100 filters and a scoop. Everything you need for your first pour-over, boxed and ready to gift."),
 dict(h="glass-carafe-brewer-6-cup",t="Glass Carafe Brewer, 6 cup",type="Brewer",tags=["brewers","pour-over"],price=52,cmp=None,sku="EB-CARAFE-06",imgs=["1637944220531-5f6fd15c1e29","1613324295642-11319a5e2f03"],
  d="Hand-blown borosilicate glass with a wooden collar and leather tie. Brews up to six cups with thick bonded filters for a sediment-free pour."),
 dict(h="gooseneck-electric-kettle",t="Gooseneck Electric Kettle, 0.8 L",type="Kettle",tags=["accessories","kettle"],price=89,cmp=109,sku="EB-KET-08",imgs=["1577847670487-fb156712e432","1620051524347-854568bb2e0f"],
  d="Variable temperature from 40 to 100 °C with a 60-minute hold. Precision spout for slow, controlled pours. Matte black stainless steel, 1200 W."),
 dict(h="french-press-1l",t="French Press, 1 L",type="Brewer",tags=["brewers","french-press"],price=39,cmp=None,sku="EB-FP-10",imgs=["1721406769891-f2ba651401d9","1609902980959-8fc750449b73"],
  d="Double-wall stainless steel keeps coffee hot for an hour. Four-layer filter, 1 litre capacity (about 4 mugs). No glass to break."),
 dict(h="moka-pot-6-cup",t="Stovetop Moka Pot, 6 cup",type="Brewer",tags=["brewers","moka"],price=44,cmp=None,sku="EB-MOKA-06",imgs=["1603387008808-d96b9631ed73","1749843988878-7b46354d1159"],
  d="Aluminium body, ergonomic handle and a safety valve. Works on gas and electric hobs. Makes 300 ml of strong, syrupy coffee in four minutes."),
 dict(h="cold-brew-pitcher",t="Cold Brew Pitcher, 1.2 L",type="Brewer",tags=["brewers","cold-brew"],price=36,cmp=None,sku="EB-CB-12",imgs=["1676213185724-8565dabeef28","1621782967300-337e387d0c39"],
  d="Fine mesh steel filter core, airtight lid and a pitcher that fits in the fridge door. Steep 12 to 18 hours for smooth, low-acid cold brew."),
 dict(h="portable-press-brewer",t="Portable Press Brewer",type="Brewer",tags=["brewers","travel"],price=45,cmp=None,sku="EB-PRESS-01",imgs=["1712664436035-64c470e9c40e","1670950444753-805b4fb5a00e"],
  d="Full immersion plus gentle pressure for a clean cup in under two minutes. Shatterproof, packs flat, comes with 350 paper filters."),
 dict(h="hand-burr-grinder",t="Hand Burr Grinder",type="Grinder",tags=["espresso","grinder","travel"],price=69,cmp=None,sku="EB-HG-01",imgs=["1758979645721-ad65bacd6708","1649460681450-f00ecbf567b5"],
  d="Conical steel burrs with 40 external click settings, from Turkish fine to French press coarse. 30 g capacity, fits in a jacket pocket."),
 dict(h="electric-burr-grinder",t="Electric Burr Grinder",type="Grinder",tags=["espresso","grinder"],price=189,cmp=219,sku="EB-EG-01",imgs=["1461988279488-1dac181a78f9","1629248990514-c350da4e7bc9"],
  d="40 mm flat burrs, 60 grind settings and a timed dose for consistent shots and pour-overs. Low retention, quiet motor, anti-static chute."),
 dict(h="compact-espresso-machine",t="Compact Espresso Machine",type="Espresso machine",tags=["espresso","machine"],price=449,cmp=499,sku="EB-ESP-01",imgs=["1608354580875-30bd4168b351","1627902511858-6ad7e004fd35"],
  d="15-bar pump, PID temperature control and a steam wand that actually textures milk. 58 mm portafilter, 1.8 L tank. Heats in 40 seconds."),
 dict(h="espresso-tamper-58mm",t="Espresso Tamper, 58 mm",type="Espresso accessory",tags=["espresso","accessories"],price=32,cmp=None,sku="EB-TMP-58",imgs=["1767515341418-2f67d387c88c","1615327072330-6c8f4c063ece"],
  d="Calibrated to 30 lb of pressure with a click, so every shot is tamped the same. Flat stainless base, walnut handle."),
 dict(h="milk-frother",t="Handheld Milk Frother",type="Accessory",tags=["accessories","milk"],price=29,cmp=None,sku="EB-FRO-01",imgs=["1671376354106-d8d21e55dddd","1649882453742-c93c481edb77"],
  d="Two whisk heads, three speeds, USB-C charging. Silky microfoam for lattes and cappuccinos in 20 seconds, plus a stand to keep it tidy."),
 dict(h="brew-scale-with-timer",t="Brew Scale with Timer",type="Accessory",tags=["accessories","scale"],price=59,cmp=None,sku="EB-SCL-01",imgs=["1676600475896-dbf8ddd44f1d","1638202539979-5b90600aacb2"],
  d="0.1 g precision up to 2 kg, auto-start timer and flow-rate display. Rechargeable, water-resistant top, silicone heat pad included."),
 dict(h="stoneware-mug-set",t="Stoneware Mug, set of 2",type="Mug",tags=["accessories","mug","gift"],price=28,cmp=None,sku="EB-MUG-02",imgs=["1495100497150-fe209c585f50","1650959858546-d09833d5317b"],
  d="350 ml speckled stoneware with a wide handle and a thick base that holds heat. Microwave and dishwasher safe.",
  options=[("Colour",["Speckled grey","Cloud white"])]),
 dict(h="ethiopia-guji-single-origin",t="Ethiopia Guji, Single Origin",type="Coffee beans",tags=["beans","single-origin","light-roast"],price=18,cmp=None,sku="EB-ETH-250",imgs=["1695245503558-5cdb37f49092","1459755486867-b55449bb39ff"],
  d="Washed heirloom varieties, light roast. Blueberry, jasmine and a tea-like body. Roasted to order and shipped within 48 hours.",
  options=[("Size",["250 g","1 kg"]),("Grind",["Whole bean","Filter","Espresso"])],prices={"1 kg":58}),
 dict(h="house-espresso-blend",t="House Espresso Blend",type="Coffee beans",tags=["beans","blend","medium-roast"],price=16,cmp=None,sku="EB-HSE-250",imgs=["1685798830559-c116586a0d33","1695245503558-5cdb37f49092"],
  d="Brazil and Colombia, medium-dark roast. Chocolate, hazelnut and a heavy, sweet crema. Built for milk drinks but great straight.",
  options=[("Size",["250 g","1 kg"]),("Grind",["Whole bean","Espresso"])],prices={"1 kg":52}),
]
def ensure_collections():
    got=gql('{ collections(first:20){ nodes{ id handle } } }')['collections']['nodes']
    ids={c['handle']:c['id'] for c in got}
    for handle,(title,desc,tag) in COLLECTIONS.items():
        if handle in ids: continue
        r=gql('mutation($i:CollectionInput!){ collectionCreate(input:$i){ collection{ id handle } userErrors{ field message } } }',
              {"i":{"title":title,"handle":handle,"descriptionHtml":f"<p>{desc}</p>","ruleSet":{"appliedDisjunctively":False,"rules":[{"column":"TAG","relation":"EQUALS","condition":tag}]}}})['collectionCreate']
        if r['userErrors']: print("collection error",handle,r['userErrors'])
        else: ids[handle]=r['collection']['id']
    return ids
def product_input(p):
    opts=p.get('options') or [("Title",["Default Title"])]
    import itertools
    combos=list(itertools.product(*[vals for _,vals in opts]))
    variants=[]
    for n,combo in enumerate(combos):
        price=p['price']
        for name,pr in (p.get('prices') or {}).items():
            if name in combo: price=pr
        variants.append({"optionValues":[{"optionName":o[0],"name":val} for o,val in zip(opts,combo)],
            "price":str(price),"compareAtPrice":(str(p['cmp']) if p['cmp'] and price==p['price'] else None),
            "sku":p['sku']+("" if len(combos)==1 else f"-{n+1:02d}"),
            "inventoryItem":{"tracked":True},"inventoryQuantities":[{"locationId":LOC,"name":"available","quantity":25}]})
    return {"handle":p['h'],"title":p['t'],"descriptionHtml":f"<p>{p['d']}</p>","vendor":V,"productType":p['type'],"tags":p['tags'],"status":"ACTIVE",
        "productOptions":[{"name":o[0],"values":[{"name":v} for v in o[1]]} for o in opts],
        "variants":variants,
        "files":[{"originalSource":U(i),"contentType":"IMAGE","alt":p['t']} for i in p['imgs']]}
def upsert(p):
    r=gql('mutation($i:ProductSetInput!){ productSet(input:$i, synchronous:true){ product{ id handle variants(first:10){ nodes{ id price sku } } media(first:5){ nodes{ id ... on MediaImage { status } } } } userErrors{ field message } } }',{"i":product_input(p)})['productSet']
    if r['userErrors']: print("ERR",p['h'],r['userErrors']); return None
    pr=r['product']; print("ok",pr['handle'],len(pr['variants']['nodes']),"variants",len(pr['media']['nodes']),"media"); return pr['id']
def publish(ids):
    for gid in ids:
        r=gql('mutation($id:ID!,$in:[PublicationInput!]!){ publishablePublish(id:$id,input:$in){ userErrors{ field message } } }',{"id":gid,"in":[{"publicationId":PUB_ONLINE},{"publicationId":PUB_SHOP}]})['publishablePublish']
        if r['userErrors']: print("publish err",gid,r['userErrors'])
if __name__=="__main__":
    which=sys.argv[1] if len(sys.argv)>1 else "all"
    cids=ensure_collections(); print("collections",cids)
    todo=P if which=="all" else [p for p in P if p['h']==which]
    pids=[]
    for p in todo:
        pid=upsert(p)
        if pid: pids.append(pid)
    publish(pids+list(cids.values()))
    print("done",len(pids))
