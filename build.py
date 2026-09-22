#!/usr/bin/env python3
"""Build alexandersobieska.com into docs/.

Run:  python3 build.py
Then preview with:  python3 -m http.server 8000 --directory docs

Everything the site says lives in this file (pages, talks, projects) or in
src/publications.bib (papers). No third-party packages needed.
"""
import datetime
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
SRC = ROOT / "src"
SITE = "https://alexandersobieska.com"
TODAY = datetime.date.today()
LEGAL_READY = True  # Impressum/privacy text checked 2026-09-22 (01_content/legal_check.md)

NAME = "Alexander Sobieska"
EMAIL = "alexander.sobieska@tum.de"
BOOKING = "https://zcal.co/alexandersobieska/work"
SCHOLAR = "https://scholar.google.com/citations?user=eD-d6CwAAAAJ"
ORCID = "https://orcid.org/0009-0003-1473-8161"
LINKEDIN = "https://www.linkedin.com/in/alexander-sobieska-67820b19a/"
TUM_PAGE = "https://get.med.tum.de/people/alexander-sobieska/"
PHOTO = "/img/alexander-sobieska.jpg"
HARMONY_URL = "https://portal.fis.tum.de/en/projects/harmony-health-related-mis-information-on-social-media-and-its-im/"
CHAIR_URL = "https://www.pm.mh.tum.de/en/ethics/institute/team/marcello-ienca/"
SML_URL = "https://sml.stanford.edu/"
INSTITUTE_URL = "https://www.pm.mh.tum.de/ethics/startseite/"
GIF_URL = "https://www.global.tum.de/en/global/gif/"
CV_PDF = "/Alexander_Sobieska_CV.pdf"
CV_SOURCE = ROOT.parent / "04_cv" / "CV_Sobieska_Alexander_2026-09_public.pdf"

LEAD = ("I study what social media feeds show people about health and the brain, "
        "and what people actually watch.")
DESCRIPTION = ("Alexander Sobieska is a doctoral researcher at the Technical University of Munich "
               "studying TikTok recommendations, health misinformation, neuroethics and online "
               "radicalization, using data that users donate from their own accounts.")

NAV = [
    ("research", "/research/", "Research and projects"),
    ("publications", "/publications/", "Publications and talks"),
    ("cv", CV_PDF, "CV (PDF)"),
]

# ---------------------------------------------------------------- research themes
THEMES = [
    {
        "key": "feed",
        "slug": "tiktok-recommendations-health-misinformation",
        "name": "What TikTok shows, and what people watch",
        "short": "What TikTok shows",
        "seo_title": "TikTok recommendations and health misinformation: what the feed shows and what users watch",
        "summary": "Donated TikTok histories linked to surveys: health content and misinformation, served and watched.",
        "body": [
            "Studies of recommendation algorithms usually look either at what a platform serves, by running test accounts, or at what users say they saw, by asking them. Neither tells you what a real person actually watched.",
            "In HARMONY, young adults donate their TikTok history, which records every video the feed served and how long it stayed on screen. Linked to surveys, this lets us ask how much health content and health misinformation reaches people, how much of it they watch rather than scroll past, and whether it relates to their wellbeing.",
        ],
        "steps": [
            "Participants answer surveys about their health and wellbeing.",
            "They download their own TikTok data and donate it to the study.",
            "The donated history shows every video the feed served and how long it stayed on screen.",
            "Linking the two lets us compare what the platform sent a person with what that person watched.",
        ],
        "projects": ["harmony"],
        "bib_theme": "feed",
    },
    {
        "key": "brain",
        "slug": "neuroethics-online-public-discussion",
        "name": "\u201cThe brain\u201d in public",
        "short": "\u201cThe brain\u201d in public",
        "seo_title": "Neurotechnology and neuroethics in online public discussion",
        "summary": "How claims about \u201cthe brain\u201d, ADHD and neurotechnology are framed online, and what neuroethics can learn from it.",
        "body": [
            "People now meet claims about \u201cthe brain\u201d, ADHD and neurotechnology mostly in online videos, not in journals. This part of my work asks how these topics are framed online, which ethical questions the public raises, and what neuroethics can learn from that.",
            "Ethics is the study of how we ought to act and what we owe each other. Neuroethics applies this to brain science and neurotechnology: for example, what changes when a device can record or alter brain activity, or when people come to explain themselves through their brain.",
        ],
        "projects": [],
        "bib_theme": "neuroethics",
    },
    {
        "key": "radical",
        "slug": "online-radicalization-misinformation",
        "name": "Radicalization and misinformation",
        "short": "Radicalization and misinformation",
        "seo_title": "Online radicalization and misinformation: language, movements and platforms",
        "summary": "How movements build their narratives and how language changes as people move toward extreme positions.",
        "body": [
            "How do movements build their narratives, and how does language change as people move toward extreme positions?",
            "Published work analyses the language of the Querdenken movement during COVID-19. Querdenken (German for \u201clateral thinking\u201d) is a protest movement that formed in Germany in 2020 against the government's pandemic measures.",
            "For my master's thesis I studied the language of r/Incels, an online forum of men who call themselves \u201cinvoluntary celibates\u201d, and how users' language changes as they radicalize.",
            "TikTalks studies radical and polarizing content on TikTok and how young adults in Bavaria meet it in their feeds.",
        ],
        "projects": ["tiktalks1", "tiktalks2"],
        "bib_theme": "radicalization",
    },
    {
        "key": "llm",
        "slug": "large-language-models-clinical-communication-information",
        "name": "Language models and how people get information",
        "short": "Language models and information",
        "seo_title": "Large language models in clinical communication and information retrieval",
        "summary": "How large language models change clinical communication and the way people look up information.",
        "body": [
            "Large language models are changing how doctors and patients communicate and how people look up information. Earlier work looked at informed consent: it argues that consent is more than an exchange of words, which limits what language models can do in consent conversations.",
            "Another part of my work asks whether large language models give a less complete account of contested historical events, such as mass atrocities, when asked in some languages than in others.",
        ],
        "projects": ["llmhistory"],
        "bib_theme": "llm-medethics",
    },
]

