"""
TF-IDF based Recommendation System
Used for Campus ERP query recommendations

This module recommends related queries using:
- TF-IDF Vectorization
- Cosine Similarity

It dynamically finds similar queries instead of using
hardcoded recommendations inside NLP Engine.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Recommender:

    def __init__(self):

        # Training queries / knowledge base
        self.queries = [

            # Attendance
            "Show students with low attendance",
            "Show attendance below 75 percent",
            "Generate attendance warning list",
            "Department wise attendance comparison",
            "Show students with high attendance",
            "Correlation between attendance and CGPA",

            # Academic
            "Show top students by CGPA",
            "Show highest marks students",
            "Show average marks department wise",
            "Show department wise CGPA comparison",
            "Show failed students",
            "Show weak subjects",
            "Show subject wise performance",

            # Fees
            "Show pending fees",
            "Show fee defaulters",
            "Fee collection summary",
            "Department wise fee collection",

            # Scholarship
            "Show scholarship details",
            "Show approved scholarships",
            "Show eligible scholarship students",
            "Show scholarship distribution",

            # Internship
            "Show internship opportunities",
            "Show highest stipend internships",
            "Show internships by domain",
            "Show internship deadlines",

            # Department
            "Show department list",
            "Show all departments",
            "Show student count by department",
            "Show faculty distribution",
            "Department wise student analysis",

            # Student personal queries
            "Show my attendance",
            "Show my marks",
            "Show my scholarship",
            "Show my fees",
            "Show my academic performance",
            "Suggest improvements for my studies"
        ]


        # Convert queries into TF-IDF vectors
        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )


        self.matrix = self.vectorizer.fit_transform(
            self.queries
        )


    def recommend(
            self,
            query,
            role="admin",
            top_k=5
    ):

        """
        Find similar queries using cosine similarity.
        """

        query_vector = self.vectorizer.transform(
            [query]
        )


        similarity_scores = cosine_similarity(
            query_vector,
            self.matrix
        )[0]


        # Sort highest similarity first
        ranked_indexes = similarity_scores.argsort()[::-1]


        recommendations = []


        for index in ranked_indexes:

            suggestion = self.queries[index]


            # Avoid showing irrelevant zero similarity results
            if similarity_scores[index] <= 0:
                continue


            # Student should only receive personal suggestions
            if role == "student":

                if "my " not in suggestion.lower() and "suggest" not in suggestion.lower():
                    continue


            recommendations.append(suggestion)


            if len(recommendations) >= top_k:
                break


        return recommendations



    def get_recommendations(
            self,
            query,
            target=None,
            intent=None,
            role="admin"
    ):
        """
        Function called by NLP Engine.

        target and intent are accepted for future improvements.
        """

        return self.recommend(
            query=query,
            role=role,
            top_k=5
        )