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
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

class ChatGPTBot:
    def __init__(self, api_key):
        # set up api_key
        openai.api_key = api_key
        self.api_key = api_key
        # for chat storing
        if 'message_history' not in st.session_state:
            st.session_state['message_history'] = []


    def chat_with_gpt(self,
                      user_message,
                      model = "gpt-3.5-turbo",
                      role = 'user',
                      message_history = []):
        request = {"role": role, "content": user_message}
        message_history.append(request)

        # other useful parameters: temperature and max_tokens
        completion = openai.ChatCompletion.create(
          model = model,
          messages = message_history
        )

        bot_message = completion['choices'][0]['message']['content']
        response = {"role": 'assistant', "content": bot_message}
        message_history.append(response)

        return message_history, bot_message


    def saying(self, bot_message, lang):
        # save bot_message as wav audio file
        bot_speech = gTTS(text = bot_message, lang = lang, slow = False)
        bot_audio_filename = 'bot-{}.wav'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        bot_speech.save(bot_audio_filename)
        # play the audio file
        bot_audio_file = open(bot_audio_filename, 'rb')
        bot_audio_bytes = bot_audio_file.read()
        st.write('Play the audio below to LISTEN to the bot')
        st.audio(bot_audio_bytes, format = 'audio/wav')


    def chatting(self, user_message, text_or_speak):
        if user_message != '':
            message_history = st.session_state['message_history']
            message_history, bot_message = self.chat_with_gpt(user_message = user_message, message_history = message_history)
            st.session_state['message_history'] = message_history
            st.session_state['user-{}'.format(text_or_speak)].append(user_message)
            st.session_state['bot-{}'.format(text_or_speak)].append(bot_message)

            # play bot's message in audio - in Chinese or English?
            threshold = 0.5
            en_words = re.findall("[a-zA-Z\']+", bot_message)
            ch_words = re.findall("[\u4e00-\u9FFF]", bot_message)  # detect chinese characters: eg. ['当', '然', '可', '以']
            total_len = len(en_words) + len(ch_words)  # length of all characters
            if total_len > 0:
                prop_ch = len(ch_words) / total_len  # proportion of Chinese part
                if prop_ch > threshold:
                    self.saying(bot_message, 'zh-CN')
                else:
                    self.saying(bot_message, 'en')
            else:
                self.saying(bot_message, 'en')


    def transcribe_voice(self, audio_bytes, model = 'whisper-1'):
        # save audio_bytes as wav file
        filename = 'user-{}.wav'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        with open(filename, 'wb') as f:
            f.write(audio_bytes)

        # transcribe voice to text
        audio_file = open(filename, 'rb')
        transcript = openai.Audio.transcribe(model, audio_file)

        return transcript['text']