# ---------------------------------------------------------------- projects
PROJECTS = {
    "harmony": {
        "name": "HARMONY: Health-Related (Mis-)Information on Social Media and Its Impact on Young Adults",
        "when": "",
        "url": HARMONY_URL,
        "text": "TikTok uses highly individualised content recommendation systems powered by artificial intelligence. While these systems boost engagement, concerns arise about their impact on young adults, particularly around mental health and exposure to health (mis-)information. HARMONY investigates how, when, and why young adults encounter health-related (mis-)information on TikTok: it collects data on users' interactions with and perceptions of TikTok's recommendation systems, analyses health-related videos, runs experiments with digital twins, and uses focus groups to learn how users judge the reliability of health content. The findings are meant to inform regulatory discussions about vulnerable groups such as young adults. An IGSSE International Project Team of TU Munich and Eindhoven University of Technology (principal investigators Marcello Ienca and Lily Frank), with the Stanford Social Media Lab and UNICEF.",
    },
    "tiktalks1": {
        "name": "TikTalks I",
        "when": "July 2024 – February 2026",
        "url": "",
        "text": "How TikTok's recommendations build personal feeds for young adults (18–24) in Bavaria, with a focus on polarizing, radical and extremist content. Participants answered a survey, used a newly created TikTok study account for seven days, and could donate their own TikTok data; focus groups and workshops added their own accounts of what they saw. Responsible Technology Hub and TUM, funded by the Bavarian State Ministry for Family, Labour and Social Affairs under its radicalization-prevention programme. Role: project manager.",
    },
    "tiktalks2": {
        "name": "TikTalks II",
        "when": "2026–2027",
        "url": "",
        "text": "Takes the data and results of TikTalks I to researchers, practitioners and the public: an expert workshop (held June 2026, jointly with HARMONY) and an international conference in 2027. Same partners and funder. Role: project manager.",
    },
    "llmhistory": {
        "name": "Global Comparative Study on Censorship in LLM-Based Chatbots",
        "when": "September 2025 – September 2026",
        "url": GIF_URL,
        "text": "As large language models increasingly shape access to information, their answers to politically, ethically and socially sensitive questions raise concerns about freedom of expression, digital rights and epistemic justice. The project compares how chatbots developed under different political and regulatory conditions handle such questions, looking both for outright refusals and for subtler strategies such as evasion, distortion or omission. The current study focuses on contested historical events. TUM and Imperial College London (principal investigator Marcello Ienca, partner Giorgio Gilestro), funded by the TUM Global Incentive Fund. Role: doctoral researcher and project coordinator.",
    },
}

# ---------------------------------------------------------------- talks
# date: ISO date for sorting; shown: what the page prints. theme: research theme key or None.
TALKS = [
    {"date": "2026-12-07", "shown": "7–8 Dec 2026", "kind": "Poster", "event": "New Directions in Social Media Research and Policy", "place": "University of Cambridge",
     "title": "TRACE: a four-layer design for reconstructing algorithmic content environments", "theme": "feed"},
    {"date": "2026-10-01", "shown": "1 Oct 2026", "kind": "Lightning talk", "event": "Trust & Safety Research Conference", "place": "Stanford University",
     "title": "Inside the For You Page: algorithmic content exposure, health misinformation and well-being among young adults on TikTok", "theme": "feed"},
    {"date": "2026-09-09", "shown": "9 Sep 2026", "kind": "Invited presentation", "event": "networking meeting of the Bavarian State Ministry for Family, Labour and Social Affairs (radicalization prevention)", "place": "Munich",
     "title": "The TikTalks project", "theme": "radical"},
    {"date": "2026-06-05", "shown": "5 Jun 2026", "kind": "Invited workshop", "event": "Health Ethics and Policy Lab (Effy Vayena), ETH Zurich", "place": "Zurich",
     "title": "Digital methods", "theme": None},
    {"date": "2025-05-27", "shown": "27 May 2025", "kind": "Talk", "event": "re:publica 25", "place": "Berlin",
     "title": "Gen Z \u201cradicalized through TikTok\u201d: myth or reality? (with Yasmin Al-Douri)", "theme": "radical"},
    {"date": "2025-04-25", "shown": "25 Apr 2025", "kind": "Joint session with Georg Starke, Ralf Jox and Sabine Salloch", "event": "Neuroethics 2025, annual meeting of INS and SINe", "place": "Munich",
     "title": "Digital bioethics: computational methods for addressing neuroethical questions", "theme": "brain"},
    {"date": "2025-04-23", "shown": "23 Apr 2025", "kind": "Poster (Best Presenter Award)", "event": "Neuroethics 2025, annual meeting of INS and SINe", "place": "Munich",
     "title": "Exploring public discourse on neurotechnology: a computational analysis of sentiment, terminology, and ethical concerns on social media", "theme": "brain"},
    {"date": "2024-10-17", "shown": "Oct 2024", "kind": "Talk", "event": "Hybrid Minds", "place": "Geneva",
     "title": "Neuroethics on YouTube: investigating ethical considerations of neurotechnology in public discourse", "theme": "brain"},
    {"date": "2024-09-20", "shown": "20 Sep 2024", "kind": "Talk", "event": "DFG Network \u201cDigital Bioethics\u201d", "place": "Hannover",
     "title": "Neuroethics on YouTube: investigating ethical considerations of neurotechnology in public discourse", "theme": "brain"},
    {"date": "2024-07-18", "shown": "18 Jul 2024", "kind": "Paper in the panel \u201cExploring the transformative powers of neurosciences\u201d", "event": "EASST-4S", "place": "Amsterdam",
     "title": "Neurorights on YouTube: investigating ethical considerations of neurotechnology in public discourse", "theme": "brain"},
    {"date": "2024-06-06", "shown": "Jun 2024", "kind": "Talk (with Marcello Ienca)", "event": "SINe 2024 \u201cMind Matters: Navigating Neuroethics in the 21st Century\u201d, Italian Society for Neuroethics", "place": "Rome",
     "title": "Neurorights on YouTube: investigating ethical considerations of neurotechnology in public discourse", "theme": "brain"},
    {"date": "2024-04-17", "shown": "17 Apr 2024", "kind": "Poster (Best Presenter Award)", "event": "Neuroethics 2024, annual meeting of the International Neuroethics Society", "place": "Baltimore",
     "title": "Neurorights on YouTube: investigating ethical considerations of neurotechnology in public discourse", "theme": "brain"},
    {"date": "2024-03-21", "shown": "21 Mar 2024", "kind": "Talk", "event": "conference \u201cBridging the gap between neurorights and cyberrights\u201d, Scuola Superiore Sant'Anna", "place": "Pisa",
     "title": "Neurorights on YouTube: investigating ethical considerations of neurotechnology in public discourse", "theme": "brain"},
    {"date": "2023-07-20", "shown": "20 Jul 2023", "kind": "Talk", "event": "IC2S2", "place": "Copenhagen",
     "title": "Decoding the discourse: analyzing the linguistic features and strategies behind the Querdenken movement's COVID-19 narrative", "theme": "radical"},
]

ORGANISED = [
    ("9–10 Jun 2026", "Expert workshop \u201cWho shapes whom? Recommendation systems, sense of self, and algorithmic influence on TikTok\u201d, HARMONY and TikTalks, Munich (co-organised with Valérie Nowak)"),
    ("Apr 2025", "Neuroethics 2025, annual meeting of INS and SINe, Munich (local organising team)"),
]

AWARDS = [
    ("2026–2027", "TikTalks II. Bavarian State Ministry for Family, Labour and Social Affairs, about €100,000 (with Yasmin Al-Douri, Responsible Technology Hub)"),
    ("2026", "2nd prize, \u201cSpeaking Across Differences\u201d award of the Verein für die Förderung des McCloy-Stipendienprogramms, to TikTalks (Responsible Technology Hub), €2,000"),
    ("2025", "Fulbright Visiting Scholar Award, Stanford Social Media Lab"),
    ("2025", "Best Presenter Award, International Neuroethics Society annual meeting (Neuroethics 2025, Munich)"),
    ("2024–2026", "TikTalks: programme for the analysis of actors behind radical content on TikTok. Bavarian State Ministry for Family, Labour and Social Affairs, about €130,000 (with Yasmin Al-Douri, Responsible Technology Hub)"),
    ("2024", "Scholar of the Graduate Center for Doctoral Researchers, Bavarian Research Institute for Digital Transformation (bidt)"),
    ("2024", "Best Presenter Award, International Neuroethics Society annual meeting (Neuroethics 2024, Baltimore)"),
    ("2021–2023", "Scholar, TUM: Junge Akademie"),
    ("2016–2020", "Scholar, Studienstiftung des Deutschen Volkes"),
]

