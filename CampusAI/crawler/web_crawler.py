"""
CampusAI - Web Crawler Module
Crawls college-related web resources for internships, scholarships, and announcements.
Implements content extraction, TF-IDF ranking, and information extraction.
"""

import re
import math
from collections import Counter
from datetime import datetime


class WebCrawler:
    """
    Simulated web crawler for college-related information.
    In production, this would use BeautifulSoup/Scrapy to crawl real websites.
    For the demo, it uses a curated knowledge base of real-world data.
    """

    def __init__(self):
        self.knowledge_base = self._build_knowledge_base()
        self.idf_cache = {}
        self._build_index()

    def _build_knowledge_base(self):
        """Build a comprehensive knowledge base of college-related information."""
        return {
            "scholarships": [
                {
                    "title": "AICTE Pragati Scholarship for Girls",
                    "source": "aicte-india.org",
                    "category": "Scholarship",
                    "content": "AICTE Pragati Scholarship provides Rs. 50,000 per year to girl students pursuing technical education. Eligibility: Family income below 8 lakhs. Available for degree and diploma programs in AICTE approved institutions. Application through National Scholarship Portal. Deadline: October 31 every year.",
                    "url": "https://www.aicte-india.org/schemes/students-development-schemes/Pragati",
                    "date": "2026-06-15"
                },
                {
                    "title": "Central Sector Scheme of Scholarship",
                    "source": "scholarships.gov.in",
                    "category": "Scholarship",
                    "content": "Central Sector Scholarship for college and university students provides Rs. 12,000 per annum for graduation and Rs. 20,000 per annum for post-graduation. Eligibility: Above 80th percentile in 12th board exam, family income below 4.5 lakhs. Renewable for entire course duration.",
                    "url": "https://scholarships.gov.in",
                    "date": "2026-05-20"
                },
                {
                    "title": "Post Matric Scholarship for SC/ST Students",
                    "source": "socialjustice.gov.in",
                    "category": "Scholarship",
                    "content": "Government of India provides Post-Matric Scholarships for SC/ST students. Covers maintenance allowance, compulsory fees, study tour charges, thesis typing. Family income limit: Rs. 2.5 lakhs per annum. Apply through state government portals. All courses from Class 11 to PhD are covered.",
                    "url": "https://socialjustice.gov.in",
                    "date": "2026-07-01"
                },
                {
                    "title": "INSPIRE Scholarship by DST",
                    "source": "online-inspire.gov.in",
                    "category": "Scholarship",
                    "content": "Innovation in Science Pursuit for Inspired Research (INSPIRE) scholarship offers Rs. 80,000 per year for BSc, MSc and doctoral students in natural and basic sciences. Selection based on board exam performance (top 1%). Administered by Department of Science and Technology, Govt. of India.",
                    "url": "https://online-inspire.gov.in",
                    "date": "2026-04-10"
                },
                {
                    "title": "Kishore Vaigyanik Protsahan Yojana (KVPY)",
                    "source": "kvpy.iisc.ac.in",
                    "category": "Scholarship",
                    "content": "KVPY fellowship for students interested in research career in science. Monthly fellowship of Rs. 5,000 to Rs. 7,000 plus annual contingency grant. Open to students from Class 11 to 1st year BSc. National level aptitude test followed by interview.",
                    "url": "https://kvpy.iisc.ac.in",
                    "date": "2026-08-01"
                },
                {
                    "title": "Maulana Azad National Fellowship",
                    "source": "ugc.ac.in",
                    "category": "Scholarship",
                    "content": "UGC Maulana Azad National Fellowship for minority community students pursuing MPhil and PhD. Fellowship of Rs. 31,000 per month for JRF and Rs. 35,000 for SRF. Contingency grant and HRA provided. Duration: 5 years for PhD, 2 years for MPhil.",
                    "url": "https://www.ugc.ac.in",
                    "date": "2026-03-15"
                },
                {
                    "title": "National Means Cum Merit Scholarship",
                    "source": "scholarships.gov.in",
                    "category": "Scholarship",
                    "content": "NMMS provides Rs. 12,000 per annum to meritorious students from economically weaker sections. For students studying in Class 9 to 12. Family income below Rs. 3.5 lakhs. Selection through state level examination. Renewable annually based on academic performance.",
                    "url": "https://scholarships.gov.in",
                    "date": "2026-09-01"
                },
                {
                    "title": "Google Generation Scholarship",
                    "source": "buildyourfuture.withgoogle.com",
                    "category": "Scholarship",
                    "content": "Google provides scholarships for students from underrepresented groups in computing. Amount: USD 10,000 for selected scholars. Eligibility: Currently enrolled in computer science or related field. Strong academic performance and demonstrated leadership. Must be enrolled in an accredited university.",
                    "url": "https://buildyourfuture.withgoogle.com/scholarships",
                    "date": "2026-02-28"
                },
            ],
            "internships": [
                {
                    "title": "TCS Digital Internship Program 2026",
                    "source": "tcs.com",
                    "category": "Internship",
                    "content": "TCS offers digital internship opportunities for final year engineering and MCA students. Domains include AI/ML, Cloud Computing, Cybersecurity, IoT, and Blockchain. Duration: 6 months with possibility of PPO. Stipend: Rs. 25,000-35,000 per month. Locations across India.",
                    "url": "https://www.tcs.com/careers",
                    "date": "2026-08-15"
                },
                {
                    "title": "Infosys InStep Global Internship",
                    "source": "infosys.com",
                    "category": "Internship",
                    "content": "Infosys InStep is a global internship program for top university students. Projects in emerging technologies like AI, blockchain, quantum computing. Duration: 2-6 months. Competitive stipend provided. Experience working with Fortune 500 clients. Apply online through Infosys careers portal.",
                    "url": "https://www.infosys.com/instep",
                    "date": "2026-07-20"
                },
                {
                    "title": "Microsoft Engage 2026",
                    "source": "microsoft.com",
                    "category": "Internship",
                    "content": "Microsoft Engage is a mentorship-cum-internship program for engineering students. Build real projects under Microsoft mentors. Focus on Azure, Microsoft 365, and Teams platform development. Duration: 4 weeks intensive program. Top performers get interview opportunity for FTE roles.",
                    "url": "https://careers.microsoft.com",
                    "date": "2026-05-01"
                },
                {
                    "title": "Amazon Summer Internship 2026",
                    "source": "amazon.jobs",
                    "category": "Internship",
                    "content": "Amazon offers summer internships for CS and IT students. Roles: SDE Intern, Data Engineering Intern, Cloud Support Intern. Stipend: Rs. 60,000-80,000 per month. Duration: 2-3 months. Locations: Bangalore, Hyderabad, Chennai. Online assessment followed by technical interviews.",
                    "url": "https://amazon.jobs",
                    "date": "2026-01-15"
                },
                {
                    "title": "Goldman Sachs Engineering Virtual Program",
                    "source": "goldmansachs.com",
                    "category": "Internship",
                    "content": "Goldman Sachs offers virtual engineering internship experience. Learn about financial technology, risk management, and algorithmic trading. Gain experience with real-world engineering challenges. Duration: 4-8 weeks. Open to final year students from all engineering branches.",
                    "url": "https://www.goldmansachs.com/careers",
                    "date": "2026-06-01"
                },
            ],
            "announcements": [
                {
                    "title": "UGC NET December 2026 Registration Open",
                    "source": "ugcnet.nta.ac.in",
                    "category": "Announcement",
                    "content": "NTA has opened registration for UGC NET December 2026 examination. Last date for registration: October 15, 2026. Exam dates: December 1-15, 2026. Exam is conducted for eligibility for Assistant Professor and JRF. Apply online at ugcnet.nta.ac.in. Fee: Rs. 1100 for general category.",
                    "url": "https://ugcnet.nta.ac.in",
                    "date": "2026-09-01"
                },
                {
                    "title": "GATE 2027 Notification Released",
                    "source": "gate.iitb.ac.in",
                    "category": "Announcement",
                    "content": "GATE 2027 notification released by IIT Bombay. Registration starts from September 2026. Exam scheduled for February 2027. New subjects added this year. GATE score valid for 3 years. Used for admission to MTech/PhD programs and recruitment in PSUs. Online application at gate.iitb.ac.in.",
                    "url": "https://gate.iitb.ac.in",
                    "date": "2026-09-15"
                },
                {
                    "title": "National Education Policy 2026 Updates",
                    "source": "education.gov.in",
                    "category": "Announcement",
                    "content": "Ministry of Education announces implementation updates for NEP 2020. Multiple entry/exit option now available in all central universities. Academic Bank of Credits operational. Four-year undergraduate programs with research option launched. Choice-based credit system revised guidelines released.",
                    "url": "https://www.education.gov.in",
                    "date": "2026-08-20"
                },
                {
                    "title": "Smart India Hackathon 2026",
                    "source": "sih.gov.in",
                    "category": "Announcement",
                    "content": "Smart India Hackathon 2026 registrations are open. Students can form teams of 6 members and propose solutions for problem statements from ministries and industry. Software and hardware editions. Winner prizes up to Rs. 1 lakh. Internal hackathon at college level followed by national finale.",
                    "url": "https://sih.gov.in",
                    "date": "2026-07-10"
                },
                {
                    "title": "NPTEL Online Certification Courses",
                    "source": "nptel.ac.in",
                    "category": "Announcement",
                    "content": "NPTEL announces new batch of online certification courses for July-December 2026. Over 600 courses available across engineering, science, and management. Free to enroll, certification exam fee Rs. 1000. Top 5% get gold certificate. Courses by IIT and IISc faculty. Register at swayam.gov.in.",
                    "url": "https://nptel.ac.in",
                    "date": "2026-06-25"
                },
            ]
        }

    def _tokenize(self, text):
        """Tokenize text into lowercase words, removing stopwords."""
        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "shall", "can", "to", "of", "in", "for",
            "on", "with", "at", "by", "from", "as", "into", "through", "during",
            "before", "after", "above", "below", "between", "out", "off", "over",
            "under", "and", "or", "but", "if", "while", "this", "that", "these",
            "those", "it", "its", "i", "me", "my", "we", "our", "you", "your",
            "he", "him", "his", "she", "her", "they", "them", "their", "what",
            "which", "who", "whom", "not", "all", "each", "every", "both", "few",
            "more", "most", "so", "than", "too", "very", "just"
        }
        words = re.findall(r'\b[a-z0-9]+\b', text.lower())
        return [w for w in words if w not in stopwords and len(w) > 1]

    def _build_index(self):
        """Build IDF index across all knowledge base entries."""
        all_docs = []
        for category_items in self.knowledge_base.values():
            all_docs.extend(category_items)

        n = len(all_docs)
        doc_freq = Counter()

        for doc in all_docs:
            tokens = set(self._tokenize(doc["content"] + " " + doc["title"]))
            for token in tokens:
                doc_freq[token] += 1

        for term, df in doc_freq.items():
            self.idf_cache[term] = math.log((n - df + 0.5) / (df + 0.5) + 1)

    def _bm25_score(self, query_tokens, doc_text, k1=1.5, b=0.75):
        """Calculate BM25 score for a document against query tokens."""
        doc_tokens = self._tokenize(doc_text)
        tf = Counter(doc_tokens)
        doc_len = len(doc_tokens)
        avg_len = 150  # Approximate average document length

        score = 0
        for token in query_tokens:
            if token in tf:
                freq = tf[token]
                idf = self.idf_cache.get(token, 0)
                numerator = freq * (k1 + 1)
                denominator = freq + k1 * (1 - b + b * (doc_len / avg_len))
                score += idf * (numerator / max(denominator, 0.001))

        return score

    # ── Search Methods ─────────────────────────────────────────────────────

    def search(self, query, category=None, top_k=10):
        """
        Search the knowledge base using BM25 ranking.

        Args:
            query: Search query string
            category: Optional filter ('scholarships', 'internships', 'announcements')
            top_k: Number of results to return
        """
        query_tokens = self._tokenize(query)
        results = []

        categories = [category] if category else self.knowledge_base.keys()

        for cat in categories:
            items = self.knowledge_base.get(cat, [])
            for item in items:
                combined_text = item["title"] + " " + item["content"]
                score = self._bm25_score(query_tokens, combined_text)

                if score > 0:
                    results.append({
                        "title": item["title"],
                        "source": item["source"],
                        "category": item["category"],
                        "content": item["content"][:300] + "..." if len(item["content"]) > 300 else item["content"],
                        "url": item["url"],
                        "date": item["date"],
                        "relevance_score": round(score, 4)
                    })

        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:top_k]

    def get_scholarships(self, query="scholarship eligibility criteria"):
        """Get scholarship-related information."""
        return self.search(query, category="scholarships", top_k=5)

    def get_internships(self, query="engineering internship opportunity"):
        """Get internship-related information."""
        return self.search(query, category="internships", top_k=5)

    def get_announcements(self, query="exam registration announcement"):
        """Get announcement-related information."""
        return self.search(query, category="announcements", top_k=5)

    def extract_key_information(self, text):
        """
        Extract structured information from unstructured text.
        Extracts dates, amounts, URLs, organizations, and deadlines.
        """
        info = {
            "dates": re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', text, re.IGNORECASE),
            "amounts": re.findall(r'Rs\.?\s*[\d,]+(?:\.\d+)?|₹\s*[\d,]+(?:\.\d+)?|\$\s*[\d,]+(?:\.\d+)?', text),
            "urls": re.findall(r'https?://[^\s]+', text),
            "emails": re.findall(r'[\w.-]+@[\w.-]+\.\w+', text),
            "deadlines": [],
            "eligibility": []
        }

        # Extract deadline mentions
        deadline_patterns = re.findall(r'(?:deadline|last date|due date)[:\s]+([^.]+)', text, re.IGNORECASE)
        info["deadlines"] = deadline_patterns

        # Extract eligibility mentions
        eligibility_patterns = re.findall(r'(?:eligibility|eligible|criteria)[:\s]+([^.]+)', text, re.IGNORECASE)
        info["eligibility"] = eligibility_patterns

        return info


# ── Singleton Instance ─────────────────────────────────────────────────────────

web_crawler = WebCrawler()
