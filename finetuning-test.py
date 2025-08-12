
from pathlib import Path
import dspy
import pandas as pd
from app.core import config

lm = dspy.LM(
    api_key=config.GROQ_API_KEY,
    model=config.DEFAULT_MODEL,
    temperature=config.DEFAULT_TEMPERATURE,
    max_tokens=config.DEFAULT_MAX_TOKENS
)
dspy.configure(lm=lm)

TRAIN_DATA_DIR = Path("train-data")
TRAIN_DATA_FILE = TRAIN_DATA_DIR / "train_data.csv"
trainlist = []

if not TRAIN_DATA_DIR.exists():
    TRAIN_DATA_DIR.mkdir(exist_ok=True)

if not TRAIN_DATA_FILE.exists():
    print(f"No training data file found at {TRAIN_DATA_FILE}")
    exit(1)

df = pd.read_csv(TRAIN_DATA_FILE, header=None)
if df.empty:
    print("No training data found in train_data.csv")
    exit(1)

for question, answer in df.values:
    # print(question, answer)
    trainlist.append(dspy.Example(question=question, answer=answer).with_inputs("question"))


class QA(dspy.Signature):
    """Answer the given question based on your training."""
    question = dspy.InputField(desc="User question about names of things and people")
    answer = dspy.OutputField(desc="an answer to the question usually one word")

# 3. Create a module
qa_module = dspy.Predict(QA)
print(qa_module(question="What is the name of the student?").answer)
# 4. Training dataset
train_data = trainlist
print(train_data)
# 5. Optimizer (prompt fine-tuning)
optimizer = dspy.teleprompt.BootstrapFewShot(metric=dspy.evaluate.answer_exact_match)
optimized_qa = optimizer.compile(student=qa_module, trainset=train_data)
# # 6. Use the optimized model
print(optimized_qa(question="What is the name of the student"))