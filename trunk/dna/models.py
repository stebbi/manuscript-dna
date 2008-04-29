from django.db.models import Model, CharField, DateField, FileField


class Sheet(Model):
    """
    Represents a manuscript bifolia. 
    
    Two pages are written on each sheet. 

    DNA samples are collected from the sheets, at recorded coordinates.
    """
   
    # The public identifier for the sheet 
    # (TODO Example identifier)
    name = CharField(max_length=32, unique=True)

    # Free text comments about the sheet 
    comments = TextField(null=True, blank=True)


class Photo(Model):
    """
    Associates a photograph with a sheet.

    Photographs can show an entire sheet but are more usually taken with 
    a microscope and associated with a particular sample.
    """

    # The sheet (partially) shown in the photograph
    sheet = ForeignKey(Sheet)

    # The photograph itself, in a format identified by the file extension
    file = FileField()


class Session(Model):
    """
    Represents a work session identified by the corresponding date.
    """
    
    # The date of the work session 
    date = DateField(unique=True)

    # Free text comments about the session 
    comments = TextField(null=True, blank=True)


class Sample(Model):
    """
    Represents a DNA sample collected from a sheet.

    Each sample is associated with the X-Y coordinates on the sheet.
    The X axis is horizontal along the lower edge of the sheet. 
    The Y axis is vertical at the center of the sheet.
    Origo (0,0) is at the center of the lower edge of the sheet.
    The reference frame is measured in millimeters.

    Each sample is associated with the session during which it was collected.

    Each sample is optionally associated with a photo of the sample site.

    Each sample has a human-readable unique identifier composed from the 
    sheet name, the session name and internal serial number for the sample.
    """

    sheet = ForeignKey(Sheet)

    # Location on the X-axis, in millimeters  
    x = IntegerField()
    # Location on the Y-axis, in millimeters 
    y = IntegerField()

    # The work session during which the sample was collected 
    session = ForeignKey(Session)

    # A (required) photo of the sample site on the sheet
    photo = ForeignKey(Photo)

    # Free text comments about the sample
    comments = TextField(null=True, blank=True)

    class Admin:
        pass

    def _getname(self):
        return u'%s-%s-%s' % (self.sheet.name, self.session.name, str(self.pk))

    # The human-readable identifier for the sample
    name = property(_getname)


class Plate(Model):
    """
    Represents a plate of sample wells. 

    Each physical plate has 96 wells but some wells may not be used.
    """
    
    # The unique string identifying the plate
    name = CharField(max_lengh=9, unique=True)


class Primer(Model):
    """
    01, 04, DL

    """
    # TODO flesh out the docstring explanation
   
    # One of 01, 04 or DL
    name = CharField(max_length=2, primary_key=True)


class Well(Model):
    """
    Represents a sample well in a plate. 

    Each plate has 96 wells but some wells may not be used.

    Each well in use stores exactly one sample.

    Each well is identified by a three letter name that records its location 
    in the plate, ranging from A01 to H12.
    """

    # The plate that the well belongs to
    plate = ForeignKey(Plate)

    # The three letter identifier for the well in the plate
    name = CharField(max_length=3)

    # The sample stored in the well
    sample = ForeignKey(Sample)

    # The primer used for the sample
    primer = ForeignKey(Primer)

    # Free text comments about the well
    comments = TextField(null=True, blank=True)

    class Admin:
        pass

    class Meta:
        unique_together = ('plate', 'name')


class Sequencing(Model):
    # TODO

    well = ForeignKey(Well)

    comments = TextField(null=True, blank=True)


class Result(Model):
    # TODO
    
    well = ForeignKey(Well)

    comments = TextField(null=True, blank=True)


