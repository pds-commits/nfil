"""Generates the six short-LP mocks so shared pieces (form, header, CTA, footer) stay identical."""
import math
from pathlib import Path

V = 22
OUT = Path(__file__).parent

REASSURE = "Free 30-minute call — no commitment."
BTN = "Book Your Free Discovery Call"

PAGES = [
    ("academic-a-split.html", "Academic · A — capable but stuck", "academic"),
    ("academic-b-photo.html", "Academic · B — a week with a coach", "academic"),
    ("academic-c-relief.html", "Academic · C — ready before college asks", "academic"),
    ("student-a-define.html", "Student EF · A — what it is, plainly", "student"),
    ("student-b-skills.html", "Student EF · B — systems that fit you", "student"),
    ("student-c-process.html", "Student EF · C — inside a session", "student"),
    ("student-d-video.html", "Student EF · D — on the call", "student"),
]


def form(dark=False, title="Book a free discovery call"):
    return f"""<div class="form-card{' dark' if dark else ''}">
  <h3>{title}</h3>
  <p class="form-sub">Tell us what’s going on. We’ll follow up to schedule.</p>
  <div class="field-row">
    <div class="field"><label>First Name *</label><input type="text" disabled placeholder="First name"></div>
    <div class="field"><label>Last Name *</label><input type="text" disabled placeholder="Last name"></div>
  </div>
  <div class="field-row">
    <div class="field"><label>Email *</label><input type="email" disabled placeholder="you@email.com"></div>
    <div class="field"><label>Phone *</label><input type="tel" disabled placeholder="(555) 000-0000"></div>
  </div>
  <div class="field">
    <label>What's the main reason you're reaching out right now? *</label>
    <select disabled>
      <option value="">-None-</option>
      <option>Academics / school support</option>
      <option>Career development</option>
      <option>College transition</option>
      <option>Elementary Executive Function enrichment</option>
      <option>Executive functioning / self-management</option>
      <option>Life management</option>
      <option>Social or communication skills</option>
      <option>Work performance</option>
      <option>Other</option>
    </select>
  </div>
  <div class="field">
    <label>Are you reaching out for yourself or someone else? *</label>
    <select disabled>
      <option value="">-None-</option>
      <option>Self</option>
      <option>Someone Else</option>
    </select>
  </div>
  <div class="field"><label>Tell Us More</label><textarea disabled></textarea></div>
  <div class="field">
    <label>How did you find us? *</label>
    <select disabled>
      <option value="">-None-</option>
      <option>Web Search</option>
      <option>Professional Referral</option>
      <option>Social media</option>
      <option>Friend/Colleague</option>
      <option>Other</option>
    </select>
  </div>
  <button class="btn btn-primary btn-block" type="button" disabled>{BTN}</button>
  <p class="form-reassure">{REASSURE}</p>
</div>"""


def cta(on_dark=False, href="#form-top"):
    color = "var(--on-dark-mute)" if on_dark else "var(--on-light-mute)"
    return f"""<div class="cta-stack">
  <a class="btn btn-primary" href="{href}">{BTN}</a>
  <p class="form-reassure" style="margin:0;text-align:left;color:{color}">{REASSURE}</p>
</div>"""


QUOTES = {
    "rania_uni": ("The coaches have been fantastic in helping him with time management, organization, and adjusting to the independence that comes with university life.", "Rania I., parent"),
    "rania_parent": ("As a parent, I was more involved in his schooling before, but now that he’s on his own, this support has been invaluable.", "Rania I., parent"),
    "christine": ("He is gaining confidence and is learning to regulate his emotions.", "Christine C., parent"),
    "emma": ("I have grown over time since starting here and I have become more confident in myself and my work and gained a better understanding of who I am personally and academically through this coaching center.", "Emma M., client"),
    "john_growth": ("We are extremely happy with the support our son has received… we have seen meaningful growth in his organization, time management, follow-through, and importantly his overall confidence.", "John D., parent"),
    "john_accountable": ("His coach has a unique ability to connect with students while holding them accountable in a supportive and respectful way.", "John D., parent"),
    "john_tools": ("He does not just teach strategies, rather he helps students understand how their brains work and gives them practical tools they can actually use in real life.", "John D., parent"),
    "connection": ("The connection my child has built with their coach is incredible. The personalized approach has made a huge difference in their ability to manage their time and responsibilities.", "Parent of a New Frontiers client"),
    "loves": ("Our son loves his coaches. They both appear to have excellent rapport with him and he’s genuinely excited to see them.", "Parent of a New Frontiers client"),
}

ARROW_L = '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M10 3L5 8l5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW_R = '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M6 3l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


STAR = '<svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M10 1.6l2.6 5.3 5.8.8-4.2 4.1 1 5.8L10 14.9l-5.2 2.7 1-5.8L1.6 7.7l5.8-.8z"/></svg>'
STARS = STAR * 5


def carousel(*keys):
    slides = "".join(f'<figure class="tcar-slide"><div class="stars" role="img" aria-label="5 out of 5 stars">{STARS}</div><blockquote>{QUOTES[k][0]}</blockquote><figcaption>— {QUOTES[k][1]}</figcaption></figure>' for k in keys)
    return f"""<div class="tcar" aria-roledescription="carousel">
  <div class="tcar-track">{slides}</div>
  <div class="tcar-nav"><div class="tcar-dots"></div><div class="tcar-arrows"><button class="tcar-btn prev" type="button" aria-label="Previous quote">{ARROW_L}</button><button class="tcar-btn next" type="button" aria-label="Next quote">{ARROW_R}</button></div></div>
</div>"""


