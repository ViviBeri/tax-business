#!/usr/bin/env python3
"""KVB ENTERPRISES site generator. Usage: python3 _builder/build.py
Edit _builder/prices.json (e.g. {"gst": "999"}) then rebuild. Empty price = "Get a quote"."""
import os, sys, glob, html, json, datetime, urllib.parse as U

B = os.path.dirname(os.path.abspath(__file__))
O = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(B)
S = "https://viviberi.github.io/tax-business"
GA = "G-KFP95JFETM"
PH = "919003633696"
TD = datetime.date.today()
E = lambda s: html.escape(s, True)
LANG = "en"
try:
    PR = json.load(open(os.path.join(B, "prices.json"), encoding="utf-8"))
except Exception:
    PR = {}

def has(p):
    """True when a hand-written page/asset exists in the output tree."""
    return os.path.exists(os.path.join(O, p))

def w(p, c):
    p = os.path.join(O, p)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(c)

def T(tag, en, ta=None, cls="", x=""):
    c = f' class="{cls}"' if cls else ""
    x = " " + x if x else ""
    return f"<{tag}{c}{x}>{ta if (LANG == 'ta' and ta) else en}</{tag}>"

def wa(m):
    return f"https://wa.me/{PH}?text=" + U.quote(L(m))

ICON = ('<svg class="wa-ico" viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>')

SV = [
 ("gst", "GST Services", "GST சேவைகள்", "Registration, returns, monthly compliance, amendments, cancellation and reconciliation assistance.", "பதிவு, ரிட்டர்ன் தாக்கல், மாதாந்திர இணக்கம், திருத்தம் மற்றும் ரத்து உதவி.",
  ["GST registration assistance", "GSTR-1 and GSTR-3B filing support", "Monthly GST compliance", "Amendment and cancellation assistance", "Reconciliation and documentation support"],
  ["PAN and Aadhaar of the proprietor, partners or directors", "Passport-size photograph", "Business address proof (for example rent agreement or electricity bill)", "Bank account details"]),
 ("itr", "Income Tax / ITR", "வருமான வரி / ITR", "Individual and business ITR preparation, tax compliance support and CA coordination where required.", "தனிநபர் மற்றும் வணிக ITR தயாரிப்பு மற்றும் வரி இணக்க உதவி.",
  ["Individual ITR filing", "Business and professional ITR filing", "Tax compliance support", "Tax audit support, coordinated through a Chartered Accountant where required"],
  ["PAN and Aadhaar", "Form 16 or income details", "Bank statements and interest certificates", "Investment and deduction proofs", "For business: turnover and expense details"]),
 ("fssai", "FSSAI", "FSSAI", "New registration/licence, renewal and modification assistance for eligible food businesses.", "உணவு வணிகங்களுக்கான புதிய பதிவு/உரிமம், புதுப்பிப்பு மற்றும் மாற்ற உதவி.",
  ["New FSSAI registration or licence", "Renewal assistance", "Modification and updates", "Guidance on which type suits your food business"],
  ["Photo ID and passport-size photograph", "Business address proof", "Details of food products or activities", "Premises details"]),
 ("pan", "PAN Card Services", "PAN அட்டை சேவைகள்", "New PAN, correction, address/details update and related assistance.", "புதிய PAN, திருத்தம் மற்றும் விவரங்கள் புதுப்பிப்பு உதவி.",
  ["New PAN application", "Correction of details", "Address and details update"],
  ["Identity proof and address proof", "Passport-size photograph", "For corrections: existing PAN and supporting documents"]),
 ("msme", "MSME / Udyam", "MSME / உத்யம்", "Udyam registration, update and documentation assistance for eligible businesses.", "தகுதியான வணிகங்களுக்கு உத்யம் பதிவு மற்றும் புதுப்பிப்பு உதவி.",
  ["Udyam registration", "Updates to existing registration", "Documentation support"],
  ["Aadhaar of the owner", "PAN", "Business and bank details", "GSTIN, if you have one"]),
 ("trademark", "Trademark", "வர்த்தக முத்திரை", "Trademark search, application filing and registration guidance.", "வர்த்தக முத்திரை தேடல், விண்ணப்பம் மற்றும் பதிவு வழிகாட்டுதல்.",
  ["Trademark search", "Application filing", "Registration guidance"],
  ["Brand name or logo", "Applicant identity and address proof", "Business details"]),
 ("dsc", "Digital Signature (DSC)", "டிஜிட்டல் கையொப்பம் (DSC)", "DSC application, renewal and related assistance.", "DSC விண்ணப்பம், புதுப்பிப்பு மற்றும் தொடர்புடைய உதவி.",
  ["New DSC application", "DSC renewal", "Help with related filings"],
  ["PAN and Aadhaar", "Passport-size photograph", "Mobile number and email ID"]),
 ("business-registration", "Business Registration", "வணிக பதிவு", "Business setup and registration support based on your business structure.", "உங்கள் வணிக அமைப்புக்கு ஏற்ற பதிவு மற்றும் தொடக்க உதவி.",
  ["Guidance on choosing a business structure", "Registration and documentation support", "Help identifying other registrations that may apply"],
  ["Identity and address proof of owners, partners or directors", "Business address proof", "Proposed business name and activity details"]),
]
SHORT = {"gst": "GST", "itr": "ITR", "fssai": "FSSAI", "pan": "PAN", "msme": "MSME", "trademark": "TM", "dsc": "DSC", "business-registration": "Business"}
LOCS = ["puducherry", "villupuram", "cuddalore", "tindivanam", "panruti", "karaikal", "tiruvannamalai", "chidambaram", "mayiladuthurai"]
TOOLS = [("gst-calculator", "GST Calculator", "Calculate GST-inclusive or GST-exclusive amounts.", "Open tool →"),
         ("gst-checklist", "GST Registration Checklist", "Common documents and information to keep ready.", "Open checklist →"),
         ("fssai-checklist", "FSSAI Checklist", "Basic information commonly required for food-business applications.", "Open checklist →"),
         ("itr-checklist", "ITR Document Checklist", "Prepare common documents before starting your return.", "Open checklist →"),
         ("business-compliance-checker", "What Does My Business Need?", "A first-pass checklist of common registrations and compliance areas.", "Open tool →"),
         ("gst-eligibility-checker", "GST Registration Eligibility Guide", "An indicative guide to whether GST registration may apply to you.", "Open tool →"),
         ("fssai-type-finder", "FSSAI Type Finder", "Find the likely FSSAI registration or licence category.", "Open tool →"),
         ("msme-category-checker", "MSME Category Checker", "Check Micro, Small or Medium category from investment and turnover.", "Open tool →")]
