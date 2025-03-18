import streamlit as st



# Set page config
st.set_page_config(
    page_title="OpenAI Web Applications",
    page_icon=":robot_face:",
    layout="centered",
    initial_sidebar_state="auto",
)

# Display the title of the web app
st.title("WELCOME TO OPENAI WEB SERVICES!")
# Display a header that briefly describes the web apps
st.header(
    (
        ":rocket: An Unofficial Platform For Custom Web Applications "
        "Powered By OpenAI APIs"
    )
)

# Display a subheader that indicates the author of the web apps
st.subheader(":sunglasses: By Maxine Xiong")

# Display a markdown bold text with instructions for the users ...
# ...and a message about upcoming OpenAI applications
st.markdown(
    "**Please feel free to explore the following web apps or share your "
    "feedback to my email <maxinexiong2@gmail.com>. More exciting OpenAI "
    "applications are coming on the way, so stay tuned! :clinking_glasses:**"
)

# Display a markdown bullet point with a microphone emoji and ...
# ...a link to "Talk To GPT" app
st.markdown("- **[:microphone: Talk To GPT](./Talk_To_GPT)**")
# Display a markdown bullet point with a computer emoji and ...
# ...a link to "CodeMaxGPT" app
st.markdown("- **[:computer: CodeMaxGPT](./CodeMaxGPT)**")

# Also display a message that the app is currently unavailable
# st.markdown(
#     "- **[:frame_with_picture: DALL·E Image Generator (coming soon)]"
#     "(./DALL·E_Image_Generator_(coming_soon))**: Currently unavailable "
#     ":no_entry: due to an issue with the validity of API keys :key: for "
#     "the DALL·E model. Awaiting resolution from OpenAI."
# )

# Display an empty line
st.text("")
# Display an image from the 'assets' folder named 'cover-page.gif'
st.image("assets/cover-page.gif")
