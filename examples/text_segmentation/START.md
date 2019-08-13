
# Text Segmentation

# Install

## Linux & Ubuntu guide

Install python and virtualenv 

```bash
# install python and virtualenv 
apt install python3.6
pip3 install virtualenv

# setup python virtual environment 
virtualenv -p python3 env3
source env3/bin/activate

# install requirements 
cd backend
pip install -r requirements.txt
```

# Start

Text segmentation for a piece of text

```bash
python server.py -c config.json -l ../examples/text_segmentation/config.xml -i ../examples/text_segmentation/tasks.json -o output
```