NOTE_EN = "Final quote is confirmed after reviewing your requirements and documents. Government/statutory charges, where applicable, may be separate."
NOTE_TA = "உங்கள் தேவைகள் மற்றும் ஆவணங்களை பரிசீலித்த பின் இறுதி விலை உறுதி செய்யப்படும். பொருந்தும் இடங்களில் அரசு/சட்டபூர்வ கட்டணங்கள் தனியாக இருக்கலாம்."
NAV = [("services", "Services", "சேவைகள்"), ("business", "Who We Help", "யாருக்கு உதவுகிறோம்"), ("locations", "Locations", "சேவை பகுதிகள்"),
       ("tools", "Free Tools", "இலவச கருவிகள்"), ("about", "About Us", "எங்களைப் பற்றி"), ("contact", "Contact", "தொடர்பு")]

TILE_ICONS = {
  "gst": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/></svg>',
  "itr": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M12 8v8M9.5 10.5h5M9.5 13.5h5"/></svg>',
  "fssai": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 4.5-3.4 7.8-8 9-4.6-1.2-8-4.5-8-9V6l8-3z"/><path d="M9 12l2 2 4-4"/></svg>',
  "pan": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="9" cy="12" r="2"/><path d="M14 11h5M14 14h4"/></svg>',
  "msme": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 21V10l5-3v14M9 21V7l6-3v17M15 21V9l5 3v9"/></svg>',
  "trademark": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M8 10h3v6M13 16V10h3M13 13h2"/></svg>',
  "dsc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 18v-8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8M4 18h16M12 12v6"/><circle cx="12" cy="9" r="1.5"/></svg>',
  "business-registration": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V7l7-4 7 4v14M9 21v-5h6v5"/></svg>',
}
TILE_ICON_FALLBACKS = {
  "gst": "📄",
  "itr": "📑",
  "fssai": "🛡️",
  "pan": "🪪",
  "msme": "🏢",
  "trademark": "™",
  "dsc": "✍️",
  "business-registration": "🏬",
}

def service_icon(slug):
    """Return a self-contained service SVG, with an accessible Unicode fallback."""
    icon = TILE_ICONS.get(slug, "")
    if icon.startswith("<svg") and icon.endswith("</svg>"):
        return icon
    fallback = TILE_ICON_FALLBACKS.get(slug, "📄")
    return f'<span class="service-icon-fallback" aria-hidden="true">{fallback}</span>'

TILE_CAPTION = {
  "gst": ("Registration &amp; Filing", "பதிவு &amp; தாக்கல்"),
  "itr": ("ITR Services", "ITR சேவைகள்"),
  "fssai": ("Registration &amp; Renewal", "பதிவு &amp; புதுப்பிப்பு"),
  "pan": ("Assistance", "உதவி"),
  "msme": ("Udyam Registration", "உத்யம் பதிவு"),
  "trademark": ("Registration", "பதிவு"),
  "dsc": ("Digital Signature", "டிஜிட்டல் கையொப்பம்"),
  "business-registration": ("Registration", "பதிவு"),
}
TILE_COLOR = {"gst": "gst", "itr": "itr", "fssai": "fssai", "pan": "pan", "msme": "msme", "trademark": "tm", "dsc": "dsc", "business-registration": "biz"}

def head(r, title, desc, path, ld="", alts=None):
    """Return the <head> markup: metadata, canonical/hreflang, Open Graph, stylesheets, GA4 and optional JSON-LD."""
    u = f"{S}/{path}"
    alt = "".join(f'<link rel="alternate" hreflang="{h}" href="{S}/{q}">' for h, q in (alts or []))
    locale = "ta_IN" if LANG == "ta" else "en_IN"
    return (f'<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark">'
            f'<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#f5f8f6">'
            f'<link rel="canonical" href="{u}"><meta property="og:type" content="website"><meta property="og:site_name" content="KVB ENTERPRISES">'
            f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{u}">'
            f'<meta property="og:image" content="{S}/assets/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="{locale}"><meta name="twitter:card" content="summary_large_image">{alt}<link rel="icon" type="image/png" href="{r}assets/logo.png">'
            f'<link rel="stylesheet" href="{r}style.css"><link rel="stylesheet" href="{r}theme.css?v=header-balance-2"><link rel="stylesheet" href="{r}design-system.css"><link rel="stylesheet" href="{r}homepage-redesign.css?v=25"><link rel="stylesheet" href="{r}styles/glass.css?v=mobile-timeline-flow-20261111"><link rel="stylesheet" href="{r}styles/astryx-foundations.css?v=2"><link rel="stylesheet" href="{r}styles/kvb-editorial-v2.css?v=1"><link rel="stylesheet" href="{r}site-quality-fix.css?v=5"><link rel="stylesheet" href="{r}styles/taste-direction.css?v=2"><link rel="stylesheet" href="{r}styles/kvb-premium-pass.css?v=10"><script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>'
            f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA}');</script>{ld}</head><body><noscript class=\"noscript-notice\">{T('span', 'JavaScript is disabled. All service information and contact links remain available.', 'JavaScript முடக்கப்பட்டுள்ளது. அனைத்து சேவைத் தகவல்களும் தொடர்பு இணைப்புகளும் கிடைக்கும்.')}</noscript>")

def header(r, alt=None, lang_fallback=None):
    home = r + ("ta/" if LANG == "ta" else "") + "index.html"
    n = "".join(T("a", en, ta, x=f'href="{home}#{i}"') for i, en, ta in NAV)
    hreflang = "en" if LANG == "ta" else "ta"
    lang_attr = "en" if LANG == "ta" else "ta"
    lang_label = "English" if LANG == "ta" else "தமிழ்"
    lg = (f'<a class="lang" href="{alt}" hreflang="{hreflang}" lang="{lang_attr}">{lang_label}</a>' if alt else
          f'<a class="lang" href="{lang_fallback}" lang="ta">தமிழ்</a>' if lang_fallback else "")
    return (f'<header class="topbar"><div class="wrap nav"><a class="brand" href="{home}" aria-label="KVB ENTERPRISES home">'
            f'<img src="{r}assets/logo.png" alt="KVB ENTERPRISES logo" width="56" height="47"><span><b>KVB</b> ENTERPRISES<small>{L("Tax &amp; Business Compliance")}</small></span></a>'
            f'<div class="nav-right"><nav id="mainNav" aria-label="Main navigation">{n}</nav>{lg}'
            f'<button class="menu" id="menuBtn" type="button" aria-label="Open menu" aria-controls="mainNav" aria-expanded="false">☰</button></div></div></header>')

