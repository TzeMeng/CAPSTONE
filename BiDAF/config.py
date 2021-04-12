exp = "exp-1"

# data directories
data_dir = "data/"
train_dir = data_dir + "train/"
test_dir = data_dir + "test/"
result = "result/"

# model paths
spacy_en = "/Users/ngtze/anaconda3/Lib/site-packages/en_core_web_sm/en_core_web_sm-3.0.0"
glove = "glove.6B/" + "glove.6B.{}d.txt"
squad_models = "output/" + exp

# preprocessing values
max_words = -1
word_embedding_size = 100
char_embedding_size = 8
max_len_context = 400
max_len_question = 50
max_len_word = 25

# training hyper-parameters
num_epochs = 10
batch_size = 32
learning_rate = 0.7
drop_prob = 0.1
hidden_size = 100
char_channel_width = 5
char_channel_size = 100
#cuda = False
cuda = True
pretrained = False