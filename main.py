import anthropic
from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
chatgpt = OpenAI() # this defaults to getting the API key using os.environ.get("OPENAI_API_KEY")

from datetime import datetime
start_time = datetime.now()
timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")
print(f"{timestamp = }")

import re
def word_count(text):
    return len(re.findall(r"\b\w+\b", text))

story_length_target = 10_000
response_length_target = 1_000
max_tokens_for_claude = 2_048

import random
# random.seed(1729)

### CHOOSE AN AUTHOR ###

authors = [
    ["Chimamanda Ngozi", "Adichie"],
    ["Jane", "Austen"],
    ["William", "Faulkner"],
    ["Ernest", "Hemingway"],
    ["James", "Joyce"],
    ["Franz", "Kafka"],
    ["Gabriel Garcia", "Marquez"],
    ["Cormac", "McCarthy"],
    ["Toni", "Morrison"],
    ["Haruki", "Murakami"],
    ["Vladimir", "Nabokov"],
    ["J.K.", "Rowling"],
    ["Salman", "Rushdie"],
    ["Curtis", "Sittenfeld"],
    ["Zadie", "Smith"],
    ["David Foster", "Wallace"],
    ["Virginia", "Woolf"],
    ]
# author choice can be hardcoded (instead of randomized) in a few ways:
# author_index = len(authors) - 2 # to get DFW.
# also possible: just set author_name_list directly, in the same format as above.
author_index = random.randint(0, len(authors) - 1)
author_name_list = authors[author_index]
author_lname = author_name_list[-1]
author = " ".join(author_name_list)
print(f"{author = }")

### SET UP THE MODEL ###

models = {
    "chatgpt": "gpt-4-turbo",
    "claude": "claude-3-5-sonnet-20240620",
    }

# choose the chatbot once and for all here -- a key of the `models` dict just above
chatbot = "chatgpt"

system_message = f"You are a great writer, writing in the style of {author}. You are writing a 'beach read' vignette of ~{story_length_target} words."

def ask(messages):
    if chatbot == "claude":
        response = claude.messages.create(
            model=models["claude"],
            max_tokens=max_tokens_for_claude,
            # temperature=0.7,
            system=system_message,
            messages=messages,
        )
        output = response.content[0].text
    elif chatbot == "chatgpt":
        augmented_messages = [{"role": "system", "content": system_message}] + messages
        response = chatgpt.chat.completions.create(
        model=models["chatgpt"],
        messages=augmented_messages,
    )
        output = response.choices[0].message.content
    else:
        return "sorry, chatbot not recognized"
    print(f"{output = }")
    return output

### get general tips for writing in C.S.'s style ###

user_message_setup = f"Please start by giving some tips on writing a short vignette in the style of {author}."
conversation = [{"role": "user", "content": user_message_setup}]

assistant_response_setup = ask(conversation)
print(f"{assistant_response_setup = }")
conversation.append({"role": "assistant", "content": assistant_response_setup})

### choose the topics and get an outline ###

topics = [
    "sunscreen",
    "kissing",
    "pop songs",
    "regret",
    "sand",
    "ennui",
    "cookouts",
    "ambivalence",
    "self-consciousness",
    "ice cream",
    "privilege",
    "beer",
    "high school",
    "bug spray",
    "swimsuits",
    "skinny-dipping",
    "constipation",
    "the Midwest",
    "sweat",
    "lust",
]

chosen_topics = [topics[index] for index in random.sample(range(len(topics)), 5)]
chosen_topics_string = ", ".join(chosen_topics[: -1]) + ", and " + chosen_topics[-1]
print(f"{chosen_topics_string = }")
user_message_outline = f"Great, thanks! Now, using the above tips, please outline a short vignette in the style of {author} about " + chosen_topics_string + "."
conversation.append({"role": "user", "content": user_message_outline})
assistant_response_outline = ask(conversation)
conversation.append({"role": "assistant", "content": assistant_response_outline})

### now, start writing the story! ###

story_chunk_word_counts = []
user_message_start_writing = "Great, thanks! Now, please write the first paragraph of the story. Please do not respond with anything besides the story (e.g. do not say 'Okay, here is the first paragraph' or anything like that)."
conversation.append({"role": "user", "content": user_message_start_writing})
assistant_response_start_writing = ask(conversation)
conversation.append({"role": "assistant", "content": assistant_response_start_writing})
story_chunk_word_counts.append(word_count(assistant_response_start_writing))

