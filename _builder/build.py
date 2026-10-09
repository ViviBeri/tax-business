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

# slug, en, ta, desc_en, desc_ta, help items, typical documents
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

def head(r, title, desc, path, ld="", alts=None):
    u = f"{S}/{path}"
    alt = "".join(f'<link rel="alternate" hreflang="{h}" href="{S}/{q}">' for h, q in (alts or []))
    return (f'<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#29135e">'
            f'<link rel="canonical" href="{u}"><meta property="og:type" content="website"><meta property="og:site_name" content="KVB ENTERPRISES">'
            f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{u}">'
            f'<meta property="og:image" content="{S}/assets/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="{"ta_IN" if LANG == "ta" else "en_IN"}"><meta name="twitter:card" content="summary_large_image">{alt}<link rel="icon" type="image/png" href="{r}assets/logo.png">'
            f'<link rel="stylesheet" href="{r}style.css"><script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>'
            f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA}');</script>{ld}</head><body>")

def header(r, alt=None):
    home = r + ("ta/" if LANG == "ta" else "") + "index.html"
    n = "".join(T("a", en, ta, x=f'href="{home}#{i}"') for i, en, ta in NAV)
    lg = (f'<a class="lang" href="{alt}" hreflang="{"en" if LANG == "ta" else "ta"}" lang="{"en" if LANG == "ta" else "ta"}">{"English" if LANG == "ta" else "தமிழ்"}</a>' if alt else "")
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
            f'<script src="{r}script.js" defer></script></body></html>')

def btn(href, en, ta, cls="primary", loc="", ico=False, ext=True):
    t = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="btn {cls}" href="{href}"{t} data-loc="{loc}">{ICON if ico else ""}<span>{ta if (LANG == 'ta' and ta) else en}</span></a>'

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
    cards = "".join(f'<a class="service-card" href="{sl(r, s[0])}" data-service="{E(s[1])}">{T("h3", s[1], s[2])}{T("p", s[3], s[4])}{price(s[0])}'
                    f'{T("span", "View service →", "சேவையைப் பார்க்க →")}</a>' for s in SV)
    b += ('<section id="services" class="section"><div class="wrap"><div class="section-head">' + T("h2", "Everything your business needs, in one place.", "உங்கள் வணிகத்திற்குத் தேவையான சேவைகள் அனைத்தும் ஒரே இடத்தில்.")
          + T("p", NOTE_EN, NOTE_TA) + f'</div><div class="cards">{cards}</div></div></section>')
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
          + '<div class="about-points"><div><b>' + L("Personal assistance") + '</b><span>' + L("Direct communication and guidance for your requirements.") + '</span></div><div><b>' + L("Clear process") + '</b><span>' + L("Understand the documents, steps and professional charges before proceeding.") + '</span></div></div></div></section>')
    locs = "".join(f'<a href="{r}locations/gst-registration-{l}.html">{L(l.title())}</a>' for l in LOCS)
    b += ('<section id="locations" class="section"><div class="wrap"><div class="section-head">' + T("h2", "Local assistance across Puducherry and nearby areas.", "புதுச்சேரி மற்றும் சுற்றுப்புறங்களில் உள்ளூர் உதவி.")
          + f'<p>{L("Choose a location to view the local GST service page.")}</p></div><div class="locations">{locs}</div></div></section>')
    tools = "".join(f'<div><h3>{L(t[1])}</h3><p>{L(t[2])}</p><a href="{r}tools/{t[0]}.html">{L(t[3])}</a></div>' for t in TOOLS)
    b += ('<section id="tools" class="section alt"><div class="wrap"><div class="section-head">' + T("h2", "Useful resources for business owners.", "தொழில் உரிமையாளர்களுக்கான பயனுள்ள வளங்கள்.") + f'</div><div class="tool-grid">{tools}</div></div></section>')
    fq = "".join(f"<details><summary>{L(q)}</summary><p>{L(a)}</p></details>" for q, a in FAQ)
    b += ('<section class="faq section"><div class="wrap"><div class="section-head">' + T("h2", "Common questions", "பொதுவான கேள்விகள்") + f'</div><div class="faq-list">{fq}</div></div></section>')
    opts = "".join(f'<option value="{E(v)}">{t if LANG == "ta" else v}</option>' for v, t in [
        ("GST Registration", "GST பதிவு"), ("GST Filing", "GST ரிட்டர்ன் தாக்கல்"), ("Income Tax / ITR", "வருமான வரி / ITR"), ("FSSAI", "FSSAI"), ("PAN Card Services", "PAN அட்டை சேவைகள்"),
        ("MSME / Udyam", "MSME / உத்யம்"), ("Trademark", "வர்த்தக முத்திரை"), ("DSC", "DSC"), ("Business Registration", "வணிக பதிவு"), ("Other", "மற்றவை")])
    b += ('<section id="contact" class="contact"><div class="wrap contact-grid"><div>' + T("h2", "Have a compliance question?", "இணக்கம் தொடர்பான கேள்வியா?")
          + T("p", "Send your requirement and Vivian can explain the process, documents and applicable professional charges.", "உங்கள் தேவையை அனுப்புங்கள். செயல்முறை, ஆவணங்கள் மற்றும் தொழில்முறை கட்டணங்களை விவியன் விளக்குவார்.")
          + f'<div class="contact-line"><strong>Vivian</strong><br>KVB ENTERPRISES<br><a href="tel:+{PH}" data-loc="contact">90036 33696</a><br>{L("Puducherry &amp; nearby areas")}<br>{L("WhatsApp enquiries welcome anytime")}</div></div>'
          '<form class="contact-box" id="enquiryForm">'
          + T("label", 'Name *<input name="name" required autocomplete="name">', 'பெயர் *<input name="name" required autocomplete="name">')
          + T("label", 'Phone / WhatsApp number *<input name="phone" type="tel" inputmode="tel" required pattern="[0-9+ ]{10,15}" autocomplete="tel">', 'தொலைபேசி / WhatsApp எண் *<input name="phone" type="tel" inputmode="tel" required pattern="[0-9+ ]{10,15}" autocomplete="tel">')
          + T("label", f'Service required<select name="service" id="service"><option value="" data-en="Select a service" data-ta="சேவையைத் தேர்ந்தெடுக்கவும்">Select a service</option>{opts}</select>', f'சேவை<select name="service" id="service"><option value="">சேவையைத் தேர்ந்தெடுக்கவும்</option>{opts}</select>')
          + T("label", 'Your message<textarea name="message" rows="3"></textarea>', 'உங்கள் தேவை<textarea name="message" rows="3"></textarea>')
          + f'<button class="btn primary wide" type="submit">{ICON}<span>{L("Send enquiry on WhatsApp")}</span></button>'
          + T("p", "This opens WhatsApp with your message ready. We use your details only to reply to your enquiry.", "இது உங்கள் செய்தியுடன் WhatsApp-ஐ திறக்கும். உங்கள் விவரங்கள் பதிலளிக்க மட்டுமே பயன்படுத்தப்படும்.") + "</form></div></section></main>")
    w("ta/index.html" if ta_ else "index.html", b + foot(r))

