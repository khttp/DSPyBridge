from docx import Document
import dspy
from app.core import config
from sentence_transformers import SentenceTransformer

lm=dspy.LM(
    model = config.DEFAULT_MODEL,
    temperature = 0.7,
    api_key=config.GROQ_API_KEY,
)
dspy.configure(lm=lm)
corpus = []
def read_docx(filepath):
    doc = Document(filepath)
    text = "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])
    return text

# Then add to your corpus manually
docx_text = read_docx("docs\Roaming_SummerOffers.docx")
corpus.append(docx_text) 

hf_model = SentenceTransformer("all-MiniLM-L6-v2")  # fast & free

def hf_embed(texts):
    if isinstance(texts, str):
        texts = [texts]
    return hf_model.encode(texts, convert_to_numpy=True).tolist()


retriever = dspy.retrievers.Embeddings(
    embedder=hf_embed,
    corpus=corpus,
    k=3  # number of docs to retrieve
)
class RAG_Segnature(dspy.Signature):
    """RAG Signature"""
    question = dspy.InputField(desc="User question about telecomunication services for vodafone")
    context = dspy.InputField(desc="Retrieved context")
    answer = dspy.OutputField(desc="Final answer")


class RAG(dspy.Module):
    def __init__(self):
        super().__init__()
        self.retrieve = retriever
        self.answer = dspy.Predict(RAG_Segnature)

    def forward(self, question):
        # Retrieve top-k docs
        docs = self.retrieve(question)
        context = "\n".join(docs)

        # Predict answer with retrieved context
        return self.answer(context=context, question=question)
rag = RAG()

# Ask a question
response = rag("Hi i want to extent my roaming till 6/6/2025")
print("Answer:", response.answer)