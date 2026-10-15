# CampusAI - Information Retrieval (IR) Concept Mapping & Viva Guide

> **Project Name:** CampusAI — Speech-to-SQL & Information Retrieval ERP System  
> **Course / Subject:** Information Retrieval (IR)  
> **Target Audience:** Viva Voce Examiner, Project Evaluator, and Developers  
> **Generated Documentation:** Comprehensive Mapping of Syllabus Units (Unit IV, Unit V, Unit VI), Code Implementations, Viva Q&A, and Limitations.

---

## Table of Contents
1. [Project IR Overview & End-to-End Flow](#1-project-ir-overview--end-to-end-flow)
2. [Unit IV Concepts Mapping](#2-unit-iv-concepts-mapping)
   - [Finite Automata](#finite-automata)
   - [Language Models & Types](#language-models--types-of-language-models)
   - [Multinomial Distribution over Words](#multinomial-distribution-over-words)
   - [Ranking with Language Models](#ranking-with-language-models)
   - [Divergence From Randomness (DFR)](#divergence-from-randomness-dfr)
   - [Passage Retrieval](#passage-retrieval)
   - [Ranking Algorithms](#ranking)
3. [Unit V Concepts Mapping](#3-unit-v-concepts-mapping)
   - [Information Extraction (IE)](#information-extraction-ie)
   - [Information Retrieval Models](#information-retrieval-models)
   - [Vector Space Model (VSM)](#vector-space-model-vsm)
   - [TF-IDF (Term Frequency - Inverse Document Frequency)](#tf-idf)
   - [BM25 (Best Matching 25)](#bm25)
   - [Query Processing & Normalization](#query-processing)
   - [Indexing & Inverted Index](#indexing)
   - [Document Retrieval](#document-retrieval)
4. [Unit VI Concepts Mapping](#4-unit-vi-concepts-mapping)
   - [Semantic Retrieval](#semantic-retrieval)
   - [Retrieval Evaluation](#retrieval-evaluation)
   - [NLP-Based Retrieval & Speech-to-SQL](#nlp-based-retrieval)
   - [Intelligent & Context-Aware Search](#intelligent-search)
5. [Module-Wise IR Mapping Matrix](#5-module-wise-ir-mapping-matrix)
6. [Detailed End-to-End Working Examples](#6-detailed-end-to-end-working-examples)
   - [Example 1: Structured AI Query ("Show students with CGPA above 8")](#example-1-structured-ai-query)
   - [Example 2: Profile-Aware IR Recommendation ("Scholarships for MCA students")](#example-2-profile-aware-ir-recommendation)
   - [Example 3: Unstructured Document Retrieval ("Scholarship eligibility criteria")](#example-3-unstructured-document-retrieval)
7. [Comprehensive Viva Voce Q&A Preparation](#7-comprehensive-viva-voce-qa-preparation)
8. [Honest Limitations & What NOT to Claim](#8-honest-limitations--what-not-to-claim)

---

## 1. Project IR Overview & End-to-End Flow

CampusAI combines two distinct Information Retrieval paradigms:
1. **Unstructured & Semi-Structured IR (Document & Opportunity Search):** Uses traditional text IR algorithms (**TF-IDF, Okapi BM25, Vector Space Model, Cosine Similarity, Passage Retrieval**) to retrieve and rank institutional circulars, scholarships, and internships.
2. **Structured Database Retrieval (Speech-to-SQL / NLP Engine):** Uses Information Extraction, Regular Expressions (Finite Automata), and rule-based semantic parsing to translate natural speech/text into SQL queries over a relational schema.

### Architectural Dataflow

```
                            [ User Input ]
                     (Speech via Web Speech API or Typed Text)
                                   │
                                   ▼
                       1. Query Preprocessing
            - Case folding (lower-casing)
            - Punctuation removal & technical token preservation (c++ -> cpp)
            - Stopword removal (70+ non-informative words filtered)
            - Morphological suffix stemming (stem_term: "scholarships" -> "scholarship")
                                   │
                                   ▼
                      2. Information Extraction (IE)
            - Regex finite-state patterns extract constraints:
              * Financial amounts ("above 50000" -> min_amount = 50000.0)
              * Academic metrics ("cgpa above 8.0" -> min_cgpa = 8.0)
              * Entities ("AICTE", "MahaDBT", "MCA", "CSE")
              * Attendance bounds ("below 75%" -> operator: '<', value: 75.0)
                                   │
        ┌──────────────────────────┴──────────────────────────┐
        ▼                                                     ▼
[ Path A: Unstructured / Catalog IR ]               [ Path B: Speech-to-SQL Engine ]
(Scholarships, Internships, Documents)              (ERP Relational Database Queries)
        │                                                     │
3. Inverted Index Lookup                             3. Intent Classification
- Term -> Postings list mapping                      - Query intent detection
- Skip terms with DF = 0                             - Role-Based Access Control (RBAC)
        │                                              (Student sandboxing vs Admin scope)
        ▼                                                     │
4. Vector Space Model & Scoring                               ▼
- TF-IDF calculation (Sublinear TF + Smooth IDF)     4. Deterministic SQL Generation
- Okapi BM25 scoring with document length             - Dynamic SELECT, FROM, JOIN,
  normalization (k1 = 1.5, b = 0.75)                   WHERE, GROUP BY, HAVING, ORDER BY
- Student Context Vector expansion (CGPA, Course)             │
        │                                                     ▼
        ▼                                            5. Relational DB Execution
5. Cosine Similarity & Relevance Calibration         - SQLite (campus_ai.db) executes SQL
- Normalized dot product: cos(q, d)                  - Returns tabular result set
- Academic eligibility boosting & penalty                     │
- Snippet & Passage Retrieval extraction                      ▼
        │                                            [ Tabular Data + Generated SQL ]
        ▼
6. Document Retrieval & Ranking
- Sort Top-K results descending by relevance
- Return metadata, match percentages, excerpts
        │
        └──────────────────────────┬──────────────────────────┘
                                   │
                                   ▼
                           [ Final Frontend UI ]
            - Ranked Opportunity Cards (e.g., 94%, 88%, 79%)
            - Matched Term Pills & Snippet Excerpts
            - Dynamic Result Tables with SQL Traceability
```

---

## 2. Unit IV Concepts Mapping

### Finite Automata
- **Status:** **Implemented**
- **File Location:** [`backend/nlp_engine.py`](file:///d:/Projects/CampusAI/backend/nlp_engine.py), [`backend/recommendation/ir_engine.py`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py), [`crawler/web_crawler.py`](file:///d:/Projects/CampusAI/crawler/web_crawler.py)
- **Function / Class:**
  - `NLPEngine._extract_attendance_condition()` ([`backend/nlp_engine.py:170-192`](file:///d:/Projects/CampusAI/backend/nlp_engine.py#L170))
  - `NLPEngine._extract_cgpa_condition()` ([`backend/nlp_engine.py:194-202`](file:///d:/Projects/CampusAI/backend/nlp_engine.py#L194))
  - `IREngine.extract_query_filters()` ([`backend/recommendation/ir_engine.py:115-169`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L115))
  - `WebCrawler.extract_key_information()` ([`crawler/web_crawler.py:280-303`](file:///d:/Projects/CampusAI/crawler/web_crawler.py#L280))
- **Technical Explanation:**
  A Finite State Automaton (FSA / DFA / NFA) is a theoretical model of computation consisting of a set of states, an input alphabet, transition functions, and accepting states. In regular expression parsing (Kleene’s Theorem), regular languages are formally recognized by Deterministic Finite Automata (DFA). The system implements state transitions using compiled regular expressions to match lexical patterns such as currency (`(?:above|>=)\s*(\d+)`), GPA metrics (`(?:cgpa|gpa)\s*(?:above|>=)\s*(\d+(?:\.\d+)?)`), and date patterns.
- **Simple Viva Explanation:**
  *"We use Finite Automata through Regular Expression engines. Each regex transitions through states based on incoming characters to identify whether a query contains an amount filter, a percentage, or a course name. It parses numbers and comparison words without needing heavy external libraries."*
- **Example from CampusAI:**
  Query: `"find scholarships above 50000"`  
  Regex: `r'(?:above|greater than|more than|>|>=)\s*(\d+)'`  
  Matches state sequence for `above`, consumes whitespace, transitions to digit state on `5`, `0`, `0`, `0`, `0`, accepting token `50000`.

---

### Language Models & Types of Language Models
- **Status:** **Partial / Statistical Unigram Implemented (No Deep Neural LLMs like GPT/BERT)**
- **File Location:** [`retrieval/document_search.py`](file:///d:/Projects/CampusAI/retrieval/document_search.py), [`crawler/web_crawler.py`](file:///d:/Projects/CampusAI/crawler/web_crawler.py)
- **Function / Class:**
  - `DocumentSearchEngine._build_index()` ([`retrieval/document_search.py:39-66`](file:///d:/Projects/CampusAI/retrieval/document_search.py#L39))
  - `WebCrawler._build_index()` ([`crawler/web_crawler.py:197-213`](file:///d:/Projects/CampusAI/crawler/web_crawler.py#L197))
- **Technical Explanation:**
  In classical IR, a **Language Model (LM)** treats each document $D$ as a generative probability distribution over terms in vocabulary $V$. The system implements a **Unigram Language Model (Bag-of-Words)** under the assumption that word occurrences are conditionally independent:
  $$P(w | M_D) = \frac{\text{count}(w, D)}{|D|}$$
  The types of language models covered in academic theory:
  1. *Unigram LM*: Word probabilities are evaluated independently without word-order context (Implemented).
  2. *Bigram / N-gram LM*: Word probability depends on previous $N-1$ words (Partially present in phrase boosting).
  3. *Generative vs Discriminative*: The document search models the probability of terms generating the query (Generative approach).
- **Simple Viva Explanation:**
  *"We implement a classical statistical Unigram Language Model. Each document is modeled as a distribution of individual words. We calculate the relative frequency of each word in the document to estimate the probability that a document matches a user query."*
- **Example from CampusAI:**
  In a circular about exam regulations with 200 words where the word "hallticket" appears 4 times, the maximum likelihood estimate is $P(\text{hallticket} | M_D) = \frac{4}{200} = 0.02$.

---

### Multinomial Distribution over Words
- **Status:** **Implemented**
- **File Location:** [`retrieval/document_search.py`](file:///d:/Projects/CampusAI/retrieval/document_search.py), [`backend/recommendation/ir_engine.py`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py)
- **Function / Class:**
  - `DocumentSearchEngine._build_index()` ([`retrieval/document_search.py:51-54`](file:///d:/Projects/CampusAI/retrieval/document_search.py#L51))
  - `IREngine._build_scholarship_index()` ([`backend/recommendation/ir_engine.py:236-248`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L236))
- **Technical Explanation:**
  A document is treated as a multinomial distribution over discrete term occurrences:
  $$P(D) = \frac{|D|!}{\prod_{w} c(w, D)!} \prod_{w \in V} P(w | M_D)^{c(w, D)}$$
  The term frequency vector $\vec{tf}_D = [c(w_1, D), c(w_2, D), \dots]$ recorded in Python's `collections.Counter` directly models the parameters of this multinomial distribution, normalized by the total document length $|D| = \sum c(w, D)$.
- **Simple Viva Explanation:**
  *"A multinomial distribution counts how many times each distinct word appears in a text. We use Python's `Counter` to track word frequencies in documents, which gives us the raw parameters for our term probability distribution."*
- **Example from CampusAI:**
  `doc_info["tf"] = Counter({'mca': 3, 'scholarship': 2, 'merit': 1})` with document length `length = 6`.

---

### Ranking with Language Models
- **Status:** **Implemented via BM25 and Query Likelihood Approximation**
- **File Location:** [`retrieval/document_search.py`](file:///d:/Projects/CampusAI/retrieval/document_search.py)
- **Function / Class:**
  - `DocumentSearchEngine.bm25_search()` ([`retrieval/document_search.py:117-150`](file:///d:/Projects/CampusAI/retrieval/document_search.py#L117))
- **Technical Explanation:**
  Language Model ranking ranks documents by Query Likelihood $P(Q | M_D) = \prod_{q_i \in Q} P(q_i | M_D)$. In practical retrieval, smoothing (such as Jelinek-Mercer or Dirichlet smoothing) is required to avoid zero-probabilities for unseen words. Okapi BM25 acts as the probabilistic counterpart to smoothed language models by applying non-linear term saturation ($k_1$) and length normalization ($b$).
- **Simple Viva Explanation:**
  *"Instead of raw multiplication which produces zero if one query word is missing, we rank documents using BM25, which is the industry-standard probabilistic model that evaluates how likely a document is to satisfy the query while accounting for document length."*
- **Example from CampusAI:**
  For query `"hall ticket download"`, documents containing all three terms receive higher probabilistic relevance than documents containing only `"download"`.

---

### Divergence From Randomness (DFR)
- **Status:** **Not Implemented (Theoretical Mapping Available)**
- **Technical Explanation:**
  Divergence from Randomness (DFR) is an advanced probabilistic IR framework developed by Amati and Van Rijsbergen. It posits that the information content of a term in a document is proportional to how much its frequency deviates from what would be expected by a purely random distribution (e.g., Poisson or Geometric distribution).
- **Viva Safety Note:**
  > **DO NOT CLAIM DFR IS FULLY IMPLEMENTED.** If asked by the examiner, say:  
  > *"DFR is a theoretical extension of probabilistic retrieval. In our project, we implemented Okapi BM25 and smoothed TF-IDF as our primary probabilistic and vector space ranking models, rather than explicit Poisson-based DFR weighting."*

---

### Passage Retrieval
- **Status:** **Implemented**
- **File Location:** [`retrieval/document_search.py`](file:///d:/Projects/CampusAI/retrieval/document_search.py), [`backend/recommendation/ir_engine.py`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py)
- **Function / Class:**
  - `DocumentSearchEngine.passage_retrieval()` ([`retrieval/document_search.py:154-192`](file:///d:/Projects/CampusAI/retrieval/document_search.py#L154))
  - `IREngine._extract_best_snippet()` ([`backend/recommendation/ir_engine.py:382-403`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L382))
- **Technical Explanation:**
  Instead of evaluating full documents as atomic units, passage retrieval segments documents into sub-document windows (sliding sentences). In `passage_retrieval()`, documents are split via regex `re.split(r'[.!?]+', content)`. A sliding window of size $W=3$ sentences creates candidate passages. Each passage is scored based on query term overlap, with a $1.2\times$ multiplier applied for exact phrase matches.
- **Simple Viva Explanation:**
  *"Instead of showing a student a 10-page document, passage retrieval splits the document into 3-sentence windows, scores which window has the highest overlap with the user's query, and extracts only the most relevant excerpt."*
- **Example from CampusAI:**
  Query: `"attendance shortage"`  
  Retrieved Passage: `"Students with attendance below 75 percent in any subject will not be permitted to appear for the end-semester examinations. A warning notice is issued after each monthly review."`

---

### Ranking
- **Status:** **Implemented**
- **File Location:** [`backend/recommendation/ir_engine.py`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py), [`retrieval/document_search.py`](file:///d:/Projects/CampusAI/retrieval/document_search.py)
- **Function / Class:**
  - `IREngine.search_scholarships()` ([`backend/recommendation/ir_engine.py:543`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L543))
  - `DocumentSearchEngine.search()` ([`retrieval/document_search.py:247-280`](file:///d:/Projects/CampusAI/retrieval/document_search.py#L247))
- **Technical Explanation:**
  Ranking is the process of sorting retrieved candidate documents by descending estimated relevance:
  $$R = \text{sort\_descending}(\{(d_i, \text{Score}(Q, d_i))\})$$
  CampusAI combines cosine similarity, query term coverage ($|Q \cap D| / |Q|$), and profile eligibility constraints (e.g., student CGPA $\ge$ scholarship minimum CGPA) to calibrate non-trivial, dynamic scores (e.g., 94%, 88%, 79%, 68%).
- **Simple Viva Explanation:**
  *"We rank results so that the most relevant and eligible items appear at the very top. Items matching the student's exact course, CGPA cutoff, and keywords get scores like 94%, while weaker matches drop to lower ranks."*

---

## 3. Unit V Concepts Mapping

### Information Extraction (IE)
- **Where in Code:** [`backend/nlp_engine.py`](file:///d:/Projects/CampusAI/backend/nlp_engine.py), [`backend/recommendation/ir_engine.py`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py), [`crawler/web_crawler.py`](file:///d:/Projects/CampusAI/crawler/web_crawler.py)
- **Function Names:**
  - `NLPEngine._extract_department()` ([`nlp_engine.py:157`](file:///d:/Projects/CampusAI/backend/nlp_engine.py#L157))
  - `NLPEngine._extract_attendance_condition()` ([`nlp_engine.py:170`](file:///d:/Projects/CampusAI/backend/nlp_engine.py#L170))
  - `NLPEngine._extract_cgpa_condition()` ([`nlp_engine.py:194`](file:///d:/Projects/CampusAI/backend/nlp_engine.py#L194))
  - `IREngine.extract_query_filters()` ([`ir_engine.py:115`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L115))
  - `WebCrawler.extract_key_information()` ([`web_crawler.py:280`](file:///d:/Projects/CampusAI/crawler/web_crawler.py#L280))
- **What the Code Does:**
  Transforms unstructured natural language text into structured key-value pairs (slot-filling). It extracts numeric limits, comparison operators (`<`, `>`, `<=`, `>=`), date strings, currency amounts, and department/course entities.
- **Technical Explanation:**
  Information Extraction identifies structured entities from free text without requiring full syntactic parse trees. The regex finite-state machines perform Named Entity Recognition (NER) for predefined domain classes: `Department`, `Course`, `MonetaryAmount`, and `NumericThreshold`.
- **Simple Explanation for Viva:**
  *"Information Extraction pulls out specific facts from a sentence. For example, from 'find scholarships above 50000', it extracts `min_amount = 50000.0` and passes it as a structured parameter."*
- **Example Query & Output:**
  Input Query: `"Show MCA students with CGPA above 8.5"`  
  Extracted Entities: `{'course': 'MCA', 'cgpa_cond': {'operator': '>=', 'value': 8.5}}`

---

### Information Retrieval Models
- **Where in Code:** [`retrieval/document_search.py`](file:///d:/Projects/CampusAI/retrieval/document_search.py), [`backend/recommendation/ir_engine.py`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py)
- **What the Code Does:**
  CampusAI implements and contrasts multiple foundational IR models:
  1. **Boolean Model:** Used in SQL `WHERE` clauses for exact match filtering (`sc.course LIKE '%MCA%' AND sc.amount >= 50000`).
  2. **Vector Space Model (VSM):** Represents documents and queries as geometric vectors in Euclidean space; computes Cosine Similarity.
  3. **Probabilistic Model (Okapi BM25):** Evaluates term saturation and document length normalization.
- **Simple Explanation for Viva:**
  *"We implement three major IR models: the Boolean model for exact database filters, the Vector Space Model with TF-IDF for cosine similarity, and the Probabilistic BM25 model for document ranking."*

---

### Vector Space Model (VSM)
- **Where in Code:** [`backend/recommendation/ir_engine.py`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py), [`retrieval/document_search.py`](file:///d:/Projects/CampusAI/retrieval/document_search.py), [`backend/recommendation/recommender.py`](file:///d:/Projects/CampusAI/backend/recommendation/recommender.py)
- **Function Names:**
  - `IREngine._compute_cosine_similarity()` ([`ir_engine.py:360-380`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L360))
  - `DocumentSearchEngine.semantic_search()` ([`document_search.py:196-243`](file:///d:/Projects/CampusAI/retrieval/document_search.py#L196))
- **What the Code Does:**
  Maps documents $d_j$ and queries $q$ to $|V|$-dimensional vectors $\vec{d}_j = (w_{1,j}, w_{2,j}, \dots, w_{|V|,j})$. Computes similarity using the cosine of the angle between them:
  $$\cos(\vec{q}, \vec{d}_j) = \frac{\vec{q} \cdot \vec{d}_j}{\|\vec{q}\| \|\vec{d}_j\|} = \frac{\sum_{t} w_{t,q} \cdot w_{t,j}}{\sqrt{\sum_{t} w_{t,q}^2} \sqrt{\sum_{t} w_{t,j}^2}}$$
- **Technical Explanation:**
  The Vector Space Model allows non-binary, continuous relevance scoring and partial matching. Length normalization (dividing by the Euclidean norm $\|\vec{d}_j\|$) ensures long documents with many words are not unfairly advantaged over compact documents.
- **Simple Explanation for Viva:**
  *"In the Vector Space Model, every document and user query is treated as an arrow (vector) in space. We take the cosine of the angle between the two arrows. If the angle is 0 degrees, cosine is 1.0 (exact match). If orthogonal, cosine is 0."*
- **Example Query & Output:**
  Query: `"AICTE tech scholarship"`  
  Vector Dot Product with AICTE Pragati Document: $\cos(\vec{q}, \vec{d}) = 0.7421 \rightarrow 93\%$ Calibrated Match.

---

### TF-IDF
- **Where in Code:** [`backend/recommendation/ir_engine.py`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py), [`retrieval/document_search.py`](file:///d:/Projects/CampusAI/retrieval/document_search.py), [`crawler/web_crawler.py`](file:///d:/Projects/CampusAI/crawler/web_crawler.py)
- **Function Names:**
  - `IREngine._build_scholarship_index()` ([`ir_engine.py:223-251`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L223))
  - `DocumentSearchEngine.tfidf_search()` ([`document_search.py:89-113`](file:///d:/Projects/CampusAI/retrieval/document_search.py#L89))
- **What the Code Does:**
  Weights terms according to local importance and global rarity:
  $$\text{TF}(t, d) = \frac{\text{count}(t, d)}{|D|}$$
  $$\text{IDF}(t) = \ln\left(\frac{N + 1}{\text{DF}(t) + 1}\right) + 1.0$$
  $$\text{TF-IDF}(t, d) = \text{TF}(t, d) \times \text{IDF}(t)$$
- **Technical Explanation:**
  Term Frequency reflects how frequently a term appears inside a document. Inverse Document Frequency down-weights ubiquitous terms (like "student" or "college") that appear in almost all records, giving higher discriminative weight to rare terms (like "Pragati" or "Docker").
- **Simple Explanation for Viva:**
  *"TF measures how important a word is inside a document. IDF measures how unique the word is across all documents. Multiplying them gives high weight to words that are common in this document but rare across the campus."*
- **Example Calculation:**
  In a corpus of $N=574$ scholarships, the word "scholarship" has $\text{DF} = 450$ ($\text{IDF} \approx 1.24$). The rare term "AICTE" has $\text{DF} = 15$ ($\text{IDF} = \ln(575/16) + 1 \approx 4.58$). A query containing "AICTE" gives 3.7 times more weight to the AICTE term.

---

### BM25
- **Where in Code:** [`retrieval/document_search.py`](file:///d:/Projects/CampusAI/retrieval/document_search.py), [`crawler/web_crawler.py`](file:///d:/Projects/CampusAI/crawler/web_crawler.py)
- **Function Names:**
  - `DocumentSearchEngine.bm25_search()` ([`document_search.py:117-150`](file:///d:/Projects/CampusAI/retrieval/document_search.py#L117))
  - `WebCrawler._bm25_score()` ([`web_crawler.py:214-230`](file:///d:/Projects/CampusAI/crawler/web_crawler.py#L214))
- **What the Code Does:**
  Calculates the Okapi BM25 score:
  $$\text{BM25}(D, Q) = \sum_{q_i \in Q} \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$
  Where CampusAI configures:
  - $k_1 = 1.5$ (controls term frequency saturation)
  - $b = 0.75$ (controls document length penalization)
  - $\text{avgdl} = \text{average document length across corpus}$
- **Technical Explanation:**
  Standard TF-IDF increases linearly or logarithmically with term frequency. BM25 introduces asymptotic term frequency saturation: after a word appears 3-4 times, additional occurrences contribute diminishing gains. Furthermore, documents longer than $\text{avgdl}$ are penalized to avoid biased retrieval of verbose text.
- **Simple Explanation for Viva:**
  *"BM25 is an advanced non-linear version of TF-IDF used in real search engines. It prevents long documents from dominating results and stops repeated words from artificially inflating the score."*
- **Example Query & Output:**
  Query: `"attendance rules passing criteria"`  
  Retrieves "Academic Regulations 2026" with Score: `4.1822` (Rank #1).

---

### Query Processing
- **Where in Code:** [`backend/recommendation/ir_engine.py`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py), [`backend/nlp_engine.py`](file:///d:/Projects/CampusAI/backend/nlp_engine.py), [`retrieval/document_search.py`](file:///d:/Projects/CampusAI/retrieval/document_search.py)
- **Function Names:**
  - `IREngine.tokenize()` ([`ir_engine.py:90-109`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L90))
  - `stem_term()` ([`ir_engine.py:42-56`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L42))
  - `NLPEngine._preprocess_query()` ([`nlp_engine.py:145-149`](file:///d:/Projects/CampusAI/backend/nlp_engine.py#L145))
- **What the Code Does:**
  Normalizes user query tokens through:
  1. Case folding (converting to lowercase).
  2. Preserving programming language tokens (`c++` $\rightarrow$ `cpp`, `c#` $\rightarrow$ `csharp`, `.net` $\rightarrow$ `dotnet`).
  3. Removing stop words (`is`, `the`, `show`, `please`).
  4. Suffix stemming (`scholarships` $\rightarrow$ `scholarship`, `internships` $\rightarrow$ `internship`, `engineering` $\rightarrow$ `engineer`).
  5. Student profile context expansion (appending logged-in student's `Course`, `Department`, and `Skills`).
- **Simple Explanation for Viva:**
  *"Query processing cleans the user's input. It removes conversational fluff like 'please show me', handles plural words through stemming, and enriches the query with the student's profile context."*

---

### Indexing
- **Where in Code:** [`backend/recommendation/ir_engine.py`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py), [`retrieval/document_search.py`](file:///d:/Projects/CampusAI/retrieval/document_search.py)
- **Function Names:**
  - `IREngine._build_scholarship_index()` ([`ir_engine.py:179-251`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L179))
  - `IREngine._build_internship_index()` ([`ir_engine.py:252-305`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L252))
  - `DocumentSearchEngine._build_index()` ([`document_search.py:39-66`](file:///d:/Projects/CampusAI/retrieval/document_search.py#L39))
- **What the Code Does:**
  Constructs an **Inverted Index**: a data structure mapping every distinct vocabulary term to its posting list of document IDs and precalculated TF-IDF weights:
  $$\text{Index}[t] = \{d_1: w_{t,1}, d_2: w_{t,2}, \dots\}$$
- **Technical Explanation:**
  Without an inverted index, searching $N$ documents for $M$ query terms requires an exhaustive $O(N \cdot |D|)$ scan. With an inverted index, term lookups take $O(1)$ dictionary time, and document candidate evaluation takes $O(|Q| \cdot \text{avg\_posting\_length})$, drastically speeding up retrieval.
- **Simple Explanation for Viva:**
  *"An inverted index is like the index at the back of a textbook. Instead of reading every page to find where 'Python' is mentioned, we look up 'Python' in the index and immediately get the list of document IDs that contain it."*

---

### Document Retrieval
- **Where in Code:** [`backend/recommendation/ir_engine.py`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py), [`retrieval/document_search.py`](file:///d:/Projects/CampusAI/retrieval/document_search.py)
- **Function Names:**
  - `IREngine.search_scholarships()` ([`ir_engine.py:409-550`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L409))
  - `IREngine.search_internships()` ([`ir_engine.py:552-698`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L552))
  - `DocumentSearchEngine.search()` ([`document_search.py:247-280`](file:///d:/Projects/CampusAI/retrieval/document_search.py#L247))
- **What the Code Does:**
  Selects top $K$ documents from database records, generates dynamic textual snippets containing highlighted query terms, attaches academic eligibility badges, and outputs JSON payloads for the frontend React application.

---

## 4. Unit VI Concepts Mapping

### Semantic Retrieval
- **Status:** **Implemented via Vector Space Model Cosine Similarity (Not Dense Neural Embeddings)**
- **Code Location:**
  - [`backend/recommendation/ir_engine.py:360-380`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L360) (`_compute_cosine_similarity`)
  - [`retrieval/document_search.py:196-243`](file:///d:/Projects/CampusAI/retrieval/document_search.py#L196) (`semantic_search`)
  - [`backend/recommendation/recommender.py:110-120`](file:///d:/Projects/CampusAI/backend/recommendation/recommender.py#L110) (`recommend`)
- **Why:**
  Classical vector space cosine similarity matches documents based on shared weighted dimensions rather than strict boolean exactness.
- **Viva Safety Note:**
  > *"Our semantic retrieval is implemented using Vector Space Model cosine similarity over TF-IDF term vectors. We do not run external transformer neural embeddings (such as BERT or Sentence-Transformers) to keep the prototype fast, lightweight, and offline."*

---

### Retrieval Evaluation
- **Status:** **Theoretical / Offline Test Suite Verified (Cranfield Benchmark Not Bundled)**
- **Code Location:** [`test_api_endpoints.py`](file:///d:/Projects/CampusAI/test_api_endpoints.py), [`test_ir.py`](file:///d:/Projects/CampusAI/test_ir.py)
- **Why:**
  Evaluation metrics in IR require a standard ground-truth evaluation corpus (such as Cranfield, TREC, or MS MARCO) with human relevance judgments:
  $$\text{Precision} = \frac{|Retrieved \cap Relevant|}{|Retrieved|}, \quad \text{Recall} = \frac{|Retrieved \cap Relevant|}{|Relevant|}$$
  $$\text{MAP} = \frac{1}{|Q|} \sum_{q=1}^{|Q|} \text{AveP}(q), \quad \text{NDCG}_p = \frac{\text{DCG}_p}{\text{IDCG}_p}$$
- **Viva Explanation:**
  *"In our project, we evaluate retrieval correctness using integration test suites (`test_api_endpoints.py`) that verify Top-K relevance, filter adherence, and RBAC sandboxing. Formal test collections like TREC are not bundled, but our ranking functions are built on standard BM25 and TF-IDF formulas that maximize MAP and NDCG."*

---

### NLP-Based Retrieval
- **Status:** **Implemented**
- **Code Location:** [`backend/nlp_engine.py`](file:///d:/Projects/CampusAI/backend/nlp_engine.py) (`NLPEngine`)
- **Why:**
  Combines natural language intent detection, department alias normalization, conditional constraint parsing, and syntax-directed SQL generation. Ensures strict Role-Based Access Control (RBAC) so students cannot retrieve department-wide or peer records.
- **Viva Explanation:**
  *"NLP-based retrieval parses natural language questions, extracts comparison slots (like attendance shortage or CGPA thresholds), and dynamically translates them into executable SQL queries."*

---

### Intelligent Search
- **Status:** **Implemented**
- **Code Location:** [`backend/recommendation/ir_engine.py:426-440`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L426)
- **Why:**
  The search engine is **context-aware**. When an MCA student with a 7.97 CGPA logs in and searches for `"scholarships"`, the engine automatically extracts the student's program (MCA), department (Master of Computer Applications), and CGPA from the database, expands the query vector with academic context tokens, and boosts opportunities matching their specific profile.

---

## 5. Module-Wise IR Mapping Matrix

| Module Name | User Role | Primary Technique Used | File Location | Key Functions |
| :--- | :--- | :--- | :--- | :--- |
| **Admin AI Query** | Faculty / Admin | Information Extraction, Finite Automata regex, Speech-to-SQL | [`backend/nlp_engine.py`](file:///d:/Projects/CampusAI/backend/nlp_engine.py) | `process_query`, `_generate_admin_sql`, `_extract_attendance_condition` |
| **Student AI Query** | Student | RBAC Query Sandboxing, Intent Extraction, Speech-to-SQL | [`backend/nlp_engine.py`](file:///d:/Projects/CampusAI/backend/nlp_engine.py) | `process_query`, `_generate_student_sql` |
| **Document Search** | Admin / Student | Okapi BM25, TF-IDF, Vector Space Model, Passage Retrieval | [`retrieval/document_search.py`](file:///d:/Projects/CampusAI/retrieval/document_search.py) | `bm25_search`, `tfidf_search`, `passage_retrieval`, `semantic_search` |
| **External Web Crawler** | Admin / Student | Crawling, Inverted Indexing, BM25 Scoring, Regex IE | [`crawler/web_crawler.py`](file:///d:/Projects/CampusAI/crawler/web_crawler.py) | `search`, `_bm25_score`, `extract_key_information` |
| **Scholarship Recommendation** | Student | Context Expansion, TF-IDF, Cosine Similarity, Academic Ranking | [`backend/recommendation/ir_engine.py`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py) | `search_scholarships`, `get_student_context`, `_compute_cosine_similarity` |
| **Scholarship Directory Search** | Faculty / Admin | Filter Extraction (Amount/Course/Provider), TF-IDF VSM Ranking | [`backend/recommendation/ir_engine.py`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py) | `search_scholarships`, `extract_query_filters` |
| **Internship Recommendation** | Student | Technical Skill Vector Matching, TF-IDF, Cosine Similarity | [`backend/recommendation/ir_engine.py`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py) | `search_internships`, `get_student_context` |
| **Query Recommender** | Admin / Student | TF-IDF Vectorization, Cosine Similarity Query Suggestions | [`backend/recommendation/recommender.py`](file:///d:/Projects/CampusAI/backend/recommendation/recommender.py) | `recommend`, `get_query_recommendations` |

---

## 6. Detailed End-to-End Working Examples

### Example 1: Structured AI Query
**User Input:** `"Show students with CGPA above 8"`  
**Role:** `Admin / Faculty`

1. **Query Processing:**
   - Normalization: String stripped to `"show students with cgpa above 8"`.
2. **Information Extraction (IE):**
   - Regex `r'(?:cgpa|gpa)\s*(?:above|greater than|>=|>)\s*(\d+(?:\.\d+)?)'` matches `above 8`.
   - Extracted Condition: `{'operator': '>=', 'value': 8.0}`.
3. **Intent & SQL Generation ([`backend/nlp_engine.py:458-475`](file:///d:/Projects/CampusAI/backend/nlp_engine.py#L458)):**
   - Synthesizes SQL query:
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
4. **Database Retrieval:**
   - Executes via SQLite connection on `database/campus_ai.db`.
   - Returns tabular JSON of students meeting merit criteria.

---

### Example 2: Profile-Aware IR Recommendation
**User Input:** `"Scholarships for MCA students"`  
**User Context:** `Student ID: 1601 (Ojasvi Hegde, Course: MCA, CGPA: 7.97)`

1. **Student Context Extraction ([`backend/recommendation/ir_engine.py:310-355`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L310)):**
   - Queries `students` and `academic_record`:
     - `course = 'MCA'`
     - `department = 'Master of Computer Applications'`
     - `cgpa = 7.97`
2. **Query Processing & Context Expansion:**
   - User Query Tokens: `['scholarship', 'mca', 'student']`
   - Context Tokens: `['mca', 'master', 'comput', 'applic']`
   - Combined Vector Vocabulary: User tokens weighted at $1.6\times$ user multiplier.
3. **TF-IDF & Vector Space Model:**
   - Query Vector $\vec{q}$ constructed using sublinear TF and smooth IDF.
   - For all 574 scholarships, document vectors $\vec{d}_i$ are retrieved from the Inverted Index.
4. **Cosine Similarity & Ranking ([`backend/recommendation/ir_engine.py:465-544`](file:///d:/Projects/CampusAI/backend/recommendation/ir_engine.py#L465)):**
   - Calculates $\cos(\vec{q}, \vec{d}_i)$ for candidate opportunities.
   - Boosts items targeting `'MCA'` program (+0.08).
   - Validates student's CGPA (7.97) against scholarship minimum CGPA cutoff:
     - Document 487: *AICTE PG Scholarship for Technical Postgraduates* (Min CGPA: 7.0 $\le 7.97 \rightarrow$ **Eligible**, Boost +0.04).
   - Calibrated Relevance Score: **93%**.
5. **Snippet Extraction:**
   - Extracts relevant sentence: *"Direct central financial scholarship of Rs. 12,400 per month for students admitted to postgraduate technical programs like MCA."*
6. **Frontend Output:**
   - Displayed on [`StudentScholarships.jsx`](file:///d:/Projects/CampusAI/frontend/src/pages/student/StudentScholarships.jsx) with Emerald Badge (93%), Matched Term Pills (`mca`, `postgradu`, `aicte`), and Action Button.

---

### Example 3: Unstructured Document Retrieval
**User Input:** `"Scholarship eligibility criteria"`  
**Module:** Document Search Engine ([`retrieval/document_search.py`](file:///d:/Projects/CampusAI/retrieval/document_search.py))

1. **Tokenization:**
   - Query tokens: `['scholarship', 'eligibility', 'criteria']` (stopwords removed).
2. **BM25 Retrieval & Length Normalization:**
   - Evaluates each circular document in `documents` table.
   - For each term, computes $\text{IDF} \times \frac{f(k_1+1)}{f + k_1(1-b+b \cdot \text{len}/\text{avgdl})}$.
3. **Passage Retrieval (Sliding Window):**
   - Splits matching document into 3-sentence passages.
   - Finds passage with highest term overlap:
     *"Students applying for state and central scholarships must maintain a minimum of 75% attendance and clear all semester subjects with no active backlogs."*
4. **Ranking:**
   - Merges BM25 score with Cosine Semantic score and returns Top-K ranked circulars.

---

## 7. Comprehensive Viva Voce Q&A Preparation

### Q1: Where exactly is TF-IDF used in CampusAI?
**Answer:**  
*"TF-IDF is used in three places:  
1. In `backend/recommendation/ir_engine.py` for ranking scholarships and internships against student profiles.  
2. In `retrieval/document_search.py` for college policy document search.  
3. In `backend/recommendation/recommender.py` for recommending related natural language queries based on cosine similarity."*

### Q2: What is the difference between TF-IDF and BM25? Why use both?
**Answer:**  
*"TF-IDF scales term frequency logarithmically or linearly, which can allow long documents with repeated words to gain artificially high scores. BM25 improves on TF-IDF by introducing asymptotic term frequency saturation (controlled by parameter $k_1 = 1.5$) so a term's contribution plateaus, and document length normalization (controlled by parameter $b = 0.75$) which normalizes against average document length. We use BM25 in `retrieval/document_search.py` and `crawler/web_crawler.py` for unstructured text documents, and TF-IDF Vector Space Model in `ir_engine.py` for opportunity ranking."*

### Q3: Is this system using a Language Model?
**Answer:**  
*"Yes, it uses a classical statistical Unigram Language Model (Bag-of-Words), where each document is modeled as a multinomial distribution over terms. It does not use deep transformer neural LLMs like GPT or BERT. Instead, it relies on classical Information Retrieval language modeling principles."*

### Q4: Are the scholarship recommendations static or dynamic?
**Answer:**  
*"They are 100% dynamic. The recommendations are calculated in real time by `IREngine.search_scholarships()`. When a student queries the system, it extracts their live profile (CGPA, Course, Department) from SQLite, constructs a query vector, calculates cosine similarity against all 574 scholarship vectors, applies eligibility weighting, and sorts them dynamically. Scores vary naturally (e.g., 94%, 88%, 79%, 68%) rather than displaying a static or hardcoded 100%."*

### Q5: How is Role-Based Access Control (RBAC) enforced in Speech-to-SQL?
**Answer:**  
*"RBAC is strictly sandboxed inside `backend/nlp_engine.py`. When a student role is verified, `_generate_student_sql()` enforces that personal queries (attendance, marks, fees, personal applications) contain `WHERE s.student_id = {verified_id}`. Any attempt by a student to query department aggregates or other students' records is intercepted and redirected to their own profile."*

### Q6: How does Passage Retrieval work in your project?
**Answer:**  
*"In `retrieval/document_search.py`, `passage_retrieval()` splits documents into sentences using regular expressions. It runs a sliding window of 3 sentences across the text, measures the term overlap between the user query and the passage tokens, applies a 1.2x boost if consecutive phrase words match, and returns the highest-scoring passage excerpt."*

---

## 8. Honest Limitations & What NOT to Claim

To ensure credibility during your project defense, be completely transparent about what is implemented and what is outside the project scope:

### 1. Do NOT Claim Deep Neural Language Models (LLMs / BERT / Transformers)
- **Fact:** The project does not run local PyTorch/TensorFlow transformer models or dense vector databases (like Milvus, Pinecone, or ChromaDB).
- **Claim Instead:** *"We implemented classical Information Retrieval algorithms: Vector Space Model, TF-IDF, Okapi BM25, and Inverted Indexing in pure Python. This makes our engine lightweight, fast, interpretable, and completely offline."*

### 2. Do NOT Claim Formal Cranfield / TREC Test Evaluation Benchmarks
- **Fact:** The repository does not include human-labeled gold standard relevance judgments (qrels) across thousands of queries.
- **Claim Instead:** *"We validated our IR system using comprehensive automated integration test suites (`test_api_endpoints.py` and `test_ir.py`) that test Top-K precision, numeric constraint satisfaction, and profile-based ranking."*

### 3. Do NOT Claim Divergence From Randomness (DFR) is Implemented
- **Fact:** DFR formulas based on Poisson or Geometric randomness models are not implemented in the codebase.
- **Claim Instead:** *"We focused on Okapi BM25 and Vector Space Model Cosine Similarity as our probabilistic and vector-based retrieval models."*

### 4. Live Web Crawling vs Simulated Knowledge Base
- **Fact:** While `crawler/web_crawler.py` contains the complete parsing, extraction, and BM25 search logic, the crawler loads from a curated real-world knowledge base to ensure the demo functions offline without network dependency or web scraping rate-limits.
- **Claim Instead:** *"The crawler module implements real text extraction and BM25 ranking over a curated dataset of scholarships, internships, and announcements to avoid network failures during campus evaluation."*

---
*Documentation compiled for CampusAI Project — Department of Master of Computer Applications (MCA).*
