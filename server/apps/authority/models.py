from django.db import models


class AuthoritySource(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["slug"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name} ({self.version})"


class Term(models.Model):
    TYPE_CHOICES = (
        ("period", "Period/Epoch/Age"),
        ("formation", "Stratigraphic Unit"),
        ("lithology", "Lithology"),
        ("place", "Place/Toponym"),
        ("other", "Other"),
    )

    source = models.ForeignKey(AuthoritySource, on_delete=models.CASCADE, related_name="terms")
    name = models.CharField(max_length=200, db_index=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="other")
    lang = models.CharField(max_length=8, default="en")
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("source", "name", "type", "lang")
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Synonym(models.Model):
    source = models.ForeignKey(AuthoritySource, on_delete=models.CASCADE, related_name="synonyms")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="synonyms")
    name = models.CharField(max_length=200, db_index=True)
    lang = models.CharField(max_length=8, default="en")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("source", "term", "name", "lang")
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover
        return self.name