SHORT_BIO = ("Alexander Sobieska is a doctoral researcher at the Chair of Ethics of AI and Neuroscience at the Technical University of Munich, supervised by Marcello Ienca. "
             "He works on the HARMONY project, which studies health information on TikTok among young adults, using data that users donate from their own accounts. "
             "His work combines computational text analysis, surveys and ethics. From October 2025 to January 2026 he was a Fulbright Visiting Scholar at the Stanford Social Media Lab. "
             "He trained in psychology and political science.")

LONG_BIO = [
    "Alexander Sobieska is a doctoral researcher at the Institute of History and Ethics in Medicine at the Technical University of Munich (TUM), in Marcello Ienca's Chair of Ethics of AI and Neuroscience. His thesis develops computational methods for bioethics: ways to study public discussion, misinformation and ethical questions in media that algorithms curate.",
    "Most of his current work is part of HARMONY, a project on health-related information and misinformation on social media and its effect on young adults. HARMONY is run by TUM and Eindhoven University of Technology, with the Stanford Social Media Lab and UNICEF. Participants donate their TikTok data, which shows every video their feed served them and how long each one stayed on screen, and they answer surveys about their health and wellbeing. This lets him compare what the platform sends a person with what that person actually watches.",
    "He is also project manager of TikTalks, run by the Responsible Technology Hub with TUM and funded by the Bavarian State Ministry for Family, Labour and Social Affairs. TikTalks I (2024–2026) collected survey answers from young adults in Bavaria and let them use new TikTok study accounts for a week; TikTalks II (2026–2027) brings the results to the public and to researchers, through an expert workshop and an international conference. With Marcello Ienca and Giorgio Gilestro (Imperial College London) he also works on a study of how AI chatbots answer questions about contested historical events in different languages.",
    "From October 2025 to January 2026 he was a Fulbright Visiting Scholar at the Stanford Social Media Lab, hosted by Jeff Hancock and Sunny Xun Liu. He holds an M.Sc. in Politics and Technology from TUM and a B.Sc. in Psychology from LMU Munich, and was a scholar of the Studienstiftung des Deutschen Volkes and TUM: Junge Akademie. He teaches medical ethics at TUM.",
]

# ---------------------------------------------------------------- helpers
def e(s):
    return html.escape(s, quote=True)


def theme_by(key):
    return next(t for t in THEMES if t["key"] == key)


def parse_bib(path):
    """Small BibTeX reader for our own file: @type{key, field = {value}, ...}."""
    text = path.read_text(encoding="utf-8")
    entries = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,]+),(.*?)\n\}", text, re.S):
        kind, key, body = m.group(1).lower(), m.group(2).strip(), m.group(3)
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", body):
            fields[fm.group(1).lower()] = re.sub(r"[{}]", "", fm.group(2)).replace("--", "–").strip()
        fields["kind"], fields["key"] = kind, key
        entries.append(fields)
    entries.sort(key=lambda f: (-int(f.get("year", 0)), f["key"]))
    return entries


def apa_authors(field):
    names = [n.strip() for n in field.split(" and ")]
    out = []
    for n in names:
        last, _, first = n.partition(",")
        initials = " ".join(p[0] + "." if "-" not in p else "-".join(q[0] + "." for q in p.split("-")) for p in first.split())
        out.append(f"{last.strip()}, {initials}".strip(", "))
    if len(out) == 1:
        return out[0]
    return ", ".join(out[:-1]) + ", & " + out[-1]


def pub_parts(p):
    authors = apa_authors(p["author"])
    year = p.get("year", "")
    title = p["title"]
    doi = p.get("doi", "")
    url = f"https://doi.org/{doi}" if doi else ""
    if p["kind"] == "article":
        venue = p["journal"]
        details = ""
        if p.get("volume"):
            details += f", {p['volume']}"
            if p.get("number"):
                details += f"({p['number']})"
        if p.get("pages"):
            details += f", {p['pages']}"
        type_label = "Journal article"
    else:
        venue = p.get("booktitle", "")
        details = f", {p['pages']}" if p.get("pages") else ""
        type_label = "Book chapter"
    plain = f"{authors} ({year}). {title}. {venue}{details}." + (f" {url}" if url else "")
    return dict(authors=authors, year=year, title=title, venue=venue, details=details,
                url=url, doi=doi, type_label=type_label, plain=plain)


def cite_html(p, link=True):
    q = pub_parts(p)
    t = f'<a href="{e(q["url"])}">{e(q["title"])}</a>' if (link and q["url"]) else e(q["title"])
    return f'{e(q["authors"])} ({e(q["year"])}). {t}. <em>{e(q["venue"])}</em>{e(q["details"])}.'


# ---------------------------------------------------------------- layout
NAV_DE = {"research": "Forschung und Projekte (englisch)", "publications": "Publikationen und Vorträge (englisch)", "cv": "Lebenslauf (PDF, englisch)"}


def nav_links(active, active_theme=None, cls="", lang="en"):
    out = []
    for key, href, label in NAV:
        if lang == "de":
            label = NAV_DE.get(key, label)
        cur = ' aria-current="page"' if key == active else ""
        out.append(f'<a href="{href}"{cur}>{e(label)}</a>')
        if key == "research" and active == "research" and cls != "menu":
            subs = []
            for t in THEMES:
                c = ' aria-current="page"' if t["key"] == active_theme else ""
                subs.append(f'<a href="/research/{t["slug"]}/"{c}>{e(t["short"])}</a>')
            out.append('<div class="subnav">' + "".join(subs) + "</div>")
    return "\n".join(out)


def contact_links(lang="en"):
    write_me, call = ("Schreiben Sie mir", "Vereinbaren Sie ein Gespräch") if lang == "de" else ("Write me", "Schedule a call with me")
    return (f'<a href="mailto:{EMAIL}">{write_me}</a>\n'
            f'<a href="{BOOKING}">{call}</a>\n'
            f'<a href="{SCHOLAR}">Google Scholar</a>\n'
            f'<a href="{ORCID}">ORCID</a>\n'
            f'<a href="{LINKEDIN}">LinkedIn</a>')


# Home page and German page are language versions of each other (hreflang).
LANG_PAIR = {"/": "/de/", "/de/": "/"}


