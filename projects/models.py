from django.db import models
from django.utils import timezone
import uuid

# Create your models here.


class Organization(models.Model):
    TYPE = (
        ('prov', 'Healthcare Provider'),
        ('univ', 'University'),
        ('fac', 'Faculty'),
        ('dept', 'Department'),
        ('rc', 'Research Centre'),
        ('team', 'Organizational team'),
        ('govt', 'Government'),
        ('edu', 'Educational Institute'),
        ('crs', 'Clinical Research Sponsor'),
        ('cg', 'Community Group'),
        ('bus', 'Non-Healthcare Business or Corporation'),
        ('other', 'Other'),
    )

    PURPOSE = (
        ('BILL', 'Billing'),
        ('ADMIN', 'Administrative'),
        ('RES', 'Research Centre'),
        ('EDU', 'Education Provider'),
        ('SUPP', 'Supplier'),
    )

    ADDRESS_TYPE = (
        ('PO', 'postal'),
        ('PH', 'physical'),
        ('BO', 'both')
    )

    active = models.BooleanField(default=True)
    type = models.CharField(max_length=12, choices=TYPE)
    name = models.CharField(max_length=255)
    purpose = models.CharField(max_length=12, choices=PURPOSE)
    addressType = models.CharField(max_length=2, default='PH', choices=ADDRESS_TYPE)
    address = models.CharField('address', max_length=1000)
    city = models.CharField(max_length=25)
    district = models.CharField(max_length=25, null=True)
    state = models.CharField(max_length=25)
    postalCode = models.CharField('post code', default='00000', max_length=12)
    country = models.CharField(max_length=2, default='MY')
    manager = models.ForeignKey('self', related_name='composition', on_delete=models.PROTECT, null=True)


class Subject(models.Model):
    SEX = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    )

    GENDER = (
        ('M', 'Male',),
        ('F', 'Female'),
        ('N', 'Non-binary'),
        ('T', 'Transgendered'),
        ('U', 'Unknown'),
        ('O', 'Others')
    )

    ETHNICITY = (
        ('ML', 'Malay'),
        ('CH', 'Chinese'),
        ('IN', 'Indian'),
        ('IB', 'Iban'),
        ('KM', 'Kadazan Murut'),
        ('IM', 'West Malaysia indigenous'),
        ('IS', 'Other East Malaysia indigenous'),
        ('EA', 'East Asian'),
        ('HI', 'Hispanic'),
        ('PI', 'Pacific Islander'),
        ('AR', 'Arab'),
        ('PE', 'Persian'),
        ('UN', 'Unspecified')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    subjectName = models.CharField('full name', null=True, max_length=120)
    prefix = models.CharField('salutations or honorifics', max_length=20, null=True, blank=True)
    suffix = models.CharField(max_length=20, null=True, blank=True)
    active = models.BooleanField(default=1)
    sex = models.CharField(max_length=1, choices=SEX)
    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)
    birthDate = models.DateField('date of birth', null=True, blank=True)
    ethnicity = models.CharField(max_length=2, choices=ETHNICITY, null=True, blank=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.subjectName


class Identification(models.Model):
    ID_TYPE = (
        ('NR', 'National registration id'),
        ('PP', 'Passport id'),
        ('EI', 'Employment id'),
    )

    idValue = models.CharField(max_length=30)
    idType = models.CharField(max_length=5, choices=ID_TYPE)
    researcher = models.ForeignKey(Subject, related_name='identifications', on_delete=models.CASCADE)

    def __str__(self):
        return self.idValue


class Address(models.Model):
    ADDRESS_USE = (
        ('H', 'home'),
        ('W', 'work'),
        ('T', 'temporary'),
        ('O', 'old'),
        ('B', 'billing')
    )

    ADDRESS_TYPE = (
        ('PO', 'postal'),
        ('PH', 'physical'),
        ('BO', 'both')
    )

    use = models.CharField(max_length=1, choices=ADDRESS_USE)
    type = models.CharField(max_length=2, choices=ADDRESS_TYPE, default='PH')
    text = models.CharField('address', max_length=1000)
    city = models.CharField(max_length=25)
    district = models.CharField(max_length=25, null=True)
    state = models.CharField(max_length=25)
    postalCode = models.CharField('post code', default='00000', max_length=12)
    country = models.CharField(max_length=2, default='MY')
    researcher = models.ForeignKey(Subject, related_name='addresses', on_delete=models.CASCADE)


class ContactPoint(models.Model):
    CONTACT_POINT_SYS = (
        ('phone', 'phone'),
        ('mobile', 'mobile'),
        ('fax', 'fax'),
        ('email', 'E-mail'),
        ('url', 'url'),
        ('sms', 'sms')
    )

    SYS_USE = (
        ('H', 'home'),
        ('W', 'work'),
        ('T', 'temporary'),
        ('O', 'old'),
        ('P', 'personal')
    )

    system = models.CharField(max_length=12, choices=CONTACT_POINT_SYS)
    value = models.CharField(max_length=255)
    use = models.CharField(max_length=1, choices=SYS_USE)
    rank = models.PositiveSmallIntegerField()
    researcher = models.ForeignKey(Subject, related_name='contact_points', on_delete=models.CASCADE)


class OrganizationContactPoint(models.Model):
    CONTACT_POINT_SYS = (
        ('phone', 'phone'),
        ('fax', 'fax'),
        ('email', 'E-mail'),
        ('url', 'url'),
        ('sms', 'sms')
    )

    SYS_USE = (
        ('T', 'temporary'),
        ('O', 'old'),
        ('B', 'billing'),
        ('E', 'enquiry'),
    )

    system = models.CharField(max_length=5, choices=CONTACT_POINT_SYS)
    value = models.CharField(max_length=255)
    use = models.CharField(max_length=1, choices=SYS_USE, default='E')
    organization = models.ForeignKey(Organization, related_name='organization_contact_points', on_delete=models.CASCADE)


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=5)
    supplier = models.ForeignKey(Organization, on_delete=models.CASCADE)