def foot(r):
    bar = (f'<div class="mbar"><a href="{wa("Hello Vivian, I would like to know about your services.")}" target="_blank" rel="noopener" data-loc="mobile-bar">{ICON}WhatsApp</a>'
           + T("a", "Call", "அழைக்க", x=f'href="tel:+{PH}" data-loc="mobile-bar"') + '</div>')
    return (bar + f'<a class="floating-wa" href="{wa("Hello Vivian, I would like to know about your services.")}" target="_blank" rel="noopener" aria-label="WhatsApp KVB ENTERPRISES" data-loc="floating">{ICON}</a>'
            f'<img class="footer-wave" src="{r}assets/footer-wave.svg" width="1180" height="140" alt="" aria-hidden="true" loading="lazy" decoding="async"><footer><div class="wrap footer"><div class="footer-brand"><img src="{r}assets/logo.png" alt="KVB ENTERPRISES logo" width="44" height="44" loading="lazy">'
            f'<div><b>KVB ENTERPRISES</b><p>{L("Tax &amp; Business Compliance Services")}</p></div></div>'
            f'<div>GST • ITR • FSSAI • PAN • MSME • Trademark • DSC<br>{L("Puducherry &amp; nearby areas")}</div>'
            f'<div><a href="{r}privacy.html">Privacy</a> • <a href="{r}terms.html">Terms</a><br>© <span class="yr">{TD.year}</span> KVB ENTERPRISES</div></div></footer>'
            f'<script src="{r}script.js?v=menu-fix-6" defer></script><script src="{r}scripts/scroll-craft.js?v=3" defer></script><script type="module" src="{r}scripts/scroll.js"></script><script type="module" src="{r}scripts/multiscroll.js"></script><script type="module" src="{r}scripts/three-hero.js?v=2"></script></body></html>')

def btn(href, en, ta, cls="primary", loc="", ico=False, ext=True):
    t = ' target="_blank" rel="noopener"' if ext else ""
    icon_html = ICON if ico else ""
    label = ta if (LANG == "ta" and ta) else en
    return f'<a class="btn {cls}" href="{href}"{t} data-loc="{loc}">{icon_html}<span>{label}</span></a>'

def price(s):
    L = PR.get(s) or []
    if not L:
        return T("em", "Get a quote", "விலை விவரம் பெறுக", "price")
    en = "<br>".join(f"{a} from ₹{c}{d}" for a, b, c, d in L)
    ta = "<br>".join(f"{b or a} ₹{c}{d.replace('/month', '/மாதம்')} முதல்" for a, b, c, d in L)
    return T("em", en, ta, "price")

STEPS = [("WhatsApp us", "WhatsApp செய்யுங்கள்", "Tell us what service you need.", "உங்களுக்குத் தேவையான சேவையைச் சொல்லுங்கள்."),
         ("Share documents", "ஆவணங்களை பகிருங்கள்", "We'll tell you exactly which documents are required.", "தேவையான ஆவணங்கள் என்னவென்று தெளிவாகச் சொல்வோம்."),
         ("We process and update you", "நாங்கள் செயல்படுத்தி தகவல் தருவோம்", "We handle the process and keep you updated.", "செயல்முறையை நாங்கள் கையாண்டு உங்களுக்கு தகவல் தருவோம்.")]

def steps():
    return '<div class="steps">' + "".join(
        f'<div class="step"><b>{i+1}</b>{T("h3", a, b)}{T("p", c, d)}</div>' for i, (a, b, c, d) in enumerate(STEPS)) + "</div>"

FAQ = [
 ("Do you provide services outside Puducherry?", "Yes. We assist clients in nearby areas including Villupuram, Cuddalore, Tindivanam, Panruti, Karaikal and other listed locations. Contact us to confirm availability."),
 ("How do I know the price?", "Each service shows a starting price where available. " + NOTE_EN),
 ("Can you help with a new business?", "Yes. We can help you understand the registrations and documentation relevant to your business type."),
 ("Do I need GST for a home bakery?", "It depends on your circumstances. GST applicability can depend on factors such as turnover and the nature of your supplies, and FSSAI requirements are a separate matter. If you're starting a home bakery, we can help you review GST, FSSAI, Udyam and other registrations that may apply before you begin."),
 ("What documents will I need?", "It depends on the service and your business type. Each service page lists commonly needed documents, and we confirm the exact list for your case on WhatsApp."),
 ("What are your working hours?", "WhatsApp enquiries are welcome at any time. We reply as soon as we can."),
 ("Is KVB ENTERPRISES a government office?", "No. KVB ENTERPRISES is an independent professional assistance service and is not a government department."),
]

def tiles_html(r):
    out = []
    for s in SV:
        slug = s[0]
        label = s[2] if LANG == "ta" else s[1]
        cap_en, cap_ta = TILE_CAPTION[slug]
        cap = cap_ta if LANG == "ta" else cap_en
        ico = service_icon(slug)
        col = TILE_COLOR[slug]
        out.append(
            f'<a class="tile tile--{col}" href="{sl(r, slug)}" data-service="{E(s[1])}">'
            f'<span class="tile-ico">{ico}</span>'
            f'<b>{label}</b>'
            f'<small>{cap}</small>'
            f'</a>')
    return ('<div class="services-grid" role="region" aria-label="Our services">'
            '<div class="tiles" id="serviceTiles">' + "".join(out) + '</div>'
            '</div>')

