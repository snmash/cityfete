#!/usr/bin/env python3
"""Generates the static pages for the City Fête Events site.

Run:  python3 build.py
Pages are written next to this file. Edit the content below, re-run, commit.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
IMG = "assets/img/"


def img(name):
    """Path to a photo or logo stored in assets/img/."""
    return IMG + name


LOGO = img("city-fete-logo.png")

NAV = [
    ("Home", "index.html"),
    ("About", "about.html"),
    ("Weddings", "weddings.html"),
    ("Testimonials", "testimonials.html"),
    ("Contact", "contact.html"),
]

# Press mentions: (name, link, logo file, display height in px, shown on Testimonials strip)
PRESS = [
    ("The Seattle Times", None, "press/seattle-times.png", 79, False),
    ("Brides", "https://www.brides.com/love-looks-like-this-married-at-united-states-canada-border-pandemic-5206827", "press/brides.jpg", 43, True),
    ("Junebug Weddings", "https://junebugweddings.com/wedding-blog/unique-peace-arch-park-micro-wedding/", "press/junebug-weddings.png", 31, True),
    ("Northwest Wedding Guide", None, "press/northwest-wedding-guide.png", 79, True),
]


def featured(large=False, more=True):
    items = []
    for name, href, logo, height, on_large in PRESS:
        if large and not on_large:
            continue
        h = round(height * 1.44) if large else height
        pic = f'<img src="{img(logo)}" alt="{escape(name)}" style="height:{h}px" loading="lazy">'
        if href:
            items.append(f'<li><a href="{href}" target="_blank" rel="noopener">{pic}</a></li>')
        else:
            items.append(f"<li>{pic}</li>")
    tail = '\n      <span class="label">+ more!</span>' if more else ""
    cls = "featured large" if large else "featured"
    return f"""    <section class="{cls}" aria-label="Featured in">
      <span class="label">Featured in:</span>
      <ul>
        {chr(10).join('        ' + i for i in items).strip()}
      </ul>{tail}
    </section>"""


def layout(slug, title, description, body, script=False):
    nav = "\n".join(
        f'          <li><a href="{href}"{" aria-current=\"page\"" if href == slug else ""}>{label}</a></li>'
        for label, href in NAV
    )
    js = '\n  <script src="assets/site.js" defer></script>' if script else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:type" content="website">
  <link rel="icon" href="{LOGO}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@200&family=Raleway:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/site.css">{js}
</head>
<body>
  <div class="page">
    <header class="site-header">
      <a class="brand" href="index.html">
        <img src="{LOGO}" alt="City Fête Events logo" width="121" height="121">
        <span>City Fête Events</span>
      </a>
      <div class="nav-row">
        <nav aria-label="Site">
          <ul class="nav">
{nav}
          </ul>
        </nav>
        <div class="social">
          <a href="https://www.instagram.com/cityfete/" target="_blank" rel="noopener">Instagram</a>
          <a href="https://www.facebook.com/cityfete" target="_blank" rel="noopener">Facebook</a>
        </div>
      </div>
    </header>

    <main>
{body}
    </main>

    <footer class="site-footer">
      &copy; City Fête Events &middot; Seattle, WA
    </footer>
  </div>
</body>
</html>
"""


def cards(items, small=False):
    out = []
    for img, alt, heading, text in items:
        out.append(f"""        <article class="card">
          <img src="{img}" alt="{escape(alt)}" loading="lazy">
          <div class="card-body">
            <h2 class="serif-title">{escape(heading)}</h2>
            <p>{escape(text)}</p>
          </div>
        </article>""")
    cls = "cards small" if small else "cards"
    return f'      <div class="{cls}">\n' + "\n".join(out) + "\n      </div>"


# ---------------------------------------------------------------- Home
GALLERY = [
    "",
    "Credit: Kelly Robbins Photography",
    "Credit: Brogan Marie Photography",
    "Credit: Felipe Callado Photography",
    "Credit: Brogan Marie Photography",
    "Credit: Brandon Wong Photography",
    "Credit: Darkroom Doctor Studios",
    "",
    "Credit: Darkroom Doctor Studios",
    "Credit: Felipe Callado Photography",
    "D+H // Kelley Farm",
    "Credit: Darkroom Doctor Studios",
]