def layout(path, title, description, active, body, active_theme=None, jsonld=None, extra_head="", home=False, lang="en"):
    canonical = SITE + path
    full_title = title if home else f"{title} · {NAME}"
    de = lang == "de"
    legal = '<a href="/legal/">Impressum und Datenschutz</a>' if de else '<a href="/legal/">Impressum and privacy</a>'
    other_lang = '<a href="/" hreflang="en" lang="en">English</a>' if de else '<a href="/de/" hreflang="de" lang="de">Deutsch</a>'
    foot = " · ".join(x for x in [legal if LEGAL_READY else "", other_lang] if x)
    egg = "" if de else """<script>
// Easter egg: type "brain" anywhere on an English page.
(function(){var k="";document.addEventListener("keydown",function(e){
if(e.metaKey||e.ctrlKey||e.altKey||/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName))return;
k=(k+e.key.toLowerCase()).slice(-5);if(k==="brain")location.href="/brain-run/";});})();
</script>"""
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    photo_side = f'<img class="photo" src="{PHOTO}" alt="Porträt von {NAME}" width="300" height="380">' if (home and de) else (f'<img class="photo" src="{PHOTO}" alt="Portrait of {NAME}" width="300" height="380">' if home else "")
    hreflang = ""
    if path in LANG_PAIR:
        en_url = SITE + (path if not de else LANG_PAIR[path])
        de_url = SITE + (LANG_PAIR[path] if not de else path)
        hreflang = (f'<link rel="alternate" hreflang="en" href="{en_url}">\n'
                    f'<link rel="alternate" hreflang="de" href="{de_url}">\n'
                    f'<link rel="alternate" hreflang="x-default" href="{en_url}">\n')
    locale, alt_locale = ("de_DE", "en_US") if de else ("en_US", "de_DE")
    role = (f'Doktorand<br><a href="{INSTITUTE_URL}">Professur für Ethik der KI und Neurowissenschaften</a><br>Technische Universität München' if de
            else f'Doctoral researcher<br><a href="{INSTITUTE_URL}">Chair of Ethics of AI and Neuroscience</a><br>Technical University of Munich')
    pron = "er/ihm" if de else "he/him"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
{hreflang}<meta property="og:type" content="{'profile' if home else 'website'}">
<meta property="og:locale" content="{locale}">
<meta property="og:locale:alternate" content="{alt_locale}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}{PHOTO}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/schibsted-grotesk-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/style.css">
{ld}{extra_head}
</head>
<body>
<a class="skip" href="#content">{'Zum Inhalt springen' if de else 'Skip to content'}</a>
<div class="page">
<aside class="side">
{photo_side}
<a class="who" href="{'/de/' if de else '/'}"><span class="name">{NAME}</span><span class="pron">{pron}</span></a>
<div class="role">{role}</div>
<nav class="nav" aria-label="{'Hauptnavigation' if de else 'Main'}">
{nav_links(active, active_theme, lang=lang)}
</nav>
<div class="contact">
{contact_links(lang)}
</div>
</aside>
<header class="topbar">
<div class="row">
<a class="home" href="{'/de/' if de else '/'}">{NAME}</a>
<details>
<summary><span class="open">{'Menü' if de else 'Menu'}</span><span class="close">{'Schließen' if de else 'Close'}</span></summary>
<nav class="menu" aria-label="{'Hauptmenü' if de else 'Main menu'}">
{nav_links(active, active_theme, "menu", lang=lang)}
</nav>
</details>
</div>
</header>
<main id="content">
{body}
<p class="foot">{foot}</p>
</main>
</div>
{egg}
</body>
</html>
"""


def write(path, content):
    target = OUT / path.strip("/") / "index.html" if not path.endswith(".html") else OUT / path.strip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------- pages
def talk_line(t, with_theme_link=False):
    return (f'<p><strong>{e(t["shown"])}</strong> · {e(t["kind"])} at {e(t["event"])}, {e(t["place"])}: '
            f'<em>{e(t["title"])}</em></p>')


def upcoming():
    return [t for t in sorted(TALKS, key=lambda t: t["date"]) if t["date"] >= TODAY.isoformat()]


def page_home(pubs):
    themes = "\n".join(
        f'<div class="theme"><a href="/research/{t["slug"]}/">{e(t["name"])}</a><p>{e(t["summary"])}</p></div>'
        for t in THEMES)
    publist = "\n".join(f"<p>{cite_html(p)}</p>" for p in pubs[:4])
    up = upcoming()
    up_html = ""
    if up:
        up_html = '<section><h2 class="label">Upcoming</h2>\n' + "\n".join(talk_line(t) for t in up) + "</section>"
    body = f"""
