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
    a = f' data-en="{E(en)}" data-ta="{E(ta)}"' if ta else ""
    c = f' class="{cls}"' if cls else ""
    x = " " + x if x else ""
    return f"<{tag}{c}{a}{x}>{en}</{tag}>"

def wa(m):
    return f"https://wa.me/{PH}?text=" + U.quote(m)

ICON = ('<svg class="wa-ico" viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>')

# slug, en, ta, desc_en, desc_ta, help items, typical documents
SV = [
 ("gst", "GST Services", "GST சேவைகள்", "Registration, returns, monthly compliance, amendments, cancellation and reconciliation assistance.", "பதிவு, ரிட்டர்ன் தாக்கல், மாதாந்திர இணக்கம், திருத்தம் மற்றும் ரத்து உதவி.",
  ["GST registration assistance", "GSTR-1 and GSTR-3B filing support", "Monthly GST compliance", "Amendment and cancellation assistance", "Reconciliation and documentation support"],
  ["PAN and Aadhaar of the proprietor, partners or directors", "Passport-size photograph", "Business address proof (for example rent agreement or electricity bill)", "Bank account details"]),
 ("itr", "Income Tax / ITR", "வருமான வரி / ITR", "Individual and business ITR preparation, tax compliance support and CA coordination where required.", "தனிநபர் மற்றும் வணிக ITR தயாரிப்பு மற்றும் வரி இணக்க உதவி.",
  ["Individual ITR filing", "Business and professional ITR filing", "Tax compliance support", "Tax audit support, carried out through a Chartered Accountant where required"],
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

def head(r, title, desc, path, ld=""):
    u = f"{S}/{path}"
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#29135e">'
            f'<link rel="canonical" href="{u}"><meta property="og:type" content="website"><meta property="og:site_name" content="KVB ENTERPRISES">'
            f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{u}">'
            f'<meta property="og:image" content="{S}/assets/logo.png"><link rel="icon" type="image/png" href="{r}assets/logo.png">'
            f'<link rel="stylesheet" href="{r}style.css"><script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>'
            f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA}');</script>{ld}</head><body>")

def header(r):
    n = "".join(T("a", en, ta, x=f'href="{r}index.html#{i}"') for i, en, ta in NAV)
    return (f'<header class="topbar"><div class="wrap nav"><a class="brand" href="{r}index.html" aria-label="KVB ENTERPRISES home">'
            f'<img src="{r}assets/logo.png" alt="KVB ENTERPRISES logo" width="56" height="56"><span><b>KVB</b> ENTERPRISES<small>Tax &amp; Business Compliance</small></span></a>'
            f'<div class="nav-right"><nav id="mainNav" aria-label="Main navigation">{n}</nav><button class="lang" id="langBtn" type="button">தமிழ்</button>'
            f'<button class="menu" id="menuBtn" type="button" aria-label="Menu" aria-expanded="false">☰</button></div></div></header>')

def foot(r):
    bar = (f'<div class="mbar"><a href="{wa("Hello Vivian, I would like to know about your services.")}" target="_blank" rel="noopener" data-loc="mobile-bar">{ICON}WhatsApp</a>'
           + T("a", "Call", "அழைக்க", x=f'href="tel:+{PH}" data-loc="mobile-bar"') + '</div>')
    return (bar + f'<a class="floating-wa" href="{wa("Hello Vivian, I would like to know about your services.")}" target="_blank" rel="noopener" aria-label="WhatsApp KVB ENTERPRISES" data-loc="floating">{ICON}</a>'
            f'<footer><div class="wrap footer"><div class="footer-brand"><img src="{r}assets/logo.png" alt="KVB ENTERPRISES logo" width="44" height="44" loading="lazy">'
            f'<div><b>KVB ENTERPRISES</b><p>Tax &amp; Business Compliance Services</p></div></div>'
            f'<div>GST • ITR • FSSAI • PAN • MSME • Trademark • DSC<br>Puducherry &amp; nearby areas</div>'
            f'<div><a href="{r}privacy.html">Privacy</a> • <a href="{r}terms.html">Terms</a><br>© <span class="yr">{TD.year}</span> KVB ENTERPRISES</div></div></footer>'
            f'<script src="{r}script.js" defer></script></body></html>')

def btn(href, en, ta, cls="primary", loc="", ico=False, ext=True):
    t = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="btn {cls}" href="{href}"{t} data-loc="{loc}">{ICON if ico else ""}<span data-en="{E(en)}" data-ta="{E(ta)}">{en}</span></a>'

def price(s):
    L = PR.get(s) or []
    if not L:
        return T("em", "Get a quote", "விலை விவரம் பெறுக", "price")
    en = "<br>".join(f"{a} from ₹{c}{d}" for a, b, c, d in L)
    ta = "<br>".join(f"{b or a} ₹{c}{d} முதல்" for a, b, c, d in L)
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
    b = head("", "KVB ENTERPRISES | Tax & Business Compliance in Puducherry", "Local tax and business compliance assistance in Puducherry and nearby areas. GST, ITR, FSSAI, PAN, MSME/Udyam, Trademark, DSC and business registration. Tamil & English, WhatsApp support.", "", ld) + header("")
    quick = "".join(f'<a href="services/{s[0]}.html">{SHORT[s[0]]}</a>' for s in SV)
    b += ('<main id="home"><section class="hero"><div class="wrap hero-grid"><div class="hero-copy">'
          + T("div", "Local tax &amp; business compliance", "உள்ளூர் வரி மற்றும் வணிக இணக்க சேவைகள்", "eyebrow")
          + T("h1", "Your Business.<br><span>Our Responsibility.</span>", "உங்கள் தொழில்.<br><span>எங்கள் பொறுப்பு.</span>")
          + T("p", "Professional assistance for GST, Income Tax / ITR, FSSAI, PAN, MSME/Udyam, Trademark, DSC and business registrations.", "GST, வருமான வரி / ITR, FSSAI, PAN, MSME/உத்யம், வர்த்தக முத்திரை, DSC மற்றும் வணிக பதிவுகளுக்கு தொழில்முறை உதவி.", "lead")
          + '<div class="actions">' + btn(wa("Hello Vivian, I need assistance with your services."), "WhatsApp Vivian", "WhatsApp-ல் பேசுங்கள்", "primary", "hero", True)
          + btn(f"tel:+{PH}", "Call now", "இப்போது அழைக்கவும்", "secondary", "hero", False, False) + "</div>"
          + T("p", "Tamil &amp; English • WhatsApp enquiries welcome anytime • Personal assistance", "தமிழ் &amp; ஆங்கிலம் • WhatsApp-ல் எப்போதும் வரவேற்கிறோம் • தனிப்பட்ட உதவி", "trust")
          + f'</div><div class="hero-card"><div class="logo-card"><img src="assets/logo.png" alt="KVB ENTERPRISES" width="100" height="100"></div>'
          + T("div", "Need help with your business compliance?", "உங்கள் வணிக இணக்கத்தில் உதவி தேவையா?", "card-title")
          + f'<div class="quick">{quick}</div><div class="mini">Call / WhatsApp<br><strong>90036 33696</strong></div></div></div></section>')
    b += ('<section class="clients"><div class="wrap clients-grid"><div class="big"><strong>300+</strong>' + T("span", "Clients served", "வாடிக்கையாளர்களுக்கு சேவை") + '</div><div>'
          + T("h2", "Trusted local support in and around Puducherry", "புதுச்சேரி மற்றும் சுற்றுப்புறங்களில் நம்பகமான உள்ளூர் உதவி")
          + T("p", "Businesses, professionals and individuals have used KVB ENTERPRISES for practical, personal compliance support.", "வணிகங்கள், தொழில்முறையாளர்கள் மற்றும் தனிநபர்கள் நடைமுறை, தனிப்பட்ட இணக்க உதவிக்காக KVB ENTERPRISES-ஐ பயன்படுத்தியுள்ளனர்.")
          + '<ul class="ticks">' + T("li", "Direct support from Vivian", "விவியனிடமிருந்து நேரடி உதவி") + T("li", "Clear steps and document lists", "தெளிவான படிகள் மற்றும் ஆவண பட்டியல்") + T("li", "Updates on WhatsApp", "WhatsApp மூலம் தகவல்") + '</ul></div></div></section>')
    cards = "".join(f'<a class="service-card" href="services/{s[0]}.html" data-service="{E(s[1])}">{T("h3", s[1], s[2])}{T("p", s[3], s[4])}{price(s[0])}'
                    f'{T("span", "View service →", "சேவையைப் பார்க்க →")}</a>' for s in SV)
    b += ('<section id="services" class="section"><div class="wrap"><div class="section-head">' + T("h2", "Everything your business needs, in one place.", "உங்கள் வணிகத்திற்குத் தேவையான சேவைகள் அனைத்தும் ஒரே இடத்தில்.")
          + T("p", NOTE_EN, NOTE_TA) + f'</div><div class="cards">{cards}</div></div></section>')
    b += ('<section id="how" class="section alt"><div class="wrap"><div class="section-head">' + T("h2", "How it works", "எப்படி செயல்படுகிறது") + "</div>" + steps()
          + '<div class="how-cta">' + btn(wa("Hello Vivian, I would like to get started."), "Start on WhatsApp →", "WhatsApp-ல் தொடங்குங்கள் →", "primary", "how-it-works", True) + "</div></div></section>")
    chips = "".join(f"<span>{c}</span>" for c in ["Restaurants &amp; Food Businesses", "Bakeries &amp; Home Bakers", "Cafés &amp; Tea Shops", "Cloud Kitchens", "Boutiques &amp; Fashion", "Retail Shops", "Supermarkets", "Salons &amp; Spas", "Clinics &amp; Small Businesses", "Traders &amp; Wholesalers", "Manufacturers", "Online Sellers", "Freelancers &amp; Professionals", "New Businesses"])
    b += ('<section id="business" class="section"><div class="wrap"><div class="section-head">' + T("h2", "Who we help", "யாருக்கு உதவுகிறோம்") + f'</div><div class="chips">{chips}</div>'
          '<div class="newbiz"><div>' + T("h3", "Starting a small business in Puducherry?", "புதுச்சேரியில் சிறு தொழில் தொடங்குகிறீர்களா?")
          + T("p", "Before you start, check which registrations may apply. We'll help you work out what applies to your business.", "தொடங்கும் முன், எந்த பதிவுகள் பொருந்தும் என்று பாருங்கள். உங்கள் வணிகத்திற்கு எது பொருந்தும் என்பதைக் கண்டறிய உதவுவோம்.")
          + '<ul class="nb-list"><li>GST</li><li>FSSAI</li><li>Udyam / MSME</li><li>Shops &amp; Establishment</li><li>Business registration</li></ul></div>'
          + btn(wa("Hello Vivian, I am starting a business and need guidance."), "Talk to Vivian", "விவியனிடம் பேசுங்கள்", "primary", "new-business", True) + "</div></div></section>")
    b += ('<section id="about" class="section alt"><div class="wrap about-grid"><div>' + T("h2", "Your local compliance partner.", "உங்கள் உள்ளூர் இணக்க துணை.")
          + T("p", "KVB ENTERPRISES provides practical tax and business compliance assistance for businesses, professionals and individuals in Puducherry and nearby areas.", "KVB ENTERPRISES புதுச்சேரி மற்றும் சுற்றுப்புறங்களில் உள்ள வணிகங்கள், தொழில்முறையாளர்கள் மற்றும் தனிநபர்களுக்கு நடைமுறை வரி மற்றும் வணிக இணக்க உதவி வழங்குகிறது.")
          + "<p>We focus on clear communication, documentation support and regular follow-up, and we are not a government office or authority.</p></div>"
          '<div class="about-points"><div><b>Personal assistance</b><span>Direct communication and guidance for your requirements.</span></div><div><b>Clear process</b><span>Understand the documents, steps and professional charges before proceeding.</span></div></div></div></section>')
    locs = "".join(f'<a href="locations/gst-registration-{l}.html">{l.title()}</a>' for l in LOCS)
    b += ('<section id="locations" class="section"><div class="wrap"><div class="section-head">' + T("h2", "Local assistance across Puducherry and nearby areas.", "புதுச்சேரி மற்றும் சுற்றுப்புறங்களில் உள்ளூர் உதவி.")
          + f'<p>Choose a location to view the local GST service page.</p></div><div class="locations">{locs}</div></div></section>')
    tools = "".join(f'<div><h3>{t[1]}</h3><p>{t[2]}</p><a href="tools/{t[0]}.html">{t[3]}</a></div>' for t in TOOLS)
    b += ('<section id="tools" class="section alt"><div class="wrap"><div class="section-head">' + T("h2", "Useful resources for business owners.", "தொழில் உரிமையாளர்களுக்கான பயனுள்ள வளங்கள்.") + f'</div><div class="tool-grid">{tools}</div></div></section>')
    fq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    b += ('<section class="faq section"><div class="wrap"><div class="section-head">' + T("h2", "Common questions", "பொதுவான கேள்விகள்") + f'</div><div class="faq-list">{fq}</div></div></section>')
    opts = "".join(f'<option value="{E(v)}" data-en="{E(v)}" data-ta="{E(t)}">{v}</option>' for v, t in [
        ("GST Registration", "GST பதிவு"), ("GST Filing", "GST ரிட்டர்ன் தாக்கல்"), ("Income Tax / ITR", "வருமான வரி / ITR"), ("FSSAI", "FSSAI"), ("PAN Card Services", "PAN அட்டை சேவைகள்"),
        ("MSME / Udyam", "MSME / உத்யம்"), ("Trademark", "வர்த்தக முத்திரை"), ("DSC", "DSC"), ("Business Registration", "வணிக பதிவு"), ("Other", "மற்றவை")])
    b += ('<section id="contact" class="contact"><div class="wrap contact-grid"><div>' + T("h2", "Have a compliance question?", "இணக்கம் தொடர்பான கேள்வியா?")
          + T("p", "Send your requirement and Vivian can explain the process, documents and applicable professional charges.", "உங்கள் தேவையை அனுப்புங்கள். செயல்முறை, ஆவணங்கள் மற்றும் தொழில்முறை கட்டணங்களை விவியன் விளக்குவார்.")
          + f'<div class="contact-line"><strong>Vivian</strong><br>KVB ENTERPRISES<br><a href="tel:+{PH}" data-loc="contact">90036 33696</a><br>Puducherry &amp; nearby areas<br>WhatsApp enquiries welcome anytime</div></div>'
          '<form class="contact-box" id="enquiryForm">'
          + T("label", 'Name *<input name="name" required autocomplete="name">', 'பெயர் *<input name="name" required autocomplete="name">')
          + T("label", 'Phone / WhatsApp number *<input name="phone" type="tel" inputmode="tel" required pattern="[0-9+ ]{10,15}" autocomplete="tel">', 'தொலைபேசி / WhatsApp எண் *<input name="phone" type="tel" inputmode="tel" required pattern="[0-9+ ]{10,15}" autocomplete="tel">')
          + T("label", f'Service required<select name="service" id="service"><option value="" data-en="Select a service" data-ta="சேவையைத் தேர்ந்தெடுக்கவும்">Select a service</option>{opts}</select>', f'சேவை<select name="service" id="service"><option value="">சேவையைத் தேர்ந்தெடுக்கவும்</option>{opts}</select>')
          + T("label", 'Your message<textarea name="message" rows="3"></textarea>', 'உங்கள் தேவை<textarea name="message" rows="3"></textarea>')
          + f'<button class="btn primary wide" type="submit">{ICON}<span data-en="Send enquiry on WhatsApp" data-ta="WhatsApp-ல் விசாரணை அனுப்பு">Send enquiry on WhatsApp</span></button>'
          + T("p", "This opens WhatsApp with your message ready. We use your details only to reply to your enquiry.", "இது உங்கள் செய்தியுடன் WhatsApp-ஐ திறக்கும். உங்கள் விவரங்கள் பதிலளிக்க மட்டுமே பயன்படுத்தப்படும்.") + "</form></div></section></main>")
    w("index.html", b + foot(""))

def svc(x):
    s, en, ta, d, dta, items, docs = x
    t = f"{en} in Puducherry | KVB ENTERPRISES"
    b = head("../", t, f"{en}: {d} Personal support from KVB ENTERPRISES in Puducherry and nearby areas.", f"services/{s}.html") + header("../")
    msg = wa(f"Hello Vivian, I need assistance with {en}.")
    rel = "".join(f'<a href="{o[0]}.html">{o[1]}</a>' for o in SV if o[0] != s)
    b += f'<main class="service-page"><div class="wrap"><a class="back" href="../index.html#services">← All services</a>{T("h1", en, ta)}{T("p", d, dta, "intro")}'
    if s == "gst":
        b += '<div class="gst-split"><a href="gst-registration.html"><b>GST Registration</b><span>New registration and application assistance →</span></a><a href="gst-filing.html"><b>GST Return Filing</b><span>GSTR-1, GSTR-3B and monthly compliance →</span></a></div>'
    b += ('<div class="service-grid"><div><section class="panel"><h2>What we can help with</h2><ul>' + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul></section>"
          '<section class="panel" style="margin-top:20px"><h2>Documents commonly needed</h2><ul>' + "".join(f"<li>{E(i)}</li>" for i in docs)
          + '</ul><p class="note">The exact list depends on your case. We confirm it with you on WhatsApp before you start.</p></section>'
          '<section class="panel" style="margin-top:20px"><h2>Pricing</h2><p>' + price(s) + f'</p>{T("p", NOTE_EN, NOTE_TA, "note")}{xnote(s)}</section></div>'
          f'<aside class="panel cta-panel"><h2>Need assistance?</h2><p>Tell Vivian what you need and get the document and process guidance for your case.</p>'
          + btn(msg, "WhatsApp 90036 33696", "WhatsApp 90036 33696", "primary wide", s, True) + '<div style="height:10px"></div>' + btn(f"tel:+{PH}", "Call now", "இப்போது அழைக்கவும்", "secondary wide", s, False, False)
          + '<p>Tamil &amp; English. Local assistance in Puducherry and nearby areas.</p></aside></div>'
          '<h2 style="margin-top:40px">How it works</h2>' + steps() + faqhtml(s) + f'<div class="related">{rel}</div></div></main>')
    w(f"services/{s}.html", b + foot("../"))

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
.gst-split{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:26px 0}.gst-split a{display:flex;flex-direction:column;gap:5px;padding:20px;border:1px solid var(--line);border-radius:16px;background:#fff;color:var(--navy);text-decoration:none;box-shadow:0 5px 18px rgba(16,35,63,.04)}.gst-split a:hover{border-color:var(--green);transform:translateY(-2px)}.gst-split b{font-size:18px}.gst-split span{font-size:13px;color:var(--muted)}.gst-split{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:26px 0}.gst-split a{display:flex;flex-direction:column;gap:5px;padding:20px;border:1px solid var(--line);border-radius:16px;background:#fff;color:var(--navy);text-decoration:none;box-shadow:0 5px 18px rgba(16,35,63,.04)}.gst-split a:hover{border-color:var(--green);transform:translateY(-2px)}.gst-split b{font-size:18px}.gst-split span{font-size:13px;color:var(--muted)}.related{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}
.related a{padding:9px 14px;border-radius:999px;background:#fff;border:1px solid var(--line);color:var(--navy);font-weight:750;text-decoration:none;font-size:14px}
.cta-panel .note,.cta-panel p{color:#d7e0ea}
@media(max-width:900px){
.gst-split{grid-template-columns:1fr}
.menu{display:block}.nav{gap:8px}
nav.open{display:flex;position:absolute;left:0;right:0;top:100%;flex-direction:column;align-items:flex-start;gap:0;background:#fff;border-bottom:1px solid var(--line);padding:8px 4% 14px;box-shadow:0 14px 30px rgba(41,19,94,.12)}
nav.open a{padding:12px 0;width:100%;font-size:16px}
.clients-grid,.steps{grid-template-columns:1fr}}
.mbar{display:none}
@media(max-width:700px){.mbar{display:grid;grid-template-columns:1fr 1fr;position:fixed;left:0;right:0;bottom:0;z-index:30;box-shadow:0 -6px 20px rgba(41,19,94,.15)}.mbar a{display:flex;justify-content:center;align-items:center;padding:14px;font-weight:850;text-decoration:none;color:#fff;background:var(--green)}.mbar a+a{background:var(--navy)}.floating-wa{display:none}body{padding-bottom:52px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.service-card{transition:none}}
"""

JS = r"""(function(){
var d=document,cur='en';
var ev=function(n,p){try{if(window.gtag)gtag('event',n,p||{})}catch(e){}};
var q=function(s){return d.querySelectorAll(s)};
function setLang(t){var ta=t==='ta';d.documentElement.lang=t;
q('[data-en]').forEach(function(e){e.innerHTML=(ta&&e.dataset.ta)?e.dataset.ta:e.dataset.en});
q('[data-ph-en]').forEach(function(e){e.placeholder=(ta&&e.dataset.phTa)?e.dataset.phTa:e.dataset.phEn});
var b=d.getElementById('langBtn');if(b)b.textContent=ta?'English':'தமிழ்';
try{localStorage.setItem('lang',t)}catch(x){}}
try{cur=localStorage.getItem('lang')||'en'}catch(x){}
if(cur==='ta')setLang('ta');
var lb=d.getElementById('langBtn');
if(lb)lb.addEventListener('click',function(){cur=cur==='ta'?'en':'ta';setLang(cur);ev('language_switch',{language:cur})});
var mb=d.getElementById('menuBtn'),nv=d.getElementById('mainNav');
if(mb&&nv){mb.addEventListener('click',function(){var o=nv.classList.toggle('open');mb.setAttribute('aria-expanded',o)});
nv.addEventListener('click',function(e){if(e.target.closest('a'))nv.classList.remove('open')})}
q('.yr').forEach(function(e){e.textContent=new Date().getFullYear()});
d.addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;
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
- `style.css`, `script.js` styling, language toggle (English/Tamil), form and analytics events
- `locations/`, `tools/`, `privacy.html`, `terms.html` are also generated; `assets/` is maintained by hand
- `sitemap.xml`, `robots.txt`

## Updating prices
Edit `_builder/prices.json`, then run `python3 _builder/build.py`.
Current starting/professional fees:
- GST registration: ₹3,000
- Monthly GST filing: ₹1,000/month
- ITR with tax audit support: ₹5,000 onwards
- FSSAI assistance: ₹4,000
- MSME/Udyam assistance: ₹1,000
- Trademark assistance: ₹10,000
Other services: contact for pricing.
Government/statutory/third-party charges, where applicable, are separate from KVB ENTERPRISES professional fees.

## Analytics
Google Analytics 4 (G-KFP95JFETM). Events: `whatsapp_click`, `call_click`, `generate_lead` (form), `select_service`, `language_switch`. No names or phone numbers are sent to Google.

KVB ENTERPRISES is an independent professional assistance service and is not a government department.
"""


def gst_split_pages():
    # Dedicated GST registration and GST return-filing pages. Keep gst.html as the GST overview/hub.
    pages = [
      ("gst-registration", "GST Registration", "GST registration assistance for eligible businesses in Puducherry and nearby areas.",
       ["Eligibility and registration guidance", "Document preparation and application assistance", "Business address and promoter details review", "Application follow-up and status guidance"],
       ["PAN and Aadhaar of proprietor, partners or directors", "Photograph", "Business address proof", "Bank account details where applicable"],
       "Registration assistance from ₹3,000",
       [
        ("Who needs GST registration?", "GST registration depends on the applicable GST rules, including turnover, nature of supplies and other circumstances. We review your business details before advising."),
        ("Is there a government fee for GST registration?", "Our ₹3,000 starting amount is our professional assistance fee. Applicable statutory or third-party charges, if any, are separate."),
        ("Can you help after registration?", "Yes. We can also assist with applicable GST return filing and ongoing compliance.")
       ]),
      ("gst-filing", "GST Return Filing", "GST return filing and monthly compliance assistance for eligible businesses in Puducherry and nearby areas.",
       ["GSTR-1 filing assistance", "GSTR-3B filing assistance", "Monthly compliance support", "Reconciliation and documentation support", "Return-related follow-up and correction guidance"],
       ["Sales and purchase records", "Sales invoices and applicable credit/debit notes", "Purchase and expense records", "GST portal credentials or authorised access as appropriate"],
       "Monthly GST filing assistance from ₹1,000/month",
       [
        ("Which GST returns can you help with?", "We assist eligible businesses with common GST return filing such as GSTR-1 and GSTR-3B, based on the taxpayer's applicable filing requirements."),
        ("What records should I maintain for GST filing?", "Sales, purchase and expense records, invoices and other relevant GST records should be maintained. We confirm what is needed for your filing."),
        ("Can you handle GST filing every month?", "Yes. Monthly filing assistance starts from ₹1,000/month, with the final fee confirmed after reviewing the business and filing requirements.")
       ])
    ]
    for slug, title, desc, helps, docs, pricing, faqs in pages:
        inner = f'<main class="service-page"><div class="wrap"><a class="back" href="../services/gst.html">← GST Services</a><h1>{E(title)}</h1><p class="intro">{E(desc)}</p>'
        inner += '<div class="service-grid"><div>'
        inner += '<section class="panel"><h2>What we can help with</h2><ul>' + ''.join(f'<li>{E(x)}</li>' for x in helps) + '</ul></section>'
        inner += '<section class="panel" style="margin-top:20px"><h2>Documents commonly needed</h2><ul>' + ''.join(f'<li>{E(x)}</li>' for x in docs) + '</ul><p class="note">The exact list depends on your case. We confirm it with you before you start.</p></section>'
        inner += f'<section class="panel" style="margin-top:20px"><h2>Pricing</h2><p><em class="price">{E(pricing)}</em></p><p class="note">{E(NOTE_EN)}</p></section></div>'
        inner += f'<aside class="panel cta-panel"><h2>Need assistance?</h2><p>Tell Vivian what you need and get the document and process guidance for your case.</p>'
        inner += btn(wa(f"Hello Vivian, I need help with {title}."), "WhatsApp 90036 33696", "WhatsApp 90036 33696", "primary wide", slug, True)
        inner += f'<div style="height:10px"></div>' + btn(f"tel:+{PH}", "Call now", "இப்போது அழைக்கவும்", "secondary wide", slug, False, False) + '<p>Tamil &amp; English. Local assistance in Puducherry and nearby areas.</p></aside></div>'
        inner += '<h2 style="margin-top:40px">How it works</h2>' + steps()
        inner += '<h2 style="margin-top:40px">Common questions</h2><div class="faq-list">' + ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in faqs) + '</div>'
        inner += '<div class="related"><a href="gst.html">GST Services</a><a href="gst-registration.html">GST Registration</a><a href="gst-filing.html">GST Return Filing</a><a href="itr.html">Income Tax / ITR</a></div></div></main>'
        shell("../", f"{title} in Puducherry | KVB ENTERPRISES", desc + " Personal assistance from KVB ENTERPRISES.", f"services/{slug}.html", inner)

def main():
    gst_split_pages()
    for x in SV:
        svc(x)
    index()
    legacy()
    old = os.path.join(O, "style.css")
    base = open(old, encoding="utf-8").read().split("/* V3 */")[0].rstrip() if os.path.exists(old) else ""
    w("style.css", base + "\n" + CSS)
    w("script.js", JS)
    w("README.md", README)
    w("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {S}/sitemap.xml\n")
    urls = [""] + [f"services/{x[0]}.html" for x in SV] + ["services/gst-registration.html", "services/gst-filing.html"] + ["locations/gst-registration-puducherry.html"] + [f"tools/{t[0]}.html" for t in TOOLS] + ["privacy.html", "terms.html"]
    w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f"<url><loc>{S}/{u}</loc><lastmod>{TD.isoformat()}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    if not os.path.exists(os.path.join(B, "prices.json")):
        json.dump({x[0]: "" for x in SV}, open(os.path.join(B, "prices.json"), "w"), indent=1)

import re
EXTRA = {
 "gst": "GST registration is filed through the official GST portal. Our fee is for professional assistance with documents, the application and follow-up; any applicable statutory or third-party charges are separate.",
 "msme": "Udyam registration on the official government portal (udyamregistration.gov.in) is free of cost, and you can register yourself there. Our fee is an optional assistance fee for documents and the application. KVB ENTERPRISES is not the government portal.",
 "fssai": "Government licence or registration fees are separate from our professional fee and depend on the type of licence.",
 "itr": "Starting price is for ITR with tax audit support. Tax audit, where applicable, is carried out by a Chartered Accountant. Non-audit ITR: contact us for pricing.",
 "trademark": "Government fees are separate from our professional fee.",
}
FAQS = {
 "gst": [
  ("Do I need GST registration for my business?", "GST registration depends on factors such as turnover, the nature of your supplies and where you operate. Some businesses are required to register while others may register voluntarily. We review your details before advising."),
  ("What documents are commonly needed for GST registration?", "Commonly PAN, Aadhaar, photograph, business address proof and bank details. The exact list depends on your business constitution and circumstances."),
  ("How much is GST registration assistance?", "Our professional assistance starts from ₹3,000. The final quote is confirmed after reviewing your requirements. Government or statutory charges, where applicable, are separate."),
  ("Can you help with monthly GST returns?", "Yes. We provide assistance with GSTR-1 and GSTR-3B filing and monthly GST compliance. Our current monthly filing assistance starts from ₹1,000/month.")
 ],
 "itr": [
  ("Can you help me file my ITR?", "Yes. We assist individuals, professionals and businesses with ITR preparation and filing based on the information and documents you provide."),
  ("Can you help if I do not have a CA?", "Yes, we can assist with ITR preparation and filing. Where a tax audit is required, the audit must be carried out by a Chartered Accountant and we coordinate the process with a CA where required."),
  ("What documents are commonly needed for ITR?", "Common documents may include PAN, Aadhaar, Form 16 or other income details, bank statements, interest certificates and investment or deduction proofs. Business cases may also require turnover and expense information."),
  ("Do you provide tax audit?", "We provide tax audit support and coordination. Where a tax audit is required, the audit is carried out through a Chartered Accountant.")
 ],
 "fssai": [
  ("Do I need FSSAI for a home bakery?", "A home-based food business may require FSSAI registration or a licence depending on its activity and applicable criteria. Tell us what you make and sell and we can help identify the appropriate category."),
  ("What is the difference between FSSAI registration and licence?", "FSSAI has different registration/licence categories based on the food business and applicable criteria. We help you identify the category to apply for."),
  ("Can you help renew or modify an FSSAI registration/licence?", "Yes. We assist with eligible renewal and modification applications and help you prepare the required information."),
  ("How much does FSSAI assistance cost?", "Our registration/licence assistance starts from ₹4,000. Government licence or registration fees, where applicable, are separate.")
 ],
 "msme": [
  ("Who can apply for Udyam registration?", "Eligible micro, small and medium enterprises can apply subject to the applicable MSME/Udyam rules. Eligibility depends on the enterprise and its activity."),
  ("Is Udyam registration free?", "Yes. Udyam registration on the official government portal is free. Our ₹1,000 starting amount is an optional professional assistance fee if you want help with the process."),
  ("Can you update an existing Udyam registration?", "Yes. We can assist with eligible updates and documentation."),
  ("How much is your Udyam assistance?", "Our professional assistance fee starts from ₹1,000. The government portal itself does not charge a registration fee.")
 ],
 "pan": [
  ("Can you help with PAN correction?", "Yes. We can assist with PAN correction and details-update applications based on the change required and supporting documents."),
  ("Can you help with a new PAN application?", "Yes. We can guide you through the applicable PAN application process and required documents."),
  ("Can you help if my PAN details and Aadhaar details do not match?", "Yes. We can help you understand the correction or update process based on the mismatch and the documents available."),
  ("What documents may be needed for PAN services?", "Requirements depend on the application. We will confirm the appropriate identity, address and supporting documents for your case.")
 ],
 "trademark": [
  ("Can you help register a trademark?", "Yes. We assist with trademark search, application filing and registration-related documentation."),
  ("Does the trademark fee include government charges?", "Our ₹10,000 starting amount is for registration assistance. Applicable government/statutory fees are separate and depend on the application."),
  ("Can you check a brand name before filing?", "Yes. We can assist with a preliminary trademark search and explain the next steps. A search does not guarantee registration."),
  ("How long does trademark registration take?", "The timeline can vary depending on examination, objections, oppositions and other factors. We cannot guarantee an approval date.")
 ],
 "dsc": [
  ("What is a Digital Signature Certificate?", "A DSC is a digital certificate used for electronic signing and authentication on supported services and portals."),
  ("Can you help with DSC renewal?", "Yes. We assist with eligible DSC applications and renewals."),
  ("What documents are needed for DSC?", "Requirements vary by certificate type and applicant. We confirm the current requirements before processing."),
  ("How much does DSC assistance cost?", "Please contact us for the current professional fee because it depends on the DSC type and validity required.")
 ],
 "business-registration": [
  ("Can you help me choose a business structure?", "Yes. We can explain the common registration options and help you identify what information and documentation you should discuss before proceeding."),
  ("Can you help with a new business setup?", "Yes. We can help you identify registrations and compliance items that may apply to your proposed business."),
  ("What documents are usually needed?", "Requirements depend on the structure and business activity. Common documents include identity/address proofs, business address details and proposed business information."),
  ("Do you guarantee registration approval?", "No. Applications are subject to the requirements and decisions of the relevant authorities. We provide documentation and application support.")
 ],
}
def xnote(s):
    return f'<p class="note">{EXTRA[s]}</p>' if s in EXTRA else ""
def faqhtml(s):
    if s not in FAQS: return ""
    return '<h2 style="margin-top:40px">Common questions</h2><div class="faq-list">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQS[s]) + "</div>"
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
        shell("../", t, TD2[t_[0]], p, m + cta + sc)
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
    shell("", "Privacy | KVB ENTERPRISES", "How KVB ENTERPRISES uses information you share and website analytics.", "privacy.html", P)
    shell("", "Terms | KVB ENTERPRISES", "Terms for using KVB ENTERPRISES professional assistance services.", "terms.html", Tm)

main()
