#!/usr/bin/env python3
"""KVB ENTERPRISES site generator. Usage: python3 _builder/build.py
Edit _builder/prices.json (e.g. {"gst": "999"}) then rebuild. Empty price = "Get a quote"."""
import os, sys, html, json, datetime, urllib.parse as U

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
         ("itr-checklist", "ITR Document Checklist", "Prepare common documents before starting your return.", "Open checklist →")]
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
    u = f"{S}/{path}"
    alt = "".join(f'<link rel="alternate" hreflang="{h}" href="{S}/{q}">' for h, q in (alts or []))
    locale = "ta_IN" if LANG == "ta" else "en_IN"
    return (f'<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#29135e">'
            f'<link rel="canonical" href="{u}"><meta property="og:type" content="website"><meta property="og:site_name" content="KVB ENTERPRISES">'
            f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{u}">'
            f'<meta property="og:image" content="{S}/assets/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="{locale}"><meta name="twitter:card" content="summary_large_image">{alt}<link rel="icon" type="image/png" href="{r}assets/logo.png">'
            f'<link rel="stylesheet" href="{r}style.css"><link rel="stylesheet" href="{r}theme.css"><script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>'
            f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA}');</script>{ld}</head><body>")

def header(r, alt=None):
    home = r + ("ta/" if LANG == "ta" else "") + "index.html"
    n = "".join(T("a", en, ta, x=f'href="{home}#{i}"') for i, en, ta in NAV)
    hreflang = "en" if LANG == "ta" else "ta"
    lang_attr = "en" if LANG == "ta" else "ta"
    lang_label = "English" if LANG == "ta" else "தமிழ்"
    lg = (f'<a class="lang" href="{alt}" hreflang="{hreflang}" lang="{lang_attr}">{lang_label}</a>' if alt else "")
    return (f'<header class="topbar"><div class="wrap nav"><a class="brand" href="{home}" aria-label="KVB ENTERPRISES home">'
            f'<img src="{r}assets/logo.png" alt="KVB ENTERPRISES logo" width="56" height="47"><span><b>KVB</b> ENTERPRISES<small>{L("Tax &amp; Business Compliance")}</small></span></a>'
            f'<div class="nav-right"><nav id="mainNav" aria-label="Main navigation">{n}</nav>{lg}'
            f'<button class="menu" id="menuBtn" type="button" aria-label="Menu" aria-expanded="false">☰</button></div></div></header>')

def foot(r):
    bar = (f'<div class="mbar"><a href="{wa("Hello Vivian, I would like to know about your services.")}" target="_blank" rel="noopener" data-loc="mobile-bar">{ICON}WhatsApp</a>'
           + T("a", "Call", "அழைக்க", x=f'href="tel:+{PH}" data-loc="mobile-bar"') + '</div>')
    return (bar + f'<a class="floating-wa" href="{wa("Hello Vivian, I would like to know about your services.")}" target="_blank" rel="noopener" aria-label="WhatsApp KVB ENTERPRISES" data-loc="floating">{ICON}</a>'
            f'<footer><div class="wrap footer"><div class="footer-brand"><img src="{r}assets/logo.png" alt="KVB ENTERPRISES logo" width="44" height="44" loading="lazy">'
            f'<div><b>KVB ENTERPRISES</b><p>{L("Tax &amp; Business Compliance Services")}</p></div></div>'
            f'<div>GST • ITR • FSSAI • PAN • MSME • Trademark • DSC<br>{L("Puducherry &amp; nearby areas")}</div>'
            f'<div><a href="{r}privacy.html">Privacy</a> • <a href="{r}terms.html">Terms</a><br>© <span class="yr">{TD.year}</span> KVB ENTERPRISES</div></div></footer>'
            f'<script src="{r}script.js" defer></script><script src="{r}ui.js" defer></script></body></html>')

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
        ico = TILE_ICONS[slug]
        col = TILE_COLOR[slug]
        out.append(
            f'<a class="tile tile--{col}" href="{sl(r, slug)}" data-service="{E(s[1])}">'
            f'<span class="tile-ico">{ico}</span>'
            f'<b>{label}</b>'
            f'<small>{cap}</small>'
            f'</a>')
    return "".join(out)

