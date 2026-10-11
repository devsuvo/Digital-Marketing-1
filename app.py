"""SD — Tech PR & Marketing agency website (Flask)."""
from flask import Flask, render_template, request, redirect, url_for, flash, abort

app = Flask(__name__)
app.secret_key = "sd-dev-secret-change-me"


def unsplash(photo_id, w=1200):
    return f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w={w}&q=80"


NAV = [
    ("Expertise", "expertise"),
    ("Capabilities", "capabilities"),
    ("Our Work", "case_studies"),
    ("Clients", "clients"),
    ("About", "about"),
    ("Careers", "careers"),
    ("News", "news"),
    ("Let's Talk", "lets_talk"),
]

EXPERTISE = {
    "ai": {
        "title": "Artificial Intelligence",
        "short": "AI is changing every industry at once. We help the teams building it cut through the noise and show what their technology actually does.",
        "hero": unsplash("1677442136019-21780ecad995", 1800),
        "headline": "Turning breakthrough models into stories people believe.",
        "stats": [("120+", "AI launches supported"), ("3x", "Average lift in share of voice"), ("40+", "Founders media-trained")],
        "points": [
            ("Category creation", "We name the problem you solve before competitors do, so your company becomes the reference point."),
            ("Technical translation", "Our team turns papers, benchmarks and architecture diagrams into plain, quotable narratives."),
            ("Trust & responsibility", "We prepare leaders to speak credibly on safety, ethics and regulation."),
        ],
    },
    "consumer": {
        "title": "Consumer Tech",
        "short": "We're early adopters ourselves. We know what makes people try something new and what keeps them using it.",
        "hero": unsplash("1511707171634-5f897ff02aa9", 1800),
        "headline": "Products people talk about at dinner.",
        "stats": [("500+", "Product reviews secured"), ("60+", "Launch events run"), ("1B+", "Impressions per year")],
        "points": [
            ("Launch moments", "From embargoed reviews to launch-day buzz, we build momentum that lasts beyond week one."),
            ("Creator networks", "We connect your product with the reviewers and creators your audience already trusts."),
            ("Retail stories", "Seasonal campaigns and gift guides that turn attention into sales."),
        ],
    },
    "enterprise": {
        "title": "Enterprise",
        "short": "SaaS, security, data or infrastructure: we help enterprise brands find a clear voice that buyers trust.",
        "hero": unsplash("1486406146926-c627a92ad1ab", 1800),
        "headline": "Making complex B2B stories impossible to ignore.",
        "stats": [("200+", "Enterprise clients"), ("85%", "Coverage in tier-one trade media"), ("25", "Analyst programs active")],
        "points": [
            ("Analyst relations", "We build relationships with the analysts who shape buying decisions."),
            ("Thought leadership", "Bylines, speaking slots and research reports that position your executives as experts."),
            ("Customer stories", "We turn happy customers into case studies, reference calls and press coverage."),
        ],
    },
    "financial": {
        "title": "FinTech & Financial",
        "short": "For new payment platforms and established investors alike, we build credibility in a market that runs on trust.",
        "hero": unsplash("1563986768609-322da13575f3", 1800),
        "headline": "Credibility is the currency we trade in.",
        "stats": [("$4B+", "Client funding announced"), ("70+", "Funding rounds launched"), ("15", "VC firms represented")],
        "points": [
            ("Funding announcements", "We turn a round into a story about vision, traction and what comes next."),
            ("Regulatory readiness", "Message discipline for the moments when compliance and reputation meet."),
            ("Investor brand", "We help venture firms stand out to the founders they want to back."),
        ],
    },
    "emerging-tech": {
        "title": "Emerging Tech",
        "short": "Climate, robotics, biotech, space: if your technology could change the world, we'll help the world hear about it.",
        "hero": unsplash("1485827404703-89b55fcc595e", 1800),
        "headline": "The future needs a narrator.",
        "stats": [("90+", "Deep-tech startups"), ("30", "Patents explained in press"), ("12", "Countries reached")],
        "points": [
            ("Science storytelling", "We make deep technical work easy to understand without dumbing it down."),
            ("Policy & impact", "We put your work in front of the policymakers and stakeholders who shape the market."),
            ("Talent branding", "We help you attract the rare engineers and scientists you need to grow."),
        ],
    },
    "blockchain": {
        "title": "Blockchain",
        "short": "We launched companies through the dot-com boom, Web 2.0 and mobile. Now we help build Web3's foundations with clear, careful communication.",
        "hero": unsplash("1639762681485-074b7f938ba0", 1800),
        "headline": "Signal over hype, every cycle.",
        "stats": [("50+", "Protocols & platforms"), ("24/7", "Community monitoring"), ("10+", "Years in Web3")],
        "points": [
            ("Community first", "Discord, X and Telegram strategies built around real engagement."),
            ("Crisis readiness", "Fast, honest communication plans for volatile markets."),
            ("Mainstream crossover", "We take your story from crypto-native outlets to business media."),
        ],
    },
}