def gallery_file(n):
    return img(f"gallery-{n:02d}.jpg")


def gallery():
    slides, thumbs = [], []
    for i, credit in enumerate(GALLERY):
        full = gallery_file(i + 1)
        thumb = img(f"gallery-{i + 1:02d}-thumb.jpg")
        alt = f"City Fête Events gallery photo {i + 1}"
        src = f'src="{full}"' if i == 0 else f'data-src="{full}"'
        active = ' class="is-active"' if i == 0 else ""
        slides.append(f'          <img {src} alt="{alt}" data-credit="{escape(credit)}"{active}>')
        thumbs.append(
            f'          <button type="button" aria-label="Show photo {i + 1}" aria-current="{"true" if i == 0 else "false"}">'
            f'<img src="{thumb}" alt="" loading="lazy" width="65" height="65"></button>'
        )
    return f"""      <section class="gallery" data-gallery aria-label="Photo gallery">
        <div class="gallery-stage">
{chr(10).join(slides)}
          <p class="gallery-caption"></p>
          <button class="gallery-btn prev" type="button" aria-label="Previous photo">&#8249;</button>
          <button class="gallery-btn next" type="button" aria-label="Next photo">&#8250;</button>
        </div>
        <div class="gallery-thumbs">
{chr(10).join(thumbs)}
        </div>
      </section>"""


HOME_CARDS = [
    (img("weddings.jpg"),
     "Wedding celebration", "Weddings",
     "Creating unforgettable wedding experiences for couples whether it's a traditional ceremony or a modern celebration. We'll bring your vision to life and help make a lasting impression for guests.."),
    (img("corporate.jpg"),
     "Corporate event", "Corporate & Business Gatherings",
     "Tailored planning and design services to create impactful and memorable corporate gatherings, business meetings, press events, and product showcases."),
    (img("milestone.jpg"),
     "Milestone celebration", "Milestone & Social Events",
     "From birthdays to anniversaries and everything in between, milestone events are a celebration of life's special moments. Our goal is to always make the event as special as the milestone. If there's a reason to celebrate it, we can plan it."),
    # The Wix site used a Wix stock photo here ("Wedding Rings"). Wix stock media is licensed
    # for Wix-hosted sites only, so a City Fête gallery photo stands in until you pick a replacement.
    (gallery_file(2),
     "Couple embracing on the beach (Kelly Robbins Photography)", "Proposals",
     "Getting engaged is a momentous occasion, and we're here to help you make it unforgettable. We craft romantic and unforgettable proposal experiences to kick off your life journey on the perfect note."),
]

home = f"""{featured()}
      <img class="hero" src="{img('hero.jpg')}" alt="Wedding party laughing together in front of a rustic barn">

      <section class="panel">
        <h1 class="display">City Fête Events</h1>
        <p class="tagline">We're more than just event planners &ndash; we're architects of fun!</p>
        <p>As a premium boutique event agency, we specialize in crafting luxury events and experiences that are tailored to each client's unique vision. From intimate private dinners and weddings to business gatherings and large social events, we focus on creating moments that leave a lasting impression on every guest.</p>
      </section>

{gallery()}

      <h2 class="display section-title">What We Do</h2>
{cards(HOME_CARDS)}

      <section class="follow">
        <h2 class="display">Follow us as we do it!</h2>
        <a class="btn" href="https://www.instagram.com/cityfete" target="_blank" rel="noopener">@cityfete on IG</a>
      </section>"""