def sl(r, slug):
    return r + ("ta/services/" if (LANG == "ta" and slug in TA_SV) else "services/") + slug + ".html"

def svc(x):
    s, en, ta, d, dta, items, docs = x
    ta_ = LANG == "ta"
    r = "../../" if ta_ else "../"
    nm = ta if ta_ else en
    t = f"{ta} - புதுச்சேரி | KVB ENTERPRISES" if ta_ else f"{en} in Puducherry | KVB ENTERPRISES"
    dd = f"{ta}: புதுச்சேரி மற்றும் சுற்றுப்புறங்களில் KVB ENTERPRISES-இடமிருந்து தொடக்க விலை, ஆவணங்கள் மற்றும் WhatsApp உதவி." if ta_ else f"{en} in Puducherry and nearby areas from KVB ENTERPRISES. Starting prices, documents and WhatsApp support."
    alts = [("en", f"services/{s}.html"), ("ta", f"ta/services/{s}.html"), ("x-default", f"services/{s}.html")] if s in TA_SV else None
    alt = (r + ("" if ta_ else "ta/") + f"services/{s}.html") if s in TA_SV else None
    b = head(r, t, dd, f"ta/services/{s}.html" if ta_ else f"services/{s}.html", "", alts) + header(r, alt)
    msg = wa(f"வணக்கம் விவியன், {ta} தொடர்பாக உதவி தேவை." if ta_ else f"Hello Vivian, I need assistance with {en}.")
    rel = "".join(f'<a href="{sl(r, o[0])}">{o[2] if ta_ else o[1]}</a>' for o in SV if o[0] != s)
    home = r + ("ta/" if ta_ else "") + "index.html"
    b += (f'<main class="service-page"><div class="wrap"><a class="back" href="{home}#services">{L("← All services")}</a>{T("h1", en, ta)}{T("p", d, dta, "intro")}'
          f'<div class="service-grid"><div><section class="panel"><h2>{L("What we can help with")}</h2><ul>' + "".join(f"<li>{L(i)}</li>" for i in items) + "</ul></section>"
          f'<section class="panel" style="margin-top:20px"><h2>{L("Documents commonly needed")}</h2><ul>' + "".join(f"<li>{L(i)}</li>" for i in docs)
          + f'</ul><p class="note">{L("The exact list depends on your case. We confirm it with you on WhatsApp before you start.")}</p></section>'
          f'<section class="panel" style="margin-top:20px"><h2>{L("Pricing")}</h2><p>' + price(s) + f'</p>{T("p", NOTE_EN, NOTE_TA, "note")}{xnote(s)}</section></div>'
          f'<aside class="panel cta-panel"><h2>{L("Need assistance?")}</h2><p>{L("Tell Vivian what you need and get the document and process guidance for your case.")}</p>'
          + btn(msg, "WhatsApp 90036 33696", "WhatsApp 90036 33696", "primary wide", s, True) + '<div style="height:10px"></div>' + btn(f"tel:+{PH}", "Call now", "இப்போது அழைக்கவும்", "secondary wide", s, False, False)
          + f'<p>{L("Tamil &amp; English. Local assistance in Puducherry and nearby areas.")}</p></aside></div>'
          f'<h2 style="margin-top:40px">{L("How it works")}</h2>' + steps() + faqhtml(s) + f'<div class="related">{rel}</div></div></main>')
    w(f"ta/services/{s}.html" if ta_ else f"services/{s}.html", b + foot(r))

