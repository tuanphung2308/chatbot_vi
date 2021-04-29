# How to set up

#### Downgrade pip

pip install --upgrade pip==20.2

#### Install rasa

pip install rasa

#### Install rasa x

pip install -U rasa-x --extra-index-url https://pypi.rasa.com/simple

#### Install VnCoreNLP

pip install vncorenlp

#### Install underthesea

pip install underthesea

#### Install spacy_vi

pip install https://gitlab.com/trungtv/vi_spacy/-/raw/master/vi_core_news_lg/dist/vi_core_news_lg-0.0.1.tar.gz

#### Requirement.txt

pip install -r requirements.txt

# How to run

#### Run VnCoreNLP

vncorenlp -Xmx500m <path to VnCoreNLP-1.1.1.jar> -p 9000 -a "wseg"

#### Run Rasa actions agent

rasa run actions

#### Run Rasa interactive GUI or server (headless)

rasa x

rasa run

# Creating data

## Classifying intent

Open nlu.yml

## Create rule (enforce transition between intent)

Open rules.yml

## Train a story (an use case)

Open stories.yml
