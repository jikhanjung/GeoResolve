import csv
from pathlib import Path
from typing import Dict

from django.core.management.base import BaseCommand, CommandError

from apps.authority.models import AuthoritySource, Term, Synonym


class Command(BaseCommand):
    help = "Load authority terms and synonyms from a directory containing terms.csv and synonyms.csv"

    def add_arguments(self, parser):  # type: ignore[no-untyped-def]
        parser.add_argument("root", nargs="?", default="data/ics/2023", help="Directory path")
        parser.add_argument("--slug", default="ics-2023", help="Authority source slug")
        parser.add_argument("--name", default="ICS", help="Authority name")
        parser.add_argument("--version", default="2023", help="Authority version")

    def handle(self, root: str, slug: str, name: str, version: str, *args, **options):  # type: ignore[no-untyped-def]
        root_path = Path(root)
        if not root_path.exists():
            raise CommandError(f"Directory not found: {root}")

        terms_csv = root_path / "terms.csv"
        syn_csv = root_path / "synonyms.csv"
        if not terms_csv.exists():
            raise CommandError(f"Missing terms.csv in {root}")

        source, _ = AuthoritySource.objects.get_or_create(slug=slug, defaults={"name": name, "version": version})
        if source.version != version:
            source.version = version
            source.save()

        # Cache created terms by (name,type,lang) key
        key_to_term: Dict[str, Term] = {}

        with terms_csv.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("name", "").strip()
                ttype = row.get("type", "other").strip() or "other"
                lang = row.get("lang", "en").strip() or "en"
                if not name:
                    continue
                term, _ = Term.objects.get_or_create(source=source, name=name, type=ttype, lang=lang)
                key_to_term[f"{name}\t{ttype}\t{lang}"] = term

        if syn_csv.exists():
            with syn_csv.open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    s_name = row.get("name", "").strip()
                    target = row.get("target", "").strip()
                    ttype = row.get("type", "other").strip() or "other"
                    lang = row.get("lang", "en").strip() or "en"
                    if not s_name or not target:
                        continue
                    term = key_to_term.get(f"{target}\t{ttype}\t{lang}")
                    if not term:
                        # Create the target term on the fly if missing
                        term, _ = Term.objects.get_or_create(source=source, name=target, type=ttype, lang=lang)
                        key_to_term[f"{target}\t{ttype}\t{lang}"] = term
                    Synonym.objects.get_or_create(source=source, term=term, name=s_name, lang=lang)

        self.stdout.write(self.style.SUCCESS(f"Loaded authority data from {root}"))

