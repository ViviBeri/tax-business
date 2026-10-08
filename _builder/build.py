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
  ["Individual ITR filing", "Business and professional ITR filing", "Tax compliance support", "CA coordination where required"],
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
    return (f'<a class="floating-wa" href="{wa("Hello Vivian, I would like to know about your services.")}" target="_blank" rel="noopener" aria-label="WhatsApp KVB ENTERPRISES" data-loc="floating">{ICON}</a>'
            f'<footer><div class="wrap footer"><div class="footer-brand"><img src="{r}assets/logo.png" alt="KVB ENTERPRISES logo" width="44" height="44" loading="lazy">'
            f'<div><b>KVB ENTERPRISES</b><p>Tax &amp; Business Compliance Services</p></div></div>'
            f'<div>GST • ITR • FSSAI • PAN • MSME • Trademark • DSC<br>Puducherry &amp; nearby areas</div>'
            f'<div><a href="{r}privacy.html">Privacy</a> • <a href="{r}terms.html">Terms</a><br>© <span class="yr">{TD.year}</span> KVB ENTERPRISES</div></div></footer>'
            f'<script src="{r}script.js" defer></script></body></html>')

def btn(href, en, ta, cls="primary", loc="", ico=False, ext=True):
    t = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="btn {cls}" href="{href}"{t} data-loc="{loc}">{ICON if ico else ""}<span data-en="{E(en)}" data-ta="{E(ta)}">{en}</span></a>'

def price(s):
    p = str(PR.get(s, "")).strip()
    return T("em", f"Starting from ₹{p}", f"₹{p} முதல்", "price") if p else T("em", "Get a quote", "விலை விவரம் பெறுக", "price")

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
    b += (f'<main class="service-page"><div class="wrap"><a class="back" href="../index.html#services">← All services</a>{T("h1", en, ta)}{T("p", d, dta, "intro")}'
          '<div class="service-grid"><div><section class="panel"><h2>What we can help with</h2><ul>' + "".join(f"<li>{i}</li>" for i in items) + "</ul></section>"
          '<section class="panel" style="margin-top:20px"><h2>Documents commonly needed</h2><ul>' + "".join(f"<li>{i}</li>" for i in docs)
          + '</ul><p class="note">The exact list depends on your case. We confirm it with you on WhatsApp before you start.</p></section>'
          '<section class="panel" style="margin-top:20px"><h2>Pricing</h2><p>' + price(s) + f'</p>{T("p", NOTE_EN, NOTE_TA, "note")}</section></div>'
          f'<aside class="panel cta-panel"><h2>Need assistance?</h2><p>Tell Vivian what you need and get the document and process guidance for your case.</p>'
          + btn(msg, "WhatsApp 90036 33696", "WhatsApp 90036 33696", "primary wide", s, True) + '<div style="height:10px"></div>' + btn(f"tel:+{PH}", "Call now", "இப்போது அழைக்கவும்", "secondary wide", s, False, False)
          + '<p>Tamil &amp; English. Local assistance in Puducherry and nearby areas.</p></aside></div>'
          '<h2 style="margin-top:40px">How it works</h2>' + steps() + f'<div class="related">{rel}</div></div></main>')
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
.related{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}
.related a{padding:9px 14px;border-radius:999px;background:#fff;border:1px solid var(--line);color:var(--navy);font-weight:750;text-decoration:none;font-size:14px}
.cta-panel .note,.cta-panel p{color:#d7e0ea}
@media(max-width:900px){
.menu{display:block}.nav{gap:8px}
nav.open{display:flex;position:absolute;left:0;right:0;top:100%;flex-direction:column;align-items:flex-start;gap:0;background:#fff;border-bottom:1px solid var(--line);padding:8px 4% 14px;box-shadow:0 14px 30px rgba(41,19,94,.12)}
nav.open a{padding:12px 0;width:100%;font-size:16px}
.clients-grid,.steps{grid-template-columns:1fr}}
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
- `locations/`, `tools/`, `privacy.html`, `terms.html`, `assets/` maintained by hand
- `sitemap.xml`, `robots.txt`

## Updating prices
Edit `_builder/prices.json` (for example `{"gst": "999"}`), then run `python3 _builder/build.py`. An empty value shows "Get a quote".

## Analytics
Google Analytics 4 (G-KFP95JFETM). Events: `whatsapp_click`, `call_click`, `generate_lead` (form), `select_service`, `language_switch`. No names or phone numbers are sent to Google.

KVB ENTERPRISES is an independent professional assistance service and is not a government department.
"""

def main():
    for x in SV:
        svc(x)
    index()
    old = os.path.join(O, "style.css")
    base = open(old, encoding="utf-8").read().split("/* V3 */")[0].rstrip() if os.path.exists(old) else ""
    w("style.css", base + "\n" + CSS)
    w("script.js", JS)
    w("README.md", README)
    w("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {S}/sitemap.xml\n")
    urls = [""] + [f"services/{x[0]}.html" for x in SV] + [f"locations/gst-registration-{l}.html" for l in LOCS] + [f"tools/{t[0]}.html" for t in TOOLS] + ["privacy.html", "terms.html"]
    w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f"<url><loc>{S}/{u}</loc><lastmod>{TD.isoformat()}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    if not os.path.exists(os.path.join(B, "prices.json")):
        json.dump({x[0]: "" for x in SV}, open(os.path.join(B, "prices.json"), "w"), indent=1)

main()