CAPABILITIES = [
    ("Public & Media Relations", "Strategic media relations, launch campaigns and reputation management for the outlets that matter to you.", unsplash("1504711434969-e33886168f5c")),
    ("Content", "Bylines, blogs, reports and executive content that build authority over time.", unsplash("1455390582262-044cdead277a")),
    ("Creative", "Brand identity, campaign concepts and visual storytelling that people remember.", unsplash("1561070791-2526d30994b5")),
    ("Custom Website Development", "Fast, conversion-focused websites built to grow with your company.", unsplash("1547658719-da2b51169166")),
    ("Social & Community", "Always-on social programs and communities that turn followers into advocates.", unsplash("1611162617213-7d7a39e9b1d7")),
    ("Paid Media", "Targeted paid campaigns that amplify earned wins and drive measurable pipeline.", unsplash("1460925895917-afdab827c52f")),
]

_NEWS_RAW = [
    ("AI", "SD Insights", "Why every AI startup needs a point of view, not just a product", unsplash("1620712943543-bcc4688e7485", 800)),
    ("Consumer Tech", "SD Insights", "The new rules of the product review embargo", unsplash("1511707171634-5f897ff02aa9", 800)),
    ("Climate", "SD Insights", "How climate founders can tell stories without greenwashing", unsplash("1473341304170-971dccb5ac1e", 800)),
    ("VC", "SD Insights", "What founders get wrong about announcing a funding round", unsplash("1559136555-9303baea8ebd", 800)),
    ("Enterprise", "SD Insights", "Analyst relations in 2026: a field guide", unsplash("1542744173-8e7e53415bb0", 800)),
    ("AI", "SD Insights", "Open-source AI and the battle for developer mindshare", unsplash("1518770660439-4636190af475", 800)),
    ("Life Sciences", "SD Insights", "Explaining biotech breakthroughs to a general audience", unsplash("1532187863486-abf9dbad1b69", 800)),
    ("Data Analytics", "SD Insights", "Data centers are the new headline. Here's how to own the story", unsplash("1558494949-ef010cbdcc31", 800)),
    ("FinTech", "SD Insights", "Trust signals that make fintech brands credible", unsplash("1563986768609-322da13575f3", 800)),
    ("Emerging Tech", "SD Insights", "Robotics PR: showing the machine, telling the human story", unsplash("1485827404703-89b55fcc595e", 800)),
    ("Blockchain", "SD Insights", "Communicating through a crypto winter", unsplash("1639762681485-074b7f938ba0", 800)),
    ("Agency", "SD News", "SD expands its content and creative studio", unsplash("1522071820081-009f0129c71c", 800)),
]

_DATES = ["Oct 08, 2026", "Oct 02, 2026", "Sep 27, 2026", "Sep 21, 2026", "Sep 14, 2026", "Sep 09, 2026",
          "Aug 30, 2026", "Aug 22, 2026", "Aug 15, 2026", "Aug 07, 2026", "Jul 29, 2026", "Jul 18, 2026"]
NEWS = [dict(cat=c, outlet=o, title=t, img=i, date=_DATES[n], read=f"{4 + n % 4} min read")
        for n, (c, o, t, i) in enumerate(_NEWS_RAW)]

PROCESS = [
    ("Discover", "We learn your business, technology, competitors and audience until we can explain it better than anyone outside your company."),
    ("Strategy", "We define the narrative, key messages and the channels and moments that will move your market."),
    ("Launch", "Media, content, creative and social go out together as one coordinated campaign."),
    ("Measure", "Clear reporting on coverage, share of voice, traffic and pipeline, and we refine every month."),
]

FAQS = [
    ("What size companies do you work with?", "Everything from seed-stage startups to public companies. Most clients are venture-backed tech companies between Series A and IPO."),
    ("How quickly can we get started?", "Most programs kick off within two weeks of signing, starting with a discovery workshop."),
    ("Do you offer project-based work?", "Yes. Alongside monthly retainers we take on launches, funding announcements, website builds and creative projects."),
    ("How do you measure success?", "We agree on KPIs up front, such as coverage quality, share of voice, traffic, leads or hiring, and report on them every month."),
    ("Do you work internationally?", "Yes. We run campaigns across North America, Europe and Asia through our partner network."),
]