CSS = r"""
/* V3 */
:root{--green:#1f7a42}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI","Noto Sans Tamil","Nirmala UI",sans-serif}
:focus-visible{outline:3px solid var(--orange);outline-offset:2px}
.brand img{width:56px;height:56px}.brand small{font-size:10px;letter-spacing:.8px}
.logo-card{width:120px;height:120px}.logo-card img{width:100px;height:100px}
.btn svg{margin-right:8px;flex:none}
.floating-wa svg{width:30px;height:30px}
.menu{display:none;width:42px;height:40px;border:1px solid var(--line);background:#fff;border-radius:10px;font-size:20px;cursor:pointer}
.service-card>b{display:none}
.service-card:nth-child(4n+3) span{color:#b45f00}
.service-card em.price{display:block;margin:0 0 10px;font-style:normal;font-weight:800;font-size:14px;color:var(--navy)}
.clients{background:#fff;border-bottom:1px solid var(--line);padding:56px 0}
.clients-grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:44px;align-items:center}
.big strong{display:block;font-size:clamp(76px,15vw,128px);line-height:1;letter-spacing:-4px;color:var(--green)}
.big span{display:block;font-size:20px;font-weight:900;color:var(--navy)}
.big:after{content:"";display:block;width:70px;height:5px;border-radius:999px;background:var(--orange);margin-top:12px}
.clients h2{margin:0 0 10px;color:var(--navy);font-size:clamp(26px,3.6vw,38px);line-height:1.12}
.clients p{color:var(--muted)}
.ticks{list-style:none;padding:0;margin:14px 0 0;display:grid;gap:8px}
.ticks li{padding-left:26px;position:relative;font-weight:750;color:var(--navy)}
.ticks li:before{content:"✓";position:absolute;left:0;color:var(--green);font-weight:900}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.step{background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px}
.step b{display:grid;place-items:center;width:42px;height:42px;border-radius:50%;background:var(--navy);color:#fff;margin-bottom:12px}
.step h3{margin:0 0 6px;color:var(--navy)}.step p{margin:0;color:var(--muted)}
.how-cta{margin-top:24px}
.nb-list{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 0;padding:0;list-style:none}
.nb-list li{padding:6px 12px;border-radius:999px;background:rgba(255,255,255,.14);font-size:13px;font-weight:700}
.contact-box select,.contact-box textarea{display:block;width:100%;margin-top:6px;padding:12px;border:1px solid #d7dee8;border-radius:10px;font:inherit;background:#fff}
.note{font-size:13px;color:var(--muted)}
.related{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}
.related a{padding:9px 14px;border-radius:999px;background:#fff;border:1px solid var(--line);color:var(--navy);font-weight:750;text-decoration:none;font-size:14px}
.cta-panel .note,.cta-panel p{color:#d7e0ea}
@media(max-width:900px){
.menu{display:block}.nav{gap:8px}
nav.open{display:flex;position:absolute;left:0;right:0;top:100%;flex-direction:column;align-items:flex-start;gap:0;background:#fff;border-bottom:1px solid var(--line);padding:8px 4% 14px;box-shadow:0 14px 30px rgba(41,19,94,.12)}
nav.open a{padding:12px 0;width:100%;font-size:16px}
.clients-grid,.steps{grid-template-columns:1fr}}
.mbar{display:none}
@media(max-width:700px){.mbar{display:grid;grid-template-columns:1fr 1fr;position:fixed;left:0;right:0;bottom:0;z-index:30;box-shadow:0 -6px 20px rgba(41,19,94,.15)}.mbar a{display:flex;justify-content:center;align-items:center;padding:14px;font-weight:850;text-decoration:none;color:#fff;background:var(--green)}.mbar a+a{background:var(--navy)}.floating-wa{display:none}body{padding-bottom:52px}}
a.lang{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 16px;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--navy);font-weight:800;text-decoration:none}
.back{display:inline-block;padding:12px 0}
.footer a{display:inline-block;padding:10px 6px}
.quick a{min-height:44px;display:flex;align-items:center;justify-content:center}
.mbar a svg{margin-right:8px}
.tool-grid a,.contact-line a{display:inline-block;padding:12px 0}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.service-card{transition:none}}
"""

JS = r"""(function(){
var d=document,cur='en';
var ev=function(n,p){try{if(window.gtag)gtag('event',n,p||{})}catch(e){}};
var q=function(s){return d.querySelectorAll(s)};
var mb=d.getElementById('menuBtn'),nv=d.getElementById('mainNav');
if(mb&&nv){mb.addEventListener('click',function(){var o=nv.classList.toggle('open');mb.setAttribute('aria-expanded',o)});
nv.addEventListener('click',function(e){if(e.target.closest('a'))nv.classList.remove('open')})}
q('.yr').forEach(function(e){e.textContent=new Date().getFullYear()});
d.addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;
if(a.classList.contains('lang')){ev('language_switch',{language:a.getAttribute('hreflang')});return}
var h=a.href||'',l=a.dataset.loc||'page',p={link_location:l,page_path:location.pathname};
if(h.indexOf('wa.me')>-1)ev('whatsapp_click',p);
else if(h.indexOf('tel:')===0)ev('call_click',p);
else if(a.classList.contains('service-card'))ev('select_service',{service:a.dataset.service,link_location:'home-card'})});
var sv=d.getElementById('service');
if(sv)sv.addEventListener('change',function(){if(sv.value)ev('select_service',{service:sv.value,link_location:'form'})});
var f=d.getElementById('enquiryForm');
if(f)f.addEventListener('submit',function(e){e.preventDefault();var g=new FormData(f),s=g.get('service')||'Not selected';
var m='New Website Enquiry\nService: '+s+'\nName: '+g.get('name')+'\nPhone: '+g.get('phone')+'\nRequirement: '+(g.get('message')||'-');
ev('generate_lead',{service:s,link_location:'form'});
var u='https://wa.me/919003633696?text='+encodeURIComponent(m);
if(!window.open(u,'_blank'))location.href=u});
})();
"""

