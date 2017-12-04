#%%
from keras.preprocessing.text import Tokenizer
tk = Tokenizer()
#%%
texts = ['this test', 'here is another', 'how about that', 'one more', 'here is a test']
tk.fit_on_texts(texts)
tk.texts_to_matrix(texts, mode='tfidf')

#%% 

#%%