CASES = [
    ("Nova Robotics", "Emerging Tech", "Took a seed-stage robotics startup from stealth to the front page in 90 days.", unsplash("1485827404703-89b55fcc595e", 900)),
    ("Lumen AI", "Artificial Intelligence", "Built a category narrative that helped close a $40M Series B.", unsplash("1677442136019-21780ecad995", 900)),
    ("PayGrid", "FinTech", "Repositioned a payments platform for enterprise buyers.", unsplash("1563986768609-322da13575f3", 900)),
    ("Orbit Home", "Consumer Tech", "Ran a holiday launch that sold out its first production run.", unsplash("1558002038-1055907df827", 900)),
    ("Vaultline", "Enterprise Security", "Turned breach research into a year-long thought leadership program.", unsplash("1550751827-4bd374c3f58b", 900)),
    ("Chainlight", "Blockchain", "Brought a Web3 infrastructure protocol into mainstream business media.", unsplash("1639762681485-074b7f938ba0", 900)),
]

CLIENTS = ["Nova Robotics", "Lumen AI", "PayGrid", "Orbit Home", "Vaultline", "Chainlight", "Helio Labs",
           "Quanta Bio", "Northwind Data", "Arcwave", "Brightseed", "Kairo Ventures", "Stratus Cloud",
           "Pixelfox", "Greenvolt", "Meridian Pay"]

TESTIMONIALS = [
    ("SD felt like part of our own team. They took the time to understand our technology and turned it into a story customers and reporters both understood.", "Ava Martinez", "VP Marketing, Helio Labs", unsplash("1494790108377-be9c29b29330", 200)),
    ("They sharpened our message until it actually stood for something. If you're building something different, SD will help you say so out loud.", "Daniel Okafor", "Co-Founder & CEO, Lumen AI", unsplash("1500648767791-00dcc994a43e", 200)),
    ("Strategic, well connected and consistent. SD has helped us and our portfolio companies get the right message to the right audience.", "Mei Tanaka", "Partner, Kairo Ventures", unsplash("1438761681033-6461ffad8d80", 200)),
    ("I've brought SD with me to two companies now. The work is excellent, the team is professional, and the results show up.", "James Holloway", "Head of Communications, Stratus Cloud", unsplash("1472099645785-5658abf4ff4e", 200)),
]

JOBS = [
    ("Senior Account Director", "San Francisco / Remote", "Full-time"),
    ("Account Executive, AI & Enterprise", "New York / Remote", "Full-time"),
    ("Content Strategist", "Remote", "Full-time"),
    ("Social Media Manager", "Remote", "Full-time"),
    ("PR Intern", "San Francisco", "Internship"),
]

TEAM = [
    ("Sarah Dean", "Founder & CEO", unsplash("1573164713988-8665fc963095", 600)),
    ("Marcus Lee", "Chief Strategy Officer", unsplash("1507679799987-c73779587ccf", 600)),
    ("Priya Nair", "VP, Media Relations", unsplash("1494790108377-be9c29b29330", 600)),
    ("Tom Becker", "Creative Director", unsplash("1500648767791-00dcc994a43e", 600)),
]


@app.context_processor
def globals_():
    return {"nav": NAV, "expertise_all": EXPERTISE, "unsplash": unsplash}


@app.route("/")
def home():
    return render_template("index.html", news=NEWS[:8], testimonials=TESTIMONIALS, capabilities=CAPABILITIES, process=PROCESS, clients=CLIENTS)


@app.route("/expertise")
def expertise():
    return render_template("expertise.html")


@app.route("/expertise/<slug>")
def expertise_detail(slug):
    item = EXPERTISE.get(slug) or abort(404)
    return render_template("expertise_detail.html", item=item, slug=slug, cases=CASES[:3])


@app.route("/capabilities")
def capabilities():
    return render_template("capabilities.html", capabilities=CAPABILITIES, process=PROCESS, faqs=FAQS)


@app.route("/case-studies")
def case_studies():
    return render_template("case_studies.html", cases=CASES)


@app.route("/clients")
def clients():
    return render_template("clients.html", clients=CLIENTS, testimonials=TESTIMONIALS)


@app.route("/about")
def about():
    return render_template("about.html", team=TEAM)


@app.route("/careers")
def careers():
    return render_template("careers.html", jobs=JOBS, testimonials=TESTIMONIALS[:2])


@app.route("/news")
def news():
    return render_template("news.html", news=NEWS, title="News", subtitle="Agency news, insights and ideas from the SD team.")


@app.route("/trending-news")
def trending_news():
    return render_template("news.html", news=NEWS[::-1], title="Trending News", subtitle="What our team is reading, writing and talking about.")


@app.route("/lets-talk", methods=["GET", "POST"])
def lets_talk():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        if not name or not email:
            flash("Please enter your name and email.", "error")
        else:
            flash(f"Thanks {name}! We'll be in touch soon.", "success")
            return redirect(url_for("lets_talk"))
    return render_template("lets_talk.html", faqs=FAQS)


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