<div class="mobile-only mobile-intro">
<img src="{PHOTO}" alt="Portrait of {NAME}" width="132" height="168">
<div class="role"><span class="muted">he/him</span><br>Doctoral researcher, <a href="{INSTITUTE_URL}">Chair of Ethics of AI and Neuroscience</a>, Technical University of Munich</div>
</div>
<section>
<h1 class="lead">{e(LEAD)}</h1>
<p class="intro">I work on <a href="{HARMONY_URL}">HARMONY</a>, which studies health information on TikTok among young adults, using data they donate from their own accounts. My work combines computational text analysis, surveys and ethics. I am supervised by <a href="{CHAIR_URL}">Marcello Ienca</a>. From October 2025 to January 2026 I was a Fulbright Visiting Scholar at the <a href="{SML_URL}">Stanford Social Media Lab</a>.</p>
</section>
<div class="mobile-only mobile-contact">
{contact_links()}
</div>
<section>
<h2 class="label"><a href="/research/">Research</a></h2>
<div class="themes">
{themes}
</div>
</section>
<section>
<h2 class="label"><a href="/publications/">Publications</a></h2>
{publist}
</section>
{up_html}
"""
    jsonld = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": NAME,
        "url": SITE + "/",
        "image": SITE + PHOTO,
        "email": "mailto:" + EMAIL,
        "jobTitle": "Doctoral researcher",
        "description": DESCRIPTION,
        "affiliation": {"@type": "CollegeOrUniversity", "name": "Technical University of Munich", "url": "https://www.tum.de"},
        "alumniOf": [
            {"@type": "CollegeOrUniversity", "name": "Technical University of Munich"},
            {"@type": "CollegeOrUniversity", "name": "Ludwig-Maximilians-Universität München"},
        ],
        "knowsAbout": ["TikTok", "recommender systems", "health misinformation", "neuroethics",
                       "online radicalization", "computational social science", "AI ethics",
                       "large language models", "data donation",
                       "Gesundheitsinformationen", "Fehlinformationen", "Neuroethik", "Radikalisierung", "Datenspende"],
        "knowsLanguage": ["en", "de"],
        "worksFor": {"@type": "CollegeOrUniversity", "name": "Technical University of Munich", "alternateName": "Technische Universität München",
                     "department": {"@type": "Organization", "name": "Institute of History and Ethics in Medicine", "alternateName": "Institut für Geschichte und Ethik der Medizin", "url": INSTITUTE_URL}},
        "workLocation": {"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": "Munich", "addressCountry": "DE"}},
        "sameAs": [SCHOLAR, ORCID, LINKEDIN, TUM_PAGE],
    }
    write("/", layout("/", f"{NAME}: TikTok, health misinformation and neuroethics research",
                      DESCRIPTION, "home", body, jsonld=jsonld, home=True))


DE_PARTS = [
    {
        "en": "tiktok-recommendations-health-misinformation",
        "slug": "tiktok-empfehlungssystem-gesundheitsinformationen",
        "name": "Was TikTok zeigt und was Menschen ansehen",
        "seo": "TikTok-Empfehlungssystem und Gesundheitsinformationen",
        "short": "Junge Erwachsene spenden ihren TikTok-Verlauf. Er verzeichnet, welche Videos das Empfehlungssystem ausgespielt hat und wie lange sie auf dem Bildschirm waren. Zusammen mit Befragungen zeigt das, wie viele Gesundheitsinformationen und Fehlinformationen bei den Teilnehmenden ankommen und wie viel davon sie sich ansehen.",
        "body": [
            "Wer Empfehlungssysteme untersucht, sieht meist nur eine Seite: Entweder man misst mit Testkonten, was eine Plattform ausspielt, oder man fragt Nutzerinnen und Nutzer, woran sie sich erinnern. Keiner der beiden Wege zeigt, was eine bestimmte Person tatsächlich angesehen hat.",
            "Im Projekt HARMONY spenden junge Erwachsene ihren TikTok-Verlauf. Er verzeichnet, welche Videos das Empfehlungssystem ausgespielt hat und wie lange sie auf dem Bildschirm blieben. Zusammen mit den Befragungen lässt sich damit untersuchen, wie viele Gesundheitsinformationen und wie viele Fehlinformationen bei den Teilnehmenden ankommen, wie viel davon sie sich ansehen statt weiterzuwischen und ob das mit ihrem Wohlbefinden zusammenhängt.",
        ],
        "steps": [
            "Die Teilnehmenden beantworten Fragen zu ihrer Gesundheit und ihrem Wohlbefinden.",
            "Sie laden ihre eigenen TikTok-Daten herunter und geben sie als Datenspende an die Studie weiter.",
            "Der gespendete Verlauf zeigt, welche Videos das Empfehlungssystem ausgespielt hat und wie lange sie auf dem Bildschirm waren.",
            "Beides zusammen zeigt, was die Plattform einer Person ausgespielt hat und was diese davon angesehen hat.",
        ],
        "bib_theme": "feed",
    },
    {
        "en": "neuroethics-online-public-discussion",
        "slug": "neuroethik-oeffentliche-debatte",
        "name": "\u201eDas Gehirn\u201c in der Öffentlichkeit",
        "seo": "Neurotechnologie und Neuroethik in der öffentlichen Debatte",
        "short": "Wie im Internet über \u201edas Gehirn\u201c, ADHS und Neurotechnologie gesprochen wird, welche ethischen Fragen die Öffentlichkeit dabei stellt und was die Neuroethik daraus lernen kann.",
        "body": [
            "Den meisten Menschen begegnen Aussagen über \u201edas Gehirn\u201c, ADHS und Neurotechnologie heute in kurzen Videos, nicht in Fachzeitschriften. In diesem Teil meiner Arbeit frage ich, wie im Internet über diese Themen gesprochen wird, welche ethischen Fragen die Öffentlichkeit dabei stellt und was die Neuroethik daraus lernen kann.",
            "Die Ethik untersucht, wie wir handeln sollen und was wir einander schulden. Die Neuroethik wendet diese Fragen auf Hirnforschung und Neurotechnologie an. Sie fragt zum Beispiel, was sich ändert, wenn ein Gerät Hirnaktivität aufzeichnen oder beeinflussen kann, oder wenn Menschen anfangen, sich selbst durch ihr Gehirn zu erklären.",
        ],
        "steps": [],
        "bib_theme": "neuroethics",
    },
    {
        "en": "online-radicalization-misinformation",
        "slug": "radikalisierung-fehlinformationen-online",
        "name": "Radikalisierung und Fehlinformationen",
        "seo": "Radikalisierung und Fehlinformationen im Internet",
        "short": "Wie Bewegungen ihre Erzählungen aufbauen und wie sich Sprache verändert, wenn sich Menschen extremen Positionen annähern.",
        "body": [
            "Wie bauen Bewegungen und Gemeinschaften ihre Erzählungen auf und wie verändert sich Sprache, wenn sich Menschen extremen Positionen annähern?",
            "In einer bereits erschienenen Arbeit habe ich die Sprache der Querdenken-Bewegung während der Corona-Pandemie untersucht. Querdenken ist eine Protestbewegung, die sich 2020 in Deutschland gegen die Pandemiemaßnahmen der Regierung formierte.",
            "In meiner Masterarbeit habe ich die Sprache des Forums r/Incels untersucht, in dem sich Männer als \u201eunfreiwillig zölibatär\u201c beschreiben. Die Frage war, wie sich die Sprache der Nutzer verändert, während sie sich radikalisieren.",
            "Im Projekt TikTalks geht es um radikale und polarisierende Inhalte auf TikTok und darum, wie junge Erwachsene in Bayern diesen Inhalten in ihren Feeds begegnen.",
        ],
        "steps": [],
        "bib_theme": "radicalization",
    },
    {
        "en": "large-language-models-clinical-communication-information",
        "slug": "sprachmodelle-medizin-informationssuche",
        "name": "Sprachmodelle und die Suche nach Informationen",
        "seo": "Sprachmodelle in der Medizin und bei der Informationssuche",
        "short": "Wie große Sprachmodelle die Kommunikation in der Medizin und die Suche nach Informationen verändern.",
        "body": [
            "Große Sprachmodelle verändern, wie in der Medizin miteinander gesprochen wird und wie Menschen nach Informationen suchen. Eine frühere Arbeit befasst sich mit der Einwilligung nach Aufklärung. Sie argumentiert, dass Einwilligung mehr ist als ein Austausch von Worten und dass genau das begrenzt, was Sprachmodelle in einem Aufklärungsgespräch leisten können.",
            "In einem weiteren Teil meiner Arbeit frage ich, ob große Sprachmodelle über umstrittene historische Ereignisse, etwa Massenverbrechen, in manchen Sprachen weniger vollständig berichten als in anderen.",
        ],
        "steps": [],
        "bib_theme": "llm-medethics",
    },
]

DE_BASE = "/de/forschung/"

for _p in DE_PARTS:
    LANG_PAIR[f"/research/{_p['en']}/"] = DE_BASE + _p["slug"] + "/"
    LANG_PAIR[DE_BASE + _p["slug"] + "/"] = f"/research/{_p['en']}/"


def page_de():
    parts = "\n".join(
        f'<div class="theme"><a href="{DE_BASE}{t["slug"]}/">{e(t["name"])}</a><p>{e(t["short"])}</p></div>'
        for t in DE_PARTS)
    body = f"""
