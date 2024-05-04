import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
from openai import OpenAI
import math
from datetime import datetime
from io import StringIO



# Define the class for the bot
class CoderBot:
    # The initializer method gets executed when a new CoderBot object (i.e. bot) is created
    def __init__(self, api_key, selected_model = 'gpt-4-turbo'):
        # Instantiate a client object using api_key
        self.api_key = api_key
        self.client = OpenAI(api_key = self.api_key)

        # Initialize session state variables
        if 'bot_messages' not in st.session_state:
            st.session_state['bot_messages'] = {}
        if 'user_messages' not in st.session_state:
            st.session_state['user_messages'] = {}
        # Create a new object of Assistant and store it as a session state variable
        if 'assistant' not in st.session_state:
            st.session_state['assistant'] = self.client.beta.assistants.create(
                    name = 'coding assistant',
                    instructions = "You are an AI coding assistant. Your role involves performing a wide range of tasks to help users program more efficiently.\
                                    These tasks may include generating code, debugging, refactoring, documenting, and addressing other custom requests from users. \
                                    Please adhere strictly to the user's requirements.",
                    tools = [{'type': 'code_interpreter'}],
                    model = selected_model
                )
        # Create a Thread for new conversation and store it as a session state variable
        if 'thread' not in st.session_state:
            st.session_state['thread'] = self.client.beta.threads.create()


    # The bot sends user's prompt to GPT model and receives API response
    # Document and update the historical user and bot messages in session state
    def chatting_gpt(self, prompt):
        if prompt.strip() != '':
            # Document the user's message in a dictionary variable in session state with the current timestamp as the key
            st.session_state['user_messages']['You <{}>:'.format(datetime.now().strftime('%H:%M:%S %Y/%m/%d'))] = prompt

            # Add the user message to the thread
            request = self.client.beta.threads.messages.create(
                thread_id = st.session_state['thread'].id,
                role = 'user',
                content = prompt
            )
            # Start a run in the thread using the current assistant and wait for comletion
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id = st.session_state['thread'].id,
                assistant_id = st.session_state['assistant'].id
            )
            # Check if the run has completed successfully
            if run.status == 'completed':
                # Retrieve the list of messages from the thread
                messages = self.client.beta.threads.messages.list(
                    thread_id = st.session_state['thread'].id
                )
                # Extract the latest bot message from the response data
                bot_message = messages.data[0].content[0].text.value
            else:
                # If the run did not complete, set bot_message to None and print the run status
                bot_message = None
                print(run.status)

            # Print the bot's response to the console
            print(bot_message)
            # Document the latest bot's messages in a dictionary variable in session state with the current timestamp as the key
            st.session_state['bot_messages']['CoderBot <{}>:'.format(datetime.now().strftime('%H:%M:%S %Y/%m/%d'))] = bot_message



