# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Bahasa Indonesia's stop words from Sastrawi library
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

st.set_page_config(page_title="Quran Search Engine", page_icon="📖", layout="wide")

st.title("Quran Search Engine")
st.write("Find ayat based on text similiarity. Currently powered by TF-IDF and cosine similarity.")

@st.cache_resource
def load_data_and_model():
  # data load
  raw_en = "https://tanzil.net/trans/en.yusufali"
  df_en = pd.read_csv(raw_en, sep="|", names=['surah', 'ayat', 'translation'], comment='#')

  raw_id = "https://tanzil.net/trans/id.indonesian"
  df_id = pd.read_csv(raw_id, sep="|", names=['surah', 'ayat', 'translation'], comment='#')

  # data cleaning
  df_en['translation'] = df_en['translation'].astype(str)
  df_en['surah'] = df_en['surah'].astype(int)
  df_en['ayat'] = df_en['ayat'].astype(int)

  df_id['translation'] = df_id['translation'].astype(str)
  df_id['surah'] = df_id['surah'].astype(int)
  df_id['ayat'] = df_id['ayat'].astype(int)

  #vectorization
  vec_en = TfidfVectorizer(stop_words='english')
  matx_en = vec_en.fit_transform(df_en['translation'])

  # Bahasa Indonesia's stop words from Sastrawi initialization
  stopword_factory = StopWordRemoverFactory()
  stop_words_id = stopword_factory.get_stop_words()

  vec_id = TfidfVectorizer(stop_words=stop_words_id)
  matx_id = vec_id.fit_transform(df_id['translation'])

  models = {
    "English": (df_en, vec_en, matx_en),
    "Bahasa Indonesia": (df_id, vec_id, matx_id)
  }

  return models

# calling function
models = load_data_and_model()

# """
# Old UI conf
# """

# query = st.text_input("Enter the keyword: ")
# top_n = st.number_input("Result maximum limit: ", min_value=1, value=10, step=1)

# if query:
#   query_vec = vectorizer.transform([query])
#   sim_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
#   top_indices = sim_scores.argsort()[-top_n:][::-1]

#   found = []
#   for i in top_indices:
#     score = sim_scores[i]
#     if score > 0:
#       quran_link = f"https://quran.com/{df.iloc[i]['surah']}/{df.iloc[i]['ayat']}"

#       found.append({
#           'Surah': df.iloc[i]['surah'],
#           'Ayat': df.iloc[i]['ayat'],
#           'Score': round(score, 4),
#           'Translation': df.iloc[i]['translation'],
#           'Link': quran_link
#       })

#   # show result logic
#   if found:
#     df_found = pd.DataFrame(found)

#     # count total similarity matches found, either can be shown or not
#     total_matches = (sim_scores > 0).sum()

#     st.success(f"Found **{total_matches}** matching ayat!\nShowing top {len(found)} results for: **'{query}'** (Total matches: {total_matches})")

#     st.dataframe(
#         df_found,
#         column_config={
#             "Link": st.column_config.LinkColumn("Quran Link")
#         },
#         hide_index=True,
#         use_container_width=True
#         )
#   else:
#     st.warning("The matches ayat with the keyword wasn't found!\nTry another or more universal keyword")

# """
# New UI conf
# """

selected_lang = st.selectbox("Select translation language / Pilih Bahasa Terjemahan:",
                options=["English", "Bahasa Indonesia"])

df, vectorizer, tfidf_matrix = models[selected_lang]

with st.form(key='search_form'):
    # Dividing layout as 2 columns (3:1)
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input("Enter the keyword: ", placeholder="e.g., fasting ramadan")
    with col2:
        top_n = st.number_input("Result maximum limit: ", min_value=1, value=10, step=1)
        
    # Submit btn should be in the form
    submit_button = st.form_submit_button(label='Search')

# --- Logic ---

# The Algorithm would only executed IF submit button clicked (or Enter pressed)
if submit_button:
    # Ensuring the query wasn't null before execution
    if query.strip() == "":
        st.warning("Please enter a keyword to start searching!")
    else:
        # Adding loading animation for more interactive UX
        with st.spinner('Searching for matching ayat...'):
            query_vec = vectorizer.transform([query])
            sim_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
            top_indices = sim_scores.argsort()[-top_n:][::-1]

            found = []
            for i in top_indices:
                score = sim_scores[i]
                if score > 0:
                    quran_link = f"https://quran.com/{df.iloc[i]['surah']}/{df.iloc[i]['ayat']}"

                    found.append({
                        'Surah': df.iloc[i]['surah'],
                        'Ayat': df.iloc[i]['ayat'],
                        'Score': round(score, 4),
                        'Translation': df.iloc[i]['translation'],
                        'Link': quran_link
                    })

        # --- show result logic ---
        if found:
            df_found = pd.DataFrame(found)

            total_matches = (sim_scores > 0).sum()

            # (A few modification on the success text so there's no duplication on total matches info)
            st.success(f"Found **{total_matches}** matching ayat! Showing top **{len(found)}** results for: **'{query}'**")

            st.dataframe(
                df_found,
                column_config={
                    "Link": st.column_config.LinkColumn("Quran Link")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.warning("The matching ayat with the keyword wasn't found!\nTry another or more universal keyword.")
