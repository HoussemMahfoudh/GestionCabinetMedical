from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Transpose, SmartResize

# Create your models here.

from django.forms import widgets, Widget

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
CITY_CHOICES = (('T', 'Tunis'), ('N', 'Nabeul'), ('A', 'Ariana'))


class MyUserManager(BaseUserManager):

    def _create_user(self, email, first_name, last_name, date_of_birth, phone_number, gender, city, address, password= None ,  **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            date_of_birth = date_of_birth,
            phone_number=phone_number,
            gender=gender,
            city=city,
            address=address,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, date_of_birth, phone_number, gender, city, address, password=None , **extra_fields):
        extra_fields.setdefault('is_patient', True)
        return self._create_user(email, first_name, last_name, date_of_birth, phone_number, gender, city, address, password=None, **extra_fields)

    def create_superuser(self, email, first_name, last_name, date_of_birth, phone_number, gender, city, address,
                    password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_doctor', True)
        return self._create_user(email, first_name, last_name, date_of_birth, phone_number, gender, city, address,
                                 password, **extra_fields)
        

    def create_user_doctor(self, email, first_name, last_name, date_of_birth, phone_number, gender, city, address, password=None , **extra_fields):
        extra_fields.setdefault('is_doctor', True)
        extra_fields.setdefault('specialite', True)

        if extra_fields.get('is_doctor') is not True:
            raise ValueError('doctor must have is_doctor=True.')

        return self._create_user(email, first_name, last_name, date_of_birth, phone_number, gender, city, address, password=None, **extra_fields)


class MyUser(AbstractBaseUser):
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = models.DecimalField( max_digits=8,decimal_places=0)

    gender = models.CharField(choices=GENDER_CHOICES, max_length=128)
    city = models.CharField(choices=CITY_CHOICES, max_length=128)
    address = models.CharField(max_length=255)
    specialite = models.CharField(max_length=233 , null=True)
    picture=models.ImageField(upload_to='upload/picture', default="user.png", max_length=255, blank=True, null=True)
    picture_thumbnail = ImageSpecField(
                                source='picture',
                                processors = [Transpose(),SmartResize(100, 100)],
                                format = 'JPEG',
                                options = {'quality': 75})
    #picture = models.FileField(upload_to='documents/%Y/%m/%d/')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'date_of_birth', 'phone_number', 'gender', 'city', 'address']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