CAROUSEL_JS = """<script>
document.querySelectorAll('.tcar').forEach(function(c){
  var t=c.querySelector('.tcar-track'),s=[].slice.call(t.children),d=c.querySelector('.tcar-dots'),i=0,timer;
  s.forEach(function(_,k){var b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Quote '+(k+1));b.onclick=function(){go(k)};d.appendChild(b)});
  function mark(){[].forEach.call(d.children,function(b,j){b.classList.toggle('on',j===i)})}
  function go(k){i=(k+s.length)%s.length;t.scrollTo({left:s[i].offsetLeft-s[0].offsetLeft,behavior:'smooth'});mark()}
  c.querySelector('.prev').onclick=function(){go(i-1)};
  c.querySelector('.next').onclick=function(){go(i+1)};
  t.addEventListener('scroll',function(){var k=Math.round(t.scrollLeft/t.clientWidth);if(k!==i){i=k;mark()}},{passive:true});
  function start(){timer=setInterval(function(){go(i+1)},4000)}
  c.addEventListener('mouseenter',function(){clearInterval(timer)});
  c.addEventListener('mouseleave',start);
  mark();start();
});
</script>"""


def page(filename, label, group, style, body):
    siblings = [p for p in PAGES if p[2] == group and p[0] != filename]
    links = " · ".join(f'<a href="{f}">{l.split("—")[0].split("·")[-1].strip()} {l.split("—")[1].strip()}</a>' for f, l, _ in siblings)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>{label}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="_shared.css?v={V}">
  <style>{style}</style>
</head>
<body>
  <div class="variant-bar">
    <span><strong>{label}</strong></span>
    <span><a href="index.html">All mocks</a> · {links}</span>
  </div>
  <header class="site-header">
    <div class="inner">
      <img class="logo" src="https://nfil.net/wp-content/uploads/2026/09/horizontal-logo-1.png" alt="New Frontiers">
      <div class="meta">
        <a href="tel:6465580085">646-558-0085</a>
        <span>info@nfil.net</span>
        <span>Worldwide · Virtual</span>
      </div>
    </div>
  </header>
{body}
  <footer class="footer-mini">
    <div class="wrap">
      <span>Virtual sessions worldwide · 646-558-0085 · info@nfil.net</span>
      <span>New Frontiers</span>
    </div>
  </footer>
{CAROUSEL_JS}
</body>
</html>
"""


HERO_SPLIT_CSS = """
.hero{padding:clamp(2.75rem,6vw,4.75rem) 0 clamp(3.5rem,7vw,6rem)}
.hero-grid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:clamp(28px,5vw,64px);align-items:start}
@media(max-width:900px){.hero-grid{grid-template-columns:minmax(0,1fr)}}
"""

PHOTO_CSS = """
.hero-photo{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);min-height:min(68vh,600px);background:var(--ink)}
.hero-photo .copy{color:var(--on-dark);padding:clamp(2.75rem,6vw,4.5rem) 28px;display:flex;align-items:center}
.hero-photo .copy .inner{max-width:500px;margin-left:auto;width:100%;padding-right:clamp(12px,3vw,40px)}
.hero-photo .media{background-size:cover;background-repeat:no-repeat;min-height:300px}
@media(max-width:900px){
  .hero-photo{grid-template-columns:1fr}
  .hero-photo .copy .inner{margin:0;padding:0;max-width:none}
  .hero-photo .media{min-height:260px;order:-1}
}
"""

FORM_BESIDE_CSS = """
.form-sect{padding:clamp(3rem,6vw,4.75rem) 0 clamp(4rem,8vw,6.5rem)}
.form-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,5vw,56px);align-items:start}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,5vw,64px);align-items:center}
.two.wide-r{grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr)}
@media(max-width:900px){.form-grid,.two,.two.wide-r{grid-template-columns:minmax(0,1fr)}}
"""

CENTER_HERO_CSS = ".hero{padding:clamp(3rem,7vw,5.5rem) 0 clamp(4rem,8vw,6.5rem)}"


# ---------- diagram builders ----------
ARROW_MARKER = """<defs><marker id="ah" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--blue)"/></marker></defs>"""


def graph_svg():
    return """<div class="diagram">
<svg viewBox="0 0 640 300" role="img" aria-label="Coach support goes down as student ownership goes up">
  <line class="g-axis" x1="40" y1="250" x2="620" y2="250"/>
  <path class="g-area" d="M40,230 C260,220 380,90 620,60 L620,250 L40,250 Z"/>
  <path class="g-support" d="M40,70 C240,80 380,200 620,230"/>
  <path class="g-own" d="M40,230 C260,220 380,90 620,60"/>
  <circle cx="318" cy="147" r="8" style="fill:var(--blue)"/>
  <circle cx="318" cy="147" r="16" style="fill:none;stroke:var(--blue);stroke-opacity:.35;stroke-width:2"/>
  <line x1="318" y1="128" x2="318" y2="84" style="stroke:var(--blue);stroke-width:1.5;stroke-dasharray:3 4"/>
  <text x="318" y="74" text-anchor="middle" class="t-strong">Plans their own week</text>
  <text x="40" y="54" class="t-label" style="fill:var(--blue)">Coach support</text>
  <text x="620" y="42" text-anchor="end" class="t-strong">Student ownership</text>
  <text x="40" y="278">First weeks</text>
  <text x="330" y="278" text-anchor="middle">Then</text>
  <text x="620" y="278" text-anchor="end">Over time</text>
</svg>
<p class="caption">Illustration — every student moves at their own pace.</p>
</div>"""


