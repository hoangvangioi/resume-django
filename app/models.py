from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager
from django.db import models
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from PIL import Image

from .fields import WEBPField

# Create your models here.


GENDER_CHOICES = [
    (_("Male"), _("Male")),
    (_("Female"), _("Female")),
    (_("Other"), _("Other")),
]

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Contact(TranslatableModel):
    translations = TranslatedFields(
        full_name = models.CharField(verbose_name=_('Full Name'), max_length=255),
        email = models.EmailField(verbose_name=_('Email')),
        subject = models.CharField(verbose_name=_('Subject'), max_length=255),
        message = models.TextField(verbose_name=_('Message')),
        date_created = models.DateField(verbose_name=_('Date created') ,auto_now_add=True),
    )
    
    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['-id']
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')


class Accounts(AbstractUser):
    first_name   = models.CharField(verbose_name=_('First name'), max_length=50)
    last_name    = models.CharField(verbose_name=_('Last name'), max_length=50)
    email        = models.EmailField(max_length=254, verbose_name='email address', unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def get_full_name(self):
        full_name = "%s %s" % (self.last_name, self.first_name)
        return full_name.strip()

    def __str__(self):
        full_name = "%s %s" % (self.last_name, self.first_name)
        return full_name.strip()

    # @classmethod


class SocialLinks(models.Model):
    account       = models.OneToOneField(Accounts, on_delete=models.CASCADE)
    website_url   = models.URLField(verbose_name=_('Website URL'))
    facebook_url  = models.URLField(verbose_name=_('Facebook URL'))
    instagram_url = models.URLField(verbose_name=_('Instagram URL'))
    github_url    = models.URLField(verbose_name=_('Github URL'))

    def __str__(self):
        return f'{self.account}'

    class Meta:
        verbose_name = _('social link')
        verbose_name_plural = _('social links')


class About(TranslatableModel):
    account = models.OneToOneField(Accounts, on_delete=models.CASCADE)
    translations = TranslatedFields(
        phone         = models.CharField(max_length=12),
        about         = models.TextField(),
        residence     = models.CharField(max_length=255),
        address       = models.CharField(max_length=255, null=True, blank=True),
        date_of_birth = models.DateField(null=True, blank=True),
        gender        = models.CharField(max_length=15, choices=GENDER_CHOICES, null=True, blank=True),
        avatar        = WEBPField(verbose_name=_('Avatar'), upload_to='avatars/'),
        job           = models.CharField(verbose_name=_('Job'), max_length=255, blank=True, null=True),
        cv            = models.FileField(verbose_name=_('Curriculum Vitae'), upload_to='cv/'),
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.avatar.path)
        image = image.resize((360, 360))
        image.save(self.avatar.path)

    def __str__(self):
        return f'{self.account}'

    class Meta:
        verbose_name = _('about')
        verbose_name_plural = _('about')


class TimeLine(TranslatableModel):
    translations = TranslatedFields(
        start = models.DateField(u'start time', default=None),
        end   = models.DateField(u'end time', default=None)
    )


class Educations(TimeLine):
    account     = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    school      = models.CharField(max_length=255)
    position    = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f'From {self.start} to {self.end}'

    class Meta:
        verbose_name = _('education')
        verbose_name_plural = _('educations')


class Experiences(TimeLine):
    account     = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    workplace   = models.CharField(max_length=255)
    position    = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f'From {self.start} to {self.end}'
    
    class Meta:
        verbose_name = _('experience')
        verbose_name_plural = _('experiences')


class Skills(TranslatableModel):
    account     = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    translations = TranslatedFields(
        skill = models.CharField(max_length=255),
        logo = models.FileField(upload_to='logo/')
    )

    class Meta:
        verbose_name = 'skill'
        verbose_name_plural = 'skills'

    def __str__(self):
        return self.skill


class Certificates(TranslatableModel):
    account     = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    translations = TranslatedFields(
        name = models.CharField(max_length=100)
    )

    class Meta:
        verbose_name = _('certificate')
        verbose_name_plural = _('certificates')

    def __str__(self):
        return self.name


class Portfolios(TranslatableModel):
    account     = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        image = WEBPField(upload_to='portfolios/'),
        tag = models.CharField(max_length=50),
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.image.path)
        image = image.resize((600, 600))
        image.save(self.image.path)

    class Meta:
        verbose_name = _('portfolio')
        verbose_name_plural = _('portfolios')


class Blog(TranslatableModel):
    account     = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    translations = TranslatedFields(
        post = models.CharField(max_length=255),
        tag = models.CharField(max_length=50),
        update_at = models.DateField(auto_now_add=True),
        image = WEBPField(upload_to='blog/'),
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.image.path)
        image.thumbnail((600, 800))
        image.save(self.image.path)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('blog')
