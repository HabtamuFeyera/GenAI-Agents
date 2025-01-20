# **GenAI-Agents** 🚀  
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) 
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-%23FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)  

Welcome to **GenAI-Agents** — your go-to repository for creating and deploying powerful AI agents with **Generative AI**. These agents are designed to perform specific tasks such as answering questions, calculations, and retrieving data from external sources (like **Wikipedia**) in a loop-driven, dynamic, and intelligent way.


## 📑 **Table of Contents**

1. [🌟 Features](#-features)  
2. [🔧 System Architecture](#-system-architecture)  
3. [🚀 Getting Started](#-getting-started)  
   - [Prerequisites](#prerequisites)  
   - [Installation](#installation)  
   - [Running the Application](#running-the-application)  
4. [🧑‍💻 Contributing](#-contributing)  
5. [📜 License](#-license)  
6. [📬 Contact](#-contact)  
7. [🙌 Acknowledgements](#-acknowledgements)  


## 🌟 **Features**

- **AI ChatBot Agent**: Utilizes GPT-4 to respond to queries, execute calculations, and search for information online.  
- **Wikipedia Search Agent**: Fetches summaries and relevant data from Wikipedia.  
- **Custom Blog Search Agent**: Retrieves relevant blog entries based on user queries.  
- **Calculation Agent**: Safely evaluates mathematical expressions.  


## 🔧 **System Architecture**

**GenAI-Agents** employs a structured **Thought-Action-Observation Loop**, ensuring thorough and accurate responses:  

1. **Thought**: The agent reasons through the user's question.  
2. **Action**: Executes the relevant operation (e.g., API calls or calculations).  
3. **PAUSE**: Waits for observations after executing an action.  
4. **Observation**: Outputs the refined result or an answer.

This modular design enables **expandable actions** and seamless integration with new APIs or tasks.


## 🚀 **Getting Started**

### **Prerequisites**  

- **Python 3.x** installed.  
- **Streamlit** for the interactive UI.  
- An active **OpenAI API Key**: Store it in an environment variable (`OPENAI_API_KEY`).  

### **Installation**

Clone the repository to your local machine:  

```bash
git clone https://github.com/HabtamuFeyera/GenAI-Agents.git
cd GenAI-Agents


Install the dependencies:  

```bash
pip install -r requirements.txt
```

### **Running the Application**

Start the **Streamlit** app:  

```bash
streamlit run app.py
```

This opens the app in your browser, ready for interaction!


## 🧑‍💻 **Contributing**

We welcome contributions to make **GenAI-Agents** even better! Follow these steps to contribute:  

1. **Fork** the repository.  
2. Create a **new branch** for your feature (`git checkout -b feature/your-feature`).  
3. Commit your changes (`git commit -m 'Add your feature'`).  
4. Push to your branch (`git push origin feature/your-feature`).  
5. Open a **Pull Request**.  


## 📜 **License**

This project is licensed under the **MIT License**. For more details, see the [LICENSE](LICENSE) file.


## 📬 **Contact**

Have questions or suggestions? Reach out anytime:

- **Habtamu Feyera**  
- 📧 Email: [habtamufeyera95@gmail.com](mailto:habtamufeyera95@gmail.com)  
- 🌐 LinkedIn: [Habtamu Feyera](https://www.linkedin.com/in/habtamu-feyera)  
- 📲 Telegram: [@DecodeAI](https://t.me/DecodeAI)



## 🙌 **Acknowledgements**

Special thanks to:

- **OpenAI GPT-4** for powering the agents.  
- **Streamlit** for enabling intuitive UI development.  
- **Wikipedia API** for providing accessible and reliable data.  


Thank you for exploring **GenAI-Agents**! We look forward to your contributions and ideas to make AI even more accessible and versatile. 😊  