def index():
    """Build the homepage for the current language (hero, services, who we help, locations, tools, FAQ, contact)."""
    ld_graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "LocalBusiness", "@id": S + "/#business",
                "name": "KVB ENTERPRISES", "url": S + "/",
                "logo": S + "/assets/logo.png", "telephone": "+" + PH,
                "description": "Independent tax and business compliance assistance in Puducherry, India.",
                "address": {"@type": "PostalAddress", "addressLocality": "Puducherry", "addressRegion": "Puducherry", "addressCountry": "IN"},
                "areaServed": [{"@type": "AdministrativeArea", "name": "Puducherry", "identifier": "IN-PY"}],
                "availableLanguage": ["English", "Tamil"],
                "makesOffer": [{"@id": S + "/#service-" + slug} for slug in ("gst", "itr", "fssai", "udyam", "pan-trademark")]
            },
            *[
                {"@type": "Service", "@id": S + "/#service-" + slug, "name": name,
                 "provider": {"@id": S + "/#business"},
                 "areaServed": {"@type": "AdministrativeArea", "name": "Puducherry", "identifier": "IN-PY"}}
                for slug, name in [
                    ("gst", "GST Registration and Filing Assistance"),
                    ("itr", "Income Tax Return Assistance"),
                    ("fssai", "FSSAI Registration and Renewal Assistance"),
                    ("udyam", "MSME / Udyam Registration Assistance"),
                    ("pan-trademark", "PAN Card and Trademark Services")
                ]
            ]
        ]
    }
    ld = '<script type="application/ld+json">' + json.dumps(ld_graph, ensure_ascii=False) + "</script>"
    ta_ = LANG == "ta"
    r = "../" if ta_ else ""
    TT = "KVB ENTERPRISES | புதுச்சேரியில் வரி மற்றும் வணிக இணக்க சேவைகள்" if ta_ else "KVB ENTERPRISES | Tax & Business Compliance in Puducherry"
    DD = "புதுச்சேரி மற்றும் சுற்றுப்புறங்களில் GST, ITR, FSSAI, PAN, MSME/உத்யம், வர்த்தக முத்திரை, DSC உதவி. தமிழ் & ஆங்கிலம், WhatsApp ஆதரவு." if ta_ else "Local tax and business compliance help in Puducherry and nearby areas: GST, ITR, FSSAI, PAN, MSME/Udyam, Trademark, DSC. Tamil & English, WhatsApp support."
    b = head(r, TT, DD, "ta/" if ta_ else "", ld, [("en", ""), ("ta", "ta/"), ("x-default", "")]) + header(r, r + ("" if ta_ else "ta/") + "index.html")
    quick = "".join(f'<a href="{sl(r, s[0])}">{L(SHORT[s[0]])}</a>' for s in SV)
    b += ('<main id="home"><section class="hero">'
      + f'<img class="hero-illustration" src="{r}assets/hero-banner.svg" width="1180" height="610" alt="{E("KVB ENTERPRISES — Tax and Business Compliance, Puducherry")}" fetchpriority="high" decoding="async">'
      + '<div class="wrap hero-grid"><div class="hero-copy">'
          + T("div", "Local tax &amp; business compliance", "உள்ளூர் வரி மற்றும் வணிக இணக்க சேவைகள்", "eyebrow")
          + T("h1", '<span class="hero-title-main">Professional Tax &amp; Business Support</span><br><span class="hero-title-accent">Clear Guidance. Reliable Support.</span>', '<span class="hero-title-main">தொழில்முறை வரி மற்றும் வணிக உதவி</span><br><span class="hero-title-accent">தெளிவான வழிகாட்டுதல். நம்பகமான ஆதரவு.</span>')
          + T("p", "Professional assistance for GST, Income Tax / ITR, FSSAI, PAN, MSME/Udyam, Trademark, DSC and business registrations.", "GST, வருமான வரி / ITR, FSSAI, PAN, MSME/உத்யம், வர்த்தக முத்திரை, DSC மற்றும் வணிக பதிவுகளுக்கு தொழில்முறை உதவி.", "lead")
          + '<div class="actions">' + btn(wa("Hello Vivian, I need assistance with your services."), "WhatsApp Vivian", "WhatsApp-ல் பேசுங்கள்", "primary", "hero", True)
          + btn(f"tel:+{PH}", "Call now", "இப்போது அழைக்கவும்", "secondary", "hero", False, False)
          + T("a", "Explore Services", "சேவைகளைப் பார்க்க", x='class="btn secondary hero-services-cta" href="#services" data-loc="hero"') + "</div>"
          + T("p", "Tamil &amp; English • WhatsApp enquiries welcome anytime • Personal assistance", "தமிழ் &amp; ஆங்கிலம் • WhatsApp-ல் எப்போதும் வரவேற்கிறோம் • தனிப்பட்ட உதவி", "trust")
          + f'</div><div class="hero-card"><div class="logo-card"><img src="{r}assets/logo.png" alt="KVB ENTERPRISES" width="100" height="83"></div>'
          + '<p class="trust">'
+   '<span class="trust-item trust-item--lang">'
+     '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 2.5 15 0 18M12 3c-2.5 2.5-2.5 15 0 18"/></svg>'
+     '<span>' + L("Tamil &amp; English") + '</span>'
+   '</span>'
+   '<span class="trust-divider" aria-hidden="true"></span>'
+   '<span class="trust-item trust-item--wa">'
+     '<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884"/></svg>'
+     '<span>' + L("WhatsApp enquiries welcome") + '</span>'
+   '</span>'
+   '<span class="trust-divider" aria-hidden="true"></span>'
+   '<span class="trust-item trust-item--person">'
+     '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/></svg>'
+     '<span>' + L("Personal assistance") + '</span>'
+   '</span>'
+ '</p>'
          + f'<div class="quick">{quick}</div><div class="mini"><span class="mini-label">Call / WhatsApp</span><a class="mini-number" href="tel:+{PH}" data-loc="hero" aria-label="Call KVB ENTERPRISES at 90036 33696">90036 33696</a></div></div></div></section>')
    b += ('<section id="services" class="section"><div class="wrap"><div class="section-head">'
          + T("h2", "Everything your business needs, in one place.", "உங்கள் வணிகத்திற்குத் தேவையான சேவைகள் அனைத்தும் ஒரே இடத்தில்.")
          + T("p", "Explore practical support for GST, income tax, food licensing and business registration. Get clear steps, document guidance and direct follow-up.", "GST, வருமானவரி, உணவு பாதுகாப்பு உரிமம் மற்றும் வணிகப் பதிவுகளுக்கான நடைமுறை உதவியைப் பெறுங்கள். தெளிவான வழிமுறைகள், ஆவண வழிகாட்டுதல் மற்றும் தொடர்ந்து தகவல் பெறலாம்.")
          + f'</div>{tiles_html(r)}</div></section>')
    b += ('<section id="why-kvb" class="section"><div class="wrap"><div class="section-head">'
          + T("h2", "Local support built around clear communication.", "தெளிவான தகவல் பரிமாற்றத்தை மையமாகக் கொண்ட உள்ளூர் உதவி.")
          + T("p", "Practical assistance for individuals, professionals and businesses in Puducherry and nearby areas.", "புதுச்சேரி மற்றும் சுற்றுப்புறங்களில் உள்ள தனிநபர்கள், தொழில்முறையாளர்கள் மற்றும் வணிகங்களுக்கு நடைமுறை உதவி.")
          + '</div><div class="glass-grid">'
          + '<article class="glass-card"><strong class="stat-counter" data-target="5" data-count="5">5</strong>' + T("h3", "Core service groups", "முக்கிய சேவைப் பிரிவுகள்") + T("p", "GST, ITR, FSSAI, Udyam and PAN / trademark assistance.", "GST, ITR, FSSAI, உத்யம் மற்றும் PAN / வர்த்தக முத்திரை உதவி.") + '</article>'
          + '<article class="glass-card"><strong class="stat-counter" data-target="2" data-count="2">2</strong>' + T("h3", "Languages", "மொழிகள்") + T("p", "Support in English and Tamil.", "ஆங்கிலம் மற்றும் தமிழில் உதவி.") + '</article>'
          + '<article class="glass-card"><strong class="stat-counter" data-target="1" data-count="1">1</strong>' + T("h3", "Local point of contact", "உள்ளூர் தொடர்பு மையம்") + T("p", "One direct channel for questions, documents and updates.", "கேள்விகள், ஆவணங்கள் மற்றும் தகவல்களுக்கு நேரடி தொடர்பு வழி.") + '</article>'
          + '</div></div></section>')
    b += ('<section id="compliance-timeline" class="section alt" data-compliance-timeline><div class="wrap">'
          + T("span", "YOUR NEXT STEPS", "உங்கள் அடுத்த படிகள்", "eyebrow")
          + T("h2", "A clear process, from first message to follow-up.", "முதல் செய்தியிலிருந்து தொடர்ந்த தகவல் வரை தெளிவான செயல்முறை.")
          + '<div class="timeline-steps">'
          + '<article class="step" data-timeline-step><b>01</b>' + T("h3", "Tell us what you need", "உங்களுக்கு தேவையானதைச் சொல்லுங்கள்") + T("p", "Share the service and a short description of your requirement.", "சேவையையும் உங்கள் தேவையின் சுருக்கத்தையும் பகிருங்கள்.") + '</article>'
          + '<article class="step" data-timeline-step><b>02</b>' + T("h3", "Review the documents", "ஆவணங்களைச் சரிபார்க்கவும்") + T("p", "We explain the documents and information relevant to your case.", "உங்கள் நிலைக்கு தேவையான ஆவணங்கள் மற்றும் தகவல்களை விளக்குகிறோம்.") + '</article>'
          + '<article class="step" data-timeline-step><b>03</b>' + T("h3", "Confirm the scope", "சேவை விவரங்களை உறுதிப்படுத்துங்கள்") + T("p", "Understand the process, professional charges and any applicable statutory fees before proceeding.", "தொடங்குவதற்கு முன் செயல்முறை, தொழில்முறை கட்டணம் மற்றும் பொருந்தும் சட்டபூர்வ கட்டணங்களை அறிந்து கொள்ளுங்கள்.") + '</article>'
          + '<article class="step" data-timeline-step><b>04</b>' + T("h3", "Receive updates", "தொடர்ந்த தகவல்களைப் பெறுங்கள்") + T("p", "We keep you informed as the agreed assistance progresses.", "ஒப்புக்கொண்ட உதவி முன்னேறும் போது உங்களுக்கு தகவல் தெரிவிக்கிறோம்.") + '</article>'
          + '</div><div class="how-cta">' + btn(wa("Hello Vivian, I would like to get started."), "Start on WhatsApp →", "WhatsApp-ல் தொடங்குங்கள் →", "primary", "how-it-works", True) + '</div></div></section>')
    b += ('<section class="proof-strip section alt"><div class="wrap"><div class="section-head">'
          + T("h2", "A practical, transparent service experience.", "நடைமுறை மற்றும் வெளிப்படையான சேவை அனுபவம்.")
          + '</div><div class="proof-chips">'
          + '<span class="glass-chip proof-chip">' + T("span", "Independent assistance", "சுயாதீன உதவி") + '</span>'
          + '<span class="glass-chip proof-chip">' + T("span", "English and Tamil", "ஆங்கிலம் மற்றும் தமிழ்") + '</span>'
          + '<span class="glass-chip proof-chip">' + T("span", "Puducherry based", "புதுச்சேரியை மையமாகக் கொண்டது") + '</span>'
          + '<span class="glass-chip proof-chip">' + T("span", "Clear document guidance", "தெளிவான ஆவண வழிகாட்டுதல்") + '</span>'
          + '</div></div></section>')
    CHIPS = [("Restaurants &amp; Food Businesses", "food-businesses"), ("Bakeries &amp; Home Bakers", "food-businesses"),
             ("Cafés &amp; Tea Shops", "food-businesses"), ("Cloud Kitchens", "food-businesses"),
             ("Boutiques &amp; Fashion", "retail-traders"), ("Retail Shops", "retail-traders"), ("Supermarkets", "retail-traders"),
             ("Salons &amp; Spas", "salons-clinics"), ("Clinics &amp; Small Businesses", "salons-clinics"),
             ("Traders &amp; Wholesalers", "retail-traders"), ("Manufacturers", "manufacturers"), ("Online Sellers", "online-sellers"),
             ("Freelancers &amp; Professionals", "professionals-freelancers"), ("Home-Based Businesses", "home-based-businesses"),
             ("New Businesses", "new-businesses")]
    chips = "".join(
        f'<a href="{r}who-we-help/{pg}.html"><span>{c}</span></a>' if (not ta_ and has(f"who-we-help/{pg}.html"))
        else (f"<span>{L(c)}</span>" if not (ta_ and pg == "home-based-businesses") else "")
        for c, pg in CHIPS)
    b += ('<section id="business" class="section"><div class="wrap"><div class="section-head">' + T("h2", "Who we help", "யாருக்கு உதவுகிறோம்") + f'</div><div class="chips">{chips}</div>'
          '<div class="newbiz"><div>' + T("h3", "Starting a small business in Puducherry?", "புதுச்சேரியில் சிறு தொழில் தொடங்குகிறீர்களா?")
          + T("p", "Before you start, check which registrations may apply. We'll help you work out what applies to your business.", "தொடங்கும் முன், எந்த பதிவுகள் பொருந்தும் என்று பாருங்கள். உங்கள் வணிகத்திற்கு எது பொருந்தும் என்பதைக் கண்டறிய உதவுவோம்.")
          + '<ul class="nb-list">' + "".join(f"<li>{L(x)}</li>" for x in ["GST", "FSSAI", "Udyam / MSME", "Shops &amp; Establishment", "Business registration"]) + '</ul></div>'
          + btn(wa("Hello Vivian, I am starting a business and need guidance."), "Talk to Vivian", "விவியனிடம் பேசுங்கள்", "primary", "new-business", True) + "</div></div></section>")
    b += ('<section id="about" class="section alt"><div class="wrap about-grid"><div>' + T("h2", "Your local compliance partner.", "உங்கள் உள்ளூர் இணக்க துணை.")
          + T("p", "KVB ENTERPRISES provides practical tax and business compliance assistance for businesses, professionals and individuals in Puducherry and nearby areas.", "KVB ENTERPRISES புதுச்சேரி மற்றும் சுற்றுப்புறங்களில் உள்ள வணிகங்கள், தொழில்முறையாளர்கள் மற்றும் தனிநபர்களுக்கு நடைமுறை வரி மற்றும் வணிக இணக்க உதவி வழங்குகிறது.")
          + "<p>" + L("We focus on clear communication, documentation support and regular follow-up, and we are not a government office or authority.") + f'</p><div class="about-visual"><img src="{r}assets/visuals/service-business-registration.jpg" alt="Business registration documents prepared for review" loading="lazy" decoding="async"></div></div>'
          + '<div class="about-points"><div><b>' + L("Personal assistance") + '</b><span>' + L("Direct communication and guidance for your requirements.") + '</span></div>'
                    + '<div><b>' + L("Clear process") + '</b><span>' + L("Understand the documents, steps and professional charges before proceeding.") + '</span></div>'
          + '</div></div></section>')
    pin_icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/></svg>'
    locs = "".join(
        f'<a class="location-card{" location-card--featured" if l == "puducherry" else ""}" href="{r}locations/gst-registration-{l}.html">'
        f'<span class="location-card__icon">{pin_icon}</span>'
        f'<span class="location-card__copy"><strong>{l.title()}</strong><small>{L("Explore local GST assistance")}</small></span>'
        f'<span class="location-card__arrow" aria-hidden="true">↗</span></a>'
        for l in LOCS)
    b += ('<section id="locations" class="section location-section"><div class="wrap">'
          '<div class="location-heading"><div class="section-head">'
          + '<span class="location-kicker">' + L("SERVICE AREAS") + '</span>'
          + T("h2", "Local assistance across Puducherry and nearby areas.", "புதுச்சேரி மற்றும் சுற்றுப்புறங்களில் உள்ளூர் உதவி.")
          + T("p", "Choose your area to view local GST registration and compliance assistance.", "GST பதிவு மற்றும் இணக்க உதவியைப் பார்க்க உங்கள் பகுதியைத் தேர்ந்தெடுக்கவும்.")
          + '</div><div class="location-summary"><span class="location-summary__number">09</span><span>' + L("service areas") + '</span></div></div>'
          + f'<div class="locations">{locs}</div>'
          + '<p class="location-note">' + L("Service availability is confirmed when you contact us. KVB ENTERPRISES is based in Puducherry and is not a government office.") + '</p>'
          + '</div></section>')
    tools = "".join(f'<div><h3>{L(title)}</h3><p>{L(description)}</p><a href="{r}tools/{slug}.html">{L(link_text)}</a></div>'
                    for slug, title, description, link_text in (TOOLS[:4] if LANG == "ta" else TOOLS))
    b += ('<section id="tools" class="section alt"><div class="wrap"><div class="section-head">'
          + T("h2", "Useful resources for business owners.", "வணிக உரிமையாளர்களுக்கான பயனுள்ள வளங்கள்.")
          + f'</div><div class="tool-grid">{tools}</div></div></section>')
    faq = "".join(f'<details><summary>{L(q)}</summary><p>{L(a)}</p></details>' for q, a in FAQ)
    b += ('<section class="faq section"><div class="wrap"><div class="section-head">'
          + T("h2", "Common questions", "அடிக்கடி கேட்கப்படும் கேள்விகள்")
          + f'</div><div class="faq-list">{faq}</div></div></section>')
    opts = "".join(f'<option value="{o}">{L(o)}</option>' for o in ["GST Registration", "GST Filing", "Income Tax / ITR", "FSSAI", "PAN Card Services", "MSME / Udyam", "Trademark", "DSC", "Business Registration", "Other"])
    b += ('<section id="contact" class="contact"><div class="wrap contact-grid"><div>'
          + T("h2", "Have a compliance question?", "இணக்க கேள்வி உள்ளதா?")
          + T("p", "Send your requirement and Vivian can explain the process, documents and applicable professional charges.", "உங்கள் தேவையை அனுப்புங்கள், செயல்முறை, ஆவணங்கள் மற்றும் தொழில்முறை கட்டணங்களை விவியன் விளக்குவார்.")
          + '<div class="contact-line"><strong>Vivian</strong><br>KVB ENTERPRISES<br>'
          + f'<a href="tel:+{PH}" data-loc="contact">90036 33696</a><br>'
          + L("Puducherry &amp; nearby areas") + '<br>' + L("WhatsApp enquiries welcome anytime") + '</div></div>'
          + '<form class="contact-box" id="enquiryForm">'
          + '<label>' + L("Name *") + '<input name="name" required autocomplete="name"></label>'
          + '<label>' + L("Phone / WhatsApp number *") + '<input name="phone" type="tel" inputmode="tel" required pattern="[0-9+ ]{10,15}" autocomplete="tel"></label>'
          + '<label>' + L("Service required") + f'<select name="service" id="service"><option value="">{L("Select a service")}</option>{opts}</select></label>'
          + '<label>' + L("Your message") + '<textarea name="message" rows="3"></textarea></label>'
          + '<button class="btn primary wide" type="submit">' + ICON + '<span>' + L("Send enquiry on WhatsApp") + '</span></button>'
          + '</form></div></section></main>')
    b += foot(r)
    return b

