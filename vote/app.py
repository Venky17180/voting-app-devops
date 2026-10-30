from flask import Flask, request, render_template_string
import redis
import os

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(
    host=redis_host,
    port=6379,
    decode_responses=True
)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Election Voting System</title>
</head>
<body>
    <h1>🗳️ Student Election Voting System</h1>
    <p>Choose your preferred candidate to cast your vote:</p>
    <form action="/vote" method="post">
        <button type="submit" name="option" value="Candidate A">Candidate A</button>
        <button type="submit" name="option" value="Candidate B">Candidate B</button>
        <button type="submit" name="option" value="Candidate C">Candidate C</button>
        <button type="submit" name="option" value="Candidate D">Candidate D</button>
    </form>
    <p>{{ message }}</p>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, message="Cast your vote!")

@app.route("/vote", methods=["POST"])
def vote():
    option = request.form.get("option")
    if option not in ["Candidate A", "Candidate B", "Candidate C", "Candidate D"]:
        return "Invalid option", 400

    redis_client.incr(f"votes:{option}")
    return render_template_string(
        HTML, message=f"Your vote for {option} was recorded!"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
