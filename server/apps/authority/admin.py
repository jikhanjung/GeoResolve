from django.contrib import admin
from .models import AuthoritySource, Term, Synonym


@admin.register(AuthoritySource)
class AuthoritySourceAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "version", "is_active")
    search_fields = ("slug", "name", "version")


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "lang", "source")
    list_filter = ("type", "lang", "source")
    search_fields = ("name",)


@admin.register(Synonym)
class SynonymAdmin(admin.ModelAdmin):
    list_display = ("name", "lang", "term", "source")
    list_filter = ("lang", "source")
    search_fields = ("name", "term__name")

