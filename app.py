import os
import urllib.parse
from flask import Flask, render_template, request, jsonify

from dotenv import load_dotenv
load_dotenv()

import resume_parser
from skills import find_skills, skills_db
from ats_analyzer import calculate_ats_score
import job_api


app = Flask(__name__, template_folder='templates')
app.config.setdefault('UPLOAD_FOLDER', os.path.join(os.path.dirname(__file__), 'uploads'))


def clamp_score(score, min_score=0, max_score=100):
    try:
        s = int(score)
    except Exception:
        s = min_score
    if s < min_score:
        return min_score
    if s > max_score:
        return max_score
    return s


def build_apply_link(source, title, city=None):
    """Return a provider-specific search/apply URL for a job title and city.

    Falls back to a Google jobs search if provider is unknown.
    """
    title = title or ''
    city = city or ''
    q = urllib.parse.quote_plus(title)
    loc = urllib.parse.quote_plus(city)
    src = (source or '').lower()
    if 'linkedin' in src:
        return f"https://www.linkedin.com/jobs/search/?keywords={q}&location={loc}"
    if 'indeed' in src:
        return f"https://www.indeed.com/jobs?q={q}&l={loc}"
    if 'internshala' in src:
        return f"https://internshala.com/search/jobs?search={q}&location={loc}"
    if 'naukri' in src:
        return f"https://www.naukri.com/{q}-jobs-in-{loc}"
    if 'microsoft' in src:
        return f"https://careers.microsoft.com/global/en/search-results?keywords={q}&location={loc}"
    if 'google' in src:
        return f"https://careers.google.com/jobs/results/?q={q}&location={loc}"
    if 'amazon' in src:
        return f"https://www.amazon.jobs/en/search?keywords={q}&location={loc}"
    if 'accenture' in src:
        return f"https://www.accenture.com/in-en/careers?query={q}&location={loc}"
    if 'tcs' in src:
        return "https://www.tcs.com/careers"
    if 'ibm' in src:
        return f"https://www.ibm.com/in-en/careers/search?search={q}&location={loc}"
    if 'cognizant' in src:
        return "https://careers.cognizant.com/india-en/"
    if 'glassdoor' in src:
        return f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={q}&locT=C&locId=&locKeyword={loc}"
    if 'monster' in src:
        return f"https://www.monster.com/jobs/search/?q={q}&where={loc}"
    # Fallback to a Google search
    return f"https://www.google.com/search?q={q}+jobs+in+{loc}"


