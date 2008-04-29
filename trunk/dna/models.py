from django.db.models import Model, CharField, DateField, FileField


class Sheet(Model):
    """
    Represents a manuscript bifolia. 
    
    Two pages appear on each sheet. 
    """
    
    name = CharField(max_length=32, unique=True)

    comments = TextField(null=True, blank=True)


class Photo(Model):
    """
    Associates a photograph with a sheet.
    """
    sheet = ForeignKey(Sheet)
    file = FileField()


class Session(Model):
    
    date = DateField(unique=True)

    comments = TextField(null=True, blank=True)


class Sample(Model):
    """
    Represents a DNA sample collected from a sheet.

    The X axis is horizontal along the lower edge of the sheet. 
    The Y axis is vertical at the center of the sheet.
    Hence, origo (0,0) is at the center of the lower edge of the sheet.
    Coordnates are stored in millimeters.

    Each sample is associated with the session during which it was collected.

    Each sample is optionally associated with a photo of the sample site.
    """

    sheet = ForeignKey(Sheet)
    x = IntegerField()
    y = IntegerField()
    session = ForeignKey(Session)
    photo = ForeignKey(Photo)

    comments = TextField(null=True, blank=True)

    class Admin:
        pass


class Plate(Model):
    """
    Represents a plate of sample wells. 

    Each physical plate has 96 wells but some wells may not be used.
    """
   
    name = CharField(max_lengh=9, unique=True)


class Primer(Model):
    """
    01, 04, DL
    """
    
    name = CharField(max_length=2, primary_key=True)


class Well(Model):

    plate = ForeignKey(Plate)
    name = CharField(max_length=3)
    sample = ForeignKey(Sample)
    primer = ForeignKey(Primer)

    comments = TextField(null=True, blank=True)

    class Admin:
        pass

    class Meta:
        unique_together = ('plate', 'name')


class Sequencing(Model):
   
    well = ForeignKey(Well)

    comments = TextField(null=True, blank=True)


class Result(Model):

    well = ForeignKey(Well)

    comments = TextField(null=True, blank=True)