def ld_graph(title, desc, path, service_name, area, crumbs):
    """One JSON-LD script: WebPage + Service + BreadcrumbList. Facts only: no prices, ratings or street address."""
    tag = "ta-IN" if LANG == "ta" else "en-IN"
    url = f"{S}/{path}"
    provider = {"@type": "ProfessionalService", "name": "KVB ENTERPRISES", "url": S + "/", "telephone": "+" + PH}
    graph = [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": tag,
         "isPartOf": {"@type": "WebSite", "name": "KVB ENTERPRISES", "url": S + "/"}},
        {"@type": "Service", "@id": url + "#service", "name": service_name, "description": desc, "url": url,
         "provider": provider, "areaServed": area},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]},
    ]
    return ('<script type="application/ld+json">'
            + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "</script>")

def service(s, r, path):
    """Build one service page (English or Tamil) with localized metadata and WebPage + Service JSON-LD."""
    slug, en, ta, de, dta, help_items, docs = s
    ta_ = LANG == "ta"
    name = ta if ta_ else en
    # Keep Tamil titles distinct when the Tamil name is the same word as the English one (e.g. FSSAI).
    title = f"{name} சேவைகள் | KVB ENTERPRISES" if (ta_ and ta == en) else f"{name} | KVB ENTERPRISES"
    desc = dta if ta_ else de
    home = S + "/" + ("ta/" if ta_ else "")
    ld = ld_graph(title, desc, path, name, [{"@type": "City", "name": l.title()} for l in LOCS],
                  [(L("Home"), home), (name, f"{S}/{path}")])
    b = head(r, title, desc, path, ld, [("en", f"services/{slug}.html"), ("ta", f"ta/services/{slug}.html")])
    b += header(r, r + ("services/" if ta_ else "ta/services/") + slug + ".html")  # link to the OTHER language
    b += '<main><section class="section"><div class="wrap">'
    b += '<nav class="crumbs"><a href="' + r + 'index.html">' + L("Home") + '</a> › ' + name + '</nav>'
    b += T("h1", en, ta)
    b += T("p", de, dta, "lead")
    b += '<div class="svc-body"><div>' + T("h2", "What we help with", "நாங்கள் எவ்வாறு உதவுகிறோம்")
    b += '<ul class="ticks">' + "".join(f'<li>{L(x)}</li>' for x in help_items) + '</ul>'
    b += T("h2", "Documents typically needed", "பொதுவாக தேவைப்படும் ஆவணங்கள்")
    b += '<ul class="ticks">' + "".join(f'<li>{L(x)}</li>' for x in docs) + '</ul></div>'
    b += '<aside class="svc-cta">' + price(slug)
    b += '<p>' + L(NOTE_EN) + '</p>'
    b += btn(wa(f"Hello Vivian, I need help with {en}."), "WhatsApp about this", "இதைப் பற்றி WhatsApp", "primary", "service", True)
    b += btn(f"tel:+{PH}", "Call now", "இப்போது அழைக்கவும்", "secondary", "service", False, False)
    b += '</aside></div></div></section></main>'
    b += foot(r)
    return b

