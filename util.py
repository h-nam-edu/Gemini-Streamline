import streamlit as st
import requests
import yaml
import time
import random
import os
import json

config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
with open(config_path, 'r') as file:
    config_data = yaml.safe_load(file)

def load_lottie():
    # Get the directory where util.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the config folder
    config_dir = os.path.join(current_dir, 'config')

    # Get filenames from the yaml config
    file_name1 = config_data.get('lottie_url1')
    file_name2 = config_data.get('lottie_url2')

    json1, json2 = None, None

    # Helper function to load a single file
    def load_local_json(filename):
        if not filename: return None
        # Build the full path: O:\...\app\config\filename.json
        full_path = os.path.join(config_dir, filename)
        try:
            with open(full_path, "r", encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ File not found: {full_path}")
            return None
        except Exception as e:
            print(f"⚠️ Error reading {filename}: {e}")
            return None

    # Load them
    json1 = load_local_json(file_name1)
    json2 = load_local_json(file_name2)

    return json1, json2

# write a stream of words
def stream_data(line):
    for word in line.split():
        yield word + " "
        time.sleep(random.uniform(0.02, 0.05))

# Store the welcome message and introduction
def welcome_message():
    return config_data['welcome_template']

def introduction_message():
    return config_data['introduction_template1'], config_data['introduction_template2']

# Show developer info at the bottom
def developer_info():
    time.sleep(2)
    st.write(stream_data(":grey[Streamline Analyst is developed by *Zhe Lin*. You can reach out to me via] :blue[wilson.linzhe@gmail.com] :grey[or] :blue[[GitHub](https://github.com/Wilson-ZheLin)]"))

def developer_info_static():
    st.write(":grey[Streamline Analyst is developed by *Zhe Lin*. You can reach out to me via] :blue[wilson.linzhe@gmail.com] :grey[or] :blue[[GitHub](https://github.com/Wilson-ZheLin)]")