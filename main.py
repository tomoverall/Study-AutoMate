import openai
from PyPDF2 import PdfReader

# OpenAI API Key
openai.api_key = ""


# PDF reader
def read_pdf(file):
    reader = PdfReader(file)
    # Testing for one page
    page = reader.pages[0]
    return page.extract_text()


# Output generator function
def generate_output(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, temperature=0.0, max_tokens=300, n=1
    )
    return response.choices[0].text


# Main function
def main():
    # The prompt is gathered from the user's notes
    page_of_notes = read_pdf("test.pdf")

    # Creating an example output from the prompt
    ideal_prompt = (
        """
        Generate sample questions and answers based on the provided text for studying purposes.

        **Example**
        Text:
        ---
        """
        + page_of_notes
        + """

        ---
        Instructions:
        Generate a set of questions and answers based on the text provided.
    """
    )

    # Calling the API with the prompt
    generated_output = generate_output(ideal_prompt)

    # Printing the output
    print(generated_output)


if __name__ == "__main__":
    main()