# Where each area sits, for the GST state code (first two digits of a GSTIN): Puducherry 34, Tamil Nadu 33.
# (where it is, registration state, state code, one factual note)
LOCINFO = {
    "puducherry": ("the Union Territory of Puducherry", "Puducherry", "34",
                   "Puducherry town is where KVB ENTERPRISES is based."),
    "karaikal": ("the Union Territory of Puducherry", "Puducherry", "34",
                 "Karaikal is a region of the Union Territory of Puducherry, although it lies apart from Puducherry town, so registrations here are made under Puducherry rather than Tamil Nadu."),
    "villupuram": ("Villupuram district, Tamil Nadu", "Tamil Nadu", "33",
                   "Villupuram is the district headquarters and is in Tamil Nadu, not in the Puducherry Union Territory."),
    "cuddalore": ("Cuddalore district, Tamil Nadu", "Tamil Nadu", "33",
                  "Cuddalore is the district headquarters and is in Tamil Nadu, not in the Puducherry Union Territory."),
    "tindivanam": ("Villupuram district, Tamil Nadu", "Tamil Nadu", "33",
                   "Tindivanam is a town in Villupuram district, so GST registration here is under Tamil Nadu."),
    "panruti": ("Cuddalore district, Tamil Nadu", "Tamil Nadu", "33",
                "Panruti is a town in Cuddalore district, so GST registration here is under Tamil Nadu."),
    "tiruvannamalai": ("Tiruvannamalai district, Tamil Nadu", "Tamil Nadu", "33",
                       "Tiruvannamalai is the district headquarters and is in Tamil Nadu."),
    "chidambaram": ("Cuddalore district, Tamil Nadu", "Tamil Nadu", "33",
                    "Chidambaram is a town in Cuddalore district, so GST registration here is under Tamil Nadu."),
    "mayiladuthurai": ("Mayiladuthurai district, Tamil Nadu", "Tamil Nadu", "33",
                       "Mayiladuthurai became a separate district in 2020, so older documents may still show Nagapattinam district."),
}
# Add ONE real, first-hand line per area here (for example something you have seen while helping local clients).
# It is shown on that area's page only when it is not empty. Do not add anything you have not verified.
LOCNOTES = {}

