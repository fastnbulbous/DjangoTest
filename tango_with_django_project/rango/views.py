from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from rango.models import Sport, Team, Player, Card, Set

def index(request):

    

    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    
    
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    sport_list = Sport.objects.all()
    
    # The following two lines are new.
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    for sport in sport_list:
        sport.url = sport.category.replace(' ', '_')
    
    player_list = Player.objects.all().order_by('name')
    team_list = Team.objects.all().order_by('name')
    
    set_list = Set.objects.all().order_by('year', 'name')
    for set in set_list:
        set.url = set.beckettURL.replace('\'', '')
    
    card_list = Card.objects.all().order_by('beckettURL')
    
    context_dict = {'players': player_list,
                    'sports' : sport_list,
                    'teams' : team_list,
                    'cards' : card_list,
                    'sets' : set_list}
    
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('rango/index.html', context_dict, context)
	
def about(request):
	# Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'someData': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('rango/about.html', context_dict, context)

def sport(request, sport_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    sport_name = sport_name_url.replace('_', ' ')

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'sport_name': sport_name}

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        sport = Sport.objects.get(category=sport_name)

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        teams = Team.objects.filter(sport=sport)
        
        # The following two lines are new.
        # We loop through each category returned, and create a URL attribute.
        # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
        for team in teams:
            team.url = team.name.replace(' ', '_')

        # Adds our results list to the template context under name pages.
        context_dict['teams'] = teams
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['sport'] = sport
    except Sport.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render_to_response('rango/sport.html', context_dict, context)

def team(request, team_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    team_name = team_name_url.replace('_', ' ')
    
    
    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'team_name': team_name}

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        team = Team.objects.get(name=team_name)
        
        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        players = Player.objects.filter(team=team)

        # The following two lines are new.
        # We loop through each category returned, and create a URL attribute.
        # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
        for player in players:
            player.url = player.name.replace(' ', '_')
        
        # Adds our results list to the template context under name pages.
        context_dict['team'] = team
       
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['players'] = players
    except Team.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render_to_response('rango/team.html', context_dict, context)    

def player(request, player_name_url):
    context = RequestContext(request)
    
    player_name = player_name_url.replace('_', ' ')
    context_dict = {'player_name': player_name}
    player = Player.objects.get(name=player_name)
    
    context_dict['player'] = player
    
    # Retrieve all of the associated pages.
    # Note that filter returns >= 1 model instance.
    cards = Card.objects.filter(players=player)
    
    for card in cards:
        card.url = card.beckettURL.replace('\'', '')
        card.image = card.imageURL.replace('\'', '')
    
    context_dict['cards'] = cards
    
    # Go render the response and return it to the client.
    return render_to_response('rango/player.html', context_dict, context) 
    
def set(request, set_name_url): 
    context = RequestContext(request)
    context_dict = {}
    # Go render the response and return it to the client.
    return render_to_response('rango/index.html', context_dict, context)  
    