# OpenAI-API-Web-Apps 

[![GitHub](https://badgen.net/badge/icon/GitHub?icon=github&color=black&label)](https://github.com/MaxineXiong)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)](https://chat.openai.com/)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://maxinexiong-openai-api-web-apps-home-xbxlm8.streamlit.app/) 

<br/>

## Table of Contents
- [Project Description](#project-description)
  - [Talk to GPT-3.5](#talk-to-gpt-35)
  - [CodeMaxGPT](#codemaxgpt)
  - [DALL·E Image Generator (Unavailable)](#dalle-image-generator-unavailable)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Usage](#usage)
  - [Get Started with Talk to GPT-3.5](#get-started-with-talk-to-gpt-35)
  - [Get Started with CodeMaxGPT](#get-started-with-codemaxgpt)
- [Contribution](#contribution)
- [License](#license)
- [Acknowledgement](#acknowledgement)

<br/>

## Project Description

Welcome to the **[unofficial platform for custom web applications powered by OpenAI APIs](https://maxinexiong-openai-api-web-apps-home-xbxlm8.streamlit.app/)**! This repository hosts 
a collection of web applications deployed on *[Streamlit Cloud](https://streamlit.io/cloud)*. These applications leverage the capabilities of OpenAI's powerful language models to provide 
unique functionalities. Currently, the platform includes three web applications:

### Talk to GPT-3.5
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://maxinexiong-openai-api-web-apps-home-xbxlm8.streamlit.app/Talk_To_GPT3.5) 

The first web application, **[Talk to GPT-3.5](https://maxinexiong-openai-api-web-apps-home-xbxlm8.streamlit.app/Talk_To_GPT3.5)**, is an interactive chatbot application that allows users to 
communicate with the model using text messages or speech input. Powered by OpenAI's **Whisper model** for speech-to-text conversion and the **gpt-3.5-turbo model** for generating high-quality 
responses, this application offers a conversational experience similar to interacting with a human expert. Users also have the option to play the bot's responses in audio format, enhancing 
the conversational experience with a greater sense of immersion and realism. Additionally, the application provides a variety of built-in prompts that assign roles or personas to the chatbot, 
providing an effective starting point for each type of conversation, and ensuring that the chatbot will produce the desired responses in an efficient manner.

### CodeMaxGPT
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://maxinexiong-openai-api-web-apps-home-xbxlm8.streamlit.app/CodeMaxGPT) 

The second web application, **[CodeMaxGPT](https://maxinexiong.github.io/intro-codemaxgpt.html)**, is designed to provide coding assistance to programmers. Built on OpenAI's gpt-3.5-turbo model, 
it is specifically tuned and optimized to cater to the diverse needs of developers, including code generation, debugging, refactoring, and documentation. The platform provides auto-prompts 
for the GPT model based on various use cases that a user may select. It also features a more user-friendly interface compared to the original [ChatGPT](https://openai.com/blog/chatgpt), allowing users to comfortably enter or 
paste code and even upload code scripts directly from their local computer. With its user-friendly interface, advanced auto-prompting features, and seamless code uploading capabilities, 
**[CodeMaxGPT](https://maxinexiong.github.io/intro-codemaxgpt.html)** is the ultimate coding companion. Whether you're a junior developer tackling complex programs or a seasoned pro exploring 
new languages or frameworks, **[CodeMaxGPT](https://maxinexiong.github.io/intro-codemaxgpt.html)** has you covered.

### DALL·E Image Generator (Unavailable)

Please note that the third web application that’s based on the DALL·E model is currently unavailable due to issues with the validity of API keys. Stay tuned for updates on the availability 
of this exciting application.

<br/>

## Features

**[Talk to GPT-3.5](https://maxinexiong-openai-api-web-apps-home-xbxlm8.streamlit.app/Talk_To_GPT3.5)** provides the following features:

1) Enables communication with the GPT model through either **text messages** or **speech input**.

2) Employs the gpt-3.5-turbo model to **generate high-quality human-like responses** to user’s prompts.

3) Utilizes OpenAI's Whisper model for accurate **speech-to-text conversion** for user’s speech input.

4) Provides an option to **play the bot’s responses in audio format** for an immersive and realistic conversational experience.

5) Offers a variety of **built-in prompts** that assign roles or personas to the chatbot, provides an effective starting point for each type of conversations, and ensures that the chatbot will produce the desired responses in an efficient manner.

Below are the features offered by **[CodeMaxGPT](https://maxinexiong.github.io/intro-codemaxgpt.html)**:

1) Built upon OpenAI’s gpt-3.5-turbo model, **specifically tuned and optimized** to provide coding assistance to programmers of all levels.

2) Supports **various coding tasks**, including code generation, debugging, refactoring, adding comments, code reviewing, generating GitHub README, and suggesting solutions to coding challenges.

3) Provides **auto-prompts** for the GPT model tailored to the various coding tasks that users may need help with.

4) Offers a **user-friendly interface** that surpasses the original ChatGPT.

5) Allows **comfortable code entry and pasting**, and **direct uploading of code scripts** from the user’s local computer, for enhanced convenience.

6) Enables users to code confidently in unfamiliar territory.

<br/>

## Repository Structure

The repository structure of the project is as follows:
```
OpenAI-API-Web-Apps/
├── .streamlit/
│   └── config.toml
├── assets/
│   ├── OpenAI-API-Desktop-Chatbot.exe
│   └── cover-page.gif
├── pages/
│   ├── 2_Talk_To_GPT3.5.py
│   ├── 3_CodeMaxGPT.py
│   └── 4_DALL·E_Image_Generator_(coming_soon).py
├── Home.py
├── packages.txt
├── requirements.txt
├── README.md
└── LICENSE
```
The description of each file and folder in the repository is as follows:

* **.streamlit/**: This folder contains the **config.toml** file, which configures the appearance of the Streamlit web application. The **config.toml** file specifies the theme settings such as primary color, background color, text color, and font.
* **assets/**: This folder contains additional assets used in the project, including the **cover-page.gif** image file for the cover page. It also includes the **OpenAI-API-Desktop-Chatbot.exe**, which is the desktop version of [**Talk to GPT-3.5**](https://maxinexiong-openai-api-web-apps-home-xbxlm8.streamlit.app/Talk_To_GPT3.5). You can find the source code for the desktop application in the [ChatGPT-3.5-Desktop-App](https://github.com/MaxineXiong/ChatGPT-3.5-Desktop-App.git) repository.
* **pages/**: This folder contains the Python code that powers the three web applications. It includes the following Python scripts:
    - **2_Talk_To_GPT3.5.py**: Python script for the [**Talk to GPT-3.5**](https://maxinexiong-openai-api-web-apps-home-xbxlm8.streamlit.app/Talk_To_GPT3.5) web application.
    - **3_CodeMaxGPT.py**: Python script for the [**CodeMaxGPT**](https://maxinexiong-openai-api-web-apps-home-xbxlm8.streamlit.app/CodeMaxGPT) web application.
    - **4_DALL·E_Image_Generator_(coming_soon).py**: Python script for the **DALL·E Image Generator** web application (coming soon).
* **Home.py**: This is a Python script for the home page of the Streamlit web applications. It contains code related to the navigation between the three web applications.
* **packages.txt**: The file manages the project dependencies and is necessary for deploying the web applications on _Streamlit Cloud_.
* **requirements.txt**: This file lists all the required Python modules and packages. It is also necessary for the deployment of the web applications on _Streamlit Cloud_. It ensures that the required dependencies are installed when deploying the applications.
* **README.md**: Provides an overview of this repository.
* **LICENSE**: The license file for the project.

<br/>

## **Usage**

The web applications are currently hosted on *Streamlit Cloud*. To access the applications, please visit [**OpenAI API Web Applications on Streamlit**](https://maxinexiong-openai-api-web-apps-home-xbxlm8.streamlit.app/). Once you visit the URL, you will be presented with a home page where you can select the desired web application. Click on the application you want to use, and it will open in a new tab or window.

### **Get Started with Talk to GPT-3.5**

To use the **Talk to GPT-3.5** application, follow these steps:

1. Visit the [**Talk to GPT-3.5 on Streamlit**](https://maxinexiong-openai-api-web-apps-home-xbxlm8.streamlit.app/Talk_To_GPT3.5).
2. Input your [OpenAI API key](https://platform.openai.com/account/api-keys) in the field at the top.
3. You can start interacting with the chatbot using either the "MESSAGE BOT" or "TALK TO BOT" options.
4. For text input, click on the "MESSAGE BOT" expander, select a built-in prompt from the dropdown menu, and press CTRL + Enter to submit. The chatbot will respond with a generated message. You can continue the conversation by entering your own messages.
5. For speech input, make sure the text message input field is cleared, then click on the "TALK TO BOT" expander, click on the microphone icon, and speak your message. The speech input will be converted to text, and the chatbot will respond accordingly.

Below are two GIF images that demonstrate the usage of the **Talk to GPT-3.5** application:


<p align='center'>
    <img width=600 src="https://github.com/MaxineXiong/OpenAI-API-Web-Apps/assets/55864839/ca2629b8-5506-42e8-814b-5319429aaf83">
    <br>Interacting through text messages
</p>

###

<p align='center'>
    <img width=600 src="https://github.com/MaxineXiong/OpenAI-API-Web-Apps/assets/55864839/9d975dc5-5d38-4ee3-8cf2-085249f166fb">
    <br>Interacting through speech input
</p>

### **Get Started with CodeMaxGPT**

To use the **CodeMaxGPT** application, follow these steps:

1. Visit the [**Introducing CodeMaxGPT**](https://maxinexiong.github.io/intro-codemaxgpt.html) webpage.
2. Click on the "Get started now" button, and you'll be directed to the [**CodeMaxGPT on Streamlit**](https://maxinexiong-openai-api-web-apps-home-xbxlm8.streamlit.app/CodeMaxGPT).
3. Input your [OpenAI API key](https://platform.openai.com/account/api-keys) in the field at the top.
4. You can now start interacting with the coding assistant by entering your text message or selecting a request from the dropdown menu. Then, enter, paste, or upload your code as needed.
5. The coding assistant will provide suggestions, completions, and other assistance based on the request prompt you select and the code you provide.
6. Feel free to explore the other features of **CodeMaxGPT** to assist you in your coding tasks.

For a detailed demonstration of using **CodeMaxGPT**, please visit the [**introduction page**](https://maxinexiong.github.io/intro-codemaxgpt.html) of the web application.

<br/>

## **Contribution**

Contributions are welcome! If you would like to contribute to the development of these web applications, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request detailing your changes.

Please ensure that your contributions align with the project's coding conventions and standards. Your efforts are greatly appreciated!

<br/>

## **License**

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/). Feel free to modify and use the code for your own purposes. However, please note that OpenAI's usage policies and guidelines still apply when using the OpenAI API.

<br/>

## **Acknowledgement**

I would like to acknowledge the following organizations and technologies for their contributions to this project:

- [OpenAI](https://openai.com/) for developing the powerful language models, including the Whisper model and gpt-3.5-turbo models, which have enabled me to create these web applications.
- [Streamlit](https://streamlit.io/) for providing Streamlit Cloud, a platform that allows me to deploy these web applications easily and efficiently.
- [Python](https://www.python.org/) for providing a powerful programming language that has been instrumental in the development of these applications.
- [GitHub](https://github.com/) for hosting this repository and providing a collaborative platform for open-source development.

Thank you for choosing to use the [**OpenAI API Web Apps**](https://maxinexiong-openai-api-web-apps-home-xbxlm8.streamlit.app/). I hope that these applications will greatly amplify your programming capabilities and boost your efficiency, both in your work and in your everyday life.

