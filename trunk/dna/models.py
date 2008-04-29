# coding=utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

"""
The primary elements of the data model are

    Sheet - represents a sheet (bifolia) in a manuscript
    
    Sample - represents a sample collected from a sheet
    
    Plate, Well - represents a plate containing 96 sample wells
    
    Sequencing - stores the measurement results for a well
    
    Result - records the final result for a sample
"""


from django.db.models import Model, CharField, DateField, ImageField, \
    ForeignKey, IntegerField, TextField


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
    
    class Admin:
        list_display = ('name',)

    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __unicode__(self):
        return self.name
    

class Session(Model):
    """
    Represents a work session identified by the corresponding date.
    """
    
    # The date of the work session 
    date = DateField(unique=True)

    # Free text comments about the session 
    comments = TextField(null=True, blank=True)

    class Admin:
        list_display = ('date',)

    def _getname(self):
        return unicode(self.date)
    name = property(_getname)

    def __eq__(self, other):
        return self.date == other.date
    
    def __hash__(self):
        return hash(self.date)
    
    def __unicode__(self):
        return self.name
    

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

    # Free text comments about the sample
    comments = TextField(null=True, blank=True)

    class Admin:
        list_display = ('name', 'sheet', 'x', 'y',)

    # The human-readable identifier for the sample
    def _getname(self):
        return u'-'.join((self.sheet.name, self.session.name, str(self.pk)))
    name = property(_getname)

    def __unicode__(self):
        return self.name
    

class Photo(Model):
    """
    Associates a photograph with a sample site on a sheet.
    """

    # The sample site shown in the photograph
    sample = ForeignKey(Sample, edit_inline=True, num_in_admin=1)

    # The photograph itself, in a format identified by the file extension
    file = ImageField(upload_to='manuscript-dna/photos/', core=True)
    
    def __unicode__(self):
        return self.get_file_url()


class Plate(Model):
    """
    Represents a plate of sample wells. 

    Each physical plate has 96 wells but some wells may not be used.
    """
    
    # The unique string identifying the plate
    name = CharField(max_length=9, unique=True)

    class Admin:
        list_display = ('name',)

    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __unicode__(self):
        return self.name
    

WELL_CHOICES = []
for i in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'):
    for j in ('01', '02', '03', '04', '05', '06', 
              '07', '08', '09', '10', '11', '12'):
        WELL_CHOICES.append((i + j, i + j))
        
PRIMER_CHOICES = (('01', '01'), ('04', '04'), ('DL', 'DL'))
    

class Well(Model):
    """
    Represents a sample well in a plate. 

    Each plate has 96 wells but some wells may not be used.

    Each well in use stores exactly one sample.

    Each well is identified by a three letter name that records its location 
    in the plate, ranging from A01 to H12.
    """

    # The plate that the well belongs to
    plate = ForeignKey(Plate, edit_inline=True, num_in_admin=1)

    # The three letter identifier for the well in the plate
    name = CharField(max_length=3, choices=WELL_CHOICES, core=True)

    # The sample stored in the well
    sample = ForeignKey(Sample)

    # The primer used for the sample in the well
    primer = CharField(max_length=2, choices=PRIMER_CHOICES, core=True)

    # Free text comments about the well
    comments = CharField(max_length=256, null=True, blank=True)

    class Meta:
        unique_together = ('plate', 'name')

    def __eq__(self, other):
        return self.plate == other.plate and self.name == other.name
    
    def __hash__(self):
        return hash(u'-'.join((self.plate.name, self.name)))
    
    def __unicode__(self):
        return self.name
    

class Sequencing(Model):
    # TODO

    well = ForeignKey(Well, edit_inline=True, num_in_admin=1)

    comments = TextField(null=True, blank=True, core=True)

    class Admin:
        pass


class Result(Model):
    # TODO
    
    well = ForeignKey(Well)

    comments = TextField(null=True, blank=True)

    class Admin:
        pass