def cycle_svg(steps):
    cx = cy = 210
    r = 140

    def pt(deg):
        a = math.radians(deg)
        return cx + r * math.cos(a), cy + r * math.sin(a)

    angles = [-90, 0, 90, 180]
    arcs, nodes = [], []
    for i, a in enumerate(angles):
        x1, y1 = pt(a + 24)
        x2, y2 = pt(a + 66)
        arcs.append(f'<path class="cyc-arc" d="M{x1:.1f},{y1:.1f} A{r},{r} 0 0 1 {x2:.1f},{y2:.1f}" marker-end="url(#ah)"/>')
        nx, ny = pt(a)
        nodes.append(
            f'<circle class="cyc-node" cx="{nx:.1f}" cy="{ny:.1f}" r="56"/>'
            f'<text x="{nx:.1f}" y="{ny - 6:.1f}" text-anchor="middle" style="font-size:13px;font-weight:700;letter-spacing:.08em;fill:var(--blue-deep)">0{i + 1}</text>'
            f'<text x="{nx:.1f}" y="{ny + 16:.1f}" text-anchor="middle" class="t-label" style="fill:var(--on-light);font-size:16px">{steps[i]}</text>'
        )
    return f"""<div class="diagram" style="max-width:540px;margin:0 auto;width:100%">
<svg viewBox="0 0 420 420" role="img" aria-label="Session loop: {', '.join(steps)}">
  {ARROW_MARKER}
  <circle class="cyc-ring" cx="{cx}" cy="{cy}" r="{r}"/>
  {''.join(arcs)}
  {''.join(nodes)}
  <text x="{cx}" y="{cy - 2}" text-anchor="middle" class="t-strong" style="font-size:18px">Every session</text>
  <text x="{cx}" y="{cy + 22}" text-anchor="middle">then again next week</text>
</svg></div>"""


def venn_svg():
    return """<div class="diagram" style="max-width:760px;margin:0 auto">
<svg viewBox="0 0 640 290" role="img" aria-label="Tutoring, academic coaching and therapy overlap but do different jobs">
  <circle class="venn-side" cx="190" cy="145" r="120"/>
  <circle class="venn-side" cx="450" cy="145" r="120"/>
  <circle class="venn-mid" cx="320" cy="145" r="120"/>
  <text x="140" y="140" text-anchor="middle" class="t-strong">Tutoring</text>
  <text x="140" y="162" text-anchor="middle">What to learn</text>
  <text x="320" y="140" text-anchor="middle" class="t-strong" style="font-size:18px">Coaching</text>
  <text x="320" y="164" text-anchor="middle" style="fill:var(--on-light)">How to get it done</text>
  <text x="500" y="140" text-anchor="middle" class="t-strong">Therapy</text>
  <text x="500" y="162" text-anchor="middle">How you’re feeling</text>
</svg></div>"""


def hub(core_title, core_sub, items):
    cx, cy, rx, ry = 280, 220, 200, 170
    angles = [-90, -30, 30, 90, 150, 210]
    lines, pills = [], []
    for (title, sub), a in zip(items, angles):
        x = cx + rx * math.cos(math.radians(a))
        y = cy + ry * math.sin(math.radians(a))
        lines.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}"/>')
        pills.append(f'<div class="pill" style="left:{x / 560 * 100:.2f}%;top:{y / 440 * 100:.2f}%"><b>{title}</b><span>{sub}</span></div>')
    return f"""<div class="hub">
  <svg viewBox="0 0 560 440" preserveAspectRatio="none" aria-hidden="true">{''.join(lines)}</svg>
  <div class="core"><div><b>{core_title}</b><span>{core_sub}</span></div></div>
  {''.join(pills)}
</div>"""


def flow(nodes):
    lis = []
    for i, (h, p) in enumerate(nodes):
        cls = "node goal" if i == len(nodes) - 1 else "node"
        lis.append(f'<li class="{cls}"><h3>{h}</h3><p>{p}</p></li>')
    return f'<ol class="flow" style="--n:{len(nodes)}">{"".join(lis)}</ol>'


def shift(rows, left="Before", right="With a coach"):
    lis = "".join(f'<li><span class="from">{a}</span><span class="arr"></span><span class="to">{b}</span></li>' for a, b in rows)
    return f'<div class="shift-head"><span>{left}</span><span></span><span>{right}</span></div><ul class="shift">{lis}</ul>'


PLANNER = """<div class="ui-card">
  <div class="ui-top"><span class="dots"><i></i><i></i><i></i></span><span>This week’s plan</span><span class="tag">Example</span></div>
  <div class="pl-grid">
    <div class="pl-day"><b>Mon</b><span class="task c1 done">Map every due date</span><span class="task c2">History essay — first paragraph<em>Started in session</em></span></div>
    <div class="pl-day"><b>Tue</b><span class="task c3">Bio lab write-up · 40 min</span><span class="task">Practice 5–7</span></div>
    <div class="pl-day"><b>Wed</b><span class="task c2">Essay body · 45 min</span><span class="task c1">Quick check-in</span></div>
    <div class="pl-day"><b>Thu</b><span class="task c3">Chem review · 2 × 25 min</span></div>
    <div class="pl-day"><b>Fri</b><span class="task c2">Essay due</span><span class="task">Evening off</span></div>
  </div>
</div>"""

RECAP = """<div class="ui-card">
  <div class="ui-top"><span class="dots"><i></i><i></i><i></i></span><span>Session recap</span><span class="tag">Example</span></div>
  <div class="recap-body">
    <p class="rk">Win</p>
    <p>Started the essay in session — the hardest part is done.</p>
    <p class="rk">This week</p>
    <ul class="checks">
      <li class="on">Every due date in one plan</li>
      <li>Essay body, Wednesday · 45 min</li>
      <li>Chem review, two 25-minute blocks</li>
      <li>Email the teacher about the lab</li>
    </ul>
    <p class="rk">Next session</p>
    <p>Same time next week — bring the draft.</p>
  </div>
</div>"""

