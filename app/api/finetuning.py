
from pathlib import Path
import dspy
import pandas as pd
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.core import config, setup_logging
from app.models.finetuning_schemas import TrainingResponse, PredictionRequest, PredictionResponse

logger = setup_logging()
router = APIRouter()

# lm = dspy.LM(
#     api_key=config.GROQ_API_KEY,
#     model=config.DEFAULT_MODEL,
#     temperature=config.DEFAULT_TEMPERATURE,
#     max_tokens=config.DEFAULT_MAX_TOKENS
# )
# dspy.configure(lm=lm)

TRAIN_DATA_DIR = Path("train-data")

# Global variable to store the optimized model
optimized_qa = None


class QA(dspy.Signature):
    """Answer questions based on training data"""
    question = dspy.InputField(desc="User question")
    answer = dspy.OutputField(desc="Answer to the question")


def load_training_data():
    """Load all CSV files from train-data directory"""
    if not TRAIN_DATA_DIR.exists():
        TRAIN_DATA_DIR.mkdir(exist_ok=True)
        logger.info(f"Created train-data directory at {TRAIN_DATA_DIR}")
    
    trainlist = []
    processed_files = []
    
    for csv_file in TRAIN_DATA_DIR.glob("*.csv"):
        try:
            df = pd.read_csv(csv_file, header=None)
            if not df.empty:
                for question, answer in df.values:
                    trainlist.append(dspy.Example(question=question, answer=answer).with_inputs("question"))
                processed_files.append(csv_file.name)
                logger.info(f"Processed {csv_file.name}: {len(df)} examples")
        except Exception as e:
            logger.error(f"Error processing {csv_file.name}: {e}")
    
    return trainlist, processed_files


@router.post("/train", response_model=TrainingResponse)
async def train_model():
    """Train the model using all CSV files in the train-data directory"""
    global optimized_qa
    
    try:
        trainlist, processed_files = load_training_data()
        print(trainlist,processed_files)
        
        if not trainlist:
            raise HTTPException(
                status_code=404,
                detail="No training data found in train-data directory"
            )
        
        # Create and optimize the model
        qa_module = dspy.Predict(QA)
        optimizer = dspy.BootstrapFewShot()
        optimized_qa = optimizer.compile(student=qa_module, trainset=trainlist)
        
        return TrainingResponse(
            files_processed=processed_files,
            examples_count=len(trainlist),
            status="success",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Training error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Training failed: {str(e)}"
        )


@router.post("/predict", response_model=PredictionResponse)
async def get_prediction(request: PredictionRequest):
    """Get a prediction for a question using the trained model"""
    if not optimized_qa:
        raise HTTPException(
            status_code=400,
            detail="Model not trained. Please call /train endpoint first"
        )
    
    try:
        result = optimized_qa(question=request.question)
        return PredictionResponse(
            question=request.question,
            answer=result.answer,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )