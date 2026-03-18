# HTTP Deep Dive — Study Notes

Hands-on study of HTTP fundamentals using the RockVault API as a live target.
All tests performed with `curl` against the local FastAPI backend.

---

## 1. Reading Server Logs

Every HTTP request leaves a trace in the server log:
```
INFO: 192.168.1.247:51093 - "GET /health HTTP/1.1" 200 OK
```

| Part | Meaning |
|---|---|
| `192.168.1.247` | Client IP address |
| `51093` | Ephemeral source port — randomly assigned per connection |
| `GET` | HTTP method |
| `/health` | Requested path |
| `HTTP/1.1` | Protocol version |
| `200 OK` | Response status code |

The source port changes on every request. The destination port (8000) is always fixed.

---

## 2. Anatomy of an HTTP Request (curl -v)
```
> GET /health HTTP/1.1        ← method, path, protocol
> Host: 192.168.1.119:8000    ← target server
> User-Agent: curl/8.5.0      ← client identification
> Accept: */*                 ← accepted response formats
```

The `>` prefix means outgoing (client → server).
The `<` prefix means incoming (server → client).
The `*` prefix means curl internal connection info.

---

## 3. Headers Can Be Faked

Any header can be overridden with `-H`:
```bash
curl http://host/health \
  -H "User-Agent: Mozilla/5.0 (totally-not-an-attacker)" \
  -H "X-Custom-Header: hello"
```

The server accepted both without complaint — **headers are not validated by default.**

**Security implication:** User-Agent based bot detection is trivially bypassed.
Custom headers can be used to probe server behavior or attempt injection attacks.

---

## 4. X-Forwarded-For Header
```bash
curl http://host/health -H "X-Forwarded-For: 10.0.0.1"
```

The uvicorn log still showed the real IP. The injected header was ignored.

**Why this matters:** In production environments behind a reverse proxy (Nginx,
Cloudflare), the app must trust `X-Forwarded-For` to know the real client IP.
If an app trusts this header without a proxy, an attacker can spoof their IP —
bypassing IP-based rate limiting or access control.

---

## 5. The OpenAPI Spec as an Attack Surface

Accessing `/openapi.json` returns the full API specification:
- All endpoints and their paths
- Accepted HTTP methods
- Request body schemas
- Possible response codes

**Security implication:** This is reconnaissance gold. Automated tools use this
file to map the entire attack surface of an API without sending a single
malicious request. Exposing `/docs` and `/openapi.json` publicly in production
is a serious misconfiguration.

**Planned fix (Phase 5):** Disable or restrict access to API documentation
in production mode.

---

## 6. Content-Type and the 422 Error

Sending a POST request without `Content-Type: application/json`:
```bash
curl -d '{"url": "..."}' http://host/download
```

curl defaulted to `application/x-www-form-urlencoded`. The server received
the body but could not extract the `url` field — returning **422 Unprocessable Entity**.

| Status | Meaning |
|---|---|
| `400 Bad Request` | Server understood the request but rejected it (invalid YouTube URL) |
| `422 Unprocessable Entity` | Server understood the format but failed to process the content |

`Content-Type` is a contract between client and server — it tells the server
how to interpret the request body. A mismatch causes processing failure.

**Security implication:** Content-Type confusion can be used to bypass input
validation in poorly implemented parsers.

---

## Tools Used

- `curl` — command line HTTP client
- `curl -v` — verbose mode, shows full request and response headers
- `curl -H` — inject or override request headers
- `curl -d` — send request body (POST)
- `/openapi.json` — FastAPI's auto-generated API specification