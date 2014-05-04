import os, sys, gc

def populate():
    python_cat = add_cat('Python')

    add_page(cat=python_cat,
        title="Official Python Tutorial",
        url="http://docs.python.org/2/tutorial/")

    add_page(cat=python_cat,
        title="How to Think like a Computer Scientist",
        url="http://www.greenteapress.com/thinkpython/")

    add_page(cat=python_cat,
        title="Learn Python in 10 Minutes",
        url="http://www.korokithakis.net/tutorials/python/")

    django_cat = add_cat("Django")

    add_page(cat=django_cat,
        title="Official Django Tutorial",
        url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    add_page(cat=django_cat,
        title="Django Rocks",
        url="http://www.djangorocks.com/")

    add_page(cat=django_cat,
        title="How to Tango with Django",
        url="http://www.tangowithdjango.com/")

    frame_cat = add_cat("Other Frameworks")

    add_page(cat=frame_cat,
        title="Bottle",
        url="http://bottlepy.org/docs/dev/")

    add_page(cat=frame_cat,
        title="Flask",
        url="http://flask.pocoo.org")

    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

    
def populate_cards():
    makeSports()
    add_team(name='Chicago Bulls', sport=basketBall())
    newyork = add_team(name='New York Knicks', sport=basketBall())
    minesota = add_team(name='Minnesota Timberwolves', sport=basketBall())
    goldenState = add_team(name='Golden State Warriors', sport=basketBall())
    boston = add_team(name='Boston Celtics', sport=basketBall())
    add_team(name='Miami Heat', sport=basketBall())
    mariners = add_team(name='Seatle Mariners', sport=baseBall())
    
    garnett = add_player(name='Kevin Garnett', team=minesota)
    sprewell = add_player(name='Latrell Sprewell', team=goldenState)
    sprewell.team.add(newyork)
    sprewell.team.add(minesota)
    garnett.team.add(boston)
    
    griffey = add_player(name='Ken Griffey Jr.', team=mariners)
    griffey.team.add(boston)
    
        # Print out what we have added to the user.
    for s in Sport.objects.all():
        for t in Team.objects.filter(sport=s):
            for p in Player.objects.filter(team=t):
                print "- {0} - {1} - {2}".format(str(s), str(t), str(p))
    
def add_team(name, sport):
    team = Team.objects.get_or_create(name=name, sport=sport)[0]
    team.save()
    return team

def basketBall():
    sport = Sport.objects.get_or_create(category='BK')[0]
    sport.save()
    return sport
    
def baseBall():
    sport = Sport.objects.get_or_create(category='BS')[0]
    sport.save()
    return sport    
    
def makeSports():
    Sport.objects.get_or_create(category='BK')[0]
    Sport.objects.get_or_create(category='BS')[0]
    Sport.objects.get_or_create(category='AF')[0]
    Sport.objects.get_or_create(category='SO')[0]
    Sport.objects.get_or_create(category='HO')[0]
    
def add_player(name, team):
    player = Player.objects.get_or_create(name=name)[0]
    #player = Player(name=name)
    #player.save()
    player.team.add(team)
    player.save()
    return player

def add_set(year, name):
    setNameWithHyphons = str(name).replace(" ", "-").strip()
    beckettURL = "http://www.beckett.com/basketball/{year}/{setNameWithHyphons}".format(year=year, setNameWithHyphons=setNameWithHyphons)
    #print "adding set:" + year + " " + name + " " + beckettURL + " " + setNameWithHyphons
    set = Set.objects.get_or_create(year=year, name=name, beckettURL=beckettURL)[0]
    return set
    
def add_card(set, maxSerialNumber, cardNumber, subset, isAutograph,  isMemorabilia, isRookieCard, beckettURL, imageURL  ):
    #remove unicode crap
    card = Card.objects.get_or_create(set=set, maxSerialNumber=maxSerialNumber, cardNumber=cardNumber, subset=subset,isAutograph=isAutograph,  isMemorabilia= isMemorabilia, isRookieCard=isRookieCard, beckettURL=beckettURL, imageURL=imageURL)[0]
    card.save()
    return card    
    
def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def populate_from_file(match):
    with open(match, 'r') as file:
        beckettItems = (pickle.load(file))
    
        print "File" + str(file)
    
        for item in beckettItems:
            if item is not None:            
                team = add_team(item['team'], basketBall())
                
                set = add_set(item['year'], item['setName'])
                
                isMerobilia = isAutograph = isRookieCard = False
                
                try:
                    isMerobilia = item['memorabilia'] > 0
                except:
                    i = 2
                
                try:
                    isAutograph = item['autograph'] > 0
                except:
                    i = 2
                    
                try:
                    isRookieCard = item['rookiecard'] > 0
                except:
                    i = 2    

                maxSerialNumber = 0;
                
                try:
                    maxSerialNumber = item['serialNumber']
                except:
                    i =2
                
                subset = ""
                try:
                    subset = item['subsetName']
                except:
                    i =2
                
                card = add_card(set, maxSerialNumber, item['cardNumber'], subset, isAutograph, isMerobilia, isRookieCard, item['beckettLink'], item['imageLink'])
                
                for playerName in item['playerNames']:
                    player = add_player(playerName, team)
                    card.players.add(player)
                """
                del card
                del team
                del player
                del set
                    
        del beckettItems[:]            
    gc.collect()
    """
                
def populate_cards_from_pickle():
    fileStart = "H:\\Code\\beckett\\tutorial\\Basketball"

    matches = []
    for filename in find_files("H:\\BeckettScrape\\Basketball", '*.pickle'):
        matches.append(filename)

    #print file

    for match in matches:
        populate_from_file(match)

# Start execution here!
if __name__ == '__main__':
    sys.path.append('H:\\Code\\DjangoTest\\tango_with_django_project\\rango')
    sys.path.append('H:\\Code\\DjangoTest\\tango_with_django_project')
    sys.path.append('H:\\Code\\beckett\\')
    
    for path in sys.path:
        print path
    
    from tutorial.items import BeckettItem
    import cPickle as pickle
    import pprint
    import sys

    import os, fnmatch
    
    print "Starting Rango population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
    from rango.models import Category, Page, Team, Sport, Player, Set, Card
    populate_cards()
    populate_cards_from_pickle()
    
    