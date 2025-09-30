from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AuthoritySource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(unique=True)),
                ("name", models.CharField(max_length=200)),
                ("version", models.CharField(blank=True, max_length=50)),
                ("url", models.URLField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["slug"]},
        ),
        migrations.CreateModel(
            name="Term",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(db_index=True, max_length=200)),
                ("type", models.CharField(choices=[("period", "Period/Epoch/Age"), ("formation", "Stratigraphic Unit"), ("lithology", "Lithology"), ("place", "Place/Toponym"), ("other", "Other")], default="other", max_length=20)),
                ("lang", models.CharField(default="en", max_length=8)),
                ("meta", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "source",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="terms", to="authority.authoritysource"),
                ),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Synonym",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(db_index=True, max_length=200)),
                ("lang", models.CharField(default="en", max_length=8)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "source",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="synonyms", to="authority.authoritysource"),
                ),
                (
                    "term",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="synonyms", to="authority.term"),
                ),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.AlterUniqueTogether(name="term", unique_together={("source", "name", "type", "lang")}),
        migrations.AlterUniqueTogether(name="synonym", unique_together={("source", "term", "name", "lang")}),
    ]

