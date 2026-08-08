
# ReliefLink AI

> "Technology matters most when it helps people in their hardest moments."

ReliefLink AI is an AI-powered disaster relief assistant built during *MLH Global Hack Week: Agents*.

When disasters happen, people are often overwhelmed. They shouldn't have to repeat the same information every time they ask for help. I wanted to explore how an AI assistant with *persistent memory* could remember important details about a person's situation and provide more helpful, context-aware responses over time.

This project is my exploration of combining conversational AI with memory to create a more human experience during emergency situations.

---

# 💡 Why I Built This

I've always been interested in using AI for problems that have real-world impact rather than just creating another chatbot.

Disaster response is one area where communication can quickly become difficult. People may need to repeatedly explain:

- where they are
- what happened
- who they're with
- what resources they need

I wondered:

> **What if the AI could simply remember?**

Instead of treating every conversation like it's the first one, the assistant could continue helping with the context it already knows.

ReliefLink AI is my first step toward exploring that idea.

---

# ✨ What It Does

The application currently allows users to:

- 💬 Chat with an AI disaster relief assistant
- 🧠 Remember important information across conversations
- ♻️ Reuse the same assistant instead of creating a new one every session
- ⚡ Continue conversations naturally using Backboard Memory
- 🎨 Interact through a clean Streamlit interface

For example, if a user previously shared:

> "I'm near F-9 Park in Islamabad and we need clean drinking water."

The assistant can remember that information later without asking the user to repeat everything.

---

# 🛠 Built With

- Python
- Streamlit
- Backboard SDK
- OpenAI GPT-5.5
- JSON persistence

---

# 📂 Project Structure

```
ReliefLinkAI/
│
├── app.py
├── ui.py
├── services/
│   └── backboard_client.py
├── assets/
├── utils/
├── reliefLink.json
├── test_assistant.py
├── test_chat.py
├── test_memory.py
└── requirements.txt
```

---

# 🚀 Getting Started

Clone the repository

```bash
git clone https://github.com/HAFSAH-SAEED/ReliefLinkAI.git
cd ReliefLinkAI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# 🧠 Persistent Memory

One of the main goals of this project was learning how AI assistants can maintain memory across conversations.

Using the **Backboard SDK**, the assistant:

- stores a reusable assistant identity
- remembers previous context
- continues conversations naturally
- avoids making users repeat important details

This project helped me better understand how persistent AI systems differ from traditional stateless chatbots.

---

# 🚧 What's Next?

This is still an early prototype, and I have plenty of ideas I'd love to explore:

- 📍 Live location sharing
- 🗺 Disaster maps
- 🏥 NGO integration
- 📱 WhatsApp support
- 🌐 Multilingual conversations
- 📸 Image-based damage reporting
- 🚨 Emergency coordination workflows

---

# 📚 What I Learned

Building ReliefLink AI taught me much more than integrating an SDK.

Along the way I learned about:

- working with AI assistants
- persistent memory architectures
- async Python debugging
- Streamlit application design
- modular project organization
- Git and GitHub workflows
- testing AI integrations

One of the biggest challenges was debugging asynchronous API calls while keeping the UI responsive. Solving those issues gave me a much better understanding of how modern AI applications are structured behind the scenes.

---

# 👩‍💻 About Me

Hi! I'm **Hafsa Saeed**, a Computer Engineering student at **NUST CEME**.

I'm interested in AI, robotics, computer vision, and building technology that solves meaningful real-world problems.

This project is part of my journey toward learning how intelligent systems can become more useful, reliable, and human-centered.

---

# 🙏 Acknowledgements

Built during **MLH Global Hack Week: Agents** using the Backboard SDK.