from utilities.data_utils import util
import os
from networks.pos_bilstm import POSModel
import numpy as np

def main():
    util.load_glove_pkl(os.getenv("DATA_DIR_DL")+str('word2vec/glove.pkl'))
    util.load_glove_txt(os.getenv("DATA_DIR_DL")+str('/word2vec/glove.840B.300d.w2vformat.txt'))
    sentences_train, lexicon_dic, classes = util.parse_pos(os.getenv("DATA_DIR_DL")+'/pos/en-train.txt')
    sentences_val, lexikon_val_dic, classes_val = util.parse_pos(os.getenv("DATA_DIR_DL")+'/pos/en-test.txt')

    print(sentences_train[1])
    print(sentences_train[3])
    embeddings = np.zeros([len(lexicon_dic), 300])
    for word in lexicon_dic:
        word_idx = lexicon_dic[word]
        embeddings[word_idx] = np.asarray(util.glove[word])

    dev = util.sen_dict_to_tuple(sentences_train, lexicon_dic, classes)
    val = util.sen_dict_to_tuple(sentences_val, lexikon_val_dic, classes_val)
    pos = POSModel(embeddings, len(classes), util)
    pos.build()

    pos.train(dev, val)

    print(pos.predict_batch([val[0][0]]))
    print(val[0][1])

if __name__ == '__main__':
    main()