README = """# KVB ENTERPRISES website

Static website for KVB ENTERPRISES, tax and business compliance assistance in Puducherry and nearby areas. Hosted on GitHub Pages: https://viviberi.github.io/tax-business/

## Structure
- `index.html`, `services/` are generated by `_builder/build.py`
- `style.css`, `script.js` styling, form and analytics events; `ta/` holds the Tamil pages (home, GST, ITR, FSSAI, MSME), linked to the English pages with hreflang
- `locations/`, `tools/`, `privacy.html`, `terms.html` are also generated; `assets/` is maintained by hand
- `sitemap.xml`, `robots.txt`

## Updating prices
Edit `_builder/prices.json` (for example `{"gst": "999"}`), then run `python3 _builder/build.py`. An empty value shows "Get a quote".

## Analytics
Google Analytics 4 (G-KFP95JFETM). Events: `whatsapp_click`, `call_click`, `generate_lead` (form), `select_service`, `language_switch`. No names or phone numbers are sent to Google.

KVB ENTERPRISES is an independent professional assistance service and is not a government department.
"""

def main():
    build_all()
    legacy()
    old = os.path.join(O, "style.css")
    base = open(old, encoding="utf-8").read().split("/* V3 */")[0].rstrip() if os.path.exists(old) else ""
    w("style.css", base + "\n" + CSS)
    w("script.js", JS)
    w("README.md", README)
    w("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {S}/sitemap.xml\n")
    urls = [""] + [f"services/{x[0]}.html" for x in SV] + ["ta/"] + [f"ta/services/{x}.html" for x in sorted(TA_SV)] + ["locations/gst-registration-puducherry.html"] + [f"tools/{t[0]}.html" for t in TOOLS] + ["privacy.html", "terms.html"]
    w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f"<url><loc>{S}/{u}</loc><lastmod>{TD.isoformat()}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    if not os.path.exists(os.path.join(B, "prices.json")):
        json.dump({x[0]: "" for x in SV}, open(os.path.join(B, "prices.json"), "w"), indent=1)

import re
EXTRA = {
 "gst": "Registering for GST on the official GST portal has no government application fee. Our fee is for assistance with documents, the application and follow-up.",
 "msme": "Udyam registration on the official government portal (udyamregistration.gov.in) is free of cost, and you can register yourself there. Our fee is an optional assistance fee for documents and the application. KVB ENTERPRISES is not the government portal.",
 "fssai": "Government licence or registration fees are separate from our professional fee and depend on the type of licence.",
 "itr": "Starting price is for ITR with tax audit support. Tax audit, where applicable, is carried out by a Chartered Accountant. Non-audit ITR: contact us for pricing.",
 "trademark": "Government fees are separate from our professional fee.",
}
FAQS = {
 "gst": [("Do I need GST registration for my small business?", "It depends on your turnover, the nature of your supplies and where you operate. Some businesses must register and others can register voluntarily. Send us your details and we will explain what applies to you."),
         ("What documents are needed for GST registration?", "Commonly PAN, Aadhaar, a photograph, business address proof and bank details. The exact list depends on your business constitution, and we confirm it with you."),
         ("Can you help with monthly GST filing?", "Yes. We assist with GSTR-1 and GSTR-3B filing and monthly compliance for eligible businesses. The final fee is confirmed after reviewing your requirements.")],
 "itr": [("Can you help with ITR filing if I do not have a CA?", "Yes, we assist individuals and businesses with ITR preparation and filing. Where a tax audit is required, it must be carried out by a Chartered Accountant, and we coordinate this for you."),
         ("What documents do I need for ITR?", "Commonly PAN, Aadhaar, income details, bank statements and investment or deduction proofs. See the list above and the ITR checklist.")],
 "fssai": [("Do I need FSSAI for a home bakery?", "Home-based food businesses may need an FSSAI registration or licence depending on turnover and activity. Tell us what you make and sell and we will guide you."),
           ("What is the difference between FSSAI registration and licence?", "They are different categories based on the size and nature of the food business. We help you identify which one applies to you.")],
 "msme": [("Who can apply for Udyam registration?", "Eligible micro, small and medium enterprises, including many small service businesses. Eligibility depends on your activity and the scheme rules."),
          ("Is Udyam registration free?", "Yes. On the official portal there is no registration fee, and you can register yourself. You can also ask us to assist for an optional service fee.")],
 "pan": [("Can you help with PAN correction?", "Yes. Share your PAN details and what needs to change, and we will guide you through the correction or update.")],
}
def xnote(s):
    return f'<p class="note">{L(EXTRA[s])}</p>' if s in EXTRA else ""
def faqhtml(s):
    if s not in FAQS: return ""
    return '<h2 style="margin-top:40px">' + L("Common questions") + '</h2><div class="faq-list">' + "".join(f"<details><summary>{L(q)}</summary><p>{L(a)}</p></details>" for q, a in FAQS[s]) + "</div>"
def rd(p): return open(os.path.join(O, p), encoding="utf-8").read()
def shell(r, title, desc, path, inner, extra=""):
    w(path, head(r, title, desc, path, extra) + header(r) + inner + foot(r))
def old(p):
    s = rd(p)
    m = re.search(r"<main.*?</main>", s, re.S).group(0)
    t = html.unescape(re.search(r"<title>(.*?)</title>", s).group(1))
    d = re.search(r'<meta name="description" content="(.*?)">', s)
    return m, t, html.unescape(d.group(1)) if d else ""