COLLEGE_CHECK = """<div class="ui-card">
  <div class="ui-top"><span class="dots"><i></i><i></i><i></i></span><span>Ready for college, on your own</span><span class="tag">Example</span></div>
  <div class="recap-body">
    <ul class="checks" style="gap:12px">
      <li class="on">Turn a syllabus into a semester plan</li>
      <li class="on">Email a professor — and ask for what you need</li>
      <li>Request accommodations without a parent doing it</li>
      <li>Study so it sticks, not just the night before</li>
    </ul>
  </div>
</div>"""

BREAKDOWN = """<div class="breakdown">
  <div class="bd-big"><span class="k">Due Friday</span><h3>Research paper</h3><p>Feels like one giant thing. So it doesn’t get started.</p></div>
  <div class="bd-arrow" aria-hidden="true"></div>
  <ol class="bd-steps">
    <li class="done"><span>Pick the question</span><em>Done in session</em></li>
    <li><span>Find three sources</span><em>30 min · Mon</em></li>
    <li><span>Outline in bullets</span><em>20 min · Tue</em></li>
    <li><span>Write the intro</span><em>25 min · Wed</em></li>
    <li><span>Draft the body</span><em>2 × 30 min · Thu</em></li>
    <li><span>Read it once, submit</span><em>15 min · Fri</em></li>
  </ol>
</div>"""

STREAK_WEEKS = [[1, 0, 1, 0, 0], [1, 1, 0, 1, 0], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]]
STREAK = '<div class="streak"><div class="row"><span></span>' + "".join(f'<span class="days">{d}</span>' for d in ["Mon", "Tue", "Wed", "Thu", "Fri"]) + "</div>" + "".join(
    f'<div class="row"><span>Week {i + 1}</span>' + "".join(f'<i class="{"on" if v else ""}"></i>' for v in w) + "</div>" for i, w in enumerate(STREAK_WEEKS)
) + "</div>"

SYSTEMS = """<div class="systems">
  <div class="sys-tools">
    <div class="sys-tool"><span class="sys-ic paper"></span>Paper planner</div>
    <div class="sys-tool"><span class="sys-ic sheet"></span>Spreadsheet</div>
    <div class="sys-tool"><span class="sys-ic cal"></span>Google Calendar</div>
  </div>
  <div class="bd-arrow" aria-hidden="true"></div>
  <div class="sys-out"><p class="k">Pick one</p><h3>Your system</h3><p>Built around how you already work, then practiced on real assignments until it sticks.</p></div>
</div>"""


def bottom(h2, sub, dark=True, proof_html=""):
    band = "bg-ink-glow band-ink" if dark else "band-white bg-dots"
    color = "#fff" if dark else "var(--on-light)"
    return f"""
  <section class="{band} sect" id="form-bottom">
    <div class="wrap bottom-grid">
      <div>
        <h2 style="color:{color}">{h2}</h2>
        <p class="lede">{sub}</p>
        {proof_html}
      </div>
      {form(dark=dark)}
    </div>
  </section>"""


WWH_ACADEMIC = """
<ul class="wwh">
  <li><b>What it is</b><span>One-on-one coaching for starting, planning, organizing and studying — done on real schoolwork.</span></li>
  <li><b>Who it’s for</b><span>High school and college students, and the parents supporting them.</span></li>
  <li><b>How it works</b><span>One or two video sessions a week, a written plan after each, and a quick check-in between when it helps.</span></li>
</ul>"""

JOURNEY = [
    ("Free 30-minute call", "Tell us what’s going on — as the student, or as someone supporting one."),
    ("Consultation &amp; coach match", "Goals and fit, then a coach paired to the student."),
    ("Weekly sessions", "On this week’s real work, by video, from anywhere."),
    ("Needing us less", "The plan becomes the student’s own."),
]


# ---------- Academic A: capable but stuck, form beside ----------
ACA_A = f"""
  <section class="bg-glow hero" id="form-top">
    <div class="wrap hero-grid">
      <div>
        <p class="eyebrow" style="color:var(--blue-deep)">Academic coaching · high school &amp; college</p>
        <h1>Academic coaching for capable students who keep getting stuck.</h1>
        <p class="beat on-light">Smart isn’t the problem. Starting, planning the week and keeping up is.</p>
        <p class="beat-support on-light">A coach works on the assignments actually in front of you — and helps build a system you’ll keep using.</p>
        {WWH_ACADEMIC}
      </div>
      <div>
        {form()}
        {carousel("rania_uni", "john_accountable", "emma")}
      </div>
    </div>
  </section>

  <section class="band-sky sect lift">
    <div class="wrap">
      <div class="sect-head"><h2>From stuck to steady</h2><p>What changes, week by week, when the work has a plan and someone in your corner.</p></div>
      {shift([
          ("Can do the work — can’t start it", "First step done in session, together"),
          ("Due dates scattered across portals", "One plan for the whole week"),
          ("Fine until the deadline, then all at once", "Small blocks spread across the week"),
          ("Parents as the reminder", "A plan the student runs"),
      ])}
    </div>
  </section>

  <section class="band-white sect">
    <div class="wrap">
      <div class="sect-head"><h2>One coach. Two people relieved.</h2><p>Whoever reaches out, the work happens between the coach and the student.</p></div>
      <div class="dual">
        <div class="dual-card" style="background:var(--sky-2)">
          <p class="k">If you’re the student</p>
          <h3>Help that isn’t your parents.</h3>
          <p>Goals set in your own words. A plan built around how you already work — paper, app or spreadsheet. Someone in your corner who isn’t grading you.</p>
        </div>
        <div class="dual-card" style="background:var(--sand);border-color:var(--sand-line)">
          <p class="k">If you’re the parent</p>
          <h3>Step back from being the reminder.</h3>
          <p>A coach holds the structure, so homework stops being a nightly negotiation — and the skills belong to them, not to you.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="band-white outer">
    <div class="inset band-sand sect">
      <div class="wrap">
        <div class="sect-head"><h2>How it goes</h2><p>The point isn’t more coaching. It’s needing less of it.</p></div>
        {flow(JOURNEY)}
      </div>
    </div>
  </section>
{bottom("Ready to get unstuck?", "Start with a free 30-minute discovery call. We’ll listen, answer questions and suggest a next step.")}
"""

