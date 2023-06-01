import streamlit as st
from streamlit_chat import message
import openai
import os
import glob
from audio_recorder_streamlit import audio_recorder
from datetime import datetime
from gtts import gTTS
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup



# Define the class for the chatbot
class ChatGPTBot:
    # The initializer method gets executed when a new ChatGPTBot object (i.e. bot) is created
    def __init__(self, api_key):
        # Set up the OpenAI API key
        openai.api_key = api_key
        self.api_key = api_key
        # Initialize the message history for chat storing
        if 'message_history' not in st.session_state:
            st.session_state['message_history'] = []


    # The bot sends the user's message to GPT model and receives API response
    # Document and update the message history between the user and the bot
    def chat_with_gpt(self,
                      user_message,
                      model = "gpt-3.5-turbo",
                      role = 'user',
                      message_history = []):
        # Assemble a request using user's message and append it to message_history
        request = {"role": role, "content": user_message}
        message_history.append(request)

        # Create a chat completion object using OpenAI API
        completion = openai.ChatCompletion.create(
          model = model,
          messages = message_history
        )  # other useful parameters: temperature and max_tokens

        # Extract bot's message from the API response
        bot_message = completion['choices'][0]['message']['content']
        # Assemble a response using bot's message and append it to message_history
        response = {"role": 'assistant', "content": bot_message}
        message_history.append(response)

        return message_history, bot_message


    # Play bot's message in audio
    def saying(self, bot_message, lang):
        # Convert bot's message from text to speech
        bot_speech = gTTS(text = bot_message, lang = lang, slow = False)
        # Save the speech as a WAV audio file
        bot_audio_filename = 'bot-{}.wav'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        bot_speech.save(bot_audio_filename)
        # Read the bot audio file
        bot_audio_file = open(bot_audio_filename, 'rb')
        bot_audio_bytes = bot_audio_file.read()
        # Display an audio button on the page that plays the bot audio file
        st.write('Play the audio below to LISTEN to the bot')
        st.audio(bot_audio_bytes, format = 'audio/wav')


    # Chat with the bot. Make the bot talk in either Chinese or English
    def chatting(self, user_message, text_or_speak):
        if user_message != '':
            # Get the latest message history stored in streamlit session state
            message_history = st.session_state['message_history']
            # Send user message to GPT model and get the updated message history and bot's message
            message_history, bot_message = self.chat_with_gpt(user_message = user_message, message_history = message_history)
            # Update the message history in streamlit session state
            st.session_state['message_history'] = message_history
            # Save the user message in streamlit session state
            st.session_state['user-{}'.format(text_or_speak)].append(user_message)
            # Save the bot's message in streamlit session state
            st.session_state['bot-{}'.format(text_or_speak)].append(bot_message)

            # Play bot's message in audio - in Chinese or English?
            threshold = 0.5
            # Get a list of English words from the the bot's message
            en_words = re.findall("[a-zA-Z\']+", bot_message)
            # Get a list of Chinese characters from the bot's message
            ch_words = re.findall("[\u4e00-\u9FFF]", bot_message)  # detect chinese characters: eg. ['当', '然', '可', '以']
            # Total number of both Chinese characters and English words
            total_len = len(en_words) + len(ch_words)
            # If the bot's message contains any Chinese character or English word
            if total_len > 0:
                # Proportion of Chinese part
                prop_ch = len(ch_words) / total_len
                if prop_ch > threshold:
                    # If the bot's message is mostly in Chinese,
                    # play the bot's audio message in Chinese
                    self.saying(bot_message, 'zh-CN')
                else:
                    # If the bot's message is mostly in English,
                    # play the bot's audio message in English
                    self.saying(bot_message, 'en')
            else:
                self.saying(bot_message, 'en')


    # Transcribe user's speech to text
    def transcribe_voice(self, audio_bytes, model = 'whisper-1'):
        # Write audio_bytes into a new WAV file
        filename = 'user-{}.wav'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        with open(filename, 'wb') as f:
            f.write(audio_bytes)

        # Transcribe audio file to text through OpenAI's whisper model
        audio_file = open(filename, 'rb')
        transcript = openai.Audio.transcribe(model, audio_file)

        # Get the transcribed text
        return transcript['text']