def legacy():
    gp = "GST registration from ₹3,000 · monthly filing from ₹1,000/month. Final quote after reviewing your requirements."
    for l in LOCS:
        p = f"locations/gst-registration-{l}.html"
        m, t, d = old(p)
        m = m.replace("<p>Contact us for pricing.</p>", f"<p>{gp}</p>")
        shell("../", t, d, p, m, "" if l == "puducherry" else '<meta name="robots" content="noindex,follow">')
    TD2 = {"gst-calculator": "Free GST calculator: work out GST-inclusive or GST-exclusive amounts.", "gst-checklist": "Checklist of documents commonly needed for GST registration.",
           "fssai-checklist": "Basic information commonly needed for FSSAI applications.", "itr-checklist": "Documents commonly needed before filing your income tax return."}
    for t_ in TOOLS:
        p = f"tools/{t_[0]}.html"
        s0 = rd(p)
        m, t, d = old(p)
        sc = re.search(r"<script>function calc.*?</script>", s0, re.S)
        sc = sc.group(0) if sc else ""
        if sc and "calculator_use" not in sc:
            sc = sc.replace("document.getElementById('out').innerHTML", "window.gtag&&gtag('event','calculator_use',{tool:'gst'});document.getElementById('out').innerHTML")
        cta = ""
        if t_[0] == "gst-calculator":
            cta = '<div class="wrap" style="padding-bottom:50px"><p>Need help with GST? ' + btn(wa("Hello Vivian, I need help with GST."), "WhatsApp Vivian", "WhatsApp-ல் பேசுங்கள்", "primary", "calculator", True) + "</p></div>"
        shell("../", t, TD2[t_[0]] + " Free from KVB ENTERPRISES, Puducherry.", p, m + cta + sc)
    P = ('<main class="legal"><div class="wrap"><a class="back" href="index.html">← Home</a><h1>Privacy</h1>'
         "<p>When you contact KVB ENTERPRISES through WhatsApp, phone or the enquiry form, information you provide is used to respond to your request and provide the requested assistance. We do not sell your personal information.</p>"
         "<p>The enquiry form on this website does not store your details. It opens WhatsApp with your message ready, and the message is sent only when you press send in WhatsApp. WhatsApp's own terms and privacy policy then apply.</p>"
         "<p>This website uses Google Analytics to understand how visitors use it, such as which pages are viewed and which buttons (WhatsApp, call, enquiry form) are clicked. Google collects this data using cookies or similar technologies. We do not send your name or phone number from the enquiry form to Google Analytics.</p>"
         "<p>Please do not send passwords, OTPs, card PINs or other highly sensitive authentication information through the enquiry form or WhatsApp. Share identity documents only when we ask for them for your service.</p>"
         f"<p>Questions about privacy: call or WhatsApp 90036 33696. Last updated: {TD.strftime('%d %B %Y')}.</p></div></main>")
    Tm = ('<main class="legal"><div class="wrap"><a class="back" href="index.html">← Home</a><h1>Terms</h1>'
          "<p>KVB ENTERPRISES provides independent professional assistance and documentation support. We are not a government department or authority, and we are not affiliated with any government portal.</p>"
          "<p>Prices shown on this website are starting prices. The final quote is confirmed after reviewing your requirements and documents, before you proceed. Government fees, statutory charges and third-party charges, where applicable, are separate from our professional fee and may vary by service and case.</p>"
          "<p>Where a task legally requires a Chartered Accountant or another licensed professional (for example a tax audit), it is carried out by that professional, and we coordinate the process.</p>"
          "<p>We assist with applications and filings. Approvals, timelines and outcomes are decided by the relevant authorities, and we cannot guarantee them. Information on this website is general and is not tax or legal advice for your specific situation.</p></div></main>")
    shell("", "Privacy | KVB ENTERPRISES", "How KVB ENTERPRISES uses information you share through WhatsApp, calls, the enquiry form and website analytics.", "privacy.html", P)
    shell("", "Terms | KVB ENTERPRISES", "Terms for using the KVB ENTERPRISES website and professional assistance services, including pricing and fees.", "terms.html", Tm)


TA_SV = {"gst", "itr", "fssai", "msme"}
def L(s):
    return TA.get(s, s) if LANG == "ta" else s
def build_all():
    global LANG
    for lg in ("en", "ta"):
        LANG = lg
        for x in SV:
            if lg == "en" or x[0] in TA_SV:
                svc(x)
        index()
    LANG = "en"