# ---------- Academic B: photo hero + a week with a coach ----------
ACA_B = f"""
  <section class="hero-photo">
    <div class="copy">
      <div class="inner">
        <p class="eyebrow">Academic coaching · high school &amp; college</p>
        <h1>School shouldn’t feel this heavy.</h1>
        <p class="beat">You know what needs to get done. Starting it is the hard part.</p>
        <p class="beat-support">Academic coaching turns a crowded week into one plan — and gets the first step done together.</p>
        {cta(on_dark=True)}
      </div>
    </div>
    <div class="media" role="img" aria-label="Virtual coaching session on a laptop video call" style="background-image:url('https://nfil.net/wp-content/uploads/2026/10/best-online-coaching.jpg');background-position:38% center"></div>
  </section>

  <section class="band-sky form-sect" id="form-top">
    <div class="wrap form-grid">
      {form()}
      <div>
        <h2 style="margin-bottom:12px">For high school and college students — and the parents behind them.</h2>
        <ul class="ticks" style="margin-top:20px">
          <li>Can do the work, but can’t get it started</li>
          <li>Everything lands at the deadline, all at once</li>
          <li>Planners and apps that last about two days</li>
          <li>Grades that don’t match the effort — or the ability</li>
        </ul>
        {carousel("rania_parent", "connection", "christine")}
      </div>
    </div>
  </section>

  <section class="band-white bg-dots sect lift">
    <div class="wrap">
      <div class="sect-head"><h2>A week with a coach</h2><p>Not a daily app. Not another lecture about time management. This:</p></div>
      <div class="two wide-r" style="align-items:start">
        <ul class="week">
          <li><span class="d">In session</span><p>Every due date, from every class, in one plan.<span>Syllabi, portals and teacher emails — one place.</span></p></li>
          <li><span class="d">Same session</span><p>Start the thing that’s been avoided — together.</p></li>
          <li><span class="d">Right after</span><p>A written recap with the plan for the week.</p></li>
          <li><span class="d">Midweek</span><p>A quick check-in, if it helps.</p></li>
          <li><span class="d">Next session</span><p>What worked, what didn’t. Adjust.<span>Small steps, not a total overhaul.</span></p></li>
        </ul>
        <div class="stack">
          {PLANNER}
          <div class="stack-2">{RECAP}</div>
        </div>
      </div>
    </div>
  </section>

  <section class="bg-fade sect">
    <div class="wrap" style="text-align:center">
      <div class="sect-head" style="display:grid;justify-items:center"><h2>Not tutoring. Not therapy.</h2><p>Different jobs. Coaching works alongside both.</p></div>
      {venn_svg()}
    </div>
  </section>
{bottom("Take the first step", "A free 30-minute discovery call. No diagnosis needed. No commitment on the call.")}
"""

# ---------- Academic C: independence before college ----------
ACA_C = f"""
  <section class="bg-fade hero">
    <div class="wrap" style="max-width:860px;text-align:center">
      <p class="eyebrow">Academic coaching · high school &amp; college</p>
      <h1 style="max-width:20ch;margin:0 auto">Academic coaching that builds independence — before college asks for it.</h1>
      <p class="beat on-light" style="margin:22px auto 0">College is coming. The reminders aren’t coming with you.</p>
      <p class="beat-support on-light" style="margin:14px auto 0">Coaching builds the habits that make school work without someone checking: planning, starting, and speaking up for yourself.</p>
      <div style="display:flex;justify-content:center">{cta()}</div>
    </div>
  </section>

  <section class="band-white bg-dots form-sect lift" id="form-top">
    <div class="wrap form-grid">
      <div>
        <h2 style="margin-bottom:18px">Sound familiar?</h2>
        <div class="chips">
          <span class="chip">Can do the work — can’t start it</span>
          <span class="chip">Fine until the deadline</span>
          <span class="chip">Planner set up, abandoned by Thursday</span>
          <span class="chip">Homework has become an argument</span>
          <span class="chip">Great at cramming, burned out by finals</span>
          <span class="chip">Good grades — someone else does the organizing</span>
        </div>
        <p class="lede" style="margin-top:26px">None of that is laziness. These are skills, and skills can be practiced.</p>
        {carousel("christine", "rania_uni", "emma")}
      </div>
      {form()}
    </div>
  </section>

  <section class="bg-grid-dark band-dark sect lift">
    <div class="wrap">
      <div class="sect-head"><h2 style="color:#fff">The goal is needing us less.</h2><p>Goals are set with the student, in their own words. Responsibility moves to them as the system sticks.</p></div>
      {graph_svg()}
      <div class="ramp" style="margin-top:28px">
        <div class="ramp-step"><div class="bar"><i style="width:33%"></i></div><p class="k">First weeks</p><h3>Plan it together</h3><p>Coach and student map the week and start the hard tasks side by side.</p></div>
        <div class="ramp-step"><div class="bar"><i style="width:66%"></i></div><p class="k">Then</p><h3>You plan, we check</h3><p>The student builds the plan. The coach asks the questions.</p></div>
        <div class="ramp-step"><div class="bar"><i style="width:100%"></i></div><p class="k">Over time</p><h3>You run it</h3><p>Planning, prioritizing and follow-through become yours.</p></div>
      </div>
    </div>
  </section>

  <section class="band-paper outer" style="background:var(--paper)">
    <div class="inset band-sand sect">
      <div class="wrap two">
        <div>
          <h2>Skills college actually asks for</h2>
          <p class="lede">Nobody checks your planner in college. These are the habits coaching practices before that day comes.</p>
        </div>
        {COLLEGE_CHECK}
      </div>
    </div>
  </section>
{bottom("Start before the pressure does.", "A free 30-minute discovery call — for the student, or for someone supporting one.")}
"""

