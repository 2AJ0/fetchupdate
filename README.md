# 🐾 FetchUpdate – AI Pet Sitter Assistant

**FetchUpdate** is a privacy-first AI tool built for local dog walkers and pet sitters. It analyzes daily photos of clients' pets and combines vision models with stored profile data (instructions, breed, owner preferences) to instantly draft warm, personalized SMS updates for pet owners.

---

## ✨ Features

- **Profile Management:** Pulls pet traits, special care instructions, and owner details directly from MongoDB Atlas.
- **Visual Activity Recognition:** Uses multimodal vision models to analyze uploaded pet photos.
- **Instant SMS Generation:** Generates concise, engaging text updates with appropriate emojis ready to copy and send.
- **Privacy-Conscious:** Avoids permanent storage of client location data or private media.

---

## 🛠️ Tech Stack

- **Frontend / UI:** [Streamlit](https://streamlit.io/)
- **Database:** [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (`pymongo`)
- **AI Models:** OpenRouter API / Gemini Vision models via Open-Weight pipelines
- **Language:** Python 3.10+