TA = {
 "Business": "வணிகம்", "Send enquiry on WhatsApp": "WhatsApp-ல் விசாரணை அனுப்பு",
 "Tax &amp; Business Compliance": "வரி & வணிக இணக்கம்", "Tax &amp; Business Compliance Services": "வரி & வணிக இணக்க சேவைகள்", "Puducherry &amp; nearby areas": "புதுச்சேரி & சுற்றுப்புறங்கள்",
 "WhatsApp enquiries welcome anytime": "WhatsApp விசாரணைகள் எப்போதும் வரவேற்கப்படுகின்றன",
 "Hello Vivian, I would like to know about your services.": "வணக்கம் விவியன், உங்கள் சேவைகள் பற்றி தெரிந்துகொள்ள விரும்புகிறேன்.",
 "Hello Vivian, I need assistance with your services.": "வணக்கம் விவியன், உங்கள் சேவைகளில் உதவி தேவை.",
 "Hello Vivian, I would like to get started.": "வணக்கம் விவியன், தொடங்க விரும்புகிறேன்.",
 "Hello Vivian, I am starting a business and need guidance.": "வணக்கம் விவியன், நான் புதிய வணிகம் தொடங்குகிறேன்; வழிகாட்டுதல் தேவை.",
 "Restaurants &amp; Food Businesses": "உணவகங்கள் & உணவு வணிகங்கள்", "Bakeries &amp; Home Bakers": "பேக்கரிகள் & வீட்டு பேக்கர்கள்", "Cafés &amp; Tea Shops": "கஃபேக்கள் & தேநீர் கடைகள்",
 "Cloud Kitchens": "கிளவுட் கிச்சன்கள்", "Boutiques &amp; Fashion": "பொட்டிக் & ஃபேஷன் கடைகள்", "Retail Shops": "சில்லறை கடைகள்", "Supermarkets": "சூப்பர் மார்க்கெட்கள்",
 "Salons &amp; Spas": "சலூன் & ஸ்பா", "Clinics &amp; Small Businesses": "கிளினிக்குகள் & சிறு வணிகங்கள்", "Traders &amp; Wholesalers": "வியாபாரிகள் & மொத்த விற்பனையாளர்கள்",
 "Manufacturers": "உற்பத்தியாளர்கள்", "Online Sellers": "ஆன்லைன் விற்பனையாளர்கள்", "Freelancers &amp; Professionals": "ஃப்ரீலான்சர்கள் & தொழில்முறையாளர்கள்", "New Businesses": "புதிய வணிகங்கள்",
 "Udyam / MSME": "உத்யம் / MSME", "Shops &amp; Establishment": "Shops & Establishment", "Business registration": "வணிக பதிவு",
 "We focus on clear communication, documentation support and regular follow-up, and we are not a government office or authority.": "தெளிவான தகவல்தொடர்பு, ஆவண உதவி மற்றும் தொடர்ச்சியான பின்தொடர்வில் கவனம் செலுத்துகிறோம். நாங்கள் அரசு அலுவலகமோ அதிகார அமைப்போ அல்ல.",
 "Personal assistance": "தனிப்பட்ட உதவி", "Direct communication and guidance for your requirements.": "உங்கள் தேவைகளுக்கு நேரடி தொடர்பு மற்றும் வழிகாட்டுதல்.",
 "Clear process": "தெளிவான செயல்முறை", "Understand the documents, steps and professional charges before proceeding.": "தொடங்கும் முன் ஆவணங்கள், படிகள் மற்றும் தொழில்முறை கட்டணங்களைப் புரிந்துகொள்ளுங்கள்.",
 "Choose a location to view the local GST service page.": "உங்கள் பகுதியைத் தேர்ந்தெடுத்து உள்ளூர் GST சேவை பக்கத்தைப் பாருங்கள்.",
 "Puducherry": "புதுச்சேரி", "Villupuram": "விழுப்புரம்", "Cuddalore": "கடலூர்", "Tindivanam": "திண்டிவனம்", "Panruti": "பண்ருட்டி", "Karaikal": "காரைக்கால்", "Tiruvannamalai": "திருவண்ணாமலை", "Chidambaram": "சிதம்பரம்", "Mayiladuthurai": "மயிலாடுதுறை",
 "GST Calculator": "GST கணக்கீட்டு கருவி", "Calculate GST-inclusive or GST-exclusive amounts.": "GST உட்பட அல்லது GST நீங்கலான தொகைகளைக் கணக்கிடுங்கள்.", "Open tool →": "கருவியைத் திறக்க →",
 "GST Registration Checklist": "GST பதிவு சரிபார்ப்பு பட்டியல்", "Common documents and information to keep ready.": "தயாராக வைத்திருக்க வேண்டிய பொதுவான ஆவணங்கள் மற்றும் தகவல்கள்.", "Open checklist →": "பட்டியலைத் திறக்க →",
 "FSSAI Checklist": "FSSAI சரிபார்ப்பு பட்டியல்", "Basic information commonly required for food-business applications.": "உணவு வணிக விண்ணப்பங்களுக்கு பொதுவாகத் தேவைப்படும் அடிப்படை தகவல்கள்.",
 "ITR Document Checklist": "ITR ஆவண சரிபார்ப்பு பட்டியல்", "Prepare common documents before starting your return.": "ரிட்டர்ன் தொடங்கும் முன் பொதுவான ஆவணங்களைத் தயார் செய்யுங்கள்.",
 "Do you provide services outside Puducherry?": "புதுச்சேரிக்கு வெளியிலும் சேவை வழங்குகிறீர்களா?",
 "Yes. We assist clients in nearby areas including Villupuram, Cuddalore, Tindivanam, Panruti, Karaikal and other listed locations. Contact us to confirm availability.": "ஆம். விழுப்புரம், கடலூர், திண்டிவனம், பண்ருட்டி, காரைக்கால் உள்ளிட்ட அருகிலுள்ள பகுதிகளிலும் உதவுகிறோம். கிடைப்பதை உறுதி செய்ய எங்களைத் தொடர்பு கொள்ளுங்கள்.",
 "How do I know the price?": "விலையை எப்படி அறிவது?", "Can you help with a new business?": "புதிய வணிகம் தொடங்க உதவ முடியுமா?",
 "Yes. We can help you understand the registrations and documentation relevant to your business type.": "ஆம். உங்கள் வணிக வகைக்கு பொருந்தும் பதிவுகள் மற்றும் ஆவணங்களைப் புரிந்துகொள்ள உதவுகிறோம்.",
 "Do I need GST for a home bakery?": "வீட்டு பேக்கரிக்கு GST தேவையா?",
 "It depends on your circumstances. GST applicability can depend on factors such as turnover and the nature of your supplies, and FSSAI requirements are a separate matter. If you're starting a home bakery, we can help you review GST, FSSAI, Udyam and other registrations that may apply before you begin.": "இது உங்கள் சூழலைப் பொறுத்தது. GST பொருந்துமா என்பது விற்றுமுதல், விற்பனையின் தன்மை போன்றவற்றைப் பொறுத்தது; FSSAI தேவை தனி விஷயம். வீட்டு பேக்கரி தொடங்கும் முன் GST, FSSAI, உத்யம் மற்றும் பொருந்தக்கூடிய பிற பதிவுகளை ஆய்வு செய்ய நாங்கள் உதவுவோம்.",
 "What documents will I need?": "எனக்கு என்ன ஆவணங்கள் தேவை?",
 "It depends on the service and your business type. Each service page lists commonly needed documents, and we confirm the exact list for your case on WhatsApp.": "சேவை மற்றும் உங்கள் வணிக வகையைப் பொறுத்தது. ஒவ்வொரு சேவை பக்கத்திலும் பொதுவாகத் தேவைப்படும் ஆவணங்கள் உள்ளன; உங்கள் நிலைக்கான சரியான பட்டியலை WhatsApp-ல் உறுதி செய்வோம்.",
 "What are your working hours?": "உங்கள் வேலை நேரம் என்ன?", "WhatsApp enquiries are welcome at any time. We reply as soon as we can.": "WhatsApp விசாரணைகள் எப்போதும் வரவேற்கப்படுகின்றன. முடிந்தவரை விரைவில் பதிலளிப்போம்.",
 "Is KVB ENTERPRISES a government office?": "KVB ENTERPRISES ஒரு அரசு அலுவலகமா?", "No. KVB ENTERPRISES is an independent professional assistance service and is not a government department.": "இல்லை. KVB ENTERPRISES ஒரு சுயாதீன தொழில்முறை உதவி சேவை; அரசுத் துறை அல்ல.",
 "← All services": "← அனைத்து சேவைகள்", "What we can help with": "நாங்கள் உதவக்கூடியவை", "Documents commonly needed": "பொதுவாகத் தேவைப்படும் ஆவணங்கள்", "Pricing": "கட்டணம்", "Need assistance?": "உதவி தேவையா?",
 "The exact list depends on your case. We confirm it with you on WhatsApp before you start.": "சரியான பட்டியல் உங்கள் நிலையைப் பொறுத்தது. தொடங்கும் முன் WhatsApp-ல் உறுதி செய்வோம்.",
 "Tell Vivian what you need and get the document and process guidance for your case.": "உங்கள் தேவையை விவியனிடம் சொல்லுங்கள்; உங்களுக்கான ஆவண மற்றும் செயல்முறை வழிகாட்டுதலைப் பெறுங்கள்.",
 "Tamil &amp; English. Local assistance in Puducherry and nearby areas.": "தமிழ் & ஆங்கிலம். புதுச்சேரி மற்றும் சுற்றுப்புறங்களில் உள்ளூர் உதவி.", "How it works": "எப்படி செயல்படுகிறது", "Common questions": "பொதுவான கேள்விகள்",
 "GST registration assistance": "GST பதிவு உதவி", "GSTR-1 and GSTR-3B filing support": "GSTR-1 மற்றும் GSTR-3B தாக்கல் உதவி", "Monthly GST compliance": "மாதாந்திர GST இணக்கம்", "Amendment and cancellation assistance": "திருத்தம் மற்றும் ரத்து உதவி", "Reconciliation and documentation support": "ஒப்பீடு மற்றும் ஆவண உதவி",
 "PAN and Aadhaar of the proprietor, partners or directors": "உரிமையாளர், பங்குதாரர்கள் அல்லது இயக்குநர்களின் PAN மற்றும் ஆதார்", "Passport-size photograph": "பாஸ்போர்ட் அளவு புகைப்படம்",
 "Business address proof (for example rent agreement or electricity bill)": "வணிக முகவரி ஆதாரம் (எ.கா. வாடகை ஒப்பந்தம் அல்லது மின்கட்டண ரசீது)", "Bank account details": "வங்கிக் கணக்கு விவரங்கள்",
 "Individual ITR filing": "தனிநபர் ITR தாக்கல்", "Business and professional ITR filing": "வணிகம் மற்றும் தொழில்முறை ITR தாக்கல்", "Tax compliance support": "வரி இணக்க உதவி",
 "Tax audit support, coordinated through a Chartered Accountant where required": "தேவைப்படும் இடங்களில் பட்டயக் கணக்காளர் (CA) மூலம் ஒருங்கிணைக்கப்படும் வரி தணிக்கை உதவி",
 "PAN and Aadhaar": "PAN மற்றும் ஆதார்", "Form 16 or income details": "படிவம் 16 அல்லது வருமான விவரங்கள்", "Bank statements and interest certificates": "வங்கி அறிக்கைகள் மற்றும் வட்டி சான்றிதழ்கள்", "Investment and deduction proofs": "முதலீடு மற்றும் விலக்கு ஆதாரங்கள்", "For business: turnover and expense details": "வணிகத்திற்கு: விற்றுமுதல் மற்றும் செலவு விவரங்கள்",
 "New FSSAI registration or licence": "புதிய FSSAI பதிவு அல்லது உரிமம்", "Renewal assistance": "புதுப்பிப்பு உதவி", "Modification and updates": "மாற்றங்கள் மற்றும் புதுப்பிப்புகள்", "Guidance on which type suits your food business": "உங்கள் உணவு வணிகத்திற்கு எந்த வகை பொருந்தும் என்ற வழிகாட்டுதல்",
 "Photo ID and passport-size photograph": "புகைப்பட அடையாள அட்டை மற்றும் பாஸ்போர்ட் அளவு புகைப்படம்", "Business address proof": "வணிக முகவரி ஆதாரம்", "Details of food products or activities": "உணவு பொருட்கள் அல்லது செயல்பாடுகளின் விவரங்கள்", "Premises details": "இடம் குறித்த விவரங்கள்",
 "Udyam registration": "உத்யம் பதிவு", "Updates to existing registration": "உள்ள பதிவில் புதுப்பிப்புகள்", "Documentation support": "ஆவண உதவி", "Aadhaar of the owner": "உரிமையாளரின் ஆதார்", "PAN": "PAN", "Business and bank details": "வணிகம் மற்றும் வங்கி விவரங்கள்", "GSTIN, if you have one": "GSTIN, இருந்தால்",
}
TA[EXTRA["gst"]] = "அதிகாரப்பூர்வ GST இணையதளத்தில் பதிவு செய்ய அரசு விண்ணப்பக் கட்டணம் இல்லை. எங்கள் கட்டணம் ஆவணங்கள், விண்ணப்பம் மற்றும் பின்தொடர்வு உதவிக்கானது."
TA[EXTRA["msme"]] = "அதிகாரப்பூர்வ அரசு இணையதளத்தில் (udyamregistration.gov.in) உத்யம் பதிவு இலவசம்; நீங்களே பதிவு செய்யலாம். எங்கள் கட்டணம் ஆவணங்கள் மற்றும் விண்ணப்பத்திற்கான விருப்பத் தேர்வான உதவிக் கட்டணம். KVB ENTERPRISES அரசு இணையதளம் அல்ல."
TA[EXTRA["fssai"]] = "அரசு உரிமம் அல்லது பதிவு கட்டணங்கள் எங்கள் தொழில்முறை கட்டணத்திலிருந்து தனி; அவை உரிம வகையைப் பொறுத்தது."
TA[EXTRA["itr"]] = "தொடக்க விலை தணிக்கை உதவியுடன் கூடிய ITR-க்கானது. தணிக்கை தேவைப்படும் இடங்களில் அதை பட்டயக் கணக்காளர் மேற்கொள்வார். தணிக்கை இல்லாத ITR: விலைக்கு தொடர்பு கொள்ளுங்கள்."
TA[FAQ[1][1]] = "கிடைக்கும் இடங்களில் ஒவ்வொரு சேவையிலும் தொடக்க விலை காட்டப்படும். " + NOTE_TA
_f = {
 "gst": [("என் சிறு வணிகத்திற்கு GST பதிவு தேவையா?", "இது உங்கள் விற்றுமுதல், விற்பனையின் தன்மை மற்றும் செயல்படும் இடத்தைப் பொறுத்தது. சில வணிகங்கள் பதிவு செய்ய வேண்டும்; மற்றவை விருப்பப்பட்டால் பதிவு செய்யலாம். உங்கள் விவரங்களை அனுப்புங்கள், எது பொருந்தும் என்று விளக்குவோம்."),
         ("GST பதிவுக்கு என்ன ஆவணங்கள் தேவை?", "பொதுவாக PAN, ஆதார், புகைப்படம், வணிக முகவரி ஆதாரம் மற்றும் வங்கி விவரங்கள். சரியான பட்டியல் உங்கள் வணிக அமைப்பைப் பொறுத்தது; அதை உங்களுடன் உறுதி செய்வோம்."),
         ("மாதாந்திர GST தாக்கலுக்கு உதவ முடியுமா?", "ஆம். தகுதியான வணிகங்களுக்கு GSTR-1 மற்றும் GSTR-3B தாக்கல் மற்றும் மாதாந்திர இணக்கத்தில் உதவுகிறோம். உங்கள் தேவைகளை பரிசீலித்த பின் இறுதிக் கட்டணம் உறுதி செய்யப்படும்.")],
 "itr": [("CA இல்லாமல் ITR தாக்கலுக்கு உதவ முடியுமா?", "ஆம். தனிநபர்கள் மற்றும் வணிகங்களுக்கு ITR தயாரிப்பு மற்றும் தாக்கலில் உதவுகிறோம். வரி தணிக்கை தேவைப்பட்டால், அதை பட்டயக் கணக்காளர் மேற்கொள்ள வேண்டும்; அதை நாங்கள் ஒருங்கிணைக்கிறோம்."),
         ("ITR-க்கு என்ன ஆவணங்கள் தேவை?", "பொதுவாக PAN, ஆதார், வருமான விவரங்கள், வங்கி அறிக்கைகள் மற்றும் முதலீடு அல்லது விலக்கு ஆதாரங்கள். மேலே உள்ள பட்டியலையும் ITR சரிபார்ப்பு பட்டியலையும் பாருங்கள்.")],
 "fssai": [("வீட்டு பேக்கரிக்கு FSSAI தேவையா?", "வீட்டிலிருந்து நடத்தும் உணவு வணிகங்களுக்கு விற்றுமுதல் மற்றும் செயல்பாட்டைப் பொறுத்து FSSAI பதிவு அல்லது உரிமம் தேவைப்படலாம். நீங்கள் என்ன தயாரித்து விற்கிறீர்கள் என்று சொல்லுங்கள், வழிகாட்டுவோம்."),
           ("FSSAI பதிவுக்கும் உரிமத்துக்கும் என்ன வித்தியாசம்?", "உணவு வணிகத்தின் அளவு மற்றும் தன்மையின் அடிப்படையில் அவை வெவ்வேறு பிரிவுகள். உங்களுக்கு எது பொருந்தும் என்பதை அடையாளம் காண உதவுகிறோம்.")],
 "msme": [("உத்யம் பதிவுக்கு யார் விண்ணப்பிக்கலாம்?", "தகுதியுள்ள குறு, சிறு மற்றும் நடுத்தர நிறுவனங்கள், பல சிறு சேவை வணிகங்கள் உட்பட. தகுதி உங்கள் செயல்பாடு மற்றும் திட்ட விதிகளைப் பொறுத்தது."),
          ("உத்யம் பதிவு இலவசமா?", "ஆம். அதிகாரப்பூர்வ இணையதளத்தில் பதிவு கட்டணம் இல்லை; நீங்களே பதிவு செய்யலாம். விருப்பப்பட்டால் உதவிக் கட்டணத்தில் எங்களிடம் உதவி கேட்கலாம்.")]}
for _k, _v in _f.items():
    for (_q, _a), (_tq, _ta) in zip(FAQS[_k], _v):
        TA[_q] = _tq; TA[_a] = _ta

main()
