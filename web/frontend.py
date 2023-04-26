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
            #login-form {
                display: none;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 300px;
                padding: 20px;
                background-color: #f2f2f2;
                border-radius: 5px;
                box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.3);
            }
            #login-form label {
                display: block;
                margin-bottom: 10px;
            }
            #login-form input {
                display: block;
                margin-bottom: 20px;
                width: 100%;
                padding: 10px;
                border-radius: 5px;
                border: none;
                box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
            }
            #login-form button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 18px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
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
    <button class="admin" onclick="showLoginForm()">Admin Login</button>
<div id="login-form">
  <h2>Login</h2>
  <form onsubmit="login(); return false;">
    <label for="username">Username:</label>
    <input type="text" id="username" name="username">
    <label for="password">Password:</label>
    <input type="password" id="password" name="password">
    <br><br>
    <button type="submit" style="background-color: #4CAF50; color: white; padding: 10px 18px; border: none; border-radius: 4px; cursor: pointer;">Login</button>
    <button onclick="closeLoginForm()" style="background-color: #ff0000; color: white; padding: 10px 18px; border: none; border-radius: 4px; cursor: pointer;">Close</button>
  </form>
</div>
<script>
function showLoginForm() {
  document.getElementById("login-form").style.display = "block";
}
function closeLoginForm() {
  document.getElementById("login-form").style.display = "none";
}
function login() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;

if (username === "admin" && password === "admin") {
  // authenticated, redirect to admin page
  window.location.replace('http://localhost:1173/');
  // do something with the Python code
} else {
  alert("Invalid username or password!");
  }
}
</script>
        <div class="centered" style="background-color: #f2f2f2; padding: 20px;">
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
</form>

        </form> 
                    </td>
             </tr>
                """
    html_content += """
                </table>
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



# @app.post("/sentiment/{ID}")
# async def delete_sentiment(ID: int):
#     conn = psycopg2.connect(host='db', database='Sentimental_Analysis', user='pgsqldev4', password='enter')
#     cur = conn.cursor()
#     cur.execute("DELETE FROM sentiments WHERE ID = %s", (ID,))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return RedirectResponse(url="http://localhost:1172", status_code=303)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1172)
