from django.http import HttpResponse

def test(request):
    return HttpResponse("Rango says: Hello world! <a href='/rango/about'>About</a>")
	
def about(request):
	return HttpResponse("Index dong <a href='/rango/'>Index</a>")
