import streamlit as st

# set page config
st.set_page_config(page_title="OpenAI Web Applications",
                   page_icon=":robot_face:",
                   layout='centered',
                   initial_sidebar_state="auto")

st.title("WELCOME TO OPENAI WEB SERVICES!")
st.header(":rocket: An Unofficial Platform For Custom Web Applications Powered By OpenAI APIs")
st.subheader(':sunglasses: By Maxine Xiong')

st.markdown('**Please feel free to explore the following web apps or share your feedback to my email <maxinexiong2@gmail.com>. \
             More exciting OpenAI applications are coming on the way, so stay tuned! :clinking_glasses:**')

st.markdown('- **[:microphone: Talk To GPT-3.5](./Talk_To_GPT3.5)**')
st.markdown('- **[:computer: CodeMaxGPT](./CodeMaxGPT)**')
st.markdown("- **[:frame_with_picture: DALL·E Image Generator (coming soon)](./DALL·E_Image_Generator_(coming_soon))**: \
             Currently unavailable :no_entry: due to an issue with the validity of API keys :key: for the DALL·E model. Awaiting resolution from OpenAI.")

st.text('')
st.image('assets/cover-page.gif')
