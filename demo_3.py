import streamlit as st
import PIL as pil

filename="file_1"
mas_data=[]
minf=0.1
maxf=1.0
delw=[]

st.header('web-сервис: тематичеcкий анализ текста')

#img=pil.Image.open('D:/DataScience/WEB/DEMO_3/photo.jpg')
img=pil.Image.open('photo.jpg')
st.sidebar.image(img)

filename = st.sidebar.selectbox("Выберите текст",["file_1","file_2","file_3","file_1"])

min_tfidf = st.sidebar.selectbox("Выберите мин.частоту слов",["0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1.0"])
max_tfidf = st.sidebar.selectbox("Выберите макс.частоту слов",["0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1.0"])
minf=float(min_tfidf)
maxf=float(max_tfidf)

but_corpus=st.sidebar.button("Создать корпус слов")
if but_corpus: 
    fig, listp=start_corpus(filename, minf, maxf)
    st.pyplot(fig)
    for curmes in listp:
        st.text(curmes)

sel_cntgroup = st.sidebar.selectbox("Выберите кол-во групп",["1","2","3","4","5","6","7","8","9","10"])
sel_cntwords = st.sidebar.selectbox("Выберите кол-во слов в группе",["1","2","3","4","5","6","7","8","9","10"])

but_lda=st.sidebar.button("Группировать слова по группам")
if but_lda: st.sidebar.text("...") 