# ---------------------------------------------------------------- About
about = f"""      <div class="split">
        <section class="split-text about-text">
          <h1 class="display">Founder &amp; Lead Planner,<br>Paruul M</h1>
          <p class="lede">I'll start by saying I'm so glad you're here!</p>
          <p class="gap">I hail from the east coast but fell in love with Seattle on my first trip here (literally, I also met my husband here that week!). My love for event planning stems from over 10+ years of experience in creating impactful press conferences, corporate events, and celebrity-hosted dinners in my day job as a PR professional.</p>
          <p class="gap">City Fête events was born out of my love for designing and producing unique events for clients. I truly believe that at the end of the day, guests will always remember how the event made them feel and I specialize in creating a personalized and memorable experience for guests.</p>
          <p>We're based out of Seattle, WA but work with clients across the country. When I'm not working with clients of my own, I'm freelancing for my planner friends and their awesome clients.</p>
          <p>Outside of event planning, you can find me busting out some dance moves (fun fact: we also offer wedding choreography services!) and listening to new music.</p>
          <a class="btn dark" href="contact.html">Message me!</a>
        </section>
        <div class="split-photo">
          <img src="{img('paruul.jpg')}" alt="Paruul M, founder and lead planner of City Fête Events" style="object-position: 7% 50%">
        </div>
      </div>"""

# ---------------------------------------------------------------- Weddings
WEDDING_CARDS = [
    (gallery_file(7),
     "Wedding ceremony (Darkroom Doctor Studios)", "Full Service Planning",
     "Are you a newly engaged couple that can't wait to plan their big day but need help getting started? Then this package is perfect for you. From venue search and budget planning to wedding design and vendor search, we'll work with you to bring your wedding to life from start to finish!"),
    (img("customized.jpg"),
     "Wedding day details", "Customized Wedding Planning",
     "Every wedding is different and requires different level of support. This option is our most popular one as we build a custom planning package based on the needs and wants of the couple and their families. Clients have the option to be as involved as they want (or not at all) in the process and we're here to help throughout all of it."),
    (img("coordination.jpg"),
     "Wedding reception", "Wedding Coordination",
     "You've done all the planning you possibly can and now you need someone to take over and make sure the day runs smoothly. We take care of all the small, technical details to make your wedding day perfect so you can enjoy the day and focus on marrying your best friend!"),
    (img("choreography.jpg"),
     "Couple dancing", "Wedding Choreography",
     "Looking for the perfect first dance to do at your reception? We'll choreograph your first dance so you can wow your family and friends as a married couple. No dance experienced required and we customize the choreography based on your needs!"),
]

weddings = f"""      <section class="intro">
        <h1 class="display">Wedding Services</h1>
        <p>Our speciality is building custom wedding planning packages for clients based on their needs. We take pride in celebrating love in all its forms, embracing and honoring the unique backgrounds, ethnicities, and cultures of our couples. From selecting the perfect venue and coordinating with vendors to designing personalized decor and managing every detail on the day-of, we'll work closely with you to ensure that your wedding day is nothing short of perfect.</p>
      </section>
{cards(WEDDING_CARDS, small=True)}"""

# ---------------------------------------------------------------- Testimonials
def note(text, who, extra=""):
    return f"""        <blockquote class="note{extra}">
          <p>{escape(text)}</p>
          <cite>{escape(who)}</cite>
        </blockquote>"""


def note_photo(name, alt, tall=False, position=""):
    cls = "note-photo tall" if tall else "note-photo"
    return f"""        <div class="{cls}">
          <img src="{img(name)}" alt="{escape(alt)}" loading="lazy"{f' style="object-position: {position}"' if position else ""}>
        </div>"""