<div class="mobile-only mobile-intro">
<img src="{PHOTO}" alt="Porträt von {NAME}" width="132" height="168">
<div class="role"><span class="muted">er/ihm</span><br>Doktorand, <a href="{INSTITUTE_URL}">Professur für Ethik der KI und Neurowissenschaften</a>, Technische Universität München</div>
</div>
<section>
<h1 class="lead">Ich untersuche, was Menschen in Social-Media-Feeds über Gesundheit und das Gehirn zu sehen bekommen und was sie davon tatsächlich ansehen.</h1>
<p class="intro">Ich bin Doktorand an der Professur für Ethik der KI und Neurowissenschaften (Institut für Geschichte und Ethik der Medizin) der Technischen Universität München; betreut werde ich von <a href="{CHAIR_URL}">Marcello Ienca</a>. Ich arbeite im Projekt <a href="{HARMONY_URL}">HARMONY</a>, das untersucht, welche Gesundheitsinformationen und Fehlinformationen junge Erwachsene auf TikTok erreichen. Grundlage sind Datenspenden der Teilnehmenden aus ihren eigenen TikTok-Konten. Dabei verbinde ich computergestützte Textanalyse, Befragungen und Ethik. Von Oktober 2025 bis Januar 2026 war ich Fulbright-Gastwissenschaftler am <a href="{SML_URL}">Stanford Social Media Lab</a>.</p>
</section>
<div class="mobile-only mobile-contact">
{contact_links("de")}
</div>
<section>
<h2 class="label">Forschung</h2>
<div class="themes">
{parts}
</div>
<p class="small muted">Jede Überschrift führt zu einer ausführlicheren deutschen Seite. Die Projekte, alle Publikationen und die Vorträge stehen auf den englischen Seiten.</p>
</section>
<section>
<h2 class="label">Kontakt</h2>
<p class="intro">Anfragen zu Vorträgen, Interviews und Zusammenarbeit sind auf Deutsch oder Englisch willkommen: <a href="mailto:{EMAIL}">Schreiben Sie mir</a> oder <a href="{BOOKING}">vereinbaren Sie ein Gespräch</a>.</p>
</section>
"""
    write("/de/", layout("/de/", f"{NAME}: Forschung zu TikTok, Gesundheitsinformationen und Neuroethik",
                         "Alexander Sobieska ist Doktorand an der Technischen Universität München und untersucht, welche Gesundheitsinformationen und Fehlinformationen TikTok jungen Erwachsenen zeigt, was sie davon tatsächlich ansehen und wie im Internet über das Gehirn und Neurotechnologie gesprochen wird.",
                         "home", body, home=True, lang="de"))


def page_de_part(t, pubs):
    paras = "\n".join(f'<p class="{"big" if i == 0 else "intro"}">{e(x)}</p>' for i, x in enumerate(t["body"]))
    steps = ""
    if t["steps"]:
        steps = '<section><h2 class="label">Wie die Daten entstehen</h2><ol class="steps">' + "".join(f"<li>{e(x)}</li>" for x in t["steps"]) + "</ol></section>"
    mine = [x for x in pubs if x.get("theme") == t["bib_theme"]]
    if mine:
        pubs_html = '<section><h2 class="label">Publikationen</h2>' + "".join(f"<p>{cite_html(x)}</p>" for x in mine) + "</section>"
    else:
        pubs_html = '<section><h2 class="label">Publikationen</h2><p class="muted">Arbeiten aus diesem Teil erscheinen hier, sobald sie veröffentlicht sind.</p></section>'
    others = " ".join(f'<a href="{DE_BASE}{o["slug"]}/">{e(o["name"])}</a>' for o in DE_PARTS if o is not t)
    body = f"""
<section>
<p class="crumb"><a href="/de/">Startseite</a> / Forschung</p>
<h1 class="title">{e(t["name"])}</h1>
{paras}
</section>
{steps}
{pubs_html}
<section><h2 class="label">Mehr dazu</h2>
<p class="intro"><a href="/research/{t["en"]}/" hreflang="en" lang="en">Die englische Fassung dieser Seite</a> nennt außerdem die Projekte und Vorträge zu diesem Teil meiner Arbeit.</p>
</section>
<section><h2 class="label">Weitere Teile meiner Arbeit</h2><div class="inline-links">{others}</div></section>
"""
    path = DE_BASE + t["slug"] + "/"
    write(path, layout(path, t["seo"], t["short"], "research", body, lang="de"))


def page_research_index():
    items = "\n".join(
        f'<div class="entry"><h2 class="item"><a href="/research/{t["slug"]}/">{e(t["name"])}</a></h2><p>{e(t["summary"])}</p></div>'
        for t in THEMES)
    projects = "".join(
        f'<section id="{k}"><h3 class="item">{e(p["name"])}</h3>' + (f'<p class="muted">{e(p["when"])}</p>' if p["when"] else "") + f'<p class="intro">{e(p["text"])}</p>'
        + (f'<p class="small"><a href="{p["url"]}">{"Official project page" if k == "harmony" else "TUM Global Incentive Fund"}</a></p>' if p.get("url") else "") + '</section>'
        for k, p in PROJECTS.items())
    body = f"""
<section>
<h1 class="title">Research and projects</h1>
<p class="big">{e(LEAD)} My work falls into four parts.</p>
</section>
<section>
{items}
</section>
<section>
<h2 class="label">Projects</h2>
</section>
{projects}
"""
    write("/research/", layout("/research/", "Research and projects", "Research themes of " + NAME + ": TikTok recommendations and health misinformation, neuroethics online, radicalization, and language models in medical ethics.", "research", body))


def page_theme(t, pubs):
    paras = "\n".join(f'<p class="{"big" if i == 0 else "intro"}">{e(p)}</p>' for i, p in enumerate(t["body"]))
    steps = ""
    if t.get("steps"):
        steps = '<section><h2 class="label">How the data comes together</h2><ol class="steps">' + "".join(f"<li>{e(s)}</li>" for s in t["steps"]) + "</ol></section>"
    projects = ""
    if t["projects"]:
        projects = '<section><h2 class="label">Projects</h2>' + "".join(
            f'<p><a href="/research/#{k}">{e(PROJECTS[k]["name"])}</a></p>' for k in t["projects"]) + "</section>"
    mine_up = [x for x in upcoming() if x["theme"] == t["key"]]
    mine_past = [x for x in sorted(TALKS, key=lambda x: x["date"], reverse=True) if x["theme"] == t["key"] and x not in mine_up]
    talks = mine_up + mine_past
    talks_html = ('<section><h2 class="label">Talks</h2>' + "".join(talk_line(x) for x in talks) + "</section>") if talks else ""
    mine = [p for p in pubs if p.get("theme") == t["bib_theme"]]
    if mine:
        pubs_html = '<section><h2 class="label">Publications</h2>' + "".join(f"<p>{cite_html(p)}</p>" for p in mine) + "</section>"
    else:
        pubs_html = '<section><h2 class="label">Publications</h2><p class="muted">Papers from this work will be listed here as they are published. See all <a href="/publications/">publications</a>.</p></section>'
    others = " ".join(f'<a href="/research/{o["slug"]}/">{e(o["name"])}</a>' for o in THEMES if o is not t)
    de_link = LANG_PAIR.get(f"/research/{t['slug']}/", "/de/")
    body = f"""
<section>
<p class="crumb"><a href="/research/">Research</a> / {e(t["seo_title"].split(":")[0])}</p>
<h1 class="title">{e(t["name"])}</h1>
{paras}
</section>
{steps}
{projects}
{talks_html}
{pubs_html}
<section><h2 class="label">Auf Deutsch</h2><p class="intro"><a href="{de_link}" hreflang="de" lang="de">Diese Seite auf Deutsch</a></p></section>
<section><h2 class="label">Other research</h2><div class="inline-links">{others}</div></section>
"""
    path = f"/research/{t['slug']}/"
    write(path, layout(path, t["seo_title"], t["summary"] + " Research by " + NAME + ", Technical University of Munich.", "research", body, active_theme=t["key"]))


def page_publications(pubs):
    theme_label = {t["bib_theme"]: t["short"] for t in THEMES}
    items = []
    for p in pubs:
        q = pub_parts(p)
        items.append(f"""<article class="pub" data-type="{e(p['kind'])}" data-theme="{e(p.get('theme', ''))}">
<p class="meta">{e(q['year'])} · {e(q['type_label'])} · {e(theme_label.get(p.get('theme'), ''))}</p>
<p class="cite">{cite_html(p)}</p>
<div class="actions"><a href="{e(q['url'])}">DOI: {e(q['doi'])}</a>
<button type="button" class="copy" data-cite="{e(q['plain'])}">Copy citation</button></div>
</article>""")
    body = f"""