# ---------- Student A: plain definition, form beside (search intent) ----------
STU_A = f"""
  <section class="bg-grid-dark band-dark hero" id="form-top">
    <div class="wrap hero-grid">
      <div>
        <p class="eyebrow">High school &amp; college · virtual</p>
        <h1>Executive Function Coaching for Students</h1>
        <p class="beat">Stuck isn’t lazy. Starting, planning and follow-through are skills — and skills can be built.</p>
        <p class="beat-support">Executive function is how the brain manages getting things done. Coaching strengthens it on real schoolwork, one week at a time.</p>
        {WWH_ACADEMIC.replace('starting, planning, organizing and studying', 'executive function skills')}
      </div>
      <div>
        {form(dark=True)}
        {carousel("john_growth", "connection", "emma")}
      </div>
    </div>
  </section>

  <section class="band-white sect lift">
    <div class="wrap">
      <div class="sect-head" style="text-align:center;display:grid;justify-items:center"><h2>What executive function covers</h2><p>We start with whatever is getting in the way right now — one thing, not everything.</p></div>
      {hub("Executive function", "How you get things done", [
          ("Getting started", "A first step small enough to take"),
          ("Planning the week", "Every deadline in one plan"),
          ("Time", "How long things really take"),
          ("Studying that works", "Not rereading the night before"),
          ("Speaking up", "Teachers, professors, accommodations"),
          ("The life around school", "Sleep, mornings, phone"),
      ])}
    </div>
  </section>

  <section class="band-sky sect">
    <div class="wrap">
      <div class="compare">
        <div class="compare-card yes" style="background:#fff"><h3>Coaching is</h3><ul class="ticks" style="margin-top:6px"><li>One-on-one, on your real schoolwork</li><li>Goals set in your own words</li><li>A written plan after every session</li></ul></div>
        <div class="compare-card" style="background:transparent;border-style:dashed;border-color:#C9D3DE"><h3>Coaching isn’t</h3><ul class="ticks" style="margin-top:6px"><li>Tutoring — it works alongside it</li><li>Therapy — it works alongside it</li><li>A daily check-in app</li></ul></div>
      </div>
    </div>
  </section>

  <section class="band-sky outer" style="padding-top:0">
    <div class="inset band-white sect">
      <div class="wrap">
        <div class="sect-head"><h2>How it goes</h2><p>From first call to running it yourself.</p></div>
        {flow(JOURNEY)}
      </div>
    </div>
  </section>
{bottom("Find out if coaching fits.", "A free 30-minute discovery call — for you, or for someone you’re supporting.")}
"""

# ---------- Student B: systems built around you ----------
STU_B = f"""
  <section class="bg-glow hero">
    <div class="wrap hero-grid" style="align-items:center">
      <div>
        <p class="eyebrow" style="color:var(--blue-deep)">Executive function coaching · students</p>
        <h1 style="max-width:18ch">Executive function coaching for students, built around how you already work.</h1>
        <p class="beat on-light">Tried planners, apps and alarms — and none of them stuck? That’s not a character flaw.</p>
        <p class="beat-support on-light">We build one system that fits you, and practice it on this week’s real work.</p>
        {cta()}
      </div>
      {SYSTEMS}
    </div>
  </section>

  <section class="band-sky form-sect lift" id="form-top">
    <div class="wrap form-grid">
      <div>
        <h2 style="margin-bottom:18px">Who it’s for</h2>
        <ul class="ticks">
          <li>High school and college students who can do the work but struggle to start, plan or keep up</li>
          <li>Students heading to college who want to manage on their own</li>
          <li>Parents ready to stop being the reminder</li>
        </ul>
        {carousel("connection", "john_tools", "christine")}
      </div>
      {form()}
    </div>
  </section>

  <section class="band-sand sect lift">
    <div class="wrap">
      <div class="sect-head"><h2>Big task, small steps</h2><p>The overwhelming thing gets broken down — and the first piece gets done in session.</p></div>
      {BREAKDOWN}
    </div>
  </section>

  <section class="bg-grid-dark band-dark sect">
    <div class="wrap two">
      <div>
        <h2 style="color:#fff;margin-bottom:12px">Small wins add up.</h2>
        <p class="lede">Progress counts even when it’s small. A three-item morning checklist. One class first. Five more minutes. Then build.</p>
        <div style="margin-top:28px">{STREAK}</div>
        <p class="lede" style="font-size:.85rem;font-style:italic;margin-top:12px">Illustration: days the plan got used without a reminder.</p>
      </div>
      <div class="facts" style="grid-template-columns:1fr 1fr;row-gap:28px">
        <div class="fact"><b>1–2 sessions a week</b><span>By video, from anywhere.</span></div>
        <div class="fact"><b>Your real work</b><span>This week’s assignments, not worksheets.</span></div>
        <div class="fact"><b>A written plan</b><span>Recap after every session.</span></div>
        <div class="fact"><b>Your goals</b><span>Set with you, in your own words.</span></div>
      </div>
    </div>
  </section>
{bottom("Ready to get unstuck?", "Start with a free 30-minute discovery call. No diagnosis needed.", dark=False)}
"""

