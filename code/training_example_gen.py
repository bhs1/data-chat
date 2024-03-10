import os
import google.generativeai as genai

genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')

with open('data/messages_truc.txt', 'r') as file:
    file_content = file.read().strip()

names = ["Greg", "Scott", "Ben"]

# TODO: Write results to files. 100 examples each. ben.txt, scott.txt, greg.txt
for name in names:
    try:
        print(f"========== In the style of {name}:")
        prompt = f"""Generate a question answer pair based on the chat history below. The question should be a full sentenace in regular plain english ending in a question mark (?).
        The answer should be in the style of {name} from the chat. You can get his style from the chat itself.

        Chat:
        {file_content}
        """

        response = model.generate_content(prompt,
                                        generation_config=genai.types.GenerationConfig(
                                            temperature=.5))
        prompt2 = "Take the output:\n " + response.text + "\n and format as json with two fields question and answer like this " + """
        {
            question: What is the risk involved 2078 Green st?
            answer: One of the bedrooms is a detached downstairs apartment only accessible through yard or garage.
        }
        """
        response = model.generate_content(prompt2,
                                        generation_config=genai.types.GenerationConfig(
                                            temperature=0.0))
        

        print(response.text)
    except:
        print("Exception!!")