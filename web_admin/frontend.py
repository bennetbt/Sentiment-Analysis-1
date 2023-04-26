from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import requests
import psycopg2
from datetime import datetime

class TextData(BaseModel):
    text: str

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    conn = psycopg2.connect(host='db', database='Sentimental_Analysis', user='pgsqldev4', password='enter')
    cur = conn.cursor()
    cur.execute("SELECT * FROM sentiments ORDER BY Timestamp DESC")
    results = cur.fetchall()
    cur.close()
    conn.close()
    pos_count, neg_count, neu_count = 0, 0, 0
    score_total = 0.0

    html_content = """
<html>
    <head>
        <title>Sentiment Analyzer</title>
        <style>
            div.centered {
                text-align: center;
            }
                        div.header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: #f2f2f2;
                padding: 10px;
                position: relative;
                height: 50px;
            }
            button.admin {
                background-color: #4CAF50;
                color: white;
                padding: 10px 18px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-right: 10px;
                position: absolute;
                top: 50px;
                right: 50px;
            }
            button.admin:last-of-type {
                margin-right: 0; /* remove margin for the last button */
                        }
        </style>
        <script>
function sendText() {
    var text = document.getElementById("text").value;
    fetch("/sentiment", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({text: text})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // update the HTML with the response data
        document.getElementById("sentence").innerHTML = "Sentence or Paragraph: " + text;
        document.getElementById("sentiment").innerHTML = "Sentiment: " + data.sentiment;
        document.getElementById("score").innerHTML = "Score: " + data.score;
        // reload the webpage to show updated results
        window.location.reload();
    })
    .catch(error => console.error(error));
}
        </script>
</head>
    <body>
       <div class="centered" style="background-color: #f2f2f2; padding: 20px;">
    <h1 style="text-align: center;">Welcome to Sentiment Analyzer</h1>
    <button class="admin" onclick="logout()">Logout</button>
<script>
    function logout() {
        window.location.href = 'http://localhost:1172';
    }
</script>
</script>
<div id="Statistics">
    <h2 style="text-align:center;">Stats:</h2>
    <table style="border: 1px solid black; margin: auto;">
        <tr>
            <th style="border: 1px solid black; text-align:center;">Avg Score</th>
            <th style="border: 1px solid black; text-align:center;">Pos Statements</th>
            <th style="border: 1px solid black; text-align:center;">Pos %</th>
            <th style="border: 1px solid black; text-align:center;">Neg Statements</th>
            <th style="border: 1px solid black; text-align:center;">Neg %</th>
            <th style="border: 1px solid black; text-align:center;">Neu Statements</th>
            <th style="border: 1px solid black; text-align:center;">Neu %</th>
        </tr>
        """
    for row in results:
            score_total += float(row[4])
            if row[3] == "positive":
                pos_count += 1
            elif row[3] == "negative":
                neg_count += 1
            else:
                neu_count += 1

    total_count = pos_count + neg_count + neu_count
    if total_count > 0:
            pos_percentage = round((pos_count / total_count) * 100, 2)
            neg_percentage = round((neg_count / total_count) * 100, 2)
            neu_percentage = round((neu_count / total_count) * 100, 2)
            average_score = round((score_total / total_count), 2)
    html_content += f"""
        <tr>
            <td style="border: 1px solid black; text-align:center;">{average_score}</td>
            <td style="border: 1px solid black; text-align:center;">{pos_count}</td>
            <td style="border: 1px solid black; text-align:center;">{pos_percentage}%</td>
            <td style="border: 1px solid black; text-align:center;">{neg_count}</td>
            <td style="border: 1px solid black; text-align:center;">{neg_percentage}%</td>
            <td style="border: 1px solid black; text-align:center;">{neu_count}</td>
            <td style="border: 1px solid black; text-align:center;">{neu_percentage}%</td>
        </tr>
    """
    html_content += """
    </table>
<p></p>	
<input type="image" img align="top" src="https://www.freecodecamp.org/news/content/images/2020/09/wall-5.jpeg" width="280" height="200">
    <div style="text-align:center">
        <h2>Enter a sentence or paragraph:</h2>
        <form onsubmit="sendText(); return false;">
            <textarea id="text" style="width: 80%; height: 150px; padding: 10px; border: 2px solid #ccc; border-radius: 4px;"></textarea>
            <br><br>
            <button type="submit" style="background-color: #4CAF50; color: white; padding: 10px 18px; border: none; border-radius: 4px; cursor: pointer;">Classify Text</button>
        </form>
            <div id="result">
                <p id="sentence"></p>
                <p id="sentiment"></p>
                <p id="score"></p>
            </div>
            <div id="history">
<h2 style="text-align:center;">Previous Results:</h2>
<table style="border: 1px solid black; margin: auto;">
    <tr>
        <th style="border: 1px solid black; text-align:center;">ID</th>
        <th style="border: 1px solid black; text-align:center;">Timestamp</th>
        <th style="border: 1px solid black; text-align:center;">Text Searched</th>
        <th style="border: 1px solid black; text-align:center;">Sentiment Result</th>
        <th style="border: 1px solid black; text-align:center;">Percentage Score</th>
                    </tr>
                    """
    for row in results:
     ID= row[0]
     timestamp = row[1]
     text = row[2]
     sentiment = row[3]
     score = row[4]
     html_content += f"""
<tr>
  <td style="border: 1px solid black; text-align:center;">{ID}</td>
  <td style="border: 1px solid black; text-align:center;">{timestamp}</td>
  <td style="border: 1px solid black; text-align:center;">{text}</td>
  <td style="border: 1px solid black; text-align:center;">{sentiment}</td>
  <td style="border: 1px solid black; text-align:center;">{score}</td>
  <td style="border: 1px solid black; text-align:center;">
    <form action="/deleteSentiment/{ID}" method="post">
      <input type="hidden" name="_method" value="post">
      <button type="submit">Delete</button>
    </form>
  </td>
  <td style="border: 1px solid black; text-align:center;">
    <form action="/editSentiment/{ID}" method="post">
      <input type="hidden" name="_method" value="post">
      <button type="submit">Edit Sentiment</button>
    </form>
  </td>
</tr>
                """
    html_content += """
                </table>
            </div>
        </div>
</div>
</body>
</html>
"""
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/sentiment")
async def analyze_sentiment(text_data: TextData):
    text = text_data.text
    r = requests.post("http://api:1171/sentiment", json={"text": text})
    result = r.json()
    sentiment = result['sentiment']
    score = result['score']*100
    print("Result : ",text,sentiment,score)
    conn = psycopg2.connect(host='db', database='Sentimental_Analysis', user='pgsqldev4', password='enter')
    cur = conn.cursor()
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO sentiments ( Timestamp, Text_Searched, Sentiment_Result, Percentage_Score) VALUES ( %s, %s, %s, %s)", ( dt_string, text, sentiment, score))
    conn.commit()
    cur.close()
    conn.close()
    return {"sentiment": sentiment, "score": score}



