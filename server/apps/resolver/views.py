from typing import Any, Dict, Optional

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authority.models import Term, Synonym


class PingView(APIView):
    permission_classes = [AllowAny]

    def get(self, _request, *args, **kwargs):  # type: ignore[no-untyped-def]
        return Response({"status": "ok", "service": "resolver"})


class ResolveView(APIView):
    permission_classes = [AllowAny]

    def _resolve_db(self, q: str) -> Optional[Dict[str, Any]]:
        if not q:
            return None
        # Exact match on Term
        t = Term.objects.filter(name__iexact=q).first()
        if t:
            return {
                "standard_name": t.name,
                "confidence": 1.0,
                "source": t.source.slug,
                "type": t.type,
            }
        # Exact match on Synonym
        s = Synonym.objects.select_related("term", "source").filter(name__iexact=q).first()
        if s:
            return {
                "standard_name": s.term.name,
                "confidence": 0.95,
                "source": s.source.slug,
                "type": s.term.type,
            }
        # Fallback: partial contains on Term
        t2 = Term.objects.filter(name__icontains=q).first()
        if t2:
            return {
                "standard_name": t2.name,
                "confidence": 0.6,
                "source": t2.source.slug,
                "type": t2.type,
            }
        return None

    def get(self, request, *args, **kwargs):  # type: ignore[no-untyped-def]
        q = request.GET.get("q", "").strip()
        db_hit = self._resolve_db(q)
        if db_hit:
            payload = {"query": q, **db_hit}
        else:
            payload = {
                "query": q,
                "standard_name": q.title() if q else None,
                "confidence": 0.5 if q else 0.0,
                "source": "demo",
            }
        return Response(payload)