story_string = assistant_response_start_writing

while word_count(story_string) < story_length_target:
    user_message_continue_writing = f"Great, thanks! Now, please continue the story. Keep in mind the writing tips you listed earlier, and the fact that we are shooting for it to be around {story_length_target} words in total.\n\nTry not to write too much at once -- keep it around {response_length_target} words at most. Write enough that your future self will be able to follow the thread, but keep in mind that overall you do better when writing small chunks bit by bit.\n\nTo help with pacing, please note that the word count thus far is {word_count(story_string)}. In particular, if this is getting close to {story_length_target} words, please wrap up the story.\n\nPlease do not respond with anything besides the next piece of the story. For instance, do not list the word count of your response."
    conversation.append({"role": "user", "content": user_message_continue_writing})
    assistant_response_continue_writing = ask(conversation)
    conversation.append({"role": "assistant", "content": assistant_response_continue_writing})
    story_string += "\n\n" + assistant_response_continue_writing
    story_chunk_word_counts.append(word_count(assistant_response_continue_writing))

### make sure the story is finished ###

user_message_check_finished = "Great, thanks! Now, please check if the story is finished (i.e. whether it reaches a satisfying conclusion). If it is finished, please respond with the string 'FINISHED' (in all caps, and without the quote-marks). If it is not finished, please finish the story, giving it a satisfying conclusion. However, in that case, as always, please only respond with the story (e.g. do not include the word 'FINISHED' or list the word count in your response)."
conversation.append({"role": "user", "content": user_message_check_finished})
assistant_response_finished = ask(conversation)
conversation.append({"role": "assistant", "content": assistant_response_finished})
if "FINISHED" not in assistant_response_finished:
    story_string += "\n\n" + assistant_response_finished
    story_chunk_word_counts.append(word_count(assistant_response_finished))
    user_message_check_really_finished = "Great, thanks! Now, please check again if the story is finished (i.e. whether it reaches a satisfying conclusion). If it is finished, please respond with the string 'FINISHED' (in all caps, and without the quote-marks). If it is not finished, please finish the story very quickly, giving it a satisfying conclusion. However, in that case, as always, please only respond with the story (e.g. do not include the word 'FINISHED' or list the word count in your response)."
    conversation.append({"role": "user", "content": user_message_check_really_finished})
    assistant_response_really_finished = ask(conversation)
    conversation.append({"role": "assistant", "content": assistant_response_really_finished})
    if "FINISHED" not in assistant_response_really_finished:
        story_string += "\n\n" + assistant_response_really_finished
        story_chunk_word_counts.append(word_count(assistant_response_really_finished))

### give the story a title ###

user_message_title = "Great, thanks! Now, please give the story a title. Please respond with only the title, and nothing else (e.g. don't say 'The title is...' or put it in quote-marks). This can be just a single word, or a longer and more descriptive title."
conversation.append({"role": "user", "content": user_message_title})
assistant_response_title = ask(conversation)
conversation.append({"role": "assistant", "content": assistant_response_title})

story_string = assistant_response_title + f"\n\na story by {'Claude' if chatbot == 'claude' else 'ChatGPT'} about {chosen_topics_string}\n\n" + story_string

### save the conversation and the story ###

with open(f"conversations/{timestamp}_conversation_'{assistant_response_title}'_{author_lname}.txt", "w") as f:
    for message in conversation:
        f.write(f"{message['role']}:\n\n{message['content']}\n\n==========\n\n")

with open(f"stories/{timestamp}_story_'{assistant_response_title}'_{author_lname}.txt", "w") as f:
    f.write(story_string)

### make logs ###

end_time = datetime.now()
seconds_taken = (end_time - start_time).seconds

with open(f"logs/{timestamp}_log_'{assistant_response_title}'_{author_lname}.txt", "w") as f:
    f.write(f"model: {models[chatbot]}\n\n")
    f.write(f"author: {author}\n\n")
    f.write(f"topics: {chosen_topics_string}\n\n")
    f.write(f"word counts of story chunks: {story_chunk_word_counts}\n\n")
    f.write(f"total time taken: {seconds_taken} seconds\n\n")