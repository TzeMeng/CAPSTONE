# CAPSTONE
## Capstone Project

The project aims to develop a smart search system for enhanced document retrieval and information extraction, by leveraging on and integrating state-of-the-art Natural Language Processing (NLP) techniques.


## Dataset Used

The primary dataset of this project is the Stanford Question Answering Dataset 2.0 (SQuAD 2.0). <br>

SQuAD is a reading comprehension dataset, consisting of questions queried to a set of Wikipedia compositions. The answer to each question is a snippet of text or span, from the corresponding context paragraph. Alternatively, the question might be unanswerable. SQuAD 2.0 combines the 107,786 questions in the first version of SQuAD 1.1 with over 50,000 unanswerable questions written to look identical to the answerable ones. There are a total of 19,035 context paragraphs to which the questions are being queried to.

An example of a context paragraph would look like this: <br>
*North Carolina consists of three main geographic sections: the Atlantic Coastal Plain, which occupies the eastern 45% of the state; the Piedmont region, which contains the middle 35%; and the Appalachian Mountains and foothills. The extreme eastern section of the state contains the Outer Banks, a string of sandy, narrow barrier islands between the Atlantic Ocean and two inland waterways or "sounds": Albemarle Sound in the north and Pamlico Sound in the south. They are the two largest landlocked sounds in the United States.*

Some examples of the question-answer pair that are queried to this context paragraph are:
- *How many main geographical sections make up North Carolina? A: three*
- *What section of North Carolina makes up 45% of the state? A: the Atlantic Coastal Plain*
- *What is the section in the middle 35% of North Carolina called? A: the Piedmont region*

## Frontend Preview:
Home Page:
![image](https://user-images.githubusercontent.com/51269684/114511173-25d34000-9c6a-11eb-9abc-fec36f4db48b.png)

Changes to Home Page after asking a question:
![image](https://user-images.githubusercontent.com/51269684/114511213-34215c00-9c6a-11eb-86a5-d0991507aa09.png)

Performance Page:
![image](https://user-images.githubusercontent.com/51269684/114511622-b7db4880-9c6a-11eb-8815-c3c698ad9fb9.png)

About Page:
![image](https://user-images.githubusercontent.com/51269684/114511237-3be10080-9c6a-11eb-9832-ca8c64fb68c0.png)
## BERT Model Workflow

BERT_Train.ipynb contains the codes to train the BERT model with the tuned parameters. <br />

BERT_Test.ipynb contains the codes to test the BERT model to produce an answer when passing a context and query, after the model weights has been inserted. <br />

bert.h5 contains the model weights. <br />

bert_optimizer_tunning_visualization.ipynb contains the visualization for the optimizer parameters tuning process. <br />

## Usage
Upload both Jupyter Notebooks to Google Collaboratory <br />
Change the runtime type under the tab runtime to TPU <br />

Run the BERT_Train notebook by clicking on Run all under runtime tab<br />
Save the bert.h5 file from the google collaboratory files on the left of the webpage<br />

Upload the bert.h5 file into google drive files by uploading to the session storage<br />
Run the BERT_Test notebook by clicking on Run all under runtime<br />
