from django.db import models

from common.models import CreatorBaseModel
from courses.models import Course


class PhysicalBook(CreatorBaseModel):
    def physical_book_location(self, filename):
        """Return dynamic location for physical book image.

        Parameters
        ----------
        filename : str
            name of the file

        Returns
        -------
        str
            Provides file path to upload image

        """

        return "physicalbook/{0}/{1}".format(self.course.id, filename)

    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to=physical_book_location, blank=True, null=True)
    course = models.ForeignKey(
        Course, related_name="physical_books", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        verbose_name = "Physical Book"
        verbose_name_plural = "Physical Books"
