# CampusAI – Intelligent Voice-Based College ERP Assistant
## Master Technical Documentation for MCA Information Retrieval (IR) Viva Preparation

> **Degree / Program:** Master of Computer Applications (MCA)  
> **Course Subject:** Information Retrieval (IR) — Units IV, V, and VI  
> **Project Type:** Voice-Enabled ERP Assistant (Speech-to-SQL + IR Search & Recommendation Engine)  
> **Target Audience:** Project Evaluator / Viva Examiner, Faculty Guide, and Developers  
> **Implementation Status:** Based strictly on actual codebase inspection of `CampusAI`.

---

## Executive Summary & Scope

CampusAI is a dual-paradigm retrieval system engineered for higher education institutions:
1. **Structured Data Retrieval (Speech-to-SQL / NLP Engine):** Translates spoken natural language into sandboxed SQL queries executed against SQLite (`campus_ai.db`) with strict Role-Based Access Control (RBAC).
2. **Unstructured & Semi-Structured Data Retrieval (IR Engine):** Applies classical Information Retrieval models (**Inverted Indexing, Okapi BM25, TF-IDF, Vector Space Model, Cosine Similarity, Passage Retrieval, and Query Expansion**) to search institutional policy circulars and recommend scholarships and internships.

---

## Table of Contents
1. [Core Concept Mapping Matrix (Units IV, V, VI)](#1-core-concept-mapping-matrix-units-iv-v-vi)
2. [Deep-Dive Concept Analyses (All 10 Verification Points)](#2-deep-dive-concept-analyses)
   - [Finite Automata & Regular Expressions](#1-finite-automata--regular-expressions)
   - [Language Models & Multinomial Distribution](#2-language-models--multinomial-distribution-over-words)
   - [Ranking with Language Models & BM25](#3-ranking-with-language-models--okapi-bm25)
   - [Passage Retrieval](#4-passage-retrieval)
   - [Information Extraction (IE)](#5-information-extraction-ie)
   - [Vector Space Model (VSM) & Cosine Similarity](#6-vector-space-model-vsm--cosine-similarity)
   - [TF-IDF (Term Frequency – Inverse Document Frequency)](#7-tf-idf-weighting)
   - [Inverted Index & Indexing Architecture](#8-inverted-index--indexing-architecture)
   - [Query Processing & Stemming](#9-query-processing-normalization--stemming)
   - [Semantic & Intelligent Retrieval](#10-semantic--intelligent-retrieval)
3. [Module 1: AI Query / Speech-to-SQL (Admin + Student)](#3-module-1-ai-query--speech-to-sql-admin--student)
4. [Module 2: Document Search Engine (BM25 + TF-IDF + Passage Retrieval)](#4-module-2-document-search-engine)
5. [Module 3: Student Scholarship Recommendation Engine](#5-module-3-student-scholarship-recommendation-engine)
6. [Module 4: Student Internship Recommendation Engine](#6-module-4-student-internship-recommendation-engine)
7. [Module 5: Information Retrieval Models Comparison](#7-module-5-information-retrieval-models-comparison)
8. [Module 6: Explicit AI vs IR vs Database Component Separation](#8-module-6-explicit-ai-vs-ir-vs-database-component-separation)
9. [Module 7: Complete System Architecture & Dataflow Diagrams](#9-module-7-complete-system-architecture--dataflow-diagrams)
10. [Module 8: High-Yield Viva Voce Questions & Evaluator Answers](#10-module-8-high-yield-viva-voce-questions--evaluator-answers)
11. [Honest Technical Limitations & What NOT to Claim](#11-honest-technical-limitations--what-not-to-claim)

---

## 1. Core Concept Mapping Matrix (Units IV, V, VI)

| Concept Name | IR Syllabus Unit | Implementation Status in CampusAI | Primary Source File & Class/Function |
| :--- | :--- | :--- | :--- |
| **Finite Automata** | Unit IV | **Fully Implemented** | `backend/nlp_engine.py` (`_extract_attendance_condition`, `_extract_cgpa_condition`)<br>`backend/recommendation/ir_engine.py` (`_extract_amount_condition`) |
| **Language Models** | Unit IV | **Implemented (Unigram Statistical)** | `retrieval/document_search.py` (`DocumentSearchEngine._build_index`)<br>`crawler/web_crawler.py` (`WebCrawler._build_index`) |
| **Types of Language Models** | Unit IV | **Partial (Unigram implemented; N-Gram phrase boost)** | `retrieval/document_search.py` (`passage_retrieval` phrase boost) |
| **Multinomial Distribution** | Unit IV | **Fully Implemented** | `retrieval/document_search.py` (`doc_info["tf"] = Counter(...)`)<br>`backend/recommendation/ir_engine.py` (`Counter(...)`) |
| **Ranking with LMs** | Unit IV | **Implemented via BM25** | `retrieval/document_search.py` (`bm25_search`) |
| **Divergence From Randomness (DFR)** | Unit IV | **Not Implemented (Theoretical Mapping Only)** | N/A — Evaluated via BM25 & TF-IDF instead |
| **Passage Retrieval** | Unit IV | **Fully Implemented** | `retrieval/document_search.py` (`passage_retrieval`)<br>`backend/recommendation/ir_engine.py` (`_extract_best_snippet`) |
| **Ranking Algorithms** | Unit IV | **Fully Implemented** | `backend/recommendation/ir_engine.py` (`search_scholarships`, `search_internships`)<br>`retrieval/document_search.py` (`search`) |
| **Information Extraction (IE)** | Unit V | **Fully Implemented** | `backend/recommendation/ir_engine.py` (`extract_query_filters`)<br>`backend/nlp_engine.py` (`_extract_department`, `_extract_attendance_condition`)<br>`crawler/web_crawler.py` (`extract_key_information`) |
| **Information Retrieval Models** | Unit V | **Fully Implemented (Boolean, VSM, BM25)** | `backend/nlp_engine.py` (Boolean SQL)<br>`backend/recommendation/ir_engine.py` (VSM Cosine)<br>`retrieval/document_search.py` (Okapi BM25) |
| **Vector Space Model (VSM)** | Unit V | **Fully Implemented** | `backend/recommendation/ir_engine.py` (`_compute_cosine_similarity`)<br>`retrieval/document_search.py` (`semantic_search`) |
| **TF-IDF Weighting** | Unit V | **Fully Implemented** | `backend/recommendation/ir_engine.py` (`_build_scholarship_index`, `_build_internship_index`)<br>`retrieval/document_search.py` (`tfidf_search`) |
| **Okapi BM25** | Unit V | **Fully Implemented** | `retrieval/document_search.py` (`bm25_search`)<br>`crawler/web_crawler.py` (`_bm25_score`) |
| **Query Processing & Stemming** | Unit V | **Fully Implemented** | `backend/recommendation/ir_engine.py` (`tokenize`, `stem_term`)<br>`backend/nlp_engine.py` (`_preprocess_query`) |
| **Inverted Indexing** | Unit V | **Fully Implemented** | `backend/recommendation/ir_engine.py` (`sch_inverted_index`, `int_inverted_index`)<br>`retrieval/document_search.py` (`doc_index`, `idf_cache`) |
| **Document Retrieval** | Unit V | **Fully Implemented** | `retrieval/document_search.py` (`search`)<br>`backend/recommendation/ir_engine.py` (`search_scholarships`) |
| **Semantic Retrieval** | Unit VI | **Implemented via VSM Cosine (Not Dense Neural)** | `backend/recommendation/ir_engine.py` (`_compute_cosine_similarity`)<br>`backend/recommendation/recommender.py` (`recommend`) |
| **Retrieval Evaluation** | Unit VI | **Partial (Offline Test Suite Verified; Cranfield Not Bundled)** | `test_api_endpoints.py`, `test_ir.py` |
| **NLP-Based Retrieval** | Unit VI | **Fully Implemented** | `backend/nlp_engine.py` (`NLPEngine.process_query`) |
| **Intelligent / Context Search** | Unit VI | **Fully Implemented** | `backend/recommendation/ir_engine.py` (`get_student_context`, `search_scholarships`) |

---

## 2. Deep-Dive Concept Analyses

### 1. Finite Automata & Regular Expressions
- **IR Syllabus Unit:** Unit IV
- **Technical Definition:** A Finite State Automaton (FSA / DFA) is a formal 5-tuple $(Q, \Sigma, \delta, q_0, F)$ defining a state machine that transitions across discrete states based on input symbols. Regular expressions are equivalent in computational power to DFAs by Kleene's Theorem.
- **Purpose in CampusAI:** Parses unstructured speech/text queries to recognize monetary amounts (`₹`, `Rs`, `k`, `lakh`), comparative operators (`above`, `below`, `between`), CGPA thresholds, and attendance shortage bounds without relying on heavy external tokenizers.
- **Exact File Location:** `backend/nlp_engine.py` (lines 170–202), `backend/recommendation/ir_engine.py` (lines 131–215).
- **Function / Class:** `NLPEngine._extract_attendance_condition()`, `IREngine._extract_amount_condition()`.
- **Input $\rightarrow$ Processing $\rightarrow$ Output:**
  - *Input:* String query: `"Show scholarships between 50000 and 100000"`.
  - *Processing:* DFA evaluates state transitions on numeric and range tokens matching regex `(?:between|from)?\s*(?:rs\.?|₹)?\s*(\d+(?:,\d+)?|\d+k)\s*(?:and|to|-)\s*(\d+(?:,\d+)?|\d+k)`.
  - *Output:* Structured dictionary: `{'field': 'amount', 'operator': 'BETWEEN', 'value': (50000.0, 100000.0)}`.
- **Simple Viva Explanation:** *"We use Finite Automata implemented via regular expressions. When a user speaks a query, the automaton transitions through character states to extract numbers and operators like 'greater than 50000' or 'between 50k and 100k' without hardcoding."*
- **Example Query:** `"find scholarships above 50000 amount"` $\rightarrow$ Operator: `>`, Value: `50000.0`.
- **Limitations:** Limited to grammar patterns captured by regex; deeply nested linguistic clauses or non-standard slang require explicit transition rules.

---

### 2. Language Models & Multinomial Distribution over Words
- **IR Syllabus Unit:** Unit IV
- **Technical Definition:** A statistical language model computes the probability distribution $P(W)$ over word sequences. Under the unigram independence assumption, each document $D$ is treated as a multinomial distribution over terms in vocabulary $V$:
  $$P(w | M_D) = \frac{\text{count}(w, D)}{|D|}$$
- **Purpose in CampusAI:** Represents policy documents and scholarship descriptions as discrete term frequency distributions for probabilistic scoring and TF-IDF term estimation.
- **Exact File Location:** `retrieval/document_search.py` (lines 39–66), `backend/recommendation/ir_engine.py` (lines 233–251).
- **Function / Class:** `DocumentSearchEngine._build_index()`, `IREngine._build_scholarship_index()`.
- **Input $\rightarrow$ Processing $\rightarrow$ Output:**
  - *Input:* Raw text content from `documents` or `scholarships` table.
  - *Processing:* Computes term counts via `collections.Counter(tokens)` and document length $|D| = \sum c(w, D)$.
  - *Output:* Maximum likelihood term frequency parameter vectors per document.
- **Simple Viva Explanation:** *"A multinomial language model treats a document as a bag-of-words where each word has a probability of appearing based on its frequency. We count words using Python's `Counter` to model the document's word distribution."*
- **Example Query:** Document containing 200 words with 4 mentions of "attendance" has $P(\text{attendance} | M_D) = 4 / 200 = 0.02$.
- **Limitations:** Assumes unigram independence (bag-of-words assumption); does not model syntactic word grammar or long-range dependencies.

---

### 3. Ranking with Language Models & Okapi BM25
- **IR Syllabus Unit:** Unit IV & Unit V
- **Technical Definition:** Instead of raw query likelihood $P(Q | M_D)$ which suffers from zero-frequency penalties for unseen words, Okapi BM25 acts as the probabilistic retrieval model applying non-linear term frequency saturation and document length normalization:
  $$\text{BM25}(D, Q) = \sum_{q_i \in Q} \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$
- **Purpose in CampusAI:** Ranks institutional circulars and external opportunities without allowing long documents or repeated terms to artificially dominate search results. Configured with standard parameters $k_1 = 1.5$ and $b = 0.75$.
- **Exact File Location:** `retrieval/document_search.py` (lines 117–150), `crawler/web_crawler.py` (lines 214–230).
- **Function / Class:** `DocumentSearchEngine.bm25_search()`, `WebCrawler._bm25_score()`.
- **Input $\rightarrow$ Processing $\rightarrow$ Output:**
  - *Input:* Cleaned query tokens and document index.
  - *Processing:* Evaluates each document's raw term frequency $f(q_i, D)$, applies saturation denominator against corpus `avg_doc_length`, and sums weighted scores.
  - *Output:* Ranked document list with BM25 score floats (e.g., `4.1822`).
- **Simple Viva Explanation:** *"BM25 is the industry-standard probabilistic ranking formula. Unlike basic word matching, it prevents long documents from having an unfair advantage and ensures that repeating the same word multiple times produces diminishing score returns."*
- **Example Query:** `"hall ticket download procedure"` $\rightarrow$ Circular "Examination Regulations 2026" ranked #1 with score `4.1822`.
- **Limitations:** Requires tuning of hyperparameters $k_1$ and $b$; does not account for semantic synonyms unless expanded during query processing.

---

### 4. Passage Retrieval
- **IR Syllabus Unit:** Unit IV
- **Technical Definition:** Passage retrieval segments large documents into smaller contiguous text blocks (passages) to localize answers and avoid document-length dilation.
- **Purpose in CampusAI:** Extracts the most relevant 3-sentence window from long college circulars or policy documents, applying a $1.2\times$ exact-phrase matching multiplier.
- **Exact File Location:** `retrieval/document_search.py` (lines 154–192), `backend/recommendation/ir_engine.py` (lines 382–403).
- **Function / Class:** `DocumentSearchEngine.passage_retrieval()`, `IREngine._extract_best_snippet()`.
- **Input $\rightarrow$ Processing $\rightarrow$ Output:**
  - *Input:* Document text and user query tokens.
  - *Processing:* Splits text into sentences via `re.split(r'[.!?]+', text)`, constructs a sliding window of size $W=3$, calculates token overlap against query tokens, and boosts exact phrase hits.
  - *Output:* Highest scoring text passage limited to 160–500 characters.
- **Simple Viva Explanation:** *"Instead of returning a 10-page document for the student to read through, passage retrieval runs a 3-sentence sliding window over the document, scores each window, and extracts only the exact paragraph that answers the student's question."*
- **Example Query:** `"minimum attendance required"` $\rightarrow$ Retrieved Passage: *"Students with attendance below 75 percent in any subject will not be permitted to appear for the end-semester examinations."*
- **Limitations:** Fixed sentence window sizes may occasionally fragment sentences across paragraph boundaries.

---

### 5. Information Extraction (IE)
- **IR Syllabus Unit:** Unit V
- **Technical Definition:** Information Extraction is the automated process of extracting structured facts (entities, relationships, numeric constraints) from unstructured natural language text.
- **Purpose in CampusAI:** Converts natural queries into structured parameters: minimum/maximum amounts, comparison operators, student CGPA criteria, department codes, and dates.
- **Exact File Location:** `backend/recommendation/ir_engine.py` (lines 115–260), `backend/nlp_engine.py` (lines 157–202).
- **Function / Class:** `IREngine.extract_query_filters()`, `NLPEngine._extract_department()`.
- **Input $\rightarrow$ Processing $\rightarrow$ Output:**
  - *Input:* `"Show MCA scholarships above 50000"`
  - *Processing:* Regex parses `MCA` into course filter and `above 50000` into `{'operator': '>', 'value': 50000.0}`.
  - *Output:* `{'course': 'MCA', 'amount_filter': {'field': 'amount', 'operator': '>', 'value': 50000.0}}`.
- **Simple Viva Explanation:** *"Information extraction pulls out key facts from natural language. If an admin asks 'Show scholarships above 50000', IE extracts the numeric threshold 50000 and the operator '>' so our system can filter database records directly."*
- **Example Query:** `"find scholarships between 25000 and 60000"` $\rightarrow$ Extracted: `operator: 'BETWEEN'`, range: `(25000.0, 60000.0)`.
- **Limitations:** Relies on deterministic rule patterns; unexpected phrasings outside defined templates may fail to trigger slot extraction.

---

### 6. Vector Space Model (VSM) & Cosine Similarity
- **IR Syllabus Unit:** Unit V
- **Technical Definition:** The Vector Space Model maps documents and queries into a continuous Euclidean vector space $\mathbb{R}^{|V|}$. Relevance is computed as the cosine of the angle between query vector $\vec{q}$ and document vector $\vec{d}$:
  $$\cos(\vec{q}, \vec{d}) = \frac{\vec{q} \cdot \vec{d}}{\|\vec{q}\| \|\vec{d}\|} = \frac{\sum_{t} w_{t,q} \cdot w_{t,d}}{\sqrt{\sum_{t} w_{t,q}^2} \sqrt{\sum_{t} w_{t,d}^2}}$$
- **Purpose in CampusAI:** Powers the core recommendation ranking in `ir_engine.py` by comparing student profile vectors (Course, Department, Skills, Query) against 574 scholarship vectors and 50 internship vectors.
- **Exact File Location:** `backend/recommendation/ir_engine.py` (lines 360–380), `retrieval/document_search.py` (lines 196–243).
- **Function / Class:** `IREngine._compute_cosine_similarity()`, `DocumentSearchEngine.semantic_search()`.
- **Input $\rightarrow$ Processing $\rightarrow$ Output:**
  - *Input:* Normalized TF-IDF query vector $\vec{q}$ and document vector $\vec{d}$ with precomputed Euclidean norms.
  - *Processing:* Dot product over shared terms divided by product of Euclidean norms.
  - *Output:* Continuous similarity score $\in [0, 1]$.
- **Simple Viva Explanation:** *"In the Vector Space Model, queries and documents are represented as arrows in space. We take the cosine of the angle between them. If the angle is 0 degrees, cosine is 1.0 (exact match). If they share no words, cosine is 0."*
- **Example Query:** Student with skills `['Python', 'SQL', 'Machine Learning']` searching `"data analyst intern"` yields $\cos(\vec{q}, \vec{d}) = 0.66$ (Ranked #1).
- **Limitations:** Orthogonal term assumption: treats all vocabulary terms as independent dimensions; does not natively recognize that "programmer" and "developer" share meaning unless stemmed or expanded.

---

### 7. TF-IDF Weighting
- **IR Syllabus Unit:** Unit V
- **Technical Definition:** Combines local term frequency with global inverse document frequency:
  $$\text{TF}(t, d) = \frac{\text{count}(t, d)}{|D|}, \quad \text{IDF}(t) = \ln\left(\frac{N + 1}{\text{DF}(t) + 1}\right) + 1.0, \quad w_{t,d} = \text{TF}(t, d) \times \text{IDF}(t)$$
- **Purpose in CampusAI:** Discounts non-discriminative terms (like "student" or "scholarship" which appear in nearly all records) while boosting distinctive terms (like "AICTE", "Pragati", "Docker", "MahaDBT").
- **Exact File Location:** `backend/recommendation/ir_engine.py` (lines 223–251), `retrieval/document_search.py` (lines 89–113).
- **Function / Class:** `IREngine._build_scholarship_index()`, `DocumentSearchEngine.tfidf_search()`.
- **Simple Viva Explanation:** *"TF measures how frequently a word appears in a specific document. IDF measures how rare that word is across the entire college database. Multiplying them highlights words that are uniquely important to that document."*
- **Example Calculation:** In $N=574$ scholarships, "scholarship" has $\text{DF}=450$ ($\text{IDF} \approx 1.24$). "AICTE" has $\text{DF}=15$ ($\text{IDF} \approx 4.58$). "AICTE" is weighted 3.7 times higher than "scholarship".
- **Limitations:** Basic TF-IDF does not prevent term saturation for very long documents (which is why BM25 is used in document search).

---

### 8. Inverted Index & Indexing Architecture
- **IR Syllabus Unit:** Unit V
- **Technical Definition:** An inverted index is a persistent data structure mapping each vocabulary term $t$ to a posting list of document IDs and associated term weights:
  $$\text{Postings}[t] = \{(\text{doc\_id}_1, \text{weight}_1), (\text{doc\_id}_2, \text{weight}_2), \dots\}$$
- **Purpose in CampusAI:** Eliminates sequential full-table scans over SQLite documents and opportunities. Enables sub-millisecond retrieval of candidate documents containing query tokens.
- **Exact File Location:** `backend/recommendation/ir_engine.py` (lines 228–251), `retrieval/document_search.py` (lines 39–66).
- **Function / Class:** `IREngine._build_scholarship_index()`, `IREngine._build_internship_index()`.
- **Input $\rightarrow$ Processing $\rightarrow$ Output:**
  - *Input:* 574 scholarship records and 50 internship records from database.
  - *Processing:* Tokenizes all descriptive text fields, computes document frequency $\text{DF}(t)$, builds term dictionary mapping to document IDs and TF-IDF weights.
  - *Output:* Precalculated dictionaries: `sch_inverted_index`, `sch_doc_vectors`, `sch_doc_norms`.
- **Simple Viva Explanation:** *"An inverted index is like the index at the back of a textbook. Instead of reading all 574 scholarships to find 'Python', we look up 'Python' in the dictionary and immediately retrieve the exact list of scholarship IDs where it appears."*
- **Example Posting List:** `sch_inverted_index["aicte"] = {484: 0.284, 485: 0.312, 486: 0.295, ...}`.
- **Limitations:** Index resides in memory (`dict`); must be rebuilt via `reload_indices()` whenever records are added or updated in the database.

---

### 9. Query Processing, Normalization & Stemming
- **IR Syllabus Unit:** Unit V
- **Technical Definition:** Query processing transforms raw user input into normalized tokens through case folding, stopword removal, character sanitation, morphological stemming, and context expansion.
- **Purpose in CampusAI:** Ensures queries like `"Show scholarships"` match documents containing `"scholarship"`, and preserves programming language tokens (`c++` $\rightarrow$ `cpp`, `c#` $\rightarrow$ `csharp`, `.net` $\rightarrow$ `dotnet`).
- **Exact File Location:** `backend/recommendation/ir_engine.py` (lines 42–109), `backend/nlp_engine.py` (lines 145–149).
- **Function / Class:** `stem_term()`, `IREngine.tokenize()`, `NLPEngine._preprocess_query()`.
- **Input $\rightarrow$ Processing $\rightarrow$ Output:**
  - *Input:* `"Please show MCA scholarships and C++ internships!"`
  - *Processing:*
    1. Case folding $\rightarrow$ `"please show mca scholarships and c++ internships!"`
    2. Preservation $\rightarrow$ `c++` replaced with `cpp`
    3. Stopword removal $\rightarrow$ removes `please`, `show`, `and`
    4. Suffix stemming $\rightarrow$ `scholarships` stripped to `scholarship`, `internships` to `internship`
  - *Output:* `['mca', 'scholarship', 'cpp', 'internship']`
- **Simple Viva Explanation:** *"Query processing cleans the user's speech. It removes conversational filler words like 'please show me', strips plural endings using suffix stemming, and expands the query with the student's degree and CGPA."*
- **Example Query:** `"scholarships"` stems to `"scholarship"` ensuring $100\%$ inverted index vocabulary recall.
- **Limitations:** Lightweight rule-based suffix stemming (`stem_term`) does not handle irregular plurals (e.g., "children" $\rightarrow$ "child") without a full dictionary lookup.

---

### 10. Semantic & Intelligent Retrieval
- **IR Syllabus Unit:** Unit VI
- **Technical Definition:** Information retrieval enhanced with contextual intelligence: utilizing user session state, academic constraints, and profile attributes to personalize search results.
- **Purpose in CampusAI:** An MCA student searching `"scholarships"` automatically receives MCA-targeted, CGPA-qualified opportunities at the top, without needing to explicitly re-type their department, semester, and CGPA in every query.
- **Exact File Location:** `backend/recommendation/ir_engine.py` (lines 310–355, 426–440).
- **Function / Class:** `IREngine.get_student_context()`, `IREngine.search_scholarships()`.
- **Input $\rightarrow$ Processing $\rightarrow$ Output:**
  - *Input:* Logged-in Student ID `1601` + Query `"scholarships"`.
  - *Processing:* Fetches Student profile (`MCA`, `CGPA: 7.97`, `Dept: Master of Computer Applications`). Expands query vector with academic context tokens and boosts opportunities where `student_cgpa >= doc.min_cgpa`.
  - *Output:* Top-ranked scholarships displayed with realistic match badges (**94%**, **88%**, **79%**) and criteria snippets.
- **Simple Viva Explanation:** *"Our search is intelligent because it is context-aware. It knows who is asking. When an MCA student with a 7.97 CGPA searches, it automatically factors in their degree and marks to prioritize scholarships they are actually eligible for."*
- **Example Query:** Student 1601 searches `"scholarships"` $\rightarrow$ *AICTE PG Scholarship for Technical Postgraduates* boosted to 93% match.
- **Limitations:** Does not use dense deep learning neural embeddings (e.g., BERT/Sentence-Transformers); semantic matching is achieved via Vector Space Model Cosine Similarity.

---

## 3. Module 1: AI Query / Speech-to-SQL (Admin + Student)

### Pipeline Architecture

```
User Voice / Text Query
          │
          ▼
1. Web Speech API (Frontend: VoiceInput.jsx -> webkitSpeechRecognition)
          │
          ▼
2. NLP Preprocessing (nlp_engine.py: _preprocess_query)
   - Case folding, punctuation stripping, tokenization
          │
          ▼
3. Information Extraction & Slot Filling (nlp_engine.py)
   - Entity Recognition: Departments via DEPT_ALIASES
   - Numeric Extractor: CGPA, Attendance %, Monetary limits via Finite Automata regex
   - Intent Classification: query, count, average, comparison
          │
          ▼
4. Role-Based Access Control (RBAC) Dispatcher (nlp_engine.py)
   ├─► IF Role == 'admin': _generate_admin_sql(query)
   │     Full institutional scope: all students, department stats, finance, staff
   │
   └─► IF Role == 'student': _generate_student_sql(query, verified_student_id)
         Sandboxed scope: WHERE s.student_id = {verified_student_id}
         Interception of bypass attempts ('all students', 'other students')
          │
          ▼
5. Dynamic SQL Generation & SQLite Execution (database.py: execute_raw_sql)
          │
          ▼
6. Tabular Result Formatting + Dynamic Query Recommendations (recommender.py)
```

### Static vs. Dynamic SQL Query Clarification
> **Crucial Viva Clarification:** The SQL queries in CampusAI are **NOT static hardcoded strings**.  
> They are **dynamically synthesized at runtime** using syntax-directed slot-filling. The SQL clauses (`SELECT`, `JOIN`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`) are constructed dynamically based on the entities, comparative operators (`>`, `<`, `BETWEEN`), and student authentication tokens extracted from the user's natural language input.

### Admin Query Deep-Dive
- **Query:** `"Show students with CGPA above 8"`
- **Step 1 (Text Processing):** Stripped to `"show students with cgpa above 8"`.
- **Step 2 (Information Extraction):** Regex `r'(?:cgpa|gpa)\s*(?:above|greater than|>=|>)\s*(\d+(?:\.\d+)?)'` identifies operator `>=` and value `8.0`.
- **Step 3 (Dynamic SQL Synthesis):**
  ```sql
  SELECT s.student_id, s.name, s.roll_number, s.course, d.department_name,
         ROUND(AVG(ar.cgpa), 2) AS cgpa
  FROM students s
  JOIN departments d ON s.department_id = d.department_id
  JOIN academic_record ar ON s.student_id = ar.student_id
  GROUP BY s.student_id
  HAVING AVG(ar.cgpa) >= 8.0
  ORDER BY cgpa DESC
  LIMIT 50;
  ```
- **Step 4 (Database Execution):** Returns tabular JSON of qualifying students across all departments.

### Student Query Deep-Dive & Sandboxing
- **Queries:** `"Show my attendance"`, `"Show my fees"`, `"Show my CGPA"`
- **RBAC Security Sandboxing:** When Student ID `1601` (Ojasvi Hegde) executes a query, `_generate_student_sql()` injects strict identity constraints:
  - `"Show my attendance"`:
    ```sql
    SELECT a.subject_name, a.total_classes, a.attended_classes, a.attendance_percent, a.semester
    FROM attendance a
    WHERE a.student_id = 1601
    ORDER BY a.semester, a.subject_name;
    ```
  - `"Show my fees"`:
    ```sql
    SELECT f.total_fee, f.paid_amount, f.pending_amount, f.payment_status, f.scholarship_applied, f.academic_year
    FROM fees f
    WHERE f.student_id = 1601;
    ```
- **Bypass Defense:** If a student attempts a bypass query such as `"Show all students"` or `"Show civil department marks"`, the engine's bypass regex patterns intercept the query and return **only** student 1601's personal identity profile record (`WHERE s.student_id = 1601`), completely blocking unauthorized access.

---

## 4. Module 2: Document Search Engine

### Pipeline Architecture
- **Source Files:** `retrieval/document_search.py`, `crawler/web_crawler.py`.
- **Data Structure:** Unstructured institutional circulars, academic bylaws, fee refund regulations, and exam circulars stored in the `documents` table (`document_id`, `title`, `category`, `content`).

```
User Query: "Scholarship eligibility criteria"
                 │
                 ▼
1. Tokenization & Case Folding (_tokenize)
   Tokens: ['scholarship', 'eligibility', 'criteria']
                 │
                 ▼
2. Parallel Multi-Model Scoring
   ├─► Method A: Okapi BM25 Ranking (bm25_search)
   │     Computes non-linear term saturation with length penalty
   │
   ├─► Method B: TF-IDF Vector Space Model (semantic_search)
   │     Computes Cosine Similarity on weighted term vectors
   │
   └─► Method C: Passage Retrieval (passage_retrieval)
         Slides 3-sentence window across document texts
                 │
                 ▼
3. Result Aggregation & Deduplication (search)
   - Merges candidate documents by document_id
   - Attaches best retrieved passage excerpt to each hit
   - Returns ranked results with relevance scores
```

### Working Example: `"Scholarship eligibility criteria"`
1. **Query Processing:** Tokens extracted: `['scholarship', 'eligibility', 'criteria']`. Stopwords (`for`, `the`, `is`) discarded.
2. **Inverted Index Lookup:** Locates document postings matching vocabulary terms.
3. **BM25 Scoring:** Documents discussing specific financial criteria receive positive weights adjusted for document length.
4. **Passage Retrieval:** Locates candidate sentence sequence:
   > *"Students applying for state and central scholarships must maintain a minimum of 75% attendance and clear all semester subjects with no active backlogs."*
5. **Output:** Top-ranked circular returned with passage preview and relevance score.

---

## 5. Module 3: Student Scholarship Recommendation Engine

### Pipeline Architecture

```
Student Logs In (e.g., Student ID 1601, MCA, CGPA: 7.97)
                 │
                 ▼
1. Query Input: "technical scholarship"
                 │
                 ▼
2. Information Extraction & Dynamic Numeric Filter (ir_engine.py)
   - Parses currency/amounts, courses, and providers
   - IF numeric amount is specified: PRUNE non-matching records BEFORE ranking
                 │
                 ▼
3. Context-Aware Query Vector Expansion (ir_engine.py: get_student_context)
   - User tokens: ['technic', 'scholarship'] (weight multiplier: 1.6x)
   - Profile tokens: ['mca', 'master', 'comput', 'applic']
   - Combined Query Vector q constructed in Vector Space Model
                 │
                 ▼
4. Vector Space Model & Cosine Similarity Calculation
   - For all candidate scholarships, calculate dot product:
     CosineSim = (q · d) / (||q|| * ||d||)
                 │
                 ▼
5. Calibrated Multi-Metric Scoring Formula
   BaseScore = 0.40 + (Coverage * 0.36) + (CosineSim * 0.30)
   + Program Alignment Boost (+0.08 for MCA match)
   + Academic CGPA Validation (CGPA 7.97 >= min_cgpa ? +0.04 : -0.10)
                 │
                 ▼
6. Document Retrieval & Formatting
   - Calibrates final percentage: max(42%, min(95%, BaseScore * 100))
   - Extracts snippet passage and matched term tags
   - Returns descending ranked opportunity cards
```

### Static vs. Dynamic Clarification
- **Scholarship Records:** Stored persistently in SQLite (`scholarships` table, 574 records).
- **Recommendation & Ranking:** **100% Dynamic**. Scores and rankings are computed on-the-fly at runtime based on the logged-in student's real-time CGPA, academic degree, and query terms. No scores are pre-baked or hardcoded.

### Working Example: Student 1601 (MCA, CGPA 7.97) searching `"technical scholarship"`
- Document ID 487 (*AICTE PG Scholarship for Technical Postgraduates*):
  - Course requirement: `MCA, M.Tech CSE` (Matches student course $\rightarrow$ +0.08 Boost).
  - Minimum CGPA cutoff: `7.0` $\le 7.97$ (Student eligible $\rightarrow$ +0.04 Boost).
  - Cosine Similarity: `0.7421`.
  - Final Calibrated Match Score: **93%** (Displayed with Emerald Badge and snippet excerpt).

---

## 6. Module 4: Student Internship Recommendation Engine

### Dataset & Attributes
- **Dataset:** 50 real-world technical internship profiles stored in SQLite (`internships` table) spanning domains such as Artificial Intelligence, Machine Learning, Cloud Computing, Full-Stack Web Development, Data Analytics, and Cybersecurity.
- **Attributes:** `role`, `company_name`, `domain`, `stipend`, `location`, `duration`, `skills_required`, `eligibility`, `description`.

### Matching & Ranking Logic
1. **Student Skill Extraction:** `get_student_context()` reads the student's passed semester subjects from `academic_record` and maps MCA students to technical competencies (`Python`, `Java`, `SQL`, `DBMS`, `Cloud Computing`, `AI/ML`, `Web Development`).
2. **Numeric Stipend Pruning:** Any query mentioning stipend constraints (e.g., `"internships above 20000"`) filters candidate records **before** vector scoring.
3. **TF-IDF & Cosine Similarity:** Constructs document vectors across `skills_required` and `role`.
4. **Skills Overlap Boost:** Direct match between student skills and internship requirements awards an eligibility boost.

### Working Example: Student searching `"Data Analyst internship"`
- Student skills: `['Python', 'SQL', 'DBMS']`.
- Role matched: *Data Analyst Intern at Cognizant* (Stipend: ₹22,000/mo).
- Matched skills: `python`, `sql`.
- Output: Returns opportunity ranked #1 with match badge (63%), skills pills, and Apply button.

---

## 7. Module 5: Information Retrieval Models Comparison

| IR Model | Theoretical Basis | Mathematical Formulation | Where Used in CampusAI | Strengths & Trade-offs |
| :--- | :--- | :--- | :--- | :--- |
| **Boolean Model** | Set Theory & Boolean Logic | $R = D_1 \land D_2 \lor \neg D_3$ | `backend/nlp_engine.py` (SQL `WHERE` clauses) | **Exact match:** Fast, transparent; no partial matching or continuous ranking. |
| **Vector Space Model (VSM)** | Linear Algebra / Euclidean Space | $\cos(\vec{q}, \vec{d}) = \frac{\vec{q} \cdot \vec{d}}{\|\vec{q}\| \|\vec{d}\|}$ | `backend/recommendation/ir_engine.py`<br>`retrieval/document_search.py` | **Partial match:** Allows graded relevance ranking; assumes term independence. |
| **Okapi BM25** | Probabilistic Model & 2-Poisson | $\sum \text{IDF} \cdot \frac{f \cdot (k_1+1)}{f + k_1(1-b+b \frac{\|D\|}{\text{avgdl}})}$ | `retrieval/document_search.py`<br>`crawler/web_crawler.py` | **Term Saturation:** Prevents long documents from dominating; highly effective for unstructured text. |
| **Unigram Language Model** | Generative Probability | $P(Q \| M_D) = \prod P(q_i \| M_D)$ | `retrieval/document_search.py` (`_build_index`) | **Statistical clarity:** Evaluates generative likelihood; requires smoothing for unseen terms. |
| **Passage Retrieval** | Sliding Window Localization | $\text{Score}(P) = \frac{\|Q \cap P\|}{\|Q\|} \times \text{Boost}$ | `retrieval/document_search.py`<br>`ir_engine.py` (`_extract_best_snippet`) | **High precision:** Isolates precise paragraphs containing answers rather than full documents. |

---

## 8. Module 6: Explicit AI vs IR vs Database Component Separation

To ensure academic rigor, CampusAI cleanly delineates responsibilities across three architectural tiers:

### 1. Artificial Intelligence & NLP Components
- **Speech Recognition:** Browser Web Speech API (`webkitSpeechRecognition`) converting acoustic audio waveforms to text strings on the client side.
- **Natural Language Preprocessing:** Case folding, punctuation stripping, domain stopword filtering, and suffix stemming (`stem_term`).
- **Information Extraction (IE):** Regular expression DFAs performing Named Entity Recognition for departments, academic metrics, and monetary numbers.
- **Intent Detection:** Syntax pattern matching classifying queries into tabular lookup, count aggregate, average comparison, or opportunity discovery.

### 2. Information Retrieval (IR) Components
- **Indexing:** Inverted Index construction mapping vocabulary terms to posting lists of document IDs and precalculated TF-IDF weights.
- **Vector Space Modeling:** High-dimensional vectorization of queries, student profiles, and catalogue descriptions.
- **Scoring & Ranking:** Cosine similarity calculation, Okapi BM25 length normalization, query term coverage calculation, and descending relevance ordering.
- **Passage Retrieval:** Sliding-window sentence extraction isolating relevant explanatory excerpts.

### 3. Database Components
- **Relational Storage:** SQLite database (`database/campus_ai.db`) managing relational tables: `students`, `departments`, `academic_record`, `attendance`, `fees`, `scholarships`, `internships`, `documents`.
- **Relational Query Execution:** Structured SQL query processing (`SELECT`, `JOIN`, `GROUP BY`, `HAVING`, `WHERE`).
- **Data Integrity:** Foreign key enforcement linking students to departments and academic history.

> **What NOT to claim:** Do NOT claim the project uses **OpenAI GPT, BERT, Deep Learning, or Neural Networks**. The project is an authentic, lightweight implementation of classical NLP, Information Retrieval, and Relational Database Engineering.

---

## 9. Module 7: Complete System Architecture & Dataflow Diagrams

### Overall System Architecture Flow

```
+-------------------------------------------------------------------------+
|                              FRONTEND UI                                |
|   (React.js + Vite + Lucide Icons + Web Speech API webkitSpeech)         |
+-------------------------------------------------------------------------+
       │ Voice Input (Speech)              │ Text Input (Typed Query)
       ▼                                   ▼
+-------------------------------------------------------------------------+
|                        FASTAPI BACKEND ROUTER                           |
|                         (backend/main.py)                               |
+-------------------------------------------------------------------------+
         │                                       │
         ▼ Route: /api/query                     ▼ Route: /api/recommendations/*
+-----------------------------------+   +---------------------------------+
|            NLP ENGINE             |   |            IR ENGINE            |
|     (backend/nlp_engine.py)       |   | (backend/recommendation/        |
|                                   |   |         ir_engine.py)           |
| - Preprocessing & Tokenization    |   |                                 |
| - Intent Classification           |   | - Tokenization & Stemming       |
| - Information Extraction (Regex)  |   | - Profile Context Expansion     |
| - RBAC Security Sandboxing        |   | - Dynamic Numeric Pruning       |
| - Dynamic SQL Synthesis           |   | - Inverted Index TF-IDF VSM     |
|                                   |   | - Cosine Similarity Scoring     |
|                                   |   | - Calibrated Ranking (42%-95%)  |
|                                   |   | - Passage Snippet Extraction    |
+-----------------------------------+   +---------------------------------+
         │                                       │
         ▼                                       ▼
+-------------------------------------------------------------------------+
|                          SQLITE DATABASE ENGINE                         |
|                         (database/campus_ai.db)                         |
|                                                                         |
| Tables: students, departments, academic_record, attendance, fees,       |
|         scholarships (574 records), internships (50 records), documents |
+-------------------------------------------------------------------------+
         │                                       │
         ▼                                       ▼
  Tabular SQL Result Set                  Ranked Opportunity Cards
  + Generated SQL Display                 + Excerpts & Match % Badges
         │                                       │
         └───────────────────┬───────────────────┘
                             ▼
+-------------------------------------------------------------------------+
|                         STUDENT / ADMIN PORTAL                          |
|             (Rendered Tables, Cards, Badges, Snippet Excerpts)          |
+-------------------------------------------------------------------------+
```

---

## 10. Module 8: High-Yield Viva Voce Questions & Evaluator Answers

### Q1: Where exactly is TF-IDF used in CampusAI?
**Answer:**  
*"TF-IDF is used in three specific modules:  
1. In `backend/recommendation/ir_engine.py` (lines 223–251) to weight scholarship descriptions and internship skill requirements for student recommendation.  
2. In `retrieval/document_search.py` (lines 89–113) for college circular and regulation search.  
3. In `backend/recommendation/recommender.py` (lines 80–120) to compute cosine similarity for suggesting related natural language queries."*

### Q2: Is your scholarship recommendation static or dynamic?
**Answer:**  
*"The database records are persistent (574 scholarships in SQLite), but the recommendation and ranking are **100% dynamic**. When a student executes a query, `IREngine.search_scholarships()` dynamically retrieves their live profile (CGPA, Course, Department), constructs a query vector, calculates cosine similarity against all candidates, applies academic eligibility rules, and ranks them at runtime. Scores are continuous percentages (e.g., 94%, 88%, 79%) rather than static hardcoded responses."*

### Q3: What is the difference between SQL retrieval and IR retrieval in your project?
**Answer:**  
*"SQL retrieval operates on **structured tabular data** using deterministic Boolean algebra (exact matches on student IDs, department names, or attendance percentages). In contrast, Information Retrieval operates on **unstructured and semi-structured text** (document circulars, scholarship criteria, job descriptions) using statistical and geometric models (BM25, TF-IDF, Vector Space Model, Cosine Similarity) to calculate continuous relevance rankings for partial matches."*

### Q4: Does your project use Artificial Intelligence?
**Answer:**  
*"Yes, CampusAI implements classical Artificial Intelligence and Natural Language Processing components: client-side acoustic speech-to-text conversion via Web Speech API, text tokenization, domain stopword filtering, suffix stemming, and Finite Automata Information Extraction for entity and numeric slot filling. We deliberately chose classical NLP and IR over deep neural LLMs like GPT or BERT to keep the application lightweight, fully explainable, offline, and computationally efficient."*

### Q5: What is the difference between TF-IDF and Okapi BM25? Why did you use both?
**Answer:**  
*"Standard TF-IDF increases linearly or logarithmically with term frequency, which can cause long documents with repetitive words to receive unfairly high scores. Okapi BM25 improves on TF-IDF by adding **term frequency saturation** ($k_1=1.5$), which ensures that after a word appears a few times, further occurrences yield diminishing returns, and **document length normalization** ($b=0.75$), which penalizes documents longer than the average corpus length. We use BM25 in `document_search.py` for long policy documents, and the Vector Space Model with TF-IDF in `ir_engine.py` for opportunity recommendation."*

### Q6: How does Passage Retrieval work in CampusAI?
**Answer:**  
*"In `retrieval/document_search.py`, `passage_retrieval()` splits documents into sentences using regular expressions. It passes a sliding window of 3 sentences across the text, calculates the term overlap between the user query and each passage, applies a 1.2x boost for exact phrase hits, and extracts only the most relevant paragraph. This allows students to immediately read the answer without reviewing a multi-page document."*

### Q7: How does your system prevent students from viewing other students' private records?
**Answer:**  
*"Role-Based Access Control (RBAC) is sandboxed inside `backend/nlp_engine.py` in `_generate_student_sql()`. The backend verifies the authenticated student's session token and forces `WHERE s.student_id = {verified_id}` into personal SQL queries (marks, fees, attendance). Any natural language query attempting to inspect other students or department statistics is intercepted and sandboxed to the student's own record."*

---

## 11. Honest Technical Limitations & What NOT to Claim

During project evaluation, maintain credibility by being upfront about design boundaries:

1. **Do NOT Claim Deep Transformer Neural Networks (BERT, RoBERTa, GPT-4)**  
   *The project implements classical statistical and vector space IR algorithms in pure Python, not multi-billion parameter neural networks.*
2. **Do NOT Claim Standard TREC / Cranfield Human Benchmark Evaluation**  
   *The system is evaluated using automated integration and regression test suites (`test_api_endpoints.py`), not third-party human-annotated gold standard query collections.*
3. **Do NOT Claim Divergence From Randomness (DFR)**  
   *DFR based on Poisson/Geometric randomness models is covered in syllabus theory but was substituted in implementation by Okapi BM25 and Vector Space Model Cosine Similarity.*
4. **Live Web Crawling Scope**  
   *`crawler/web_crawler.py` contains full text extraction and BM25 ranking logic, but populates from a curated knowledge base of college resources to guarantee 100% offline reliability during examination demonstrations.*

---
*Documentation compiled for CampusAI Project — Master of Computer Applications (MCA) Viva Voce Defense.*