# Define the class for the app
class App:
    # Dictionary mapping the file extensions to programming languages {file extension: language}
    EXTENSIONS = {'.html': 'html', '.css': 'css', '.js': 'javascript', '.py':
                  'python', '.java': 'java', '.c': 'c_cpp', '.cs': 'csharp', '.PHP': 'php',
                  '.swift': 'swift', '.bas': 'vba', '.txt': 'plain_text'}

    # The initializer method gets executed when a new object of the App is created
    def __init__(self):
        # set page config
        st.set_page_config(page_title="CodeMaxGPT",
                           page_icon=":computer:",
                           layout='wide',
                           initial_sidebar_state="collapsed")
        # Initialize the bot instance as None
        self.bot = None
        # Add 'vba' into code language selections
        self.LANGUAGES = LANGUAGES
        self.LANGUAGES.append('vba')
        # Remove duplicates from the list of languages
        self.LANGUAGES = list(set(self.LANGUAGES))
        # Initialize session state variables for config data storage
        if 'files' not in st.session_state:
            st.session_state['files'] = {}
        if 'code_theme' not in st.session_state:
            st.session_state['code_theme'] = ''
        if 'code_font_size' not in st.session_state:
            st.session_state['code_font_size'] = ''


    # Send user's prompt to the bot
    def send_prompt(self, prompt):
        # Check if there's any code uploaded
        if len(st.session_state['files']) > 0:
            st.text('')
            # Iterate over the code files in reverse order
            for file in list(st.session_state['files'].keys())[::-1]:
                # Display the names of the code files uploaded on the web page
                if file != 'Original Code':
                    st.text('[{} uploaded]'.format(file))
        # The bot sends user's prompt to GPT model for chat processing
        self.bot.chatting_gpt(prompt = prompt)


    # Get user's code from the code editor
    def get_code(self, initial_code, initial_lang):
        # Dropdown box for code language selecton
        code_language = self.c1.selectbox("Language Mode", options=self.LANGUAGES, index = self.LANGUAGES.index(initial_lang))
        # Dropdown box for editor theme selection. The editor theme by default is 'tomorrow_night'
        st.session_state['code_theme'] = self.c1.selectbox("Editor Theme", options=THEMES, index=THEMES.index('tomorrow_night'))
        # Dropdown box for editor font size selection. The font size ranges between 5 and 24, and is 14 by default
        st.session_state['code_font_size'] = self.c1.slider("Font size", 5, 24, 14)

        # Code editor for the user to input their code
        with self.c2:
            code = st_ace(
                            placeholder="Input your code here",
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
                            height=self.code_editor_height,
                            value = initial_code
                        )  # readonly=False: make the code editor editable
        # Get user's code
        return code


    # Determine the code language based on the file extension
    def get_code_language(self, file_name, default_lang):
        # Set the specified default language as the intitial value of code_language
        code_language = default_lang
        # Check if the file name contains a file extension
        if (file_name.strip() != '') and ('.' in file_name):
            # Extract the file extension
            file_extension = '.' + file_name.split('.')[1]
            # Check if the file extension exists in the EXTENSIONS dictionary
            if file_extension in self.EXTENSIONS.keys():
                # Set the code language based on the file extension
                code_language = self.EXTENSIONS[file_extension]
            else:
                # If the file extension is not found, set the language as plain text
                code_language = 'plain_text'
        # Return the determined code language
        return code_language


    # Send user's text prompt only to the bot
    def send_no_code(self, user_message):
        # 'Send' button appears only when the user message is entered
        if user_message.strip() != '':
            # If the 'Send' button is clicked
            if self.col1.button('Send'):
                prompt = user_message
                # Send the text prompt to the bot
                self.send_prompt(prompt)


    # Send user's text prompt and the code input together to the bot
    def send_code(self, user_message, file_name, initial_code):
        # Determine code language based on the file extension
        initial_code_language = self.get_code_language(file_name = file_name, default_lang = 'python')
        # Get user's code in string
        code = self.get_code(initial_code = initial_code, initial_lang = initial_code_language)
        # The 'Send' button appears only when user has uploaded their code
        if code.strip() != '':
            # Construct the prompt containing the code
            if file_name.strip() == '':
                prompt_code = 'Here is the code:\n' + code
            else:
                # Include code file name in the prompt
                prompt_code = "Here is the '{}' code:\n{}".format(file_name, code)
            # Combine the user's text prompt and code prompt together
            prompt = user_message + '\n' + prompt_code
            # self.col3.text(prompt)
            # Add 3 lines of white space
            self.c1.markdown('#')
            self.c1.markdown('#')
            self.c1.markdown('##')
            # If the 'Send' button is clicked
            if self.c1.button('Send'):
                # Store the uploaded code in the session state
                if file_name.strip() != '':
                    # If the uploaded code has a file name, use the file name as the key
                    if 'Original Code' in st.session_state['files'].keys():
                        del st.session_state['files']['Original Code']
                    st.session_state['files'][file_name] = code
                else:
                    # If the uploaded code doesn't have a file name, use 'Original Code' as the key
                    st.session_state['files']['Original Code'] = code
                # Send the final prompt to the bot
                self.send_prompt(prompt)


    # Three ways of uploading code
    def uploading_code(self, user_message):
        # Dropdown box for selecting a method to upload code
        upload_method = self.col1.selectbox(label = 'How would you prefer to upload your code?', options = ['Not now', 'Enter / paste my code', 'Upload my code script'])
        # If the user choose not to upload the code now...
        if upload_method == 'Not now':
            # send the user's text prompt only to the bot
            self.send_no_code(user_message)
        # If the user choose to enter or paste the code manually...
        if upload_method == 'Enter / paste my code':
            self.c2, self.c1 = st.columns([9, 2])
            # Set the height of code editor to 496
            self.code_editor_height = 496
            # Display a text input field for file name
            file_name = self.c1.text_input('File Name', placeholder = 'eg. index.html', help = 'Please provide the filename, or leave it blank if not applicable.')
            # Send the user's text prompt and the manually entered/pasted code together to the bot
            self.send_code(user_message = user_message,
                           file_name = file_name,
                           initial_code = '')
        # If the user choose to input the code by uploading a code script...
        if upload_method == 'Upload my code script':
            # Display a file uploader
            uploaded_file = st.file_uploader("Upload a file from your local computer")
            if uploaded_file is not None:
                # Get file name
                file_name = uploaded_file.name
                # Get the script code in string
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                script_code = stringio.read()
                # Set the height of code editor to 410
                self.code_editor_height = 410
                # Automatically paste the script code to the code editor
                # and send the user's text prompt and code input together to the bot
                self.c2, self.c1 = st.columns([9, 2])
                self.send_code(user_message = user_message,
                               file_name = file_name,
                               initial_code = script_code)


    # Display the uploaded code inside Expanders on the web page
    def show_code_uploaded(self):
        # Check if there's any code uploaded
        if len(st.session_state['files']) > 0:
            self.col3.markdown('Expand to view the uploaded code below:')
            # Iterate over the uploaded code files in reverse order
            for file, code in list(st.session_state['files'].items())[::-1]:
                # Display an Expander for each code file
                with self.col3.expander(label = file, expanded = False):
                    # Determine the code language for the code editor
                    code_language = self.get_code_language(file, 'plain_text')
                    # Display the uploaded code in code editor inside each Expander
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
                            height=300
                         ) # readonly=True: make the code editor read only


    # Display chat history
    def output_chat_history(self):
        # Check if there are any messages stored in the bot messages session state
        if len(st.session_state['bot_messages']) > 0:
            # Convert the bot and user messages into lists of tuples
            bot_messages_pairs = list(st.session_state['bot_messages'].items())
            user_messages_pairs = list(st.session_state['user_messages'].items())

            # Loop through the messages in reverse order to display the most recent first
            for i in range(len(bot_messages_pairs)-1, -1, -1):
                # Retrieve the label and content for both bot and user messages based on current index
                label_bot = bot_messages_pairs[i][0]
                content_bot = bot_messages_pairs[i][1]
                label_user = user_messages_pairs[i][0]
                content_user = user_messages_pairs[i][1]

                # Display the bot's message label
                st.markdown("<span style='color:#6699FF'><strong>" + label_bot + "</strong></span>", unsafe_allow_html=True)
                # Display the bot's message content
                st.markdown(content_bot)

                # Display user's message label
                st.markdown("<span style='color:#6699FF'><strong>" + label_user + "</strong></span>", unsafe_allow_html=True)
                # Display the user's message content
                st.markdown(content_user)



    # Run the application
    def run(self):
        # Set the page title
        st.title('Welcome to CodeMaxGPT')
        # st.header('Code Big, Even If You Are Junior!')
        # Display a subheader that briefly describe the coding assistant web app
        st.subheader("Simplifying Coding With CodeMaxGPT: Your AI Coding Assistant For Easy Code Generation, Debugging, Refactoring, and Documentation :computer:")

        # Get the API key from the user
        cl1, cl2, cl3 = st.columns([1, 0.8, 1])
        KEY = cl1.text_input("Enter your API Key", type="password",
                              help = "To create and collect an API key, visit https://platform.openai.com/api-keys, \
                                      click on 'Create new secret key' and then click 'Copy' and paste your API key in the field below. \
                                      Note: Please be mindful of the usage you are consuming.\
                                      To keep track of your ongoing usage and cost, please visit https://platform.openai.com/usage.")

        # Get the GPT model selected by the user
        MODEL = cl3.selectbox('Select a GPT model', ('gpt-4-turbo', 'gpt-3.5-turbo'),
                               help = "For many basic tasks, the difference between GPT4 \
                                       and GPT-3.5 model is not significant. However, in more complex reasoning situation, \
                                       GPT-4 is much more capable than any of the previous models, though it does come at a higher usage cost. \
                                       Please visit https://platform.openai.com/docs/models/overview for more information on GPT models.")

        # Mark down a breakline
        st.markdown("***")

        # If API key is not entered
        if KEY == '':
            st.error('Please enter your API key to start the service!')
        # If API key is entered
        else:
            # Initialize the bot with the provided API key and selected model
            self.bot = CoderBot(api_key = KEY, selected_model = MODEL)

            st.text('')
            self.col1, col2, self.col3 = st.columns([1, 0.25, 1])

            # Dropdown box for coding task selection
            action = self.col1.selectbox(label = 'How can the bot assist with your code?',
                                         options = ['Specify Custom Requirements', 'Debug Code', 'Refactor Code',  \
                                                    'Refactor Code to OOP', 'Comment Code', 'Review Code', \
                                                    'Generate GitHub README', \
                                                    'Suggest a Solution For a Coding Challenge', \
                                                    '[Delete all previously uploaded files]'], index = 0)

            # If user choose to generate a GitHub README
            if action == 'Generate GitHub README':
                # Display code uploaded
                self.show_code_uploaded()
                # Display text input field for repo URL
                repo_url = self.col1.text_input('Enter HTTPS URL of a remote GitHub repo',
                                                 placeholder = 'https://github.com/<user>/<repo>.git',
                                                 help = 'If you intend to generate a README for a particular GitHub repository, \
                                                 please input the [HTTPS URL](https://docs.github.com/en/get-started/getting-started-with-git/about-remote-repositories) of that repo in the field below. \
                                                 Alternatively, if you wish to generate one for the uploaded program, leave the field blank.')
                # Construct the prompt based on the repo URL entry
                if repo_url.strip() == '':
                    prompt = "Generate the GitHub README for the entire program."
                else:
                    prompt = "Generate the GitHub README for the github repo: {}.".format(repo_url)
                # 'Generate' button only appears when there's code uploaded or when a repo URL is provided
                if (st.session_state['files'] != {}) or (repo_url.strip() != ''):
                    # If 'Generate' button is clicked
                    if self.col1.button('Generate'):
                        # Send the prompt to the bot
                        self.send_prompt(prompt)
                        # Get the generated README content
                        readme = list(st.session_state['bot_messages'].values())[-1]
                        # Display a download button for README file
                        self.col1.download_button(label = 'Download README for immediate use',
                                                  data = readme,
                                                  file_name = 'README.txt',
                                                  mime = 'text/plain')
                        # Note on README content
                        st.text('')
                        st.markdown("[_Note: This action quickly generates a README for your project. For further customization, \
                                    please copy the generated content and choose to work with 'Specify Custom Requirements' option._]")
                        # Display README in code editor
                        st_ace(
                                value = readme,
                                language = 'plain_text',
                                theme='tomorrow_night',
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
                             ) # readonly=True: make the code editor read only

            # If user wants to get a suggested solution for a coding challenge
            elif action == 'Suggest a Solution For a Coding Challenge':
                # Coding languages available for solving code challenges
                coding_langs = ['Python', 'Java', 'MySQL', 'MS SQL Server', 'Oracle SQL', 'JavaScript',
                               'C#', 'C', 'C++', 'Ruby', 'Swift', 'Go', 'Scala', 'Kotlin', 'Rust',
                               'PHP', 'TypeScript', 'Racket', 'Erlang', 'Elixir', 'Dart']
                _c1, _c2 = self.col1.columns([3, 1])
                # Display a text area for inputing coding challenge
                coding_problem = _c1.text_area('Input the coding challenge',
                                              placeholder = "Describe the challenge in detail:\neg. Create an algorithm that returns a list of prime numbers up until the given number x. \
                                                             \nOR\nPaste the website URL of the coding problem:\neg. https://leetcode.com/problems/number-of-enclaves/",
                                              value = '', height = 170)
                # Dropdown box for coding language selection
                lang_selected = _c2.selectbox("Language Mode", options = coding_langs, index = 0)
                # Construct the prompt based on the selected coding language
                if 'SQL' in lang_selected:
                    prompt = 'Solve the problem in {}:\n'.format(lang_selected) + coding_problem + '\nExplain the solution and display it in a code block.'
                else:
                    prompt = 'Solve the problem in {}:\n'.format(lang_selected) + coding_problem \
                             + '\nExplain the solution and display it in a code block.\nAlso, Clarify the time and space complexity of the solution.'
                # 'Send' button only appears if the coding problem is entered
                if coding_problem.strip() != '':
                    # Add 3 lines of white space
                    _c2.markdown('##')
                    _c2.markdown('###')
                    _c2.markdown('###')
                    # If the 'Send' button is clicked
                    if _c2.button('Send'):
                        # Send the prompt to the bot
                        self.send_prompt(prompt)

            # If user selects a coding task other than 'Generate GitHub README' and 'Suggest a Solution For a Coding Challenge'
            else:
                # Construct prompt based on the selected coding task
                if action == 'Specify Custom Requirements':
                    user_message = self.col1.text_area('Specify your requirements here',
                                                  placeholder = "Try:\nBuild an app in Python where users... \
                                                                \nWrite a documentation page for the entire program... \
                                                                \nMake the code more elegant... \
                                                                \nWrite a test program for the code using unittest...",
                                                  value = '', height = 180)
                if action == 'Debug Code':
                    user_message = "Debug the code. Clarify where went wrong and what caused the error. Rewrite the code in a code block."
                if action == 'Refactor Code':
                    user_message = "Refactor the code in a more efficient way. Rewrite the code in a code block."
                if action == 'Refactor Code to OOP':
                    user_message = "Refactor the code in a more efficient way. Rewrite the code to OOP in a code block."
                if action == 'Comment Code':
                    user_message = 'Add comments to the code line by line. Display all the comments and code inside a code block.'
                if action == 'Review Code':
                    user_message = "Review the code. Provide feedback on any issues you identify \
                                    by pointing out the line numbers and briefly explaining the problem. Suggest \
                                    how to improve. Display the updated code inside a code block."
                if action == '[Delete all previously uploaded files]':
                    st.session_state['files'] = {}
                    user_message = self.col1.text_area('Specify your requirements here',
                                                        value = 'Please disregard any previously provided code.', height = 180)

                # Choose a method to upload code
                self.uploading_code(user_message)

                # Display the code uploaded (if any) for view
                self.show_code_uploaded()

            st.text('')

            # Output chat history
            self.output_chat_history()




# Check if the module is being executed as the main module
if __name__ == '__main__':
    # Create an instance of the App class
    app = App()
    # Call run() method to start the application
    app.run()
