import anthropic
import os

from dotenv import load_dotenv
load_dotenv()
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

from datetime import datetime
start_time = datetime.now()
timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")

import re
def word_count(text):
    return len(re.findall(r"\b\w+\b", text))

import random
# random.seed(1729)

### SET UP THE MODEL ###

model = "claude-3-5-sonnet-20240620"
system_message = "You are a great writer, writing in the style of Curtis Sittenfeld. You are writing a 'beach read' vignette of ~1000 words."

def ask_claude(messages):
    response = claude.messages.create(
        model=model,
        max_tokens=1000,
        # temperature=0.7,
        system=system_message,
        messages=messages,
    )
    output = response.content[0].text
    print(f"{output = }")
    return output

### get general tips for writing in C.S.'s style ###

user_message_setup = "Please start by giving some tips on writing a short vignette in the style of Curtis Sittenfeld."
conversation = [{"role": "user", "content": user_message_setup}]

assistant_response_setup = ask_claude(conversation)
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

chosen_topics = [topics[index] for index in random.sample(range(20), 5)]
chosen_topics_string = ", ".join(chosen_topics[: -1]) + ", and " + chosen_topics[-1]
user_message_outline = "Great, thanks! Now, using the above tips, please outline a short story about " + chosen_topics_string + "."
conversation.append({"role": "user", "content": user_message_outline})
assistant_response_outline = ask_claude(conversation)
conversation.append({"role": "assistant", "content": assistant_response_outline})

### now, start writing the story! ###

story_chunk_word_counts = []
user_message_start_writing = "Great, thanks! Now, please write the first paragraph of the story. Please do not respond with anything besides the story (e.g. do not say 'Okay, here is the first paragraph' or anything like that)."
conversation.append({"role": "user", "content": user_message_start_writing})
assistant_response_start_writing = ask_claude(conversation)
conversation.append({"role": "assistant", "content": assistant_response_start_writing})
story_chunk_word_counts.append(word_count(assistant_response_start_writing))

story_string = assistant_response_start_writing

while word_count(story_string) < 1000:
    user_message_continue_writing = f"Great, thanks! Now, please continue the story. Keep in mind the writing tips you listed earlier, and the fact that we are shooting for it to be around 1000 words in total.\n\nTo help with pacing, please note that the word count thus far is {word_count(story_string)}. In particular, if this is getting towards 1000 words, please wrap up the story.\n\nPlease do not respond with anything besides the next piece of the story. For instance, do not list the word count of your response."
    conversation.append({"role": "user", "content": user_message_continue_writing})
    assistant_response_continue_writing = ask_claude(conversation)
    conversation.append({"role": "assistant", "content": assistant_response_continue_writing})
    story_string += "\n\n" + assistant_response_continue_writing
    story_chunk_word_counts.append(word_count(assistant_response_continue_writing))

### make sure the story is finished ###

user_message_check_finished = "Great, thanks! Now, please check if the story is finished (i.e. whether it reaches a satisfying conclusion). If it is finished, please respond with the string 'FINISHED' (in all caps, and without the quote-marks). If it is not finished, please finish the story, giving it a satisfying conclusion. However, in that case, as always, please only respond with the story (e.g. do not include the word 'FINISHED' or list the word count in your response)."
conversation.append({"role": "user", "content": user_message_check_finished})
assistant_response_finished = ask_claude(conversation)
conversation.append({"role": "assistant", "content": assistant_response_finished})
if "FINISHED" not in assistant_response_finished:
    story_string += "\n\n" + assistant_response_finished
    story_chunk_word_counts.append(word_count(assistant_response_finished))
    user_message_check_really_finished = "Great, thanks! Now, please check again if the story is finished (i.e. whether it reaches a satisfying conclusion). If it is finished, please respond with the string 'FINISHED' (in all caps, and without the quote-marks). If it is not finished, please finish the story very quickly, giving it a satisfying conclusion. However, in that case, as always, please only respond with the story (e.g. do not include the word 'FINISHED' or list the word count in your response)."
    conversation.append({"role": "user", "content": user_message_check_really_finished})
    assistant_response_really_finished = ask_claude(conversation)
    conversation.append({"role": "assistant", "content": assistant_response_really_finished})
    if "FINISHED" not in assistant_response_really_finished:
        story_string += "\n\n" + assistant_response_really_finished
        story_chunk_word_counts.append(word_count(assistant_response_really_finished))

### give the story a title ###

user_message_title = "Great, thanks! Now, please give the story a title. Please respond with only the title, and nothing else (e.g. don't say 'The title is...' or put it in quote-marks). This can be just a single word, or a longer and more descriptive title."
conversation.append({"role": "user", "content": user_message_title})
assistant_response_title = ask_claude(conversation)
conversation.append({"role": "assistant", "content": assistant_response_title})

story_string = assistant_response_title + f"\n\na story by Claude about {chosen_topics_string}\n\n" + story_string

### save the conversation and the story ###

with open(f"conversations/{timestamp}_conversation_'{assistant_response_title}'.txt", "w") as f:
    for message in conversation:
        f.write(f"{message['role']}: {message['content']}\n\n")

with open(f"stories/{timestamp}_story_'{assistant_response_title}'.txt", "w") as f:
    f.write(story_string)

### make logs ###

end_time = datetime.now()
seconds_taken = (end_time - start_time).seconds

with open(f"logs/{timestamp}_log_'{assistant_response_title}'.txt", "w") as f:
    f.write(f"model: {model}\n\n")
    f.write(f"topics: {chosen_topics_string}\n\n")
    f.write(f"word counts of story chunks: {story_chunk_word_counts}\n\n")
    f.write(f"total time taken: {seconds_taken} seconds\n\n")
