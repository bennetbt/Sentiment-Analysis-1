import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from fastapi import FastAPI
from pydantic import BaseModel

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

class TextData(BaseModel):
    text: str

app = FastAPI()

@app.post("/sentiment")
async def analyze_sentiment(text_data: TextData):
    text = text_data.text
    scores = sia.polarity_scores(text)
    score = scores['compound']
    print("word: ", text, "score: ", score)
    if score > 0:
        sentiment = 'positive'
    elif score < 0:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    return {"sentiment": sentiment, "score": score}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1171)
