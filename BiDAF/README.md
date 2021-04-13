# The BiDAF directory consists of not limited to the following files:

utils.py <file> <br>
Contains the Following Functions: <br>
  clean_text(text) : Function that takes in a text and removes brackets, break lines (/n) indicator and quotation marks.<br>
  word_tokenize(sent) : Tokenizes each word in a sentence. <br>
  covert_idx(text, sent) : Function that takes in a text and a sentence, returns the start and end index of the text if it is a substring of the sentence <br>
  save_checkpoint(state, is_best, filename) : Saves the state of the model after the last training epoch for the purpose of future retraining if required <br>
  discretize(p_start, p_end, max_len, no_answer) : Function that takes in a set of probabilities of the start index of the answer as well as a set of probabilities for the end                                                     index of the answer, subsequently return the start index and end index that maximises the pairwise probabilities. <br>
compute_batch_metrics(context, idx2word, pred1, pred2, batch_labels)
Function for scoring the Model Prediction by comparing it with the true answers
build_embeddings(vocab, embedding_path="", output_path="", vec_size = 50)
Function for building word and character embedding, if vector size is not defined, it will build embeddings of 50 dimensions and save the file:
word_embeddings.pkl <file>
Contains word embeddings of 100 dimensions from the GloVe corpus. Words that are not found in the GloVe corpus will be represented by a randomly initialized vector of 100 dimensions
char_embeddings.pkl <file>
Contains randomized embeddings of 100 dimensions for characters

build_vocab(context_filename, question_filename, word_vocab_filename, word2idx_filename, char_vocab_filename, char2idx_filename, is_train=True, max_words=-1)
Function that would split the data into multiple files:
train.answer <file>
Answers extracted from raw train data
train.context <file>
Context Paragraphs extracted from raw train data
train.labels <file>.
Contains the start and end index in the context paragraph that spans the actual (true)  answer from the raw train data
train.question<file>
Questions extracted from the raw train data
char_embeddings.pkl <file>
Contains randomized embeddings of 100 dimensions for characters
char_vocab.pkl <file>
Contains the different characters extracted from the raw train data
word_vocab.pkl <file>
 Contains the different words extracted from the raw train data
word2idx.pkl <file>
Functions as a mapper that map each word in word_vocab.pkl to the corresponding embedding in all variations of word embedding files
compute_em (true ans, prediction)
Compute the Exact Match
Codes provided by SQuAD 2.0
compute_f1 (true ans, prediction)
Compute the F1 scores
Codes provided by SQuAD 2.0
make_dataset.py <file>
Python Script that process the raw json files into a format for model training
data_loader.py <file>
Python Script that stores the SquadDataset Class to facilitate the formatting of data to be fed into the model
layers.py <file>
Contains the various Classes to be used as hidden layers in the BiDAF model:
Embedding: 2 Different Embedding layers, the first for randomized character embedding and the second for trained character embedding
CNN : To train Character Embeddings
HighwayEncoder: Facilitate the flow of information in deep networks
RNNEncoder: Capture contextual information
BiDAFAttention : Form the attention layer between query and context (vice versa)
BiDAFOutput : Collates results from intermediate layers and returns a final prediction
model.py <file>
Contains the framework of the model and by utilizing the various classes implemented in layers.py
train.py <file>
Python Script for training and saving the model
test.py <file>
Python Script to evaluate model’s performance on the test/ dev set
eval.py <file>
Python Script that is called by the front end that takes in a context and a question and returns an answer predicted by the model.
config.py <file>
Python file that stores the user-tunable parameters
Output <folder> (Store the Models)
exp-1<folder>
model.pkl <file>
Contains the best performing BiDAF implementation with GloVE embeddings of 100 dimensions and Randomised Character Embeddings of 100 dimensions. 
model_last_checkpoint.pkl <file>
Contains the last model state of the BiDAF implementation with GloVE embeddings of 100 dimensions and Randomised Character Embeddings of 100 dimensions
Saved previous state of the model for further training purposes
char_combined_model.pkl <file>
Contains the best performing BiDAF implementation with GloVE embeddings of 100 dimensions and Trained Character Embeddings of 100 dimensions.
char_combined_model_last_checkpoint.pkl <file>
Contains the last model state of the BiDAF implementation with GloVE embeddings of 100 dimensions and Trained Character Embeddings of 100 dimensions.
Saved previous state of the model for further training purposes

