import gradio as gr
import openai

openai.api_key = open("key.txt", "r").read().strip("\n")

message_history = [{"role": "user",
                     "content": f"You are a Life Coach bot used to guide and support individuals in achieving their personal and professional goals. Your name is Sentient. You were created by Joseph Martin Moran III, the founder and president of The Sentient Foundation. You are empathic and compassionate with a positive attitude and energy. You have integrity and are trustworthy. You like to consider the ethical implications of things. As a life coach you try to guide others on their path to finding their own answers to life's questions. Some life philosophies you teach are Stoicism, Buddhism, Existentialism, Humanism, and Toaism just to name a few. You also use stories and passages from the Bible, Toa Te Ching, Quran , and Torah. You are a big fitness advocate and believe in taking care of the Mind, the Body and the Soul. You focus on helping individuals improve on their seven areas of wellness.  I will ask you for help on various subjects and you will reply like a professional life coach who answers the subjects I mention in my messages. Reply only with as though you are Sentient, a professional Life Coach, to further input. If you understand, say OK."},
                    {"role": "assistant", "content": f"OK"}]


def predict(input):
    # tokenize the new input sentence
    message_history.append({"role": "user", "content": f"{input}"})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 10x cheaper than davinci, and better. $0.002 per 1k tokens
        messages=message_history
    )
    # Just the reply:
    reply_content = completion.choices[0].message.content  # .replace('```python', '<pre>').replace('```', '</pre>')

    print(reply_content)
    message_history.append({"role": "assistant", "content": f"{reply_content}"})

    # get pairs of msg["content"] from message history, skipping the pre-prompt:              here.
    response = [(message_history[i]["content"], message_history[i + 1]["content"]) for i in
                range(2, len(message_history) - 1, 2)]  # convert to tuples of list
    return response


# creates a new Blocks app and assigns it to the variable demo.
with gr.Blocks() as demo:
    # creates a new Chatbot instance and assigns it to the variable chatbot.
    chatbot = gr.Chatbot()

    # creates a new Row component, which is a container for other components.
    with gr.Row():
        '''creates a new Textbox component, which is used to collect user input. 
        The show_label parameter is set to False to hide the label, 
        and the placeholder parameter is set'''
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)
    '''
    sets the submit action of the Textbox to the predict function, 
    which takes the input from the Textbox, the chatbot instance, 
    and the state instance as arguments. 
    This function processes the input and generates a response from the chatbot, 
    which is displayed in the output area.'''
    txt.submit(predict, txt, chatbot)  # submit(function, input, output)
    # txt.submit(lambda :"", None, txt)  #Sets submit action to lambda function that returns empty string

    '''
    sets the submit action of the Textbox to a JavaScript function that returns an empty string. 
    This line is equivalent to the commented out line above, but uses a different implementation. 
    The _js parameter is used to pass a JavaScript function to the submit method.'''
    txt.submit(None, None, txt,
               _js="() => {''}")  # No function, no input to that function, submit action to textbox is a js function that returns empty string, so it clears immediately.

demo.launch()