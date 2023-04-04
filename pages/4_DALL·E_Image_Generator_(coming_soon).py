# st.markdown('![Test Image](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)')
import streamlit as st
import openai

class ImageGenerator:
    def __init__(self, api_key):
        # set up api_key
        openai.api_key = api_key
        self.api_key = api_key
        # for image storing
        if 'prompts' not in st.session_state:
            st.session_state['prompts'] = []
        if 'image_urls' not in st.session_state:
            st.session_state['image_urls'] = []

    def DallE_generate(self, prompt, num_images, image_size):
        # check for API: https://platform.openai.com/docs/guides/images/introduction
        pass

    def generating_images(self):
        if self.api_key == '':
            st.error('Please enter your API key to initiate the generation!')
        else:
            st.error('The image generation is TEMPORARILY UNAVAILABLE :no_entry: due to an issue with the validity of API keys :key: for the DALL·E model. Awaiting resolution :pick: from OpenAI.')
            pass





def main():
    # set page config
    st.set_page_config(page_title="DALL·E Image Generator",
                       page_icon=":art:",
                       layout='centered',
                       initial_sidebar_state="auto")

    st.title('Welcome to DALL·E Image Generator')
    st.subheader("Experience The Magic Of OpenAI's DALL·E Image Generator Bot: Describe, Create, Amaze! :art: ")

    # Enter API Key
    col1, col2 = st.columns([1, 1])
    KEY = col1.text_input("Please paste your API key and hit the 'Enter' key", type="password",
                           help = "To create and collect an API key, visit https://platform.openai.com/account/api-keys, \
                           click on 'API Key', then select 'Create new secret key' and click 'Copy'. \
                           Note: Please be mindful of the number of requests you've sent to GPT-3.5, \
                           as exceeding the free credits limit of $18 may result in additional fees.\
                           To check your usage, visit https://platform.openai.com/account/api-keys and click on 'Usage'.")

    st.markdown("***")

    # initialize the bot
    bot = ImageGenerator(KEY)

    # text area for prompt
    prompt = st.text_area("Describe The Desired Image",
                           placeholder = "Provide a detailed description here",
                           value = '')

    col1, col2, col3 = st.columns([1, 0.3, 1])
    # number input area for num_images
    num_images = col1.number_input('How many image variants to generate', value = 1)
    num_images = int(num_images)
    # select box for image size
    col3.selectbox('Select the size of image', ('1024x1024', '512x512', '256x256'))

    col1, col2 = st.columns([3, 1])
    # submit button
    if prompt == '':
        col2.button('Submit and Generate', help = 'Please ensure all fields have been completed.', disabled = True)
    else:
        if col2.button('Submit and Generate', disabled = False):
            bot.generating_images()

    st.text('')

    st.markdown('![Test Image](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)')



if __name__ == '__main__':
    main()