<section>
<h1 class="title">Publications and talks</h1>
<p class="intro">Also on <a href="{SCHOLAR}">Google Scholar</a> and <a href="{ORCID}">ORCID</a>. Jump to <a href="#talks">talks</a>.</p>
</section>
<h2 class="label">Publications</h2>
<div class="pubs" style="display:flex;flex-direction:column;gap:28px">
{chr(10).join(items)}
</div>
<script>
(function(){{
  [].forEach.call(document.querySelectorAll('.copy'),function(b){{
    b.addEventListener('click',function(){{
      var t=b.dataset.cite;
      (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){{b.textContent='Copied';}},function(){{window.prompt('Copy this citation:',t);}});
    }});
  }});
}})();
</script>
{talks_block()}
"""
    write("/publications/", layout("/publications/", "Publications and talks", "Publications by " + NAME + " on health misinformation, neuroethics, radicalization and language models in medical ethics.", "publications", body))


def talks_block():
    up = upcoming()
    past = [t for t in sorted(TALKS, key=lambda t: t["date"], reverse=True) if t not in up]
    up_html = ('<section><h3 class="item">Upcoming</h3>' + "".join(talk_line(t) for t in up) + "</section>") if up else ""
    return f"""
<section id="talks"><h2 class="label">Talks</h2>
<p class="intro">For talk invitations, <a href="mailto:{EMAIL}">write me</a> or <a href="{BOOKING}">schedule a call with me</a>. Talks in English or German.</p>
</section>
{up_html}
<section><h3 class="item">Selected talks</h3>{"".join(talk_line(t) for t in past)}</section>
<section><h3 class="item">Workshops and meetings organised</h3>{"".join(f'<p><strong>{e(w)}</strong> · {e(t)}</p>' for w, t in ORGANISED)}</section>
<section><h3 class="item">Awards and funding</h3>{"".join(f'<p><strong>{e(w)}</strong> · {e(a)}</p>' for w, a in AWARDS)}</section>
"""


IMPRESSUM_ADDRESS = ["Alexander Sobieska", "c/o Technische Universität München",
                     "Institut für Geschichte und Ethik der Medizin", "Ismaninger Straße 22",
                     "81675 München", "Deutschland"]

PRIVACY_DE = [
    ("1. Verantwortlicher", [
        "Verantwortlich für die Datenverarbeitung auf dieser Website ist Alexander Sobieska, c/o Technische Universität München, Institut für Geschichte und Ethik der Medizin, Ismaninger Straße 22, 81675 München, E-Mail: alexander.sobieska@tum.de. Diese Website ist ein privates Angebot und keine Website der Technischen Universität München."]),
    ("2. Keine Cookies, keine Analyse", [
        "Diese Website setzt keine Cookies, speichert nichts auf Ihrem Endgerät und verwendet keine Analyse- oder Tracking-Werkzeuge. Schriftarten werden von dieser Website selbst geladen; Inhalte anderer Anbieter sind nicht eingebunden."]),
    ("3. Hosting bei GitHub Pages", [
        "Die Website wird bei GitHub Pages bereitgestellt, einem Dienst der GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA, bzw. für Nutzerinnen und Nutzer im EWR der GitHub B.V., Prins Bernhardplein 200, 1097 JB Amsterdam, Niederlande. Wenn Sie eine Seite aufrufen, überträgt Ihr Browser technisch notwendige Angaben an die Server von GitHub, insbesondere Ihre IP-Adresse, die aufgerufene Adresse, Datum und Uhrzeit sowie Angaben zu Browser und Betriebssystem. Nach Angaben von GitHub wird die IP-Adresse von Besucherinnen und Besuchern zu Sicherheitszwecken protokolliert und gespeichert. GitHub verarbeitet diese Daten insoweit zu eigenen Zwecken; es gilt die Datenschutzerklärung von GitHub: https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement. Ich selbst erhalte von GitHub keine Daten über einzelne Seitenaufrufe.",
        "Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Mein berechtigtes Interesse liegt darin, diese Website zuverlässig und sicher bereitzustellen.",
        "Dabei können Daten in die USA übermittelt werden. Für die USA besteht ein Angemessenheitsbeschluss der Europäischen Kommission (EU-U.S. Data Privacy Framework, Beschluss vom 10. Juli 2023, Art. 45 DSGVO). GitHub, Inc. ist nach eigenen Angaben nach diesem Rahmen zertifiziert (https://www.dataprivacyframework.gov/list) und stützt sich zusätzlich auf die Standardvertragsklauseln der Europäischen Kommission.",
        "GitHub nennt keine feste Speicherdauer für diese Protokolle; sie werden nach Angaben von GitHub gespeichert, solange es für Sicherheitszwecke erforderlich ist."]),
    ("4. Kontakt per E-Mail", [
        "Wenn Sie mir eine E-Mail schreiben, verarbeite ich Ihre Adresse und den Inhalt Ihrer Nachricht, um Ihre Anfrage zu beantworten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO; mein berechtigtes Interesse ist die Beantwortung Ihrer Anfrage. Die angegebene Adresse ist eine Adresse der Technischen Universität München; E-Mails laufen daher über deren E-Mail-System. Ich lösche Ihre Nachricht, sobald sie für die Bearbeitung nicht mehr erforderlich ist, sofern keine gesetzlichen Aufbewahrungspflichten entgegenstehen."]),
    ("5. Links zu anderen Websites", [
        "Diese Website verlinkt auf andere Angebote, etwa zcal.co (Terminbuchung), Google Scholar, ORCID und LinkedIn. Erst wenn Sie einem solchen Link folgen, erhält der jeweilige Anbieter Daten von Ihnen; dafür gelten dessen Datenschutzbestimmungen."]),
    ("6. Ihre Rechte", [
        "Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17) und Einschränkung der Verarbeitung (Art. 18). Sie können der Verarbeitung Ihrer Daten, die auf Art. 6 Abs. 1 lit. f DSGVO beruht, aus Gründen, die sich aus Ihrer besonderen Situation ergeben, jederzeit widersprechen (Art. 21 DSGVO). Wenden Sie sich dazu an die oben genannte E-Mail-Adresse.",
        "Sie haben außerdem das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren (Art. 77 DSGVO). Für mich zuständig ist das Bayerische Landesamt für Datenschutzaufsicht (BayLDA), Promenade 18, 91522 Ansbach, https://www.lda.bayern.de."]),
    ("7. Weitere Angaben", [
        "Sie sind nicht verpflichtet, Daten bereitzustellen; ohne die technisch notwendigen Angaben kann die Website jedoch nicht angezeigt werden. Eine automatisierte Entscheidungsfindung einschließlich Profiling findet nicht statt.",
        "Stand: September 2026"]),
]

PRIVACY_EN = [
    ("1. Controller", [
        "The person responsible for data processing on this website is Alexander Sobieska, c/o Technical University of Munich, Institute of History and Ethics in Medicine, Ismaninger Straße 22, 81675 Munich, Germany, email: alexander.sobieska@tum.de. This is a private website, not a website of the Technical University of Munich."]),
    ("2. No cookies, no analytics", [
        "This website sets no cookies, stores nothing on your device and uses no analytics or tracking tools. Fonts are loaded from this website itself; no content from other providers is embedded."]),
    ("3. Hosting on GitHub Pages", [
        "The website is served by GitHub Pages, a service of GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA, or, for users in the EEA, GitHub B.V., Prins Bernhardplein 200, 1097 JB Amsterdam, the Netherlands. When you open a page, your browser sends technically necessary information to GitHub's servers, in particular your IP address, the address requested, date and time, and details of your browser and operating system. According to GitHub, visitors' IP addresses are logged and stored for security purposes. GitHub processes this data for its own purposes; GitHub's privacy statement applies: https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement. I do not receive any data about individual page visits from GitHub.",
        "The legal basis is Art. 6(1)(f) GDPR. My legitimate interest is to provide this website reliably and securely.",
        "Data may be transferred to the USA. The European Commission has adopted an adequacy decision for the USA (EU-U.S. Data Privacy Framework, decision of 10 July 2023, Art. 45 GDPR). GitHub, Inc. states that it is certified under this framework (https://www.dataprivacyframework.gov/list) and also relies on the European Commission's standard contractual clauses.",
        "GitHub does not state a fixed retention period for these logs; according to GitHub they are kept as long as needed for security purposes."]),
    ("4. Contact by email", [
        "If you email me, I process your address and the content of your message to answer your request. The legal basis is Art. 6(1)(f) GDPR; my legitimate interest is answering your request. The address given is a Technical University of Munich address, so emails pass through its email system. I delete your message once it is no longer needed, unless legal retention duties apply."]),
    ("5. Links to other websites", [
        "This website links to other services, such as zcal.co (booking), Google Scholar, ORCID and LinkedIn. Those providers receive data from you only once you follow such a link; their privacy terms then apply."]),
    ("6. Your rights", [
        "You have the right of access (Art. 15 GDPR), rectification (Art. 16), erasure (Art. 17) and restriction of processing (Art. 18). You may object at any time, on grounds relating to your particular situation, to processing based on Art. 6(1)(f) GDPR (Art. 21 GDPR). To do so, write to the email address above.",
        "You also have the right to lodge a complaint with a data protection supervisory authority (Art. 77 GDPR). The authority responsible for me is the Bavarian State Office for Data Protection Supervision (BayLDA), Promenade 18, 91522 Ansbach, Germany, https://www.lda.bayern.de."]),
    ("7. Further information", [
        "You are not obliged to provide data, but without the technically necessary information the website cannot be displayed. No automated decision-making, including profiling, takes place.",
        "Last updated: September 2026"]),
]


def linkify(text):
    out = e(text)
    return re.sub(r"(https?://[^\s<]+?)([.,;)]?)(?=\s|$)", lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>{m.group(2)}', out)


def page_legal():
    def block(sections):
        return "".join(f'<section><h3 class="item">{e(h)}</h3>' + "".join(f'<p class="intro">{linkify(t)}</p>' for t in ps) + "</section>" for h, ps in sections)
    address = "<br>".join(e(x) for x in IMPRESSUM_ADDRESS)
    body = f"""
