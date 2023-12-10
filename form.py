from wtforms import Form, StringField, IntegerField, DateField, SelectField ,validators
from wtforms.validators import NumberRange, ValidationError, URL




message_erreur_lenght = 'Le champ doit contenir entre 1 et 50 caractères'
message_erreur_lenght_30 = 'Le champ doit contenir entre 3 et 30 caractères'
message_erreur_lenght_100 = 'Le champ doit contenir entre 3 et 100 caractères'
message_erreur_lenght_250 = 'Le champ doit contenir entre 10 et 250 caractères'
message_erreur_lenght_1000 = 'Le champ doit contenir entre 1 et 1000 caractères'
message_erreur_lenght_min = 'Le champ doit contenir un minimum de 1 caractères'
message_erreur_required = 'Le champ est obligatoire'
message_erreur_min = 'La valeur doit être supérieure ou égale à 1'
message_erreur_min_zero = 'La valeur doit être supérieure ou égale à 0'
message_erreur_min_annee = 'La valeur doit être supérieure ou égale à 1850'



class FilmForm(Form):
    
    titre = StringField('Titre', [validators.Length(min=1, max=50, message=message_erreur_lenght), validators.DataRequired(message=message_erreur_required)])

    annee = IntegerField('Année', [validators.DataRequired(message=message_erreur_required), NumberRange(min=1850, message=message_erreur_min_annee)])

    dateSortie = DateField('Date de sortie', [validators.DataRequired(message=message_erreur_required)])
    def validate_dateSortie(form, field):
        if field.data.year < 1850:
            raise ValidationError('La date ne peut pas être inférieure à l\'année 1850')
    
    rated = SelectField('Noté', choices=[('G', 'G'), ('PG', 'PG'), ('PG-13', 'PG-13'), ('R', 'R'), ('NC-17', 'NC-17')], validators=[validators.DataRequired(message=message_erreur_required)])

    duree = IntegerField('Durée', [validators.DataRequired(message=message_erreur_required), NumberRange(min=1, message=message_erreur_min)])

    realisateur = StringField('Réalisateur', [validators.DataRequired(message=message_erreur_required), validators.Length(min=3, max=100, message=message_erreur_lenght)])

    writers = StringField('Scénariste', [validators.DataRequired(message=message_erreur_required), validators.Length(min=3, max=100, message=message_erreur_lenght_100)])

    acteurs = StringField('Acteurs', [validators.DataRequired(message=message_erreur_required), validators.Length(min=3, max=100, message=message_erreur_lenght_100)])

    genres = StringField('Genres', [validators.DataRequired(message=message_erreur_required), validators.Length(min=3, max=30, message=message_erreur_lenght_30)])

    synopsis = StringField('Synopsis', [validators.DataRequired(message=message_erreur_required), validators.Length(min=10, max=250, message=message_erreur_lenght_250)])

    langue = StringField('Langue', [validators.DataRequired(message=message_erreur_required), validators.Length(min=1, max=50, message=message_erreur_lenght)])

    pays = StringField('Pays', [validators.DataRequired(message=message_erreur_required), validators.Length(min=1, max=50, message=message_erreur_lenght)])

    typeFilm = StringField('Type', [validators.DataRequired(message=message_erreur_required), validators.Length(min=1, max=50, message=message_erreur_lenght)])

    reponse = SelectField('Réponse', choices=[('True', 'Oui'), ('False', 'Non')], validators=[validators.DataRequired(message=message_erreur_required)])

    image = StringField('Image', [validators.DataRequired(message=message_erreur_required), validators.Length(min=1, max=1000, message=message_erreur_lenght_1000), URL(message='L\'url doit être valide')])

    awards = StringField('Prix Gagnés', [validators.DataRequired(message=message_erreur_required), validators.Length(min=3, max=100, message=message_erreur_lenght_100)])

    metascore = IntegerField('Metascore', [validators.DataRequired(message=message_erreur_required), NumberRange(min=0, message=message_erreur_min_zero)])

    imdbRating = IntegerField('Note Imdb', [validators.DataRequired(message=message_erreur_required), NumberRange(min=0, message=message_erreur_min_zero)])

    imdbVotes = IntegerField('Votes Imdb', [validators.DataRequired(message=message_erreur_required), NumberRange(min=0, message=message_erreur_min_zero)])

    imdbID = StringField('ID Imdb', [validators.DataRequired(message=message_erreur_required), validators.Length(min=1, max=50, message=message_erreur_lenght)])

    def validate(self):
        initial_validation = super(FilmForm, self).validate()
        if not initial_validation:
            return False

        if self.annee.data != self.dateSortie.data.year:
            self.annee.errors.append("L'année doit être égale à l'année de la date de sortie")
            return False

        return True