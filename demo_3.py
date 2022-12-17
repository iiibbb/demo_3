import streamlit as st
import xlrd
from pymorphy2 import MorphAnalyzer
from gensim import models, corpora
import numpy as np
import matplotlib as mplt
import nltk as nltk 
import PIL as pil

filename="file_1"
mas_data=[]
minf=0.1
maxf=1.0
delw=[]
cur_del_words=[]
corpus=[]

stopwords = nltk.corpus.stopwords.words("russian")
stemmer=nltk.stem.SnowballStemmer(language="russian")
stopwords = nltk.corpus.stopwords.words('russian') 
morph = MorphAnalyzer() 



#*****************************************************************
class Prepare(object):    
    
    def __init__(self, mas, del_words, minf, maxf):
        self.stemmer=stemmer 
        self.ru_stopwords = stopwords
        self.morph = morph 
        self.patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
         
        self.mas=mas
        self.del_words=del_words
        self.minf=minf
        self.maxf=maxf
                        
    def prepareWord(self, old_word):
        new_word=old_word
        if not isinstance(old_word,str): return(" ") 
        new_word=re.sub(self.patterns, ' ', new_word) 
        new_word=new_word.translate(new_word,self.patterns)
        new_word=new_word.lower()
        #word=stemmer.stem(word) 
        new_word=morph.normal_forms(new_word)[0]
        if new_word not in self.ru_stopwords and new_word not in self.del_words:  
            if len(new_word)>3:
                if 'NOUN' in morph.tag(new_word)[0]:
                    #print("("+old_word+") = "+new_word)
                    #print("*****************")             
                    return new_word            
        return " "     
    
#**********************************************************    

    def histogramm(self, all_mes_words):
    
        my_dictionary = corpora.Dictionary(all_mes_words)
        bow_corpus =[my_dictionary.doc2bow(mes, allow_update = True) for mes in all_mes_words]
   
        #print(bow_corpus)
        #print("*************************************")
        word_weight =[]
        for doc in bow_corpus:
            for id, freq in doc:
                word_weight.append([my_dictionary[id], freq])
        #print(word_weight)
        #print("*************************************")
        tfIdf = models.TfidfModel(bow_corpus, smartirs ='ntc')

        weight_tfidf =[]
        for doc in tfIdf[bow_corpus]:
            for id, freq in doc:
                weight_tfidf.append([my_dictionary[id], np.around(freq, decimals=3)]) 

        sort_weight_tfidf=sorted(weight_tfidf,key=lambda freq: freq[1]) 

        wrd=[]
        val=[]
        new_del_words=[]
        for i in range(len(sort_weight_tfidf)):
            curval=float(sort_weight_tfidf[i][1])
            if curval>=self.minf and curval<=self.maxf: 
                #print(str(i))
                #print(sort_weight_tfidf[i]) 
                wrd.append(sort_weight_tfidf[i][0])
                val.append(float(sort_weight_tfidf[i][1]))
            else:
                new_del_words.append(sort_weight_tfidf[i][0])
        #print("*************************************")

        fig, ax = mplt.pyplot.subplots(figsize =(10, 7)) 
        ax.hist(val, bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
            
        return new_del_words, fig

#**********************************************************
        
    def prepare_all(self):
        all_mes_words=[]
        all_sent_words=[]
        all_words=[]
        print("*************************************") 
        for line in self.mas:  
            cur_mes_words=[]
            for sent in nltk.sent_tokenize(line): 
                cur_sent_words=[]
                for word in nltk.word_tokenize(sent):
                    word=self.prepareWord(word)  
                    if word!=" ":
                        cur_sent_words.append(word)
                        all_words.append(word)
                        cur_sent_words.append(word)
                        cur_mes_words.append(word)
                all_sent_words.append(cur_sent_words)        
            all_mes_words.append(cur_mes_words)    

        new_del_words, fig=self.histogramm(all_mes_words)
        return all_mes_words, all_sent_words, all_words, new_del_words, fig
    
    
#**********************************************************

def start_corpus(file, minf, maxf):    
                    
    #rb = xlrd.open_workbook("D:/DataScience/WEB/DEMO_3/post_news_1.xls",formatting_info=True)
    rb = xlrd.open_workbook("post_news_1.xls",formatting_info=True)
    sheet = rb.sheet_by_index(0)
    mas_data = sheet.col_values(0)
         
    prep = Prepare(mas_data, delw, minf, maxf)
    all_mes_words, all_sent_words, all_words, curdelw, fig = prep.prepare_all()
    cur_del_words=curdelw
    corpus=all_mes_words
    
    list_posts=[]
    list_posts.addItem("*********************************************************")
    list_posts.addItem("Создание корпуса слов дл сообщений канала "+file)
    list_posts.addItem("Всего сообщений = "+str(len(all_mes_words)))
    list_posts.addItem("Всего преддложений = "+str(len(all_sent_words)))
    list_posts.addItem("Всего слов = "+str(len(all_words)))
    list_posts.addItem("Всего удалено слов = "+str(len(curdelw)))
    list_posts.addItem("Всего осталось слов = "+str(len(all_words)-len(curdelw)))
    list_posts.addItem("*********************************************************")
       
    return fig, list_posts


#**************************************************************

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