testimonials = f"""      <figure class="quote-hero" style="margin:0">
        <img src="{img('testimonial-hero.jpg')}" alt="Couple dancing under string lights at dusk">
        <figcaption>
          &ldquo;Thank you so much for all your help Paruul! You made our standard of wedding planner way too high now. You didn't miss anything and kept the whole day so smooth. Thank you!&rdquo;
          <cite>Derek + Linh</cite>
        </figcaption>
      </figure>

{featured(large=True, more=False)}

      <h1 class="display notes-title">Love notes from clients:</h1>
      <div class="notes">
{note_photo('client-devyn-hunter.jpg', 'Devyn and Hunter')}
{note('"Paruul was essential to our event. We had all the pieces in place but she coordinated all the vendors, prepared the event time line and kept the event running smoothly. We had no hiccups or problems and it was so worth it. Thank you Paruul! We couldn’t have pulled it off without you."', 'Devyn + Hunter')}
{note_photo('client-farah-malcolm.jpg', 'Farah and Malcolm at their Peace Arch wedding (Felipe Callado Photography)')}
{note('"CF did an amazing job planning our border wedding! Paruul took on the challenge and still made the whole process fun! She kept up with the constantly changing covid guidelines and leaned in to making those changes. Paruul helped us navigate all the challenges, kept us under budget and made our day perfectly beautiful by making sure we incorporated elements that showcased who we are as a couple. Thank you!!"', 'Farah + Malcolm')}
{note_photo('client-heather-yarian.jpg', 'Heather and Yarian', tall=True, position='right center')}
{note('When it came to our wedding we took a very DIY approach to planning it. But we eventually started realizing just how many tiny details were adding up. We are so glad we made the decision to hire Paruul to be our day-of coordinator. She did a fantastic job of asking questions, setting a timeline, running our rehearsal, and managing different people’s expectations. Even though we used her for day-of coordinator, we appreciated that she set up meetings months before our wedding so we felt prepared and aware of what to expect the week and day of. Our wedding was stress-free and we didn’t have to worry about a thing. Paruul did a great job of working with our other vendors and bringing all the information into a central cohesive place. She is very easy to work with and we are very grateful we had her in our corner during our big day.', 'Heather + Yarian')}
        <!-- The Wix site used a Wix stock photo here. Wix stock media is licensed for Wix-hosted
             sites only, so this tile is left as a plain panel until you add your own photo. -->
        <div class="note-photo tall blank" aria-hidden="true"></div>
{note('"Our wedding day went smoothly all thanks to CF! I made a last minute decision to hire a wedding coordinator and I\'m so glad I did. Paruul was amazing - she created a detailed timeline for the day and even joined our rehearsal to make sure the wedding party felt comfortable with how the ceremony would be run. Highly recommend if you\'re looking for a worry-free day!"', 'Kelsey + Mark', ' after-blank')}
      </div>"""

# ---------------------------------------------------------------- Contact
CONTACT_EMAIL = "paruul@cityfete.com"

contact = f"""      <div class="split">
        <section class="split-text contact-text">
          <h1 class="display">Let's chat!</h1>
          <p class="contact-lede">If you are just starting to plan your event and your date is flexible, feel free to book a consultation today using the below link. If you already have a date set, send us an email with the details.</p>
          <p class="contact-cta"><a class="btn" href="https://calendly.com/cityfete/consultation" target="_blank" rel="noopener">Book a Consultation</a></p>
          <p class="contact-cta"><a class="btn dark" href="mailto:{CONTACT_EMAIL}">Contact us</a></p>
          <p class="contact-email"><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
        </section>
        <div class="split-photo">
          <img src="{img('contact.jpg')}" alt="Pavilion among the trees at Peace Arch park (Felipe Callado Photography)">
        </div>
      </div>"""

PAGES = [
    ("index.html", "City Fête Events | Seattle Wedding Planner",
     "City Fête Events is a luxury wedding planning and event planning company, based in Seattle, Washington but services weddings and events across the United States. We plan all types of weddings and specialize in South Asian / Indian wedding planning.",
     home, True),
    ("about.html", "About | City Fête Events",
     "Meet Paruul M, founder and lead planner of City Fête Events, a Seattle-based boutique wedding and event planning agency.",
     about, False),
    ("weddings.html", "Weddings | City Fête Events",
     "Wedding services from City Fête Events: full service planning, customized planning, wedding coordination, and wedding choreography.",
     weddings, False),
    ("testimonials.html", "Testimonials | City Fête Events",
     "Love notes from City Fête Events clients.",
     testimonials, False),
    ("contact.html", "Let's chat! | City Fête Events",
     "Book a consultation or email City Fête Events the details of your wedding or event.",
     contact, False),
]

for slug, title, description, body, script in PAGES:
    (ROOT / slug).write_text(layout(slug, title, description, body, script), encoding="utf-8")
    print("wrote", slug)

(ROOT / ".nojekyll").write_text("")