class App:
    def __init__(self):
        # set page config
        st.set_page_config(page_title="Talk To GPT-3.5",
                           page_icon=":microphone:",
                           layout='centered',
                           initial_sidebar_state="auto")
        # remove all audio files
        for file in glob.glob('./*.wav'):
            os.remove(file)
        # for chat storing
        if 'bot-text' not in st.session_state:
            st.session_state['bot-text'] = []
        if 'user-text' not in st.session_state:
            st.session_state['user-text'] = []
        if 'bot-speak' not in st.session_state:
            st.session_state['bot-speak'] = []
        if 'user-speak' not in st.session_state:
            st.session_state['user-speak'] = []
        # load up-to-date built-in prompts
        if 'prompts' not in st.session_state:
            driver.get('https://github.com/f/awesome-chatgpt-prompts/blob/main/prompts.csv')
            st.code(driver.page_source)
            # get html without opening browser
            try:
                # load prompts from https://github.com/f/awesome-chatgpt-prompts/blob/main/prompts.csv
                # driver.get('https://github.com/f/awesome-chatgpt-prompts/blob/main/prompts.csv')
                # html = driver.page_source
                # read html to get dataframe
                dfs = pd.read_html(html)
                df = dfs[0]
                # drop useless column
                if 'Unnamed: 0' in df.columns:
                    df = df.drop('Unnamed: 0', 1)
                # update prompt column
                df['prompt'] = df['prompt'].apply(lambda x: self.transform_prompt(x))
                st.session_state['prompts'] = df
            except:
                st.error('Unable to load the built-in prompts. Please check [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts/blob/main/prompts.csv) for more details.')


    def transform_prompt(self, x):
        # add full stop to each prompt end
        if x[-1] != '.':
            x = x + '.'
        # find the sentences that contain 'my first...'
        list_my_first = re.findall(r'. my first [^.]+.', x.lower())
        if len(list_my_first) > 0:
            my_first = list_my_first[-1]
            cutoff_id = x.lower().index(my_first)
            # remove the last 'my first...' sentence from the prompt
            prompt = x[: cutoff_id + 1]
        else:
            prompt = x
        # add "Reply "OK" to confirm." to the end of each prompt
        if prompt[-22:] != """Reply "OK" to confirm.""":
            prompt = prompt + """ Reply "OK" to confirm."""
        return prompt


    def output_chat_history(self, text_or_speak):
        # output chat history
        if (len(st.session_state['bot-{}'.format(text_or_speak)]) > 0):
            for i in range(len(st.session_state['bot-{}'.format(text_or_speak)]) - 1, -1, -1):
                message(st.session_state['bot-{}'.format(text_or_speak)][i], is_user = False, avatar_style = 'bottts-neutral', seed = 75, key = 'bot-{}-{}'.format(text_or_speak, i))
                message(st.session_state['user-{}'.format(text_or_speak)][i], is_user = True, avatar_style = 'adventurer-neutral', seed = 124, key = 'user-{}-{}'.format(text_or_speak, i))


    def run(self):
        st.title('Welcome to Talk To GPT-3.5')
        st.subheader("Emplowering Conversations: A ChatBot You Can Message Or Talk To, Powered By OpenAI's GPT 3.5 Turbo Model and Whisper Model :robot_face:")

        # Enter API Key
        col1, col2 = st.columns([1, 1])
        KEY = col1.text_input("Please paste your API key and hit the 'Enter' key", type="password",
                               help = "To create and collect an API key, visit https://platform.openai.com/account/api-keys, \
                               click on 'API Key', then select 'Create new secret key' and click 'Copy'. \
                               Note: Please be mindful of the number of requests you've sent to GPT-3.5, \
                               as exceeding the free credits limit of $18 may result in additional fees.\
                               To check your usage, visit the same website and click on 'Usage'.")

        st.markdown("***")

        if KEY != '':
            # initialize chatbot
            bot = ChatGPTBot(KEY)

            st.markdown("""*Pro tip: If you wish to initiate a new conversation, you can either \
                           refresh the webpage or request the bot to disregard all previous instructions \
                           by inputting the command, "ignore all previous instructions before this one".*""")

            # Two Expanders
            st.text('')
            # message to bot
            with st.expander(":memo: MESSAGE BOT"):
                df_prompts = st.session_state['prompts']
                # get list of prompts
                prompts = sorted(list(df_prompts['act']))
                prompts = tuple(['None'] + prompts)
                # select box for prompts
                prompt_act_selected = st.selectbox(label = 'Select a built-in prompt',
                                                   options = prompts, index = 0,
                                                   help = "The collection of built-in prompts was imported from \
                                                           [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts).")
                # initial value for text message field
                if prompt_act_selected == 'None':
                    initial_value = ''
                else:
                    prompt_id = list(df_prompts[df_prompts.act == prompt_act_selected].index)[0]
                    initial_value = df_prompts.loc[prompt_id, 'prompt']
                # populate text message field with initial value
                user_message_text = st.text_area('Send text message',
                                                  placeholder = "Type your text message here and hit the 'Enter' key",
                                                  value = initial_value, height = 120)
                # send text message to bot
                bot.chatting(user_message_text, 'text')
                # output chat history
                st.text('')
                self.output_chat_history('text')
                st.text('')

            # talk to bot
            with st.expander(':speaking_head_in_silhouette: TALK TO BOT'):
                if user_message_text != '':
                    st.error('Please ensure that all content has been deleted from the text message field')
                else:
                    # record user's voice
                    audio_bytes = audio_recorder(pause_threshold = 3.0)  # stop after pausing for 3 seconds
                    if audio_bytes:
                        # transcribe voice to get user message
                        user_message_voice = bot.transcribe_voice(audio_bytes = audio_bytes)
                        st.success('Voice recording finished. Feel free to continue.')
                        # send voice message to bot
                        bot.chatting(user_message_voice, 'speak')
                    # output chat history
                    st.text('')
                    self.output_chat_history('speak')
                st.text('')

        else:
            st.error('Please enter your API key to initiate your chat!')


        # donwloading button for Desktop App
        st.text('')
        col1, col2 = st.columns([14, 7.3])
        desktop_binary_file = 'assets/OpenAI-API-Desktop-ChatBot.exe'
        with open(desktop_binary_file, 'rb') as file:
            col2.download_button(label = ':computer: Download Desktop Version',
                                 data = file,
                                 file_name = 'OpenAI-API-Desktop-ChatBot.exe',
                                 mime = 'application/octet-stream',
                                 help = 'It is recommended to install [Python](https://www.python.org/downloads/) on your local computer prior to running the desktop program.')
        st.text('')



if __name__ == '__main__':
    firefoxOptions = Options()
    firefoxOptions.add_argument("--headless")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(
        options=firefoxOptions,
        service=service,
    )

    app = App()
    app.run()
