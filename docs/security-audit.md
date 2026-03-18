# RockVault — Security Audit

Hands-on security audit of the RockVault application.
Each vulnerability is documented with proof of concept, impact analysis, and fix.

**Environment:** Local only — Ubuntu Server 24, FastAPI 0.3.0
**Audit started:** 2026-03-18
.
---

## Vulnerability 1 — Information Disclosure via Exposed API Documentation

**Severity:** Medium  
**Status:** Fixed ✅

### Description
The FastAPI application exposed its full API documentation publicly via:
- `/docs` — Swagger UI with interactive endpoint testing
- `/redoc` — ReDoc documentation
- `/openapi.json` — Full OpenAPI specification with all endpoints, schemas, and parameters

### Proof of Concept
```bash
curl http://192.168.1.119:8000/openapi.json
# Returns full API spec — all endpoints, methods, request schemas and error codes
```

### Impact
An attacker accessing `/openapi.json` obtains a complete map of the attack surface
without sending a single malicious request. Automated tools like `nuclei` and
`swagger-jacker` use this file to generate targeted attack payloads automatically.

### Fix
Added an HTTP middleware that intercepts requests to documentation endpoints
and returns 404 in non-development environments:
```python
@app.middleware("http")
async def block_docs_in_production(request: Request, call_next):
    if ENVIRONMENT != "development" and request.url.path in ["/docs", "/redoc", "/openapi.json"]:
        return JSONResponse(status_code=404, content={"detail": "Not found."})
    return await call_next(request)
```

Environment is controlled via `.env` file (not tracked by Git).

### Lessons Learned
- `docs_url=None` in FastAPI constructor did not fully disable the routes in v0.135.1
- Middleware-based blocking is more reliable than constructor parameters
- `.env` files must never be committed to version control