# ---------- Student C: inside a session, photo ----------
STU_C = f"""
  <section class="hero-photo">
    <div class="copy">
      <div class="inner">
        <p class="eyebrow">Executive function coaching · students</p>
        <h1>Executive function coaching that starts with this week.</h1>
        <p class="beat">Not more advice. Real help with the assignments in front of you.</p>
        <p class="beat-support">Every session: what got done, what’s stuck, a plan — and the first step, together.</p>
        {cta(on_dark=True)}
      </div>
    </div>
    <div class="media" role="img" aria-label="Student waving to her coach on a video call" style="background-image:url('https://nfil.net/wp-content/uploads/2022/05/virtual-coaching.png');background-size:auto 114%;background-position:62% 50%;background-color:#EEF0EF"></div>
  </section>

  <section class="band-white bg-dots sect">
    <div class="wrap two">
      {cycle_svg(["Review", "Assess", "Strategize", "Plan"])}
      <div>
        <h2 style="margin-bottom:22px">Inside a session</h2>
        <ul class="week">
          <li><span class="d">01 Review</span><p>What got done.<span>Wins first. Small ones count.</span></p></li>
          <li><span class="d">02 Assess</span><p>What’s stuck.<span>What’s due, what’s been avoided, what’s next.</span></p></li>
          <li><span class="d">03 Strategize</span><p>Break it down.<span>Then start the hard part together, in session.</span></p></li>
          <li><span class="d">04 Plan</span><p>Write the week.<span>A plan with real times — sent right after.</span></p></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="band-sky form-sect lift" id="form-top">
    <div class="wrap form-grid">
      {form()}
      <div>
        <h2 style="margin-bottom:12px">What you leave every session with</h2>
        <p class="lede" style="margin-bottom:22px">A written recap and a plan for the week — so it lives on paper, not in anyone’s memory.</p>
        {RECAP}
      </div>
    </div>
  </section>

  <section class="band-sand sect lift">
    <div class="wrap">
      <div class="sect-head"><h2>Shame doesn’t build habits. Small wins do.</h2><p>Falling behind can feel personal — for you, or for someone you’re supporting. Coaching swaps the guilt for a next step.</p></div>
      {shift([
          ("“I’m so behind.”", "“What’s the one next step?”"),
          ("Another plan that didn’t work", "An experiment we adjust next week"),
          ("All or nothing", "Five more minutes counts"),
      ], left="The old story", right="In coaching")}
      {carousel("loves", "john_accountable", "rania_parent")}
    </div>
  </section>

  <section class="band-white sect">
    <div class="wrap facts">
      <div class="fact"><b>High school &amp; college</b><span>And the parents supporting them.</span></div>
      <div class="fact"><b>1–2 sessions a week</b><span>By video, plus a check-in between when it helps.</span></div>
      <div class="fact"><b>Not tutoring or therapy</b><span>Works alongside both.</span></div>
      <div class="fact"><b>Built to fade out</b><span>Responsibility moves to the student over time.</span></div>
    </div>
  </section>
{bottom("Start with one week.", "A free 30-minute discovery call — tell us what’s going on, and we’ll suggest a next step.")}
"""

def icon(d, size=18):
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'


IC_MIC = icon('<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>')
IC_CAM = icon('<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/>')
IC_SHARE = icon('<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M12 14V8M9 10.5L12 8l3 2.5M8 21h8"/>')
IC_CHAT = icon('<path d="M4 5h16v11H8l-4 4z"/>')
IC_LAPTOP = icon('<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>', 22)
IC_SPOT = icon('<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>', 22)
IC_BOOK = icon('<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M9 7h6"/>', 22)

VIDEO_CALL = f"""<div class="vc" role="img" aria-label="Example of a virtual coaching session: shared weekly plan, coach and student on video">
  <div class="vc-top"><span class="live"></span><span>Weekly coaching session</span><span class="time">24:10</span></div>
  <div class="vc-body">
    <div class="vc-share">
      <div class="bar"><i></i>Shared screen · This week’s plan</div>
      <div class="pl-grid">
        <div class="pl-day"><b>Mon</b><span class="task c2">History essay — first paragraph<em>Starting now</em></span></div>
        <div class="pl-day"><b>Tue</b><span class="task c3">Bio lab · 40 min</span></div>
        <div class="pl-day"><b>Wed</b><span class="task c2">Essay body · 45 min</span></div>
      </div>
      <div class="vc-chat">
        <div class="vc-msg"><b>Coach</b>Let’s do the first paragraph together — just ten minutes.</div>
        <div class="vc-msg me"><b>You</b>Ok. Opening the doc now.</div>
      </div>
    </div>
    <div class="vc-tiles">
      <div class="vc-tile speaking"><div class="av" style="--c:#D8B497;--s:#4F6E96"></div><span class="nm">Coach</span><span class="wave"><i style="height:6px"></i><i style="height:12px"></i><i style="height:8px"></i><i style="height:14px"></i></span></div>
      <div class="vc-tile you"><div class="av" style="--c:#B98D6E;--s:#6C8F6A"></div><span class="nm">You</span></div>
    </div>
  </div>
  <div class="vc-ctrl"><span>{IC_MIC}</span><span>{IC_CAM}</span><span class="on">{IC_SHARE}</span><span>{IC_CHAT}</span><span class="end">Leave</span></div>
</div>"""