# Define the class for the chat app
class ChatApp:
    # The initializer method gets executed when a new object of ChatApp is created
    def __init__(self):
        # Set page config
        st.set_page_config(page_title="Talk To GPT-3.5",
                           page_icon=":microphone:",
                           layout='centered',
                           initial_sidebar_state="auto")
        # Remove all previously existing audio files
        for file in glob.glob('./*.wav'):
            os.remove(file)
        # Initialize session state variables for chat storing
        if 'bot-text' not in st.session_state:
            st.session_state['bot-text'] = []
        if 'user-text' not in st.session_state:
            st.session_state['user-text'] = []
        if 'bot-speak' not in st.session_state:
            st.session_state['bot-speak'] = []
        if 'user-speak' not in st.session_state:
            st.session_state['user-speak'] = []
        if 'prompts' not in st.session_state:
            try:
                headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
                # Load a series of role-based prompts from https://github.com/f/awesome-chatgpt-prompts/blob/main/prompts.csv
                r = requests.get('https://github.com/f/awesome-chatgpt-prompts/blob/main/prompts.csv', headers = headers)
                # Retrieve the html content of the URL through BeautifulSoup
                c = r.content
                soup = BeautifulSoup(c, 'html.parser')
                # Get html of the loading page in appropriate layout
                html = soup.prettify()
                # Read html to get the dataframe of prompts
                dfs = pd.read_html(html)
                df = dfs[0]
                # Drop useless column
                if 'Unnamed: 0' in df.columns:
                    df = df.drop('Unnamed: 0', 1)
                # Update prompt column
                df['prompt'] = df['prompt'].apply(lambda x: self.transform_prompt(x))
                # Save the prompts in session state
                st.session_state['prompts'] = df
            except:
                # If prompt loading fails, display an error message on the web page
                st.error('Unable to load the built-in prompts. Please check [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts/blob/main/prompts.csv) for more details.')

    # Transform a prompt to appropriate format
    def transform_prompt(self, x):
        # Add full stop to the end of each prompt
        if x[-1] != '.':
            x = x + '.'
        # Find the sentences within the prompt that contain 'My first...'
        list_my_first = re.findall(r'. my first [^.]+.', x.lower())
        # If the pattern was found in the prompt...
        if len(list_my_first) > 0:
            my_first = list_my_first[-1]
            cutoff_id = x.lower().index(my_first)
            # remove the last 'My first...' sentence from the prompt
            prompt = x[: cutoff_id + 1]
        else:
            prompt = x
        # Add "Reply "OK" to confirm." to the end of each prompt
        if prompt[-22:] != """Reply "OK" to confirm.""":
            prompt = prompt + """ Reply "OK" to confirm."""
        return prompt

    # Display chat history as conversation dialogs
    def output_chat_history(self, text_or_speak):
        # Check if there is chat history for the specified conversation type (text or speak)
        if (len(st.session_state['bot-{}'.format(text_or_speak)]) > 0):
            # Iterate through the chat history in reverse order, displaying dialogs from newest to oldest
            for i in range(len(st.session_state['bot-{}'.format(text_or_speak)]) - 1, -1, -1):
                # Display the bot's message first
                message(st.session_state['bot-{}'.format(text_or_speak)][i], is_user = False, avatar_style = 'bottts-neutral', seed = 75, key = 'bot-{}-{}'.format(text_or_speak, i))
                # Display the user's message right after bot's message
                message(st.session_state['user-{}'.format(text_or_speak)][i], is_user = True, avatar_style = 'adventurer-neutral', seed = 124, key = 'user-{}-{}'.format(text_or_speak, i))


    # Run the Chatbot application
    def run(self):
        # Set the page title
        st.title('Welcome to Talk To GPT-3.5')
        # Display a subheader that briefly describe the chatbot web app
        st.subheader("Emplowering Conversations: A ChatBot You Can Message Or Talk To, Powered By OpenAI's GPT 3.5 Turbo Model and Whisper Model :robot_face:")

        # Get the API key from the user
        col1, col2 = st.columns([1, 1])
        KEY = col1.text_input("Please paste your API key and hit the 'Enter' key", type="password",
                               help = "To create and collect an API key, visit https://platform.openai.com/account/api-keys, \
                               click on 'API Key', then select 'Create new secret key' and click 'Copy'. \
                               Note: Please be mindful of the number of requests you've sent to GPT-3.5, \
                               as exceeding the free credits limit of $18 may result in additional fees.\
                               To check your usage, visit the same website and click on 'Usage'.")

        # Mark down a breakline
        st.markdown("***")

        # If API key is entered
        if KEY != '':
            # Initialize the chatbot with the provided API key
            bot = ChatGPTBot(KEY)

            # Mark down a pro tip for users
            st.markdown("""*Pro tip: If you wish to initiate a new conversation, you can either \
                           refresh the webpage or request the bot to discard all previous instructions \
                           by inputting the command, "ignore all previous instructions before this one".*""")

            # Display an empty line
            st.text('')
            # Two Expanders for communication with the bot
            # Expander 1: Message to bot
            with st.expander(":memo: MESSAGE BOT"):
                df_prompts = st.session_state['prompts']
                # Get list of roles for prompts
                prompts = sorted(list(df_prompts['act']))
                # Add "You want the bot to act as..." to the prompt list
                prompts = tuple(['You want the bot to act as...'] + prompts)
                # Dropdown box for built-in prompt selection
                prompt_act_selected = st.selectbox(label = 'Choose a built-in prompt (optional)',
                                                   options = prompts, index = 0,
                                                   help = "The collection of built-in prompts were imported from \
                                                           [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts).")
                # Set the initial value for text message field based on the selected prompt
                if prompt_act_selected == 'You want the bot to act as...':
                    initial_value = ''
                else:
                    prompt_id = list(df_prompts[df_prompts.act == prompt_act_selected].index)[0]
                    initial_value = df_prompts.loc[prompt_id, 'prompt']
                # Text message input field with initial value
                user_message_text = st.text_area('Send text message',
                                                  placeholder = "Type your text message here and press Ctrl+Enter to submit",
                                                  value = initial_value, height = 120)
                # Send user's text message to the bot
                bot.chatting(user_message_text, 'text')
                # Output chat history
                st.text('')
                self.output_chat_history('text')
                st.text('')

            # Expander 2: Talk to bot
            with st.expander(':speaking_head_in_silhouette: TALK TO BOT'):
                # Check if the text message field entry is cleared
                if user_message_text != '':
                    st.error('Please ensure that all content has been deleted from the text message field')
                else:
                    # Audio button to record user's voice
                    audio_bytes = audio_recorder(neutral_color = '#FFFFFF',
                                                 pause_threshold = 3.0)  # stop after pausing for 3 seconds
                    if audio_bytes:
                        # Transcribe the user's voice to get user's voice message in text
                        user_message_voice = bot.transcribe_voice(audio_bytes = audio_bytes)
                        # Display a status message
                        st.success('Voice recording finished. Feel free to continue.')
                        # Send user's voice message in text to the bot
                        bot.chatting(user_message_voice, 'speak')
                    # Output chat history
                    st.text('')
                    self.output_chat_history('speak')
                st.text('')

        # If API key is not entered
        else:
            st.error('Please enter your API key to initiate your chat!')


        # Desktop App for downloading
        st.text('')
        col1, col2 = st.columns([14, 7.3])
        desktop_binary_file = 'assets/OpenAI-API-Desktop-ChatBot.exe'
        with open(desktop_binary_file, 'rb') as file:
            # Display a download button for the desktop version of the chatbot
            col2.download_button(label = ':computer: Download Desktop Version',
                                 data = file,
                                 file_name = 'OpenAI-API-Desktop-ChatBot.exe',
                                 mime = 'application/octet-stream',
                                 help = 'It is recommended to install [Python](https://www.python.org/downloads/) on your local computer prior to running the desktop program.')
        st.text('')



# Check if the module is being executed as the main module
if __name__ == '__main__':
    # Create an instance of ChatApp class
    chat_app = ChatApp()
    # Call run() method to start the chat application
    chat_app.run()
