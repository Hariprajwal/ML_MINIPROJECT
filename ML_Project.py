from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML + CSS Template as a single string
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Performance Predictor</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f0f4f8;
            padding: 40px;
        }
        .container {
            background: #ffffff;
            padding: 30px;
            border-radius: 12px;
            max-width: 500px;
            margin: auto;
            box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.1);
        }
        h2 {
            text-align: center;
            color: #333333;
        }
        label {
            display: block;
            margin-top: 15px;
            font-weight: 500;
        }
        input[type="number"] {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            border: 1px solid #ccc;
            border-radius: 8px;
        }
        button {
            margin-top: 25px;
            padding: 10px 15px;
            width: 100%;
            background-color: #007bff;
            border: none;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 25px;
            font-size: 18px;
            text-align: center;
            font-weight: bold;
            color: #2c3e50;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Student Performance Predictor</h2>
        <form method="POST">
            <label for="marks">Internal Assessment Marks (0-100):</label>
            <input type="number" name="marks" required min="0" max="100">

            <label for="attendance">Attendance % (0-100):</label>
            <input type="number" name="attendance" required min="0" max="100">

            <label for="assignments">Assignment Score (0-100):</label>
            <input type="number" name="assignments" required min="0" max="100">

            <label for="extra">Extracurricular Participation Score (0-100):</label>
            <input type="number" name="extra" required min="0" max="100">

            <button type="submit">Predict</button>
        </form>

        {% if result %}
            <div class="result">Prediction: {{ result }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

# Decision tree logic implemented manually
def decision_tree_predict(marks, attendance, assignments, extra):
    if marks >= 40:
        if attendance >= 75:
            if assignments >= 50:
                return "Pass"
            elif extra >= 60:
                return "Pass"
            else:
                return "Fail"
        else:
            if extra >= 70:
                return "Pass"
            else:
                return "Fail"
    else:
        return "Fail"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            marks = int(request.form["marks"])
            attendance = int(request.form["attendance"])
            assignments = int(request.form["assignments"])
            extra = int(request.form["extra"])
            result = decision_tree_predict(marks, attendance, assignments, extra)
        except ValueError:
            result = "Invalid input. Please enter numbers between 0 and 100."
    return render_template_string(HTML_PAGE, result=result)

# Use this to prevent SystemExit errors in Jupyter or IDEs
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, use_reloader=False, port=port)