def index():
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "ProfessionalService", "name": "KVB ENTERPRISES", "url": S + "/",
        "logo": S + "/assets/logo.png", "image": S + "/assets/logo.png", "telephone": "+" + PH,
        "description": "Tax and business compliance assistance in Puducherry and nearby areas: GST, ITR, FSSAI, PAN, MSME/Udyam, Trademark, DSC and business registration.",
        "areaServed": [{"@type": "City", "name": l.title()} for l in LOCS], "availableLanguage": ["English", "Tamil"]}, ensure_ascii=False) + "</script>"
    ta_ = LANG == "ta"
    r = "../" if ta_ else ""
    TT = "KVB ENTERPRISES | புதுச்சேரியில் வரி மற்றும் வணிக இணக்க சேவைகள்" if ta_ else "KVB ENTERPRISES | Tax & Business Compliance in Puducherry"
    DD = "புதுச்சேரி மற்றும் சுற்றுப்புறங்களில் GST, ITR, FSSAI, PAN, MSME/உத்யம், வர்த்தக முத்திரை, DSC உதவி. தமிழ் & ஆங்கிலம், WhatsApp ஆதரவு." if ta_ else "Local tax and business compliance help in Puducherry and nearby areas: GST, ITR, FSSAI, PAN, MSME/Udyam, Trademark, DSC. Tamil & English, WhatsApp support."
    b = head(r, TT, DD, "ta/" if ta_ else "", ld, [("en", ""), ("ta", "ta/"), ("x-default", "")]) + header(r, r + ("" if ta_ else "ta/") + "index.html")
    quick = "".join(f'<a href="{sl(r, s[0])}">{L(SHORT[s[0]])}</a>' for s in SV)
    b += ('<main id="home"><section class="hero"><div class="wrap hero-grid"><div class="hero-copy">'
          + T("div", "Local tax &amp; business compliance", "உள்ளூர் வரி மற்றும் வணிக இணக்க சேவைகள்", "eyebrow")
          + T("h1", "Your Business.<br><span>Our Responsibility.</span>", "உங்கள் தொழில்.<br><span>எங்கள் பொறுப்பு.</span>")
          + T("p", "Professional assistance for GST, Income Tax / ITR, FSSAI, PAN, MSME/Udyam, Trademark, DSC and business registrations.", "GST, வருமான வரி / ITR, FSSAI, PAN, MSME/உத்யம், வர்த்தக முத்திரை, DSC மற்றும் வணிக பதிவுகளுக்கு தொழில்முறை உதவி.", "lead")
          + '<div class="actions">' + btn(wa("Hello Vivian, I need assistance with your services."), "WhatsApp Vivian", "WhatsApp-ல் பேசுங்கள்", "primary", "hero", True)
          + btn(f"tel:+{PH}", "Call now", "இப்போது அழைக்கவும்", "secondary", "hero", False, False) + "</div>"
          + T("p", "Tamil &amp; English • WhatsApp enquiries welcome anytime • Personal assistance", "தமிழ் &amp; ஆங்கிலம் • WhatsApp-ல் எப்போதும் வரவேற்கிறோம் • தனிப்பட்ட உதவி", "trust")
          + f'</div><div class="hero-card"><div class="logo-card"><img src="{r}assets/logo.png" alt="KVB ENTERPRISES" width="100" height="83"></div>'
          + T("div", "Need help with your business compliance?", "உங்கள் வணிக இணக்கத்தில் உதவி தேவையா?", "card-title")
          + f'<div class="quick">{quick}</div><div class="mini">Call / WhatsApp<br><strong>90036 33696</strong></div></div></div></section>')
    b += ('<section class="clients"><div class="wrap clients-grid"><div class="big"><strong>300+</strong>' + T("span", "Clients served", "வாடிக்கையாளர்களுக்கு சேவை") + '</div><div>'
          + T("h2", "Trusted local support in and around Puducherry", "புதுச்சேரி மற்றும் சுற்றுப்புறங்களில் நம்பகமான உள்ளூர் உதவி")
          + T("p", "Businesses, professionals and individuals have used KVB ENTERPRISES for practical, personal compliance support.", "வணிகங்கள், தொழில்முறையாளர்கள் மற்றும் தனிநபர்கள் நடைமுறை, தனிப்பட்ட இணக்க உதவிக்காக KVB ENTERPRISES-ஐ பயன்படுத்தியுள்ளனர்.")
          + '<ul class="ticks">' + T("li", "Direct support from Vivian", "விவியனிடமிருந்து நேரடி உதவி") + T("li", "Clear steps and document lists", "தெளிவான படிகள் மற்றும் ஆவண பட்டியல்") + T("li", "Updates on WhatsApp", "WhatsApp மூலம் தகவல்") + '</ul></div></div></section>')
    b += ('<section id="services" class="section"><div class="wrap"><div class="section-head">'
          + T("h2", "Everything your business needs, in one place.", "உங்கள் வணிகத்திற்குத் தேவையான சேவைகள் அனைத்தும் ஒரே இடத்தில்.")
          + T("p", NOTE_EN, NOTE_TA)
          + f'</div><div class="tiles">{tiles_html(r)}</div></div></section>')
    b += ('<section id="how" class="section alt"><div class="wrap"><div class="section-head">' + T("h2", "How it works", "எப்படி செயல்படுகிறது") + "</div>" + steps()
          + '<div class="how-cta">' + btn(wa("Hello Vivian, I would like to get started."), "Start on WhatsApp →", "WhatsApp-ல் தொடங்குங்கள் →", "primary", "how-it-works", True) + "</div></div></section>")
    chips = "".join(f"<span>{L(c)}</span>" for c in ["Restaurants &amp; Food Businesses", "Bakeries &amp; Home Bakers", "Cafés &amp; Tea Shops", "Cloud Kitchens", "Boutiques &amp; Fashion", "Retail Shops", "Supermarkets", "Salons &amp; Spas", "Clinics &amp; Small Businesses", "Traders &amp; Wholesalers", "Manufacturers", "Online Sellers", "Freelancers &amp; Professionals", "New Businesses"])
    b += ('<section id="business" class="section"><div class="wrap"><div class="section-head">' + T("h2", "Who we help", "யாருக்கு உதவுகிறோம்") + f'</div><div class="chips">{chips}</div>'
          '<div class="newbiz"><div>' + T("h3", "Starting a small business in Puducherry?", "புதுச்சேரியில் சிறு தொழில் தொடங்குகிறீர்களா?")
          + T("p", "Before you start, check which registrations may apply. We'll help you work out what applies to your business.", "தொடங்கும் முன், எந்த பதிவுகள் பொருந்தும் என்று பாருங்கள். உங்கள் வணிகத்திற்கு எது பொருந்தும் என்பதைக் கண்டறிய உதவுவோம்.")
          + '<ul class="nb-list">' + "".join(f"<li>{L(x)}</li>" for x in ["GST", "FSSAI", "Udyam / MSME", "Shops &amp; Establishment", "Business registration"]) + '</ul></div>'
          + btn(wa("Hello Vivian, I am starting a business and need guidance."), "Talk to Vivian", "விவியனிடம் பேசுங்கள்", "primary", "new-business", True) + "</div></div></section>")
    b += ('<section id="about" class="section alt"><div class="wrap about-grid"><div>' + T("h2", "Your local compliance partner.", "உங்கள் உள்ளூர் இணக்க துணை.")
          + T("p", "KVB ENTERPRISES provides practical tax and business compliance assistance for businesses, professionals and individuals in Puducherry and nearby areas.", "KVB ENTERPRISES புதுச்சேரி மற்றும் சுற்றுப்புறங்களில் உள்ள வணிகங்கள், தொழில்முறையாளர்கள் மற்றும் தனிநபர்களுக்கு நடைமுறை வரி மற்றும் வணிக இணக்க உதவி வழங்குகிறது.")
          + "<p>" + L("We focus on clear communication, documentation support and regular follow-up, and we are not a government office or authority.") + "</p></div>"
          + '<div class="about-points"><div><b>' + L("Personal assistance") + '</b><span>' + L("Direct communication and guidance for your requirements.") + '</span></div>'
          + '<div><b>' + L("Clear process") + '</b><span>' + L("Understand the documents, steps and professional charges before proceeding.") + '</span></div
