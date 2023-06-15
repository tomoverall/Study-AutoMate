import openai
import csv
from PyPDF2 import PdfReader
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)
from io import BytesIO


# OpenAI API Key
openai.api_key = ""

# Flask app
app = Flask(__name__, static_folder="static")


# CSV Exporter
def export_to_csv(question, answer):
    fieldnames = ["Question", "Answer"]

    with open("flashcards.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for question, answer in zip(question, answer):
            writer.writerow({"Question": question, "Answer": answer})


# PDF reader
def read_pdf(file):
    pages = []
    reader = PdfReader(file)
    # Getting all pages
    for page in reader.pages:
        pages.append(page.extract_text())
    return "".join(pages)


# Output generator function
def generate_output(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, temperature=0.0, max_tokens=300, n=1
    )
    return response.choices[0].text


@app.route("/")
def welcome():
    return render_template("welcome.html")


# Main route to render the index.html template
@app.route("/index")
def index():
    return render_template("index.html")


# Route to handle the form submission# Route to process the uploaded PDF file
@app.route("/process", methods=["POST"])
def process():
    # Getting the PDF file
    file = request.files["file"]
    # Reading the PDF file to obtain the pages of text from the notes
    pages = read_pdf(file)
    # Creating an example output from the prompt
    ideal_prompt = (
        """
        Generate sample questions and answers based on the provided text for studying purposes.

        **
        Q: What is the mitochondria?
        A: The mitochondria is the powerhouse of the cell.
        **

        Text:
        ---
        """
        + pages
        + """

        ---
        Instructions:
        Generate a set of questions and answers based on the text provided.
    """
    )

    # Calling the API with the prompt
    generated_output = generate_output(ideal_prompt)

    questions = ["What is the definition of biology?"]
    answers = [
        "Biology is the science of Living Things, also known as Life Science, from the Greek bios, life, and logos, word or knowledge."
    ]

    # Parsing the output and separating the questions and answers
    for line in generated_output.split("\n"):
        if ("Q:") in line and line.replace("Q:", "").strip() not in questions:
            questions.append(line.replace("Q:", "").strip())
        elif ("A:") in line and line.replace("A:", "").strip() not in answers:
            answers.append(line.replace("A:", "").strip())

    # Exporting the questions and answers to Anki
    export_to_csv(questions, answers)

    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run()
