# FM-001 — FastMoss Public / Pre-Auth Architecture

## Question

What public/pre-auth web application architecture is observable from the FastMoss entry surface before using an authenticated account?

## Status

**Answered sufficiently to proceed.** This experiment maps the public client architecture and authentication boundary. It does not attempt to reproduce business data or claim access to authenticated endpoints.

## Findings

### 1. Entry access is browser-context sensitive

A disposable headless Chromium reached `https://www.fastmoss.com/` but received a FastMoss-branded **Web Security** page asking for one more check. A separate ordinary headed Chromium with a disposable profile loaded the real FastMoss application without bypassing any control.

This establishes an edge/WAF behavior difference between browser contexts. It does not establish the WAF vendor or exact detection mechanism.

### 2. Public frontend architecture

REA bundle evidence identifies **Next.js** with high confidence and **React** with medium confidence. Runtime assets include Next.js App Router-style chunk paths such as:

```text
/_next/static/chunks/main-app-...
/_next/static/chunks/app/[locale]/layout-...
/_next/static/chunks/app/[locale]/(pureLayout)/page-...
/_next/static/chunks/app/[locale]/error-...
```

A stable bundle capture contained 119 script chunks and 42 endpoint observations/candidates. Static endpoint detection is useful for reconnaissance but is not a complete runtime call inventory.

### 3. First-party origin roles

Observed runtime traffic supports this coarse decomposition:

```text
www.fastmoss.com
  -> Next.js web application
  -> same-origin /api/* requests

uscdn.fastmoss.com
  -> images / logos / region assets / product media

tracking.fastmoss.com
  -> /api/notify/index telemetry calls
```

Third-party analytics/marketing traffic was also observed to Google, Clarity, LinkedIn, Reddit, Bing and related services. Those are not part of the core data backend model unless later evidence shows otherwise.

### 4. Static authentication/client contracts

The public shipped client contains static references to endpoints including:

```text
/api/user/login
/api/user/register
/api/user/index/userInfo
/api/user/userPayTrial
/api/user/user
/api/user/userExtend
/api/user/getTagsList
/api/oauth/bindAccount
/api/oauth/oauthBindLogin
/api/oauth/setGoogleAccount
/api/oauth/setTkAccount
/api/captcha/config
/api/captcha/verify
```

These are **shipped-client observations only**. Their presence does not establish that they are callable without authentication, that they return useful data, or that they represent the full authentication system.

### 5. Public runtime API calls

A controlled headed launch observed successful HTTP responses for public initialization requests including:

```text
GET /api/author/index/country
GET /api/info/pagerInfo        (multiple type values)
GET /api/info/handle           (multiple type values)
GET /api/user/index/userInfo
POST https://tracking.fastmoss.com/api/notify/index
```

FM-001 did **not** retain response bodies for these calls. HTTP 200 therefore proves only that the request completed with that HTTP status in this browser context; it does not prove response semantics or access to authenticated business data.

### 6. Public information architecture

The public page links directly to major product surfaces including:

```text
/dashboard
/e-commerce/saleslist
/e-commerce/search
/influencer/search
/shop-marketing/search
/shop-marketing/tiktok
/live/search
/live/tiktok
/media-source/video
/creativecenter/search
/monitor/videoMonitor
/pricing
```

It also exposes AI-oriented surfaces and links to the separate public developer site for **MCP / CLI / API**.

A visible `Inicie o Teste Gratuito` button has no simple anchor URL in the observed DOM. Its behavior should be investigated as a separate bounded authentication-boundary experiment rather than inferred here.

### 7. Locale behavior is contextual

The manually launched headed browser resolved to `/pt`, while the REA-controlled headed launch remained at `/`. Locale/profile/browser context therefore affects route selection. `/pt` must not be treated as the universal canonical root.

### 8. Source maps

No usable source maps were observed/fetched from the real FastMoss bundle during FM-001. Our methodology must therefore work with minified shipped chunks, static recovery, runtime initiators and execution coverage rather than depend on source maps.

## Tool behavior learned during FM-001

`inspect-web-page` is intentionally unsuitable for surviving a full page reload:

- with script-source capture enabled, a reload produced a stale `script_id` race (`Debugger.getScriptSource: No script for id`);
- without source capture, navigation correctly terminated the inspection as `target_changed`.

For initial navigation/reload capture, use `capture-browser-scenario`; use `inspect-web-page` on a stable page state.

## Evidence classes

The experiment keeps three separate inventories:

- `artifacts/static-api-endpoints.json` — things shipped in client code;
- `artifacts/runtime-api-endpoints.json` — requests actually observed during controlled public startup;
- `artifacts/dom-actions.json` — links/buttons observed in the loaded public DOM using a CDP helper.

Do not merge these evidence classes into one “API list.”

## Architectural interpretation

The simplest model supported by current evidence is:

```text
Edge / Web Security behavior
        ↓
Next.js + React web client
        ↓
same-origin /api/* application backend
        ├── public/init information
        ├── user/auth contracts
        └── later business-domain APIs (not yet mapped)
        ↓
first-party CDN + tracking services
```

There is not yet evidence for a more exotic backend topology. We will add complexity only when observations require it.

## Unknowns carried forward

- What exact client action opens/controls trial/login state?
- Which major product routes are usable pre-auth, and what happens when they are entered directly?
- Which business-domain endpoints are called by Product Search, Product Detail, Creator, Shop, Video and LIVE?
- Which endpoint families require a valid authenticated user state?
- What request signing, nonce, timestamp or client middleware semantics are present around `_time` and `cnonce`?
- Which values are computed client-side versus returned server-side?

## Next experiment

**FM-002 — Product Search public/auth boundary.**

Question: when navigating through the public `Pesquisar produtos do TikTok` surface, what exact route transition, authentication gate, network requests and client modules are observed, and where does unauthenticated navigation stop?
