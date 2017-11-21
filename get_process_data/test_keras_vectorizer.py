#%%
from keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer()
#%%
texts = ['this test', 'here is another', 'how about that', 'one more', 'here is a test']
tokenizer.fit_on_texts(texts)
tokenizer.texts_to_matrix()

#%% 

#%%
