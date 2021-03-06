from keras.models import Sequential, model_from_json
from keras.preprocessing import sequence
from gensim import corpora, models
import sys, pickle, re, os
import numpy as np
from utils import *
X_raw = sys.argv[1]

# X_raw = "How,To,Install,Latest,Ethereum,Node,on,Ubuntu,16.04|Fake,News:,Venezuela,Rejects,“False,Information”,on,Petro,Whitepaper|Korbit:,Non-Koreans,Prohibited,from,KRW,Deposits,at,All,Domestic,Cryptocurrency,Exchanges|European,Central,Bank,to,Discuss,Bitcoin,and,Blockchain,With,Youth|Greg,Maxwell,Resigns,from,Blockstream,to,Focus,on,‘Deep,Protocol,Work’|More,Retail,Investors,Coming?,Bitcoin,Investment,Trust,Sees,91-to-1,Stock,Split|(+),Ethereum,Wannabes,Face,Big,Challenge|Bitcoin,Price,Gains,10%,as,Cryptocurrency,Market,Continues,to,Recover|‘Bitcoin,Bank’,Denies,Policy,Change,on,International,Cryptocurrency,Wire,Transfers|Decentralized,Travel,Distribution,Platform,Eliminates,Middlemen,to,Make,Your,Trips,Cheaper|Russia’s,largest,bank,has,launched,a,Blockchain,Lab|Lightning,Network,May,Not,Solve,Bitcoin's,Scaling,'Trilemma'|Battle-Testing,Lightning:,26,Schools,Start,Contest,to,Secure,Bitcoin’s,Layer,2|Venezuela,to,Issue,Petro,Cryptocurrency,through,Token,Sale,,Plans,Tax,Deals,to,Bolster,Adoption|Bitcoin,Under,Increasing,Scrutiny,on,Island,of,Bali|Price,Analysis,,Jan.,19:,Bitcoin,,Ethereum,,Bitcoin,Cash,,Ripple,,IOTA,,Litecoin,,NEM,,Cardano|BitPay,Integrates,With,ShapeShift,to,Enable,Instant,BTC-BCH,Exchange|Keep,Calm,And,Hodl?,CNBC,Guest,Tells,Bitcoin,Critic,to,‘Piss,Off’|Bitcoin,Mining,Isn’t,an,‘Environmental,Armageddon’,:,Credit,Suisse,Report|Trading,Bots,to,Govern,an,Investment,Strategy,of,Newly,Created,Decentralized,Autonomous,Funds"

# dictionary = corpora.Dictionary.load('../crawler/saved/model_dict.pkl')
# docs = [doc.split(",") for doc in X_raw.lower().split("|")]
# dict_doc2idx = [dictionary.doc2idx(doc) for doc in docs]

# max_gram_len = 360
# X = np.array(sequence.pad_sequences(dict_doc2idx, maxlen=max_gram_len, padding='post'))
X_raw = [s.replace(","," ") for s in X_raw.lower().split("|")]
saved_path = os.path.join(os.path.dirname(__file__), './saved/')
texts, corpus = extract_text_n_corpus(X_raw, remove_uniq=False)
word2vec = models.Word2Vec.load(saved_path + 'model_word2vec.pkl')
X, invalid_rows = texts_to_word_vec(word2vec, texts)
X = np.delete(X, invalid_rows, 0)

# print("Verify persisted model...")
weights = pickle.load(open(saved_path + 'model_weights_week.pkl', 'rb'))
model_json = pickle.load(open(saved_path + 'model_json_week.pkl', 'rb'))
model = model_from_json(model_json)
# print("\tv: Model loaded successfully!")
model.set_weights(weights)
pred = model.predict(X)
print(",".join([str(i) for i in pred.mean(axis=0)]), builtin=True)
