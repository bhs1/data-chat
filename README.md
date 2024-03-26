# A bot to chat with imessages.

## Basic functionality
* Chunk the chat.db file on macbook into a vector database
* When a question is given, retreive N most relevant chunks and insert into LLM context window
## Finetuning training data preparation
* Use Google Gemini Pro to generate training examples in my roommates' writing styles. 
    * The context window for gemini pro is quite large so was able to fit almost the entire imessage.
* Add some hacky stripts to clean the gemini output into json
## Finetuning Mistral 7B
* Wrote this [colab](https://colab.research.google.com/drive/17reXuUO1y2wZaBDZP47q_lYksJzqjppN#scrollTo=xlyd8pfRWiyy) to finetune mistral 7b model using parameter efficient finetuning (lora). 
    * Did this in two of my roommates voices and stored the lora weights so the model can be very quickly swapped between their two distinct voice patterns.
    * Feel free to request colab access.
