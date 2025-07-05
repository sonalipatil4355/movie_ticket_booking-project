from django.db import models

genres = [('Action','Action'),('Adventure','Adventure'),('Comedy','Comedy'),
          ('Drama','Drama'),('Horror','Horror'),('Romance','Romance'),('Thriller','Thriller')]

languages = [('English','English'),('Marathi','Marathi'),('Hindi','Hindi'),('Spanish','Spanish'),('Kannada','Kannada'),
             ('Tamil','Tamil'),('Telugu','Telugu'),('Malayalam','Malayalam')]
class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=200, choices=genres, null=True, blank=True)
    language = models.CharField(max_length=200, choices=languages, null=True, blank=True)
    synopsis = models.TextField(max_length=255, null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    trailer_url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=[('Released', 'Released'), ('Upcoming', 'Upcoming')], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='movie_posters/', null=True, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)
    slug = models.SlugField(max_length=2000, unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            raw = f"{self.title} {self.release_date} {self.language} {self.genre}"
            clean = raw.replace(' ', '-').replace('(', '').replace(')', '').replace(':', '').replace('&', '').replace('?', '').replace(',', '').replace('.', '')
            self.slug = clean
        super().save(*args, **kwargs)



class Cast(models.Model):
    movie = models.ForeignKey(Movie, related_name='casts', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='casts/', null=True, blank=True)
