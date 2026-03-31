# SimpleQuranSE

> [!NOTE]
> Deployment: https://simplequranse-zeynthedev.streamlit.app/

# 📖 Simple Quran Search Engine

A simple, interactive web-based search engine for the Quran, built using Python and **Streamlit**. This project utilizes the **Vector Space Model (VSM)** in Information Retrieval to find the most relevant Ayahs based on user text queries.

## ⚙️ How It Works
Unlike exact-match search engines (Boolean Retrieval), this app uses Natural Language Processing (NLP) techniques to find semantic similarities:
1. **TF-IDF (Term Frequency-Inverse Document Frequency):** Converts the entire English translation of the Quran into a mathematical matrix, giving higher weight to unique/important keywords and ignoring common stop words.
2. **Cosine Similarity:** Calculates the angle between the user's query vector and the document vectors to determine the relevancy score. The closer the score is to 1.0, the more relevant the Ayah is.

## ✨ Features
* **Top-N Results:** Users can specify how many top results they want to see.
* **Smart Ranking:** Results are sorted dynamically from the highest similarity score to the lowest.
* **Direct Integration:** Includes clickable links to [Quran.com](https://quran.com) for each retrieved Ayah for further reading and context.

## 🛠️ Tech Stack
* **Language:** Python 3
* **Frontend/Framework:** Streamlit
* **Data Manipulation:** Pandas
* **Machine Learning/NLP:** Scikit-learn
* **Dataset:** English-Bahasa Indonesia Translations of the Quran (Yusuf Ali/Kemenag RI) dynamically fetched from [Tanzil.net](https://tanzil.net).

## 🚀 How to Run Locally

If you want to run this application on your local machine (or WSL), follow these steps:

**1. Clone the repository**
```bash
git clone https://github.com/ZeynTheDev/SimpleQuranSE.git
cd SimpleQuranSE
```
**2. Create a virtual environment (Recommended)**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
**3. Install dependencies**
```bash
pip install -r requirements.txt
```
**4. Run the app**
```bash
streamlit run app.py  # Replace 'app.py' with your actual python file name
```

## 📄 License
This project is open-source and available under the MIT License.

## ✍️ Dev Note
Bahasa Indonesia support was released!

**Note: Sorry, today I have no mood to chitchat as usual. Something bad occured on my IRL so sorry.*