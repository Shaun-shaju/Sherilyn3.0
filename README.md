# **Sherilyn AI** 🤖✨  
*A Personal AI Assistant for Text & Image-Based Learning*  

Sherilyn AI is an advanced personal AI assistant designed by **S. Shaun Benedict**. It offers an intelligent chatbot, personal tutoring via text and images, and secure user authentication, all within a user-friendly interface.  

## **🚀 Features**  
✅ **AI Chat** – Engage in natural conversations with an AI-powered assistant.  
✅ **Personal Tutor** – Get answers via both text and image-based queries.  
✅ **Firestore Integration** – Securely saves and retrieves chat history.  
✅ **Streamlit UI** – Interactive and easy-to-use web interface.  
✅ **Authentication System** – Secure login and sign-up functionality.  
✅ **Offline Mode** – Packaged with PyInstaller for standalone execution.  

## **🛠️ Tech Stack**  
- **Python** – Backend logic  
- **Streamlit** – UI Framework  
- **Google Firestore** – Database for storing chat history  
- **PyInstaller** – Converts the app into a standalone `.exe`  
- **Google AI Studio** – AI-powered responses  

## **📦 Installation**  

### **1️⃣ Install Dependencies**  
Ensure you have Python installed, then run:  
```bash
pip install -r requirements.txt
```

### **2️⃣ Run the Application**  
Launch the app with:  
```bash
streamlit run main.py
```

## **📂 Directory Structure**  
```
Sherilyn-AI/
│── logs/                  # Chat history logs  
│── pages/                 # Streamlit pages  
│── server/                # Backend AI processing  
│── main.py                # Entry point  
│── requirements.txt       # Dependencies  
│── README.md              # Project description  
```

## **🔒 Packaging with PyInstaller**  
To generate a standalone executable:  
```bash
pyinstaller --noconfirm --onefile --windowed --hidden-import=all_modules main.py
```

## **💡 Future Enhancements**  
- 🗣️ Voice-based interaction  
- 🌍 Multi-language support  
- 📚 AI-powered content summarization  

## **🤝 Contributing**  
Feel free to fork this project, open issues, and submit pull requests! 🚀  

---
*Designed with ❤️ by S. Shaun Benedict*
```
