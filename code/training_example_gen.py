import os
import google.generativeai as genai

genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')

with open('data/messages_truc.txt', 'r') as file:
    file_content = file.read().strip()

# Split file_content into 10 equal size chunks in a list
chunk_size = len(file_content) // 10
chunks = [file_content[i:i + chunk_size] for i in range(0, len(file_content), chunk_size)]

# If the file content doesn't divide evenly by 10, add the remainder to the last chunk
if len(file_content) % 10:
    chunks[-1] += file_content[-chunk_size:]

names = ["Greg", "Scott", "Ben"]
for name in names:
    output_file = f"data/{name.lower()}_chunked.txt"
    with open(output_file, 'w') as f:
        for chunk in chunks:
            print(name)
            try:
                prompt = f"""Generate 10 unique question answer pairs based on the chat history below. The question should be a full sentence in regular plain English ending in a question mark (?).
                The answer should be in the style of {name} from the chat. You can get his style from the chat itself.

                Chat:
                {chunk}
                """

                response = model.generate_content(prompt,
                                                  generation_config=genai.types.GenerationConfig(
                                                      temperature=.5))
                prompt2 = "Take the output:\n " + response.text + "\n and format as json with two fields question and answer like this " + """
                {
                    "question": "What is the risk involved 2078 Green st?",
                    "answer": "One of the bedrooms is a detached downstairs apartment only accessible through yard or garage."
                }
                """
                response = model.generate_content(prompt2,
                                                  generation_config=genai.types.GenerationConfig(
                                                      temperature=0.0))
                f.write(response.text + "\n")
                print(response.text)
            except Exception as e:
                print(f"Exception while generating content for {name}: {e}")