class Specification(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    application = models.CharField(max_length=25)
    specification = models.JSONField(null=True)


class Project(models.Model):
    title = models.CharField(max_length=400)
    voteID = models.CharField(max_length=25)
    projectNumber = models.CharField(max_length=25)
    startDate = models.DateField()
    endDate = models.DateField()
    researchers = models.ManyToManyField(Subject, through='SubjectRole', through_fields=('project', 'subject'))
    consumables = models.ManyToManyField(Specification, through='Consumable',
                                         through_fields=('project', 'specification'))


class Consumable(models.Model):
    specification = models.ForeignKey(Specification, related_name='specifications', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='projects', on_delete=models.CASCADE)
    quantityRequired = models.IntegerField(default=1)
    quantityRemaining = models.IntegerField(default=0)
    unit = models.CharField(max_length=12, null=True)
    estimateCost = models.DecimalField
    justification = models.CharField(max_length=400, null=True)


class SubjectRole(models.Model):
    ROLE = (
        ('pi', 'Principal researcher'),
        ('co', 'Co researcher'),
        ('student', 'Research student'),
        ('so', 'Scientific officer'),
        ('employee', 'Company employee'),
    )

    organization = models.ForeignKey(Organization, related_name='organizations', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE)


class Vote(models.Model):
    voteNo = models.ForeignKey(Project, on_delete=models.CASCADE)
    items = models.JSONField(null=True)


class Initiation(models.Model):
    formNumber = models.CharField(max_length=12)
    revNo = models.IntegerField(default=0)
    effectiveDate = models.DateField(default=timezone.now)
    lineItem = models.ForeignKey(Consumable, on_delete=models.CASCADE)
    listOfSuppliers = models.JSONField(null=True)
    rfqSendDate = models.DateField(null=True)
    rfqCloseDate = models.DateField(null=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)


class InitiationRole(models.Model):
    ROLE = (
        ('prepare', 'Prepared by'),
        ('initiate', 'Initiated by'),
        ('supervisor', 'Approved by supervisor'),
        ('hod', 'Approved by HOD'),
    )

    role = models.CharField(max_length=12)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    initiation = models.ForeignKey(Initiation, on_delete=models.DO_NOTHING)
    date = models.DateField(default=timezone.now)