def location(l, r, path):
    """Build one GST location page with area-specific GST state-code content, FAQ and internal links."""
    city = l.title()
    where, region, code, note = LOCINFO[l]
    title = ("GST Assistance in Puducherry | KVB ENTERPRISES" if l == "puducherry"
             else f"GST Registration in {city} | KVB ENTERPRISES")
    desc = (f"GST registration and compliance assistance in {city} and nearby areas. WhatsApp and Tamil support."
            if l == "puducherry" else
            f"GST registration and compliance assistance in {city}, Puducherry and nearby areas. WhatsApp and Tamil support.")
    url = f"{S}/{path}"
    ld = ld_graph(title, desc, path, f"GST registration in {city}", [{"@type": "City", "name": city}],
                  [(L("Home"), S + "/" + ("ta/" if LANG == "ta" else "")), (f"GST {city}", url)])
    b = head(r, title, desc, path, ld, [("en", f"locations/gst-registration-{l}.html")])
    b += header(r, lang_fallback=r + "ta/services/gst.html")
    b += '<main><section class="section"><div class="wrap">'
    b += '<nav class="crumbs"><a href="' + r + 'index.html">' + L("Home") + '</a> › GST ' + city + '</nav>'
    b += T("h1", f"GST Registration in {city}", f"{city}-இல் GST பதிவு")
    area_en = (f"businesses in {city} and nearby areas." if l == "puducherry"
               else f"businesses in {city} and nearby areas of Puducherry and Tamil Nadu.")
    b += T("p", f"We provide GST registration and compliance assistance for {area_en}", f"{city} மற்றும் அதைச் சுற்றியுள்ள பகுதிகளில் உள்ள வணிகங்களுக்கு GST பதிவு மற்றும் இணக்க உதவி வழங்குகிறோம்.", "lead")
    b += '<div class="svc-body"><div>'
    b += T("h2", "Services available", "கிடைக்கும் சேவைகள்")
    b += '<ul class="ticks"><li>GST registration</li><li>GSTR-1 / GSTR-3B filing</li><li>Monthly compliance</li><li>Amendment and cancellation</li></ul>'
    b += T("h2", "Documents typically needed", "பொதுவாக தேவைப்படும் ஆவணங்கள்")
    b += '<ul class="ticks"><li>PAN and Aadhaar</li><li>Address proof</li><li>Bank details</li><li>Business details</li></ul>'

    # Area-specific section: where the area sits and which GST state code applies.
    extra_note = (" " + LOCNOTES[l]) if LOCNOTES.get(l) else ""
    b += f'<h2>GST in {city}: what to know</h2>'
    b += (f'<p>{city} is in {where}. A business whose principal place of business is here registers for GST under {region}, '
          f'so its GSTIN begins with {code}. {note}{extra_note}</p>')
    elig = (f' The <a href="{r}tools/gst-eligibility-checker.html">GST Registration Eligibility Guide</a> gives an indicative first check.'
            if has("tools/gst-eligibility-checker.html") else "")
    checker = (f' You can also try <a href="{r}tools/business-compliance-checker.html">What Does My Business Need?</a>.'
               if has("tools/business-compliance-checker.html") else "")
    b += '<div class="faq-list">'
    b += (f'<details><summary>Which GST state code applies to a business in {city}?</summary>'
          f'<p>Businesses in {city} register under {region}, and the first two digits of the GSTIN are the state or Union Territory code ({code}). '
          f'The registration state follows your principal place of business, so we confirm it when we review your details.</p></details>')
    b += (f'<details><summary>Do I need GST registration for a small business in {city}?</summary>'
          f'<p>It depends on factors such as turnover, the kind of goods or services you supply, and whether you sell across states or online. '
          f'We review your case before recommending registration.{elig}</p></details>')
    b += (f'<details><summary>Can you also help with FSSAI or Udyam?</summary>'
          f'<p>Yes. Many small businesses need these alongside GST. See <a href="{r}services/fssai.html">FSSAI</a> and '
          f'<a href="{r}services/msme.html">MSME / Udyam</a>.{checker}</p></details>')
    b += '</div>'

    # Internal links: related pages and the other areas.
    rel = []
    if has("services/gst-registration.html"):
        rel.append(f'<a href="{r}services/gst-registration.html">GST registration details</a>')
    if has("services/gst-filing.html"):
        rel.append(f'<a href="{r}services/gst-filing.html">GST return filing</a>')
    if l == "puducherry":
        for fn, label in (("fssai-puducherry", "FSSAI in Puducherry"), ("itr-filing-puducherry", "ITR filing in Puducherry"),
                          ("msme-udyam-puducherry", "MSME / Udyam in Puducherry")):
            if has(f"locations/{fn}.html"):
                rel.append(f'<a href="{fn}.html">{label}</a>')
    if rel:
        b += '<h2>Related pages</h2><p>' + " • ".join(rel) + '</p>'
    b += '<h2>Other areas we serve</h2><p>' + " • ".join(
        f'<a href="gst-registration-{x}.html">{x.title()}</a>' for x in LOCS if x != l) + '</p>'
    b += '</div><aside class="svc-cta">'
    b += btn(wa(f"Hello Vivian, I need GST help in {city}."), "WhatsApp about this", "இதைப் பற்றி WhatsApp", "primary", "location", True)
    b += btn(f"tel:+{PH}", "Call now", "இப்போது அழைக்கவும்", "secondary", "location", False, False)
    b += '</aside></div></div></section></main>'
    b += foot(r)
    return b

