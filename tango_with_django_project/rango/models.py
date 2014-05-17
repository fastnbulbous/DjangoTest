from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class Sport(models.Model):
    BASKETBALL = 'BK'
    BASEBALL = 'BS'
    AMERICAN_FOOTBALL = 'AF'
    SOCCER = 'SO'
    HOCKEY = 'HO'
    CATEGORY_CHOICES = (
        (BASKETBALL, 'Basketball'),
        (BASEBALL, 'Baseball'),
        (AMERICAN_FOOTBALL, 'Football'),
        (SOCCER, 'Soccer'),
        (HOCKEY, 'Hockey'),
    )
    category = models.CharField(max_length=2,
                                choices=CATEGORY_CHOICES,
                                default=BASKETBALL,
                                unique=True)
                                
    def __unicode__(self):
        return self.category

class Team(models.Model):
    sport = models.ForeignKey(Sport)
    name = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=128)
    team = models.ManyToManyField(Team)
    
    def __unicode__(self):
        return self.name     

class Set(models.Model):
    name = models.TextField()
    year = models.CharField(max_length=128)
    beckettURL = models.URLField() # should be able to fill this in with the data i have eg: http://www.beckett.com/basketball/2003-04/exquisite-collection/ - www.becket.com/$sport/$year/$setname

    def __unicode__(self):
        return self.year + " " + self.name      
    
class Card(models.Model):
    set = models.ForeignKey(Set)
    players = models.ManyToManyField(Player)
    maxSerialNumber = models.PositiveIntegerField()
    cardNumber = models.CharField(max_length=128)
    subset = models.CharField(max_length=128)
    isAutograph = models.BooleanField(default=False)
    isMemorabilia = models.BooleanField(default=False)
    isRookieCard = models.BooleanField(default=False)
    beckettURL = models.URLField(max_length=500)
    imageURL = models.URLField(max_length=500)
    
    def playerNames(self):
        names = ""
        for player in self.players.all():
            names += player.name + " "
        return names.strip();
    
    def __unicode__(self):
        
        return str(self.set) + " " + str(self.cardNumber) + " " + self.playerNames()
  

  
class CardInstance(models.Model):
    card = models.ForeignKey(Card)
    serialNumber = models.PositiveIntegerField()
    
    def __unicode__(self):
        return str(self.card) + " (" + str(self.serialNumber) + ")"        

class CardInstanceMedia(models.Model):
    cardInstance = models.ManyToManyField(CardInstance)
    imageURL = models.URLField()

    def __unicode__(self):
        return str(self.imageURL) 

class CardInstanceSales(models.Model):
    cardInstance = models.ManyToManyField(CardInstance) #probably should be foriegn key ajar
    ebayNumber = models.CharField(max_length=128)
    otherURL = models.URLField()
    saleDate = models.DateField()
    saleAmount = models.FloatField()
    evidenceImageURL = models.URLField()

    def __unicode__(self):
        return " - " + str(self.ebayNumber)
    