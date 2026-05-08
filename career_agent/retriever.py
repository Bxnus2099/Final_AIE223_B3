import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# Load Dataset
# =========================
df = pd.read_csv("data/jobs.csv")

# =========================
# Load Multilingual Model
# =========================
model = SentenceTransformer(
    'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
)

# =========================
# Create Text Corpus
# =========================
corpus = (
    df["job_title"] + " " +
    df["skills"] + " " +
    df["description"]
).tolist()

# =========================
# Create Embeddings
# =========================
corpus_embeddings = model.encode(corpus)

# =========================
# Semantic Search
# =========================
def search_jobs(query, top_k=3):

    # Encode query
    query_embedding = model.encode([query])

    # Cosine similarity
    sims = cosine_similarity(
        query_embedding,
        corpus_embeddings
    )[0]

    # Threshold
    dynamic_threshold = max(sims) * 0.8
    absolute_threshold = 0.45

    threshold = max(
        dynamic_threshold,
        absolute_threshold
    )

    # Top results
    top_idx = [
        i for i in sims.argsort()[::-1]
        if sims[i] >= threshold
    ][:top_k]

    results = []

    for idx in top_idx:

        job = df.iloc[idx].to_dict()

        job["score"] = float(sims[idx])

        results.append(job)

    return results, sims[top_idx]