@app.post("/deleteSentiment/{ID}")
async def delete_sentiment(ID: int):
    conn = psycopg2.connect(host='db', database='Sentimental_Analysis', user='pgsqldev4', password='enter')
    cur = conn.cursor()
    cur.execute("DELETE FROM sentiments WHERE ID = %s", (ID,))
    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse(url="http://localhost:1173", status_code=303)


@app.post("/editSentiment/{ID}", response_class=HTMLResponse)
async def edit_sentiment(request: Request, ID: int):
    conn = psycopg2.connect(host='db', database='Sentimental_Analysis', user='pgsqldev4', password='enter')
    cur = conn.cursor()
    cur.execute("SELECT * FROM sentiments WHERE ID = %s", (ID,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result is None:
        # Handle the case where no result is returned from the query
        return HTMLResponse(content="No results found for ID {}".format(ID), status_code=404)

    html_content = f"""
        <html>
            <head>
                <title>Edit Sentiment Result</title>
                <style>
                    div.centered {{
                        text-align: center;
                    }}
                </style>
                <script>
                    function sendText(sentiment) {{
                        var text = document.getElementById("text").value;
                        fetch("/sentiment", {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json'
                            }},
                            body: JSON.stringify({{text: text}})
                        }})
                        .then(response => response.json())
                        .then(data => {{
                            console.log(data);
                            var select = document.getElementById("sentiment");
                            var options = select.options;
                            for (var i = 0; i < options.length; i++) {{
                                var option = options[i];
                                if (option.value === data.sentiment) {{
                                    option.selected = true;
                                }}
                            }}
                        }})
                    }};
                </script>
            </head>
            <body>
                <div class="centered">
                    <form method="POST" action="/updateSentiment/{ID}">
                        <label for="text">Text:</label>
                        <input type="text" name="text" id="text" value="{result[2]}" size="50" /><br>
                        <label for="sentiment">Sentiment:</label>
                        <select id="sentiment" name="sentiment">
                            <option value="positive" {'selected' if result[3] == "positive" else ''}>positive</option>
                            <option value="negative" {'selected' if result[3] == "negative" else ''}>negative</option>
                            <option value="neutral" {'selected' if result[3] == "neutral" else ''}>neutral</option>
                        </select>
                        <input type="hidden" name="initial_sentiment" value="{result[3]}">
                        <br>
                        <input type="submit" value="Save Changes">
                    </form>
                </div>
            </body>
        </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/updateSentiment/{ID}", response_class=RedirectResponse)
async def save_edited_sentiment(request: Request, ID: int, sentiment: str = Form(...), initial_sentiment: str = Form(...)):
    conn = psycopg2.connect(host='db', database='Sentimental_Analysis', user='pgsqldev4', password='enter')
    cur = conn.cursor()
    cur.execute("UPDATE sentiments SET Sentiment_Result = %s WHERE ID = %s", (sentiment, ID,))
    conn.commit()
    cur.close()
    conn.close()

    return RedirectResponse(url="http://localhost:1173", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1173)