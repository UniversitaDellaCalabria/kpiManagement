from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.utils.translation import gettext as _


class User(AbstractUser):
    GENDER = (
        ('M', _('Maschio')),
        ('F', _('Femmina')),
        ('O', _('Altro')),
    )

    is_active = models.BooleanField(_('attivo'), default=True)
    email = models.EmailField('email address', blank=False, null=True,)
    matricola_dipendente = models.CharField(_('Matricola Dipendente'),
                                            max_length=6,
                                            blank=True, null=True,
                                            help_text="fonte CSA")
    matricola_studente = models.CharField(_('Matricola Studente'),
                                          max_length=6,
                                          blank=True, null=True,
                                          help_text="fonte Esse3")
    first_name = models.CharField(_('Nome'), max_length=100, blank=False, null=True)
    last_name = models.CharField(_('Cognome'), max_length=100, blank=False, null=True)
    codice_fiscale = models.CharField(_('Codice Fiscale'),
                                      max_length=16,
                                      unique=True)
    gender = models.CharField(_('Genere'), choices=GENDER,
                              max_length=12, blank=True, null=True)
    place_of_birth = CountryField('Luogo di nascita', max_length=30,
                                  blank=True, null=True)
    birth_date = models.DateField('Data di nascita',
                                  null=True, blank=True)
    created_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL)
    manual_user_update = models.DateTimeField(_('Ultimo aggiornamento manuale dei dati'), blank=True, null=True)

    # short_description = models.CharField(_('Descrizione breve'), max_length=33, blank=True, null=True)
    # bio = models.TextField('Biografia, note', max_length=2048, blank=True, null=True)
    # avatar  = models.ImageField('Avatar, foto', upload_to='avatars/', null=True, blank=True)
    # webpage_url = models.CharField(_('Pagina web'), max_length=512, blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name', 'username']
        verbose_name_plural = _("Utenti UNICAL")

    def __str__(self):
        return '{} {}'.format(self.last_name,  self.first_name)
