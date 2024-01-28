from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
HOSTELS = [
    ('ht1', 'Aryabhatta'),
    ('ht2', 'Dhanrajgiri 1'),
    ('ht3', 'Dhanrajgiri 2'),
    ('ht4', 'Vishwesaraiya'),
    ('ht5', 'SN Bose'),
    ('ht6', 'Satish Dhawan'),
    ('ht7', 'Morvi 1'),
    ('ht8', 'Morvi 2'),
    ('ht9', 'CV Raman'),
    ('ht10', 'Rajputana'),
    ('ht11', 'Limbdi'),
    ('ht12', 'New Girls'),
    ('ht13', 'Old Girls')
]

BRANCHES = [
    ('cse', 'Computer Science and Engineering'),
    ('mnc', 'Mathematics and Computation'),
    ('ece', 'Electronics and Communication Engineering'),
    ('ee', 'Electrical Engineering'),
    ('me', 'Mechanical Engineering'),
    ('chem', 'Chemical Engineering'),
    ('cer', 'Ceramic Engineering'),
    ('civ', 'Civil Engineering'),
    ('mat', 'Material Science'),
    ('phe', 'Pharmaceutical Engineering'),
    ('min', 'Mining'),
    ('ic', 'Industrial Chemistry')
]

class UserManager(BaseUserManager):
    def create_user(self, id, email, password=None, role = 'EMPLOYEE', **extra_fields):
        if not id:
            raise ValueError('An id is required.')
        if not password:
            raise ValueError('A password is required.')

        email = self.normalize_email(email)
        user = self.model(email=email, id=id, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, id, email, password=None, role='EMPLOYEE', **extra_fields):
        if not id:
            raise ValueError('An id is required.')
        if not password:
            raise ValueError('A password is required.')

        user = self.create_user(id, email, password, role=role, **extra_fields)
        if role =='EMPLOYEE':
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False
        user.is_active = True
        group_name = 'employee' if role == 'EMPLOYEE' else 'student'
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        EMPLOYEE = "EMPLOYEE", 'Employee'
        STUDENT = "STUDENT", 'Student'

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.EMPLOYEE)
    id = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(_("password"), max_length=128)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email', 'password', 'role']

    objects = UserManager()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.role == 'EMPLOYEE':
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        return super().save(*args, **kwargs)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    dob = models.DateField(default='2004-04-25')
    hostel = models.CharField(max_length=100, choices=HOSTELS, blank=True)
    branch = models.CharField(max_length=100, choices=BRANCHES, blank = True)
    image = models.ImageField(default = 'default.png', upload_to = 'profile_pics')

    def __str__(self):
        return str(self.user.id)

class Items(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
    name = models.CharField(max_length = 100, blank = True)
    description = models.TextField()
    image = models.ImageField(default='default.png', upload_to='item_pics')

    def __str__(self):
        return str(self.user.id) + " item " + str(self.pk)

class toSell(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.IntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return str(self.user.id) + "toSell" + str(self.item_id)

class Purchased(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.IntegerField()
    price = models.PositiveIntegerField()
    purchased_from = models.IntegerField(default=1)
    purchased_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.id) + "Purchased" + str(self.item_id)

class Lost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.IntegerField()
    description = models.TextField()
    def __str__(self):
        return str(self.user.id) + "Lost" + str(self.item_id)

class Sold(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.IntegerField()
    price = models.PositiveIntegerField()
    sold_to = models.IntegerField()
    sold_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.id) + "Sold" + str(self.item_id)