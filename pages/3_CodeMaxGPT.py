import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
import openai
import math
from datetime import datetime
from io import StringIO


class CoderBot:
    def __init__(self, api_key):
        # set up api_key
        openai.api_key = api_key
        # store config data
        if 'message_history' not in st.session_state:
            st.session_state['message_history'] = []
        if 'bot_messages' not in st.session_state:
            st.session_state['bot_messages'] = {}


    def chatting_gpt(self,
                     prompt,
                     model = "gpt-3.5-turbo",
                     role = 'user'):
        if prompt != '':
            request = {"role": role, "content": prompt}
            st.session_state['message_history'].append(request)

            # other useful parameters: temperature and max_tokens
            completion = openai.ChatCompletion.create(
              model = model,
              messages = st.session_state['message_history'],
              temperature = 0.2
            )

            bot_message = completion['choices'][0]['message']['content']
            response = {"role": 'assistant', "content": bot_message}
            st.session_state['message_history'].append(response)

            st.session_state['bot_messages']['CoderBot <{}>:'.format(datetime.now().strftime('%H:%M:%S %Y/%m/%d'))] = bot_message



class App:
    # {extension: language}
    EXTENSIONS = {'.html': 'html', '.css': 'css', '.js': 'javascript', '.py':
                  'python', '.java': 'java', '.c': 'c_cpp', '.cs': 'csharp', '.PHP': 'php',
                  '.swift': 'swift', '.bas': 'vba', '.txt': 'plain_text'}

    def __init__(self):
        # set page config
        st.set_page_config(page_title="CodeMaxGPT",
                           page_icon=":computer:",
                           layout='wide',
                           initial_sidebar_state="collapsed")
        self.bot = None
        # add 'vba' into code language selections
        self.LANGUAGES = LANGUAGES
        self.LANGUAGES.append('vba')
        self.LANGUAGES = list(set(self.LANGUAGES))
        # store config data
        if 'files' not in st.session_state:
            st.session_state['files'] = {}
        if 'code_theme' not in st.session_state:
            st.session_state['code_theme'] = ''
        if 'code_font_size' not in st.session_state:
            st.session_state['code_font_size'] = ''


    def send_prompt(self, prompt):
        # output which files have been uploaded
        if len(st.session_state['files']) > 0:
            st.text('')
            for file in list(st.session_state['files'].keys())[::-1]:
                if file != 'Original Code':
                    st.text('[{} uploaded]'.format(file))
        # send prompt to bot
        self.bot.chatting_gpt(prompt = prompt)


    def get_code(self, c1, c2, initial_code, initial_lang):
        code_language = c1.selectbox("Language Mode", options=self.LANGUAGES, index = self.LANGUAGES.index(initial_lang))
        st.session_state['code_theme'] = c1.selectbox("Editor Theme", options=THEMES, index=THEMES.index('gruvbox'))
        st.session_state['code_font_size'] = c1.slider("Font size", 5, 24, 14)

        with c2:
            code = st_ace(
                            placeholder="Paste your code here",
                            language=code_language,
                            theme=st.session_state['code_theme'],
                            keybinding='vscode',
                            font_size=st.session_state['code_font_size'],
                            tab_size=4,
                            show_gutter=True,
                            show_print_margin=False,
                            wrap=False,
                            auto_update=True,
                            readonly=False,
                            min_lines=45,
                            key="ace",
                            height=500,
                            value = initial_code
                        )
        return code


    def get_code_language(self, file_name, default_lang):
        code_language = default_lang
        if (file_name != '') and ('.' in file_name):
            file_extension = '.' + file_name.split('.')[1]
            if file_extension in self.EXTENSIONS.keys():
                code_language = self.EXTENSIONS[file_extension]
            else:
                code_language = 'plain_text'
        return code_language


    def send_no_code(self, col1, user_message):
        if user_message != '':
            c1, c2 = col1.columns([7.9, 1])
            if c2.button('Send'):
                prompt = user_message
                # send prompt
                self.send_prompt(prompt)


    def send_code(self, c1, c2, user_message, file_name, initial_code):
        # identify code language according to file extension
        code_language = self.get_code_language(file_name, 'python')
        # get code
        code = self.get_code(c1, c2, initial_code, code_language)
        # code part of prompt
        if code != '':
            if file_name == '':
                prompt_code = 'Here is the code:\n' + code
            else:
                prompt_code = "Here is the '{}' code:\n{}".format(file_name, code)
            # print out the code
            prompt = user_message + '\n' + prompt_code
            # col2.text(prompt)
            c1_, c2_ = c2.columns([13.2, 1])
            if c2_.button('Send'):
                # store uploaded code
                if file_name != '':
                    if 'Original Code' in st.session_state['files'].keys():
                        del st.session_state['files']['Original Code']
                    st.session_state['files'][file_name] = code
                else:
                    st.session_state['files']['Original Code'] = code
                # send prompt
                self.send_prompt(prompt)


    def uploading_code(self, col1, user_message):
        upload_method = col1.selectbox(label = 'How would you prefer to upload your code?', options = ['Not now', 'Paste my code', 'Upload my code script'])
        if upload_method == 'Not now':
            self.send_no_code(col1, user_message)
        if upload_method == 'Paste my code':
            c1, c2 = st.columns([2, 9])
            # input field for file name
            file_name = c1.text_input('File Name', placeholder = 'eg. index.html', help = 'Please provide the filename, or leave it blank if not applicable.')
            # send manually pasted code
            self.send_code(c1, c2, user_message, file_name, '')
        if upload_method == 'Upload my code script':
            # file uploader
            uploaded_file = st.file_uploader("Upload a file from your local computer")
            if uploaded_file is not None:
                c1, c2 = st.columns([2, 9])
                # get file name
                file_name = uploaded_file.name
                # get script code
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                script_code = stringio.read()
                # automatically paste script code to code editor and send
                self.send_code(c1, c2, user_message, file_name, script_code)


    def show_code_uploaded(self, col2):
        if len(st.session_state['files']) > 0:
            col2.markdown('Expand to view the uploaded code below:')
            for file, code in list(st.session_state['files'].items())[::-1]:
                with col2.expander(label = file, expanded = False):
                    # set language for code editor
                    code_language = self.get_code_language(file, 'plain_text')
                    # code editor
                    st_ace(
                            value = code,
                            language = code_language,
                            theme=st.session_state['code_theme'],
                            keybinding='vscode',
                            font_size=st.session_state['code_font_size'],
                            tab_size=4,
                            show_gutter=True,
                            show_print_margin=False,
                            wrap=False,
                            auto_update=True,
                            readonly=True,
                            min_lines=45,
                            key="ace-{}".format(file),
                            height=400
                         )


    def run(self):
        st.title('Introducing CodeMaxGPT')
        st.header('Code Big, Even If You Are Junior!')
        st.subheader("Simplifying Coding With CodeMaxGPT-3.5: Your AI Coding Assistant For Easy Code Generation, Refactoring, and Documentation :computer:")

        cl1, cl2 = st.columns([1, 2])
        # Enter API Key
        KEY = cl1.text_input("Please paste your API key and hit the 'Enter' key", type="password",
                               help = "To create and collect an API key, visit https://platform.openai.com/account/api-keys, \
                               click on 'API Key', then select 'Create new secret key' and click 'Copy'. \
                               Note: Please be mindful of the number of requests you've sent to GPT-3.5, \
                               as exceeding the free credits limit of $18 may result in additional fees.\
                               To check your usage, visit the same website and click on 'Usage'.")

        st.markdown("***")

        if KEY == '':
            st.error('Please enter your API key to start the service!')
        else:
            # initialize chatbot
            self.bot = CoderBot(KEY)

            st.text('')
            col1, col2 = st.columns([1, 1.25])

            # Select an action
            action = col1.selectbox(label = 'Select a desired action for your code',
                                    options = ['Specify Custom Requirements', 'Refactor Code',  \
                                               'Refactor Code to OOP', 'Comment Code', 'Generate GitHub README'], index = 0)

            if action == 'Generate GitHub README':
                # display code uploaded
                self.show_code_uploaded(col2)
                # input field for repo url
                repo_url = col1.text_input('Enter HTTPS URL of a remote GitHub repo',
                                          placeholder = 'https://github.com/<user>/<repo>.git',
                                          help = 'If you desire to generate a README for a particular GitHub repository, \
                                          please input the HTTPS URL of that repo in the field below. \
                                          Alternatively, if you wish to generate one for the uploaded program, leave the field blank.')
                if repo_url == '':
                    prompt = "Generate the GitHub README for the entire program."
                else:
                    prompt = "Generate the GitHub README for the github repo: {}.".format(repo_url)
                # Generate button
                if (st.session_state['files'] != {}) or (repo_url != ''):
                    c1, c2 = col1.columns([5, 1])
                    if c2.button('Generate'):
                        # send prompt
                        self.send_prompt(prompt)
                        # get README content
                        readme = list(st.session_state['bot_messages'].values())[-1]
                        # download button for README file
                        c1.download_button(label = 'Download README for immediate use',
                                           data = readme,
                                           file_name = 'README.txt',
                                           mime = 'text/plain')
                        # note on README content
                        st.text('')
                        st.markdown("[_Note: This action quickly generates a README for your project. For further customization, \
                                    please copy the generated content and choose to work with 'Specify Custom Requirements' option._]")
                        # display README in code editor
                        st_ace(
                                value = readme,
                                language = 'plain_text',
                                theme='gruvbox',
                                keybinding='vscode',
                                tab_size=4,
                                show_gutter=True,
                                show_print_margin=False,
                                wrap=False,
                                auto_update=True,
                                readonly=True,
                                min_lines=45,
                                key="ace-readme",
                                height=500
                             )
            else:
                if action == 'Specify Custom Requirements':
                    user_message = col1.text_area('Specify your requirements here',
                                                  placeholder = "Try:\nBuild an app in Python where users... \
                                                                \nDebug the code... \
                                                                \nWrite a documentation page for the entire program... \
                                                                \nMake the code more elegant... \
                                                                \nWrite a test program for the code using unittest...",
                                                  value = '', height = 200)
                if action == 'Refactor Code':
                    user_message = "Refactor the code in a more efficient way. Rewrite the code in a code block."
                if action == 'Refactor Code to OOP':
                    user_message = "Refactor the code in a more efficient way. Rewrite the code to OOP in a code block."
                if action == 'Comment Code':
                    user_message = 'Add comments to the code.'

                # choose a code uploading method
                self.uploading_code(col1, user_message)

                # display code uploaded
                self.show_code_uploaded(col2)

            st.text('')
            # print out bot's historical responses
            if len(st.session_state['bot_messages']) > 0:
                for key, value in list(st.session_state['bot_messages'].items())[::-1]:
                    st.markdown("<span style='color:#FF4B4B'><strong>" + key + "</strong></span>", unsafe_allow_html=True)
                    st.markdown(value)
                    st.markdown('---')




if __name__ == '__main__':
    app = App()
    app.run()