SCRUB_PARTS = [
    (18, "Check in", "What got done", "Wins first — small ones count."),
    (24, "Open it up", "Screens shared", "Your portal, your planner, what’s due."),
    (34, "Start it", "The hard part, together", "The avoided task gets its first step — live."),
    (24, "Plan it", "Write the week", "Real times, in the tool you already use."),
]
SCRUB = (
    '<div class="scrub"><div class="scrub-ends"><span>Start of the call</span><span>End of the call</span></div>'
    '<div class="scrub-bar">' + "".join(f'<i class="{"played" if n < 2 else ""}" style="flex:{w}"></i>' for n, (w, *_ ) in enumerate(SCRUB_PARTS)) + '<span class="scrub-head" style="left:42%"></span></div>'
    '<div class="scrub-ch">' + "".join(f'<div style="flex:{w}"><p class="k">{k}</p><h3>{h}</h3><p>{p}</p></div>' for w, k, h, p in SCRUB_PARTS) + "</div></div>"
)

STU_D = f"""
  <section class="bg-glow hero">
    <div class="wrap hero-grid vid" style="align-items:center">
      <div>
        <p class="eyebrow" style="color:var(--blue-deep)">Virtual · high school &amp; college</p>
        <h1>Executive Function Coaching for Students — from wherever you are.</h1>
        <p class="beat on-light">You don’t have to figure it out alone at your desk.</p>
        <p class="beat-support on-light">One-on-one video sessions on this week’s real assignments: screens shared, the week planned, and the first step started together.</p>
        {cta()}
      </div>
      <div class="hero-video">
        <video src="media/virtual-session-v2.mp4" poster="media/virtual-session-v2-poster.jpg" autoplay muted loop playsinline aria-label="A student at home on a video coaching session, taking notes while her coach talks on screen"></video>
      </div>
    </div>
  </section>

  <section class="band-sky form-sect lift" id="form-top">
    <div class="wrap form-grid">
      <div>
        <h2 style="margin-bottom:18px">Why virtual works</h2>
        <ul class="ticks">
          <li>Sessions fit around school, practice and everything else — no commute</li>
          <li>Your real setup on screen: your portal, your planner, your assignments</li>
          <li>The same coach whether you’re at home, in a dorm, or abroad</li>
          <li>For students who can do the work but struggle to start, plan or keep up — and the parents supporting them</li>
        </ul>
        {carousel("connection", "rania_uni", "emma")}
      </div>
      {form()}
    </div>
  </section>

  <section class="band-white sect">
    <div class="wrap">
      <div class="sect-head"><h2>What happens on the call</h2><p>The same rhythm every session, so it turns into a habit.</p></div>
      {SCRUB}
      <div class="after">
        <div><span class="k">After the call</span><p>A written recap with the plan for the week.</p></div>
        <div><span class="k">Midweek</span><p>A quick check-in, if it helps. Not a daily app.</p></div>
      </div>
    </div>
  </section>

  <section class="band-light sect">
    <div class="wrap">
      <div class="sect-head"><h2>Same coach. Two people relieved.</h2></div>
      <div class="dual">
        <div class="dual-card" style="background:var(--sky-2)">
          <p class="k">If you’re the student</p>
          <h3>Just open the laptop.</h3>
          <p>Goals in your own words, from your own desk. Someone in your corner who isn’t a parent or a teacher.</p>
        </div>
        <div class="dual-card" style="background:var(--sand);border-color:var(--sand-line)">
          <p class="k">If you’re the parent</p>
          <h3>No driving. No nightly reminders.</h3>
          <p>The coach holds the structure, so you can step back — and home can feel like home again.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="bg-grid-dark band-dark sect">
    <div class="wrap">
      <div class="sect-head"><h2 style="color:#fff">All you need</h2><p>Not tutoring, not therapy — coaching that works alongside both.</p></div>
      <div class="kit">
        <div><span class="ic">{IC_LAPTOP}</span><div><b>A laptop or tablet</b><span>With a camera and mic.</span></div></div>
        <div><span class="ic">{IC_SPOT}</span><div><b>A quiet-ish spot</b><span>Bedroom, dorm, library room.</span></div></div>
        <div><span class="ic">{IC_BOOK}</span><div><b>This week’s work</b><span>We start with what’s actually due.</span></div></div>
      </div>
    </div>
  </section>
{bottom("Start with one call.", "A free 30-minute discovery call — for you, or for someone you’re supporting. On video, of course.")}
"""

VID_CSS = """
.hero-grid.vid{grid-template-columns:minmax(0,.82fr) minmax(0,1.3fr);gap:clamp(28px,4vw,56px)}
.hero-grid.vid h1{font-size:clamp(2rem,3.5vw,2.85rem);max-width:none}
.hero-grid.vid .beat{font-size:clamp(1.1rem,1.8vw,1.3rem)}
@media(min-width:1200px){.hero-grid.vid .hero-video{margin-right:-90px}}
@media(max-width:900px){.hero-grid.vid{grid-template-columns:minmax(0,1fr)}}
"""

STACK_CSS = """
.stack{position:relative}
.stack-2{margin:-28px 0 0 auto;width:78%;position:relative}
@media(max-width:900px){.stack-2{width:100%;margin:16px 0 0}}
"""

BODIES = {
    "academic-a-split.html": (HERO_SPLIT_CSS, ACA_A),
    "academic-b-photo.html": (PHOTO_CSS + FORM_BESIDE_CSS + STACK_CSS, ACA_B),
    "academic-c-relief.html": (FORM_BESIDE_CSS + CENTER_HERO_CSS, ACA_C),
    "student-a-define.html": (HERO_SPLIT_CSS, STU_A),
    "student-b-skills.html": (HERO_SPLIT_CSS + FORM_BESIDE_CSS, STU_B),
    "student-c-process.html": (PHOTO_CSS + FORM_BESIDE_CSS, STU_C),
    "student-d-video.html": (HERO_SPLIT_CSS + FORM_BESIDE_CSS + VID_CSS, STU_D),
}

for fname, label, group in PAGES:
    style, body = BODIES[fname]
    (OUT / fname).write_text(page(fname, label, group, style, body))
    print("wrote", fname)