<section>
<h1 class="title">Impressum und Datenschutz</h1>
<p class="intro" lang="de">Impressum und Datenschutzerklärung stehen, wie gesetzlich vorgesehen, auf Deutsch; darunter folgt eine englische Übersetzung der Datenschutzerklärung. Bei Abweichungen gilt die deutsche Fassung.</p>
<p class="intro">The legal notice and the privacy notice are in German, as German law requires, followed by an English translation of the privacy notice. If the versions differ, the German one applies.</p>
</section>
<section lang="de">
<h2 class="label">Impressum</h2>
<p class="intro">Angaben gemäß § 5 DDG und § 18 Abs. 1 MStV</p>
<p class="intro">{address}</p>
<p class="intro">E-Mail: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p class="intro">Dies ist die private Website von Alexander Sobieska. Sie ist kein Angebot der Technischen Universität München; die TUM ist für die Inhalte nicht verantwortlich.</p>
</section>
<section lang="de">
<h2 class="label">Datenschutzerklärung</h2>
{block(PRIVACY_DE)}
</section>
<section>
<h2 class="label">Privacy notice (English translation)</h2>
{block(PRIVACY_EN)}
</section>
"""
    write("/legal/", layout("/legal/", "Impressum and privacy", "Legal notice (Impressum) and privacy notice for alexandersobieska.com.", "", body))


def page_404():
    body = """
<section>
<h1 class="title">Page not found</h1>
<p class="intro">This page does not exist. Go to the <a href="/">home page</a> or see the <a href="/publications/">publications</a>.</p>
<p class="small muted">While you are here: the brain went for a <a href="/brain-run/">run</a>.</p>
</section>
"""
    (OUT / "404.html").write_text(layout("/404.html", "Page not found", "Page not found.", "", body), encoding="utf-8")


def extras():
    # hidden easter egg page, not in the nav and not in the sitemap
    (OUT / "brain-run").mkdir(parents=True, exist_ok=True)
    shutil.copy(SRC / "brain-run.html", OUT / "brain-run" / "index.html")
    shutil.copy(CV_SOURCE, OUT / CV_PDF.lstrip("/"))
    shutil.copy(SRC / "style.css", OUT / "style.css")
    css = (SRC / "fonts.css").read_text() + "\n" + (SRC / "style.css").read_text()
    (OUT / "style.css").write_text(css, encoding="utf-8")
    (OUT / "CNAME").write_text("alexandersobieska.com\n")
    (OUT / ".nojekyll").write_text("")
    (OUT / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#1740D1"/>'
        '<text x="32" y="42" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="28" font-weight="700" fill="#fff">AS</text></svg>')
    urls = ["/", "/research/", "/publications/"] + (["/legal/"] if LEGAL_READY else []) + [f"/research/{t['slug']}/" for t in THEMES]
    urls.insert(1, "/de/")
    for _t in DE_PARTS:
        urls.append(DE_BASE + _t["slug"] + "/")
    alt = (f'<xhtml:link rel="alternate" hreflang="en" href="{SITE}/"/>'
           f'<xhtml:link rel="alternate" hreflang="de" href="{SITE}/de/"/>'
           f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>')
    def alts(u):
        if u not in LANG_PAIR:
            return ""
        en = u if not u.startswith("/de/") else LANG_PAIR[u]
        deu = LANG_PAIR[u] if not u.startswith("/de/") else u
        return (f'<xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}"/>'
                f'<xhtml:link rel="alternate" hreflang="de" href="{SITE}{deu}"/>'
                f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{en}"/>')
    sm = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY.isoformat()}</lastmod>{alts(u)}</url>" for u in urls)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{sm}</urlset>\n')
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")


def main():
    if OUT.exists():
        for sub in OUT.iterdir():
            if sub.is_dir() and sub.name not in ("fonts", "img"):
                shutil.rmtree(sub)
    pubs = parse_bib(SRC / "publications.bib")
    page_home(pubs)
    page_de()
    for _t in DE_PARTS:
        page_de_part(_t, pubs)
    page_research_index()
    for t in THEMES:
        page_theme(t, pubs)
    page_publications(pubs)
    if LEGAL_READY:
        page_legal()
    page_404()
    extras()
    print(f"Built {len(list(OUT.rglob('*.html')))} pages into {OUT}")


if __name__ == "__main__":
    main()
