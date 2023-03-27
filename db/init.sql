CREATE TABLE IF NOT EXISTS sentiments (
    ID SERIAL PRIMARY KEY,
    Timestamp TIMESTAMP NOT NULL,
    Text_Searched VARCHAR(255) NOT NULL,
    Sentiment_Result VARCHAR(255) NOT NULL,
    Percentage_Score NUMERIC(5,2) NOT NULL
);