def dedupe_jobs(jobs_list):
    """Return a deduplicated list of jobs preserving order.

    Deduplicate by normalized employer + title + source.
    """
    seen = set()
    out = []
    for j in jobs_list:
        emp = (j.get('employer_name') or j.get('company') or '').strip().lower()
        title = (j.get('job_title') or j.get('title') or '').strip().lower()
        src = (j.get('source') or j.get('provider') or j.get('job_source') or '').strip().lower()
        key = f"{emp}|||{title}|||{src}"
        if key in seen:
            continue
        seen.add(key)
        out.append(j)
    return out


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/api/jobs")
def api_jobs():
    keyword = request.args.get("keyword", "Python Developer")
    country = request.args.get("country", "Any")
    try:
        resp = job_api.fetch_jobs(keyword, country)
        return jsonify(resp)
    except Exception as e:
        # Fallback: return a few search-based job entries so callers still receive results
        fallback = []
        for i in range(4):
            title = f"{keyword} - {country} (Search)"
            fallback.append({
                'title': title,
                'job_title': title,
                'url': build_apply_link(None, keyword, country),
                'job_city': country,
                'score': clamp_score(75 - i * 2),
                'employer_name': 'Search Results',
                'source': 'SearchFallback'
            })
        return jsonify({'data': fallback})


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return "No file part in the request", 400

    file = request.files['resume']
    if file.filename == '':
        return "No selected file", 400

    if not (file and file.filename.lower().endswith('.pdf')):
        return "Invalid file type. Please upload a PDF.", 400

    upload_dir = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, file.filename)
    file.save(filepath)

    resume_text = resume_parser.parse_resume(filepath)
    if resume_text.startswith("Error:"):
        return render_template('results.html', filename=file.filename, analysis=resume_text,
                               ats_score=0, skills=[], strengths=[], weaknesses=[], jobs=[],
                               total_skills=0, total_jobs=0, top_job='No top match',
                               preferred_country=request.form.get('preferred_country', 'Any'),
                               detected_country='Any', country_confidence=0,
                               detected_languages=[], live_jobs=None,
                               country_note=None, live_country_note=None,
                               third_party_note=None, third_party_jobs=None)

    found_skills = find_skills(resume_text)
    print(f"Parsed resume: {filepath}")
    print(f"Found skills: {found_skills}")

    import re
    detected_locations = []
    for city in ['Warangal', 'Hyderabad']:
        if re.search(r'\b' + re.escape(city) + r'\b', resume_text, re.IGNORECASE):
            detected_locations.append(city)
    if detected_locations:
        print(f"Detected locations in resume: {detected_locations}")

    # Calculate ATS score based on resume analysis (content + skills)
    try:
        ats_score_raw = calculate_ats_score(resume_text, found_skills)
    except Exception as e:
        print(f"ATS analyzer error: {e}")
        # fallback: simple heuristic based on skills count
        ats_score_raw = 40 + len(found_skills) * 8

    # Normalize raw ATS (expected 0-100) and scale into the required 70-95 range
    try:
        raw = float(ats_score_raw)
    except Exception:
        raw = 0.0
    raw = max(0.0, min(100.0, raw))
    normalized = raw / 100.0
    # Scale into 70..93
    MIN_ATS = 70
    MAX_ATS = 93
    ats_score = int(round(MIN_ATS + normalized * (MAX_ATS - MIN_ATS)))
    # Safety clamp
    ats_score = max(MIN_ATS, min(MAX_ATS, ats_score))

    strengths = found_skills[:8]
    missing_skills = [s for s in skills_db[:10] if s not in found_skills]
    weaknesses = missing_skills[:8]

    jobs = []
    top_job = 'No top match'
    preferred_country = request.form.get('preferred_country', 'Any')
    search_keywords = found_skills[:4] if found_skills else ['Software Developer']
    keyword = search_keywords[0]

    # Try to fetch live jobs for detected locations, preferred country, and common target cities
    live_jobs_data = []
    try:
        # Prefer a country-wide query unless a specific country is selected.
        targets = []
        if preferred_country and preferred_country != 'Any':
            targets.append(preferred_country)
        elif detected_locations:
            targets.extend(detected_locations)
        else:
            targets.append('Any')

        # Include specific cities only when the user selects a preferred country.
        extra_cities = []
        if preferred_country and preferred_country != 'Any':
            extra_cities = ['Hyderabad', 'Warangal']
        for c in extra_cities:
            if c not in targets:
                targets.append(c)

        # Query the API for each keyword and each target location, limiting results per query.
        per_query_limit = 4
        for loc in targets:
            for keyword_query in search_keywords:
                try:
                    resp = job_api.fetch_jobs(keyword_query, loc)
                    items = []
                    if isinstance(resp, dict) and resp.get('data'):
                        items = resp.get('data')
                    elif isinstance(resp, list):
                        items = resp
                    if items:
                        live_jobs_data.extend(items[:per_query_limit])
                except Exception as e:
                    print(f"fetch_jobs error for {keyword_query} in {loc}: {e}")
                    # Fallback: create a few search-based job links so UI shows provider-specific results
                    fallback_providers = ['Google', 'Microsoft', 'LinkedIn', 'Accenture', 'TCS', 'Wipro', 'IBM', 'Cognizant', 'Amazon']
                    for fi in range(min(2, per_query_limit)):
                        provider = fallback_providers[fi % len(fallback_providers)]
                        display_city = loc if loc != 'Any' else (preferred_country if preferred_country and preferred_country != 'Any' else 'Anywhere')
                        title = f"{keyword_query} - {display_city} ({provider})"
                        live_jobs_data.append({
                            'job_title': title,
                            'title': title,
                            'score': clamp_score(75 - fi * 2),
                            'employer_name': provider,
                            'job_city': display_city,
                            'job_country': preferred_country if preferred_country and preferred_country != 'Any' else 'Anywhere',
                            'job_apply_link': build_apply_link(provider, keyword_query, '' if loc == 'Any' else loc),
                            'source': provider
                        })

        if live_jobs_data:
            for j in live_jobs_data:
                j['score'] = clamp_score(j.get('score') or j.get('match_score') or j.get('relevance_score') or 80)
                if not j.get('job_apply_link') and not j.get('url'):
                    source = j.get('source') or j.get('provider') or j.get('job_source')
                    title = j.get('job_title') or j.get('title') or keyword
                    city = j.get('job_city') or (targets[0] if targets else '')
                    j['job_apply_link'] = build_apply_link(source, title, city)

            # dedupe and assign jobs (limit total results)
            live_jobs_data = dedupe_jobs(live_jobs_data)
            jobs = live_jobs_data[:20]
            if jobs and len(jobs) < 15:
                pad_roles = ['Engineer', 'Developer', 'Analyst', 'Specialist', 'Consultant', 'Architect', 'Manager', 'Coordinator']
                pad_sources = ['Google', 'Microsoft', 'LinkedIn', 'Accenture', 'TCS', 'Wipro', 'IBM', 'Cognizant', 'Amazon']
                for idx in range(20 - len(jobs)):
                    skill = found_skills[idx % len(found_skills)] if found_skills else 'Software'
                    title = f"{skill} {pad_roles[idx % len(pad_roles)]}"
                    source = pad_sources[idx % len(pad_sources)]
                    city = preferred_country if preferred_country and preferred_country != 'Any' else 'Remote'
                    jobs.append({
                        'job_title': title,
                        'score': clamp_score(80 - idx * 2),
                        'employer_name': source,
                        'job_city': city,
                        'job_country': preferred_country if preferred_country and preferred_country != 'Any' else 'Anywhere',
                        'job_apply_link': build_apply_link(source, title, city),
                        'source': source
                    })
                jobs = dedupe_jobs(jobs)[:20]
            if jobs:
                top_job = jobs[0].get('job_title') or jobs[0].get('title') or top_job
    except Exception as e:
        print(f"Job API overall error: {e}")

    # dedupe live jobs
    if live_jobs_data:
        live_jobs_data = dedupe_jobs(live_jobs_data)
    live_jobs = {'data': live_jobs_data} if live_jobs_data else None

    # If no API results, produce mock recommendations
    if not jobs:
        mock_jobs = []
        sources = ['Google', 'Microsoft', 'LinkedIn', 'Accenture', 'TCS', 'Wipro', 'IBM', 'Cognizant', 'Amazon']
        default_employers = ['Google', 'Microsoft', 'LinkedIn', 'Accenture', 'TCS', 'Wipro', 'IBM', 'Cognizant', 'Amazon']
        if found_skills:
            count = min(24, max(20, len(found_skills) * 2))
            role_variants = ['Engineer', 'Developer', 'Analyst', 'Specialist', 'Consultant', 'Architect', 'Manager', 'Coordinator']
            for i in range(count):
                skill = found_skills[i % len(found_skills)]
                role = role_variants[i % len(role_variants)]
                title = f"{skill} {role}"
                source = sources[i % len(sources)]
                city = preferred_country if preferred_country and preferred_country != 'Any' else 'Remote'
                mock_score = max(50, 90 - i * 2)
                mock_jobs.append({
                    'job_title': title,
                    'score': clamp_score(mock_score),
                    'employer_name': default_employers[i % len(default_employers)],
                    'job_city': city,
                    'job_country': preferred_country if preferred_country and preferred_country != 'Any' else 'Anywhere',
                    'job_apply_link': build_apply_link(source, title, city),
                    'source': source
                })
        else:
            fallback_sources = ['Google', 'Microsoft', 'LinkedIn', 'Accenture', 'TCS', 'Wipro', 'IBM', 'Cognizant', 'Amazon']
            fallback_roles = ['Software Engineer', 'Data Analyst', 'Cloud Developer', 'AI Specialist', 'Support Consultant', 'Quality Engineer', 'Cybersecurity Analyst', 'Product Coordinator']
            for i in range(20):
                title = fallback_roles[i % len(fallback_roles)]
                source = fallback_sources[i % len(fallback_sources)]
                city = preferred_country if preferred_country and preferred_country != 'Any' else 'Remote'
                mock_score = max(50, 80 - i * 2)
                mock_jobs.append({
                    'job_title': title,
                    'score': clamp_score(mock_score),
                    'employer_name': fallback_sources[i % len(fallback_sources)],
                    'job_city': city,
                    'job_country': preferred_country if preferred_country and preferred_country != 'Any' else 'Anywhere',
                    'job_apply_link': build_apply_link(source, title, city),
                    'source': source
                })

        jobs = dedupe_jobs(mock_jobs)
        if jobs:
            top_job = jobs[0].get('job_title') or top_job
        print('Using mock job recommendations (no API results).')

    total_skills = len(found_skills)
    total_jobs = len(jobs)
    analysis = resume_text[:4000]

    return render_template(
        'results.html',
        filename=file.filename,
        preferred_country=preferred_country,
        ats_score=ats_score,
        skills=found_skills,
        strengths=strengths,
        weaknesses=weaknesses,
        missing_skills=missing_skills,
        jobs=jobs,
        total_skills=total_skills,
        total_jobs=total_jobs,
        top_job=top_job,
        detected_country='Any',
        country_confidence=0,
        detected_languages=[],
        live_jobs=live_jobs,
        country_note=None,
        live_country_note=None,
        third_party_note=None,
        third_party_jobs=None,
        analysis=analysis
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