def privacy_or_terms():
    is_privacy = True
    title = "Privacy Policy | KVB ENTERPRISES"
    desc = "Privacy policy for KVB ENTERPRISES website."
    b = head("", title, desc, "privacy.html")
    b += header("")
    b += '<main><section class="section"><div class="wrap">' + T("h1", "Privacy Policy", "தனியுரிமைக் கொள்கை")
    b += "<p>We respect your privacy. This website collects only the information you provide through the enquiry form or WhatsApp. We do not sell or share your information with third parties. Google Analytics 4 may collect anonymous usage data.</p>"
    b += '</div></section></main>'
    b += foot("")
    return b

def terms_page():
    title = "Terms of Use | KVB ENTERPRISES"
    desc = "Terms of use for KVB ENTERPRISES website."
    b = head("", title, desc, "terms.html")
    b += header("")
    b += '<main><section class="section"><div class="wrap">' + T("h1", "Terms of Use", "பயன்பாட்டு விதிமுறைகள்")
    b += "<p>KVB ENTERPRISES is an independent professional assistance service and is not a government department. Information on this site is provided in good faith. Final quotes are confirmed after reviewing requirements and documents.</p>"
    b += '</div></section></main>'
    b += foot("")
    return b

def sitemap_urls():
    """Return (relative_url, priority) pairs for generated and hand-written pages; used by both sitemap files."""
    urls = [("", "1.0"), ("ta/", "0.9"), ("privacy.html", "0.3"), ("terms.html", "0.3")]
    for s in SV:
        urls.append((f"services/{s[0]}.html", "0.8"))
        urls.append((f"ta/services/{s[0]}.html", "0.7"))
    for l in LOCS:
        urls.append((f"locations/gst-registration-{l}.html", "0.7"))
    for t in TOOLS:
        urls.append((f"tools/{t[0]}.html", "0.5"))
    # Hand-written pages that live beside the generated ones are picked up automatically.
    seen = {u for u, _ in urls}
    for pattern, pri in (("services/*.html", "0.7"), ("locations/*.html", "0.6"),
                         ("who-we-help/*.html", "0.6"), ("tools/*.html", "0.5")):
        for path in sorted(glob.glob(os.path.join(O, pattern))):
            u = os.path.relpath(path, O).replace(os.sep, "/")
            # Old thin city pages (locations/<city>.html) are superseded by gst-registration-<city>.html.
            if u.startswith("locations/") and os.path.basename(u)[:-5] in LOCS:
                continue
            if u not in seen:
                urls.append((u, pri))
                seen.add(u)
    return urls

def sitemap():
    """Return sitemap.xml built from sitemap_urls()."""
    today = TD.isoformat()
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u, pri in sitemap_urls():
        xml += f'  <url><loc>{S}/{u}</loc><lastmod>{today}</lastmod><priority>{pri}</priority></url>\n'
    xml += '</urlset>'
    return xml

def sl(r, slug):
    return f"{r}services/{slug}.html"

def L(s):
    if LANG == "ta":
        m = {"Tax &amp; Business Compliance": "வரி மற்றும் வணிக இணக்கம்",
             "Home": "முகப்பு", "Services": "சேவைகள்"}
        return m.get(s, s)
    return s

def main():
    """Generate every page and both sitemap files into the output directory."""
    global LANG
    # English
    LANG = "en"
    w("index.html", index())
    for s in SV:
        w(f"services/{s[0]}.html", service(s, "../", f"services/{s[0]}.html"))
    for l in LOCS:
        w(f"locations/gst-registration-{l}.html", location(l, "../", f"locations/gst-registration-{l}.html"))
    w("privacy.html", privacy_or_terms())
    w("terms.html", terms_page())
    # Tamil
    LANG = "ta"
    w("ta/index.html", index())
    for s in SV:
        w(f"ta/services/{s[0]}.html", service(s, "../../", f"ta/services/{s[0]}.html"))
    # Sitemap
    w("sitemap.xml", sitemap())
    w("sitemap.txt", "\n".join(f"{S}/{u}" for u, _ in sitemap_urls()) + "\n")

if __name__ == "__main__":
    main()