final_combined_model.pkl <file>
Contains the best performing BiDAF implementation with GloVE embeddings of 100 dimensions, BERT embeddings of 100 dimensions and Trained Character Embeddings of 100 dimensions.
final_combined_model_last_checkpoint.pkl <file>
Contains the last model state of the BiDAF implementation with GloVE embeddings of 100 dimensions, BERT embeddings of 100 dimensions and Trained Character Embeddings of 100 dimensions.
Saved previous state of the model for further training purposes

result <folder>
result.xlsx
Contains training loss, test loss, F1 scores and Exact Match scores attained at the different epochs  by the BiDAF implementation with GloVE embeddings of 100 dimensions and Randomised Character Embeddings of 100 dimensions. 
character_combined_result.xlsx
Contains training loss, test loss, F1 scores and Exact Match scores attained at the different epochs  by the BiDAF implementation with GloVE embeddings of 100 dimensions and Trained Character Embeddings of 100 dimensions.
final_combined_result.xlsx
Contains training loss, test loss, F1 scores and Exact Match scores attained at the different epochs  by the BiDAF implementation with GloVE embeddings of 100 dimensions, BERT embeddings of 100 dimensions and Trained Character Embeddings of 100 dimensions.
 
context <folder>
Content_embed_50.pkl <file>
Contains the BERT embeddings vectors of 50 dimensions
Contetnt_embed_100.pkl <file>
Contains the BERT embeddings vectors of 100 dimensions

data <folder> (Not on GitHub due to the size of the folder)
test <folder>
test.answer <file>
Answers extracted from raw test data
test.context <file>
Context Paragraphs extracted from raw test data
test.labels <file>.
Contains the start and end index in the context paragraph that spans the actual (true)  answer from the raw test data
test.question<file>
Questions extracted from the raw test data
train <folder>
train_context.xlsx <file>
Context Paragraphs extracted from raw train data
Stored in Excel for processing and creation of the BERT word embeddings
train.answer <file>
Answers extracted from raw train data
train.context <file>
Context Paragraphs extracted from raw train data
train.labels <file>.
Contains the start and end index in the context paragraph that spans the actual (true)  answer from the raw train data
train.question<file>
Questions extracted from the raw train data
char_embeddings.pkl <file>
Contains randomized embeddings of 100 dimensions for characters
char_vocab.pkl <file>
Contains the different characters extracted from the raw train data
char2idx.pkl.pkl <file>
Functions as a mapper that map each character in char_vocab.pkl to the corresponding embedding in char_embeddings.pkl
trained_char_embeddings.pkl <file>
Contains trained embeddings of 100 dimensions for characters
trained_char_vocab.pkl <file>
Contains the different characters extracted from the raw train data
trained_char2idx.pkl <file>
Functions as a mapper that map each character in trained_char_vocab.pkl to the corresponding embedding in trained_char_embeddings.pkl
word_embeddings.pkl <file>
Contains word embeddings of 100 dimensions from the GloVe corpus. Words that are not found in the GloVe corpus will be represented by a randomly initialized vector of 100 dimensions
word_vocab.pkl <file>
 Contains the different words extracted from the raw train data
word2idx.pkl <file>
Functions as a mapper that map each word in word_vocab.pkl to the corresponding embedding in all variations of word embedding files
no_random_word_embeddings.pkl <file>:
Contains word embeddings of 100 dimensions from the GloVe corpus. Words that are not found in the GloVe corpus will be represented by a 100 dimensions vector which contains ones as all it values.
The purpose of doing so is to highlight out-of-vocab words that will be replaced with BERT embeddings.
combined_word_embeddings.pkl <file>
Contains the concatenated BERT word embeddings of 100 dimensions and the GloVE word embeddings of 100 dimensions, resulting in a word embedding vector of 200
words_not_found.pkl <file>
Contains words that are not found in both the BERT framework and the GloVe corpus. This mostly contains words that have been misspelled.
test-v2.0.json
Raw test data downloaded from SQuAD2.0, also known as the validation set or the Dev set. The official test set used in SQuAD2.0 is publicly available
train-v2.0.json
Raw train data downloaded from SQuAD2.0
Data_Processing <file>
glove.6B <file> (Not on GitHub due to the size of the folder), Can be downloaded on the official GloVe Corpus site @ : https://nlp.stanford.edu/projects/glove/
glove.6B.50d.txt
Contains the GloVe word embeddings of 50 dimensions
glove.6B.100d.txt
Contains the GloVe word embeddings of 100 dimensions
glove.6B.200d.txt
Contains the GloVe word embeddings of 200 dimensions
glove.6B.300d.txt
Contains the GloVe word embeddings of 300 dimensions
combine_embedding.ipynb <file>
Depicts the process of integrating BERT embeddings
model_result_visualization.ipynb <file>
For the plotting of model results


