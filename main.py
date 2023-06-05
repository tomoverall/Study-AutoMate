import openai
import csv
from PyPDF2 import PdfReader

# OpenAI API Key
openai.api_key = ""

# CSV Exporter
def export_to_csv(question, answer):
    fieldnames = ["Question", "Answer"]

    with open("flashcards.csv", "a", newline="") as csvfile:
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


# Main function
def main():
    # Reading the PDF file to obtain the pages of text from the notes
    pages = read_pdf("test.pdf")

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

    questions = []
    answers = []

    # Parsing the output and separating the questions and answers
    for line in generated_output.split("\n"):
        if ("Q:") in line:
            questions.append(line)
        elif ("A:") in line:
            answers.append(line)

    # Printing the questions and answers
    for i in range(len(questions)):
        print(questions[i])
        print(answers[i])
    
    export_to_csv(questions, answers)


if __name__ == "__main__":
    main()
