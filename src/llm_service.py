import os
import yaml
import json
import re
import streamlit as st
from openai import OpenAI
from langchain_core.prompts import PromptTemplate

# Load Config
config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

# Global Config Variables
model4_name = config["model4_name"]
model3_name = config["model3_name"]
default_api_key = config["openai_api_key"]

def get_gemini_client(api_key):
    """Helper to create the OpenAI client pointing to Google"""
    return OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

def extract_json(content):
    """Helper to parse JSON from the AI response"""
    if '```json' in content:
        match = re.search(r'```json\n(.*?)```', content, re.DOTALL)
        if match: 
            return json.loads(match.group(1))
    # Fallback if no markdown blocks
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return content

def decide_encode_type(attributes, data_frame_head, model_type=4, user_api_key=None):
    try:
        model_name = str(model_type) # Uses "gemini-flash-latest", etc.
        api_key = user_api_key if user_api_key else default_api_key
        client = get_gemini_client(api_key)
        
        template = config["numeric_attribute_template"]
        prompt_template = PromptTemplate(input_variables=["attributes", "data_frame_head"], template=template)
        final_prompt = prompt_template.format(attributes=attributes, data_frame_head=data_frame_head)
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0
        )
        return extract_json(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Detailed Error in decide_encode_type: {e}") 
        st.stop()

def decide_fill_null(attributes, types_info, description_info, model_type=4, user_api_key=None):
    try:
        model_name = str(model_type)
        api_key = user_api_key if user_api_key else default_api_key
        client = get_gemini_client(api_key)
        
        template = config["null_attribute_template"]
        prompt_template = PromptTemplate(input_variables=["attributes", "types_info", "description_info"], template=template)
        final_prompt = prompt_template.format(attributes=attributes, types_info=types_info, description_info=description_info)
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0
        )
        return extract_json(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Detailed Error in decide_fill_null: {e}")
        st.stop()

def decide_model(shape_info, head_info, nunique_info, description_info, model_type=4, user_api_key=None):
    try:
        model_name = str(model_type)
        api_key = user_api_key if user_api_key else default_api_key
        client = get_gemini_client(api_key)

        template = config["decide_model_template"]
        prompt_template = PromptTemplate(input_variables=["shape_info", "head_info", "nunique_info", "description_info"], template=template)
        final_prompt = prompt_template.format(shape_info=shape_info, head_info=head_info, nunique_info=nunique_info, description_info=description_info)

        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0
        )
        return extract_json(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Detailed Error in decide_model: {e}")
        st.stop()

def decide_cluster_model(shape_info, description_info, cluster_info, model_type=4, user_api_key=None):
    try:
        model_name = str(model_type)
        api_key = user_api_key if user_api_key else default_api_key
        client = get_gemini_client(api_key)

        template = config["decide_clustering_model_template"]
        prompt_template = PromptTemplate(input_variables=["shape_info", "description_info", "cluster_info"], template=template)
        final_prompt = prompt_template.format(shape_info=shape_info, description_info=description_info, cluster_info=cluster_info)

        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0
        )
        return extract_json(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Detailed Error in decide_cluster_model: {e}")
        st.stop()

def decide_regression_model(shape_info, description_info, Y_name, model_type=4, user_api_key=None):
    try:
        model_name = str(model_type)
        api_key = user_api_key if user_api_key else default_api_key
        client = get_gemini_client(api_key)

        template = config["decide_regression_model_template"]
        prompt_template = PromptTemplate(input_variables=["shape_info", "description_info", "Y_name"], template=template)
        final_prompt = prompt_template.format(shape_info=shape_info, description_info=description_info, Y_name=Y_name)

        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0
        )
        return extract_json(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Detailed Error in decide_regression_model: {e}")
        st.stop()

def decide_target_attribute(attributes, types_info, head_info, model_type=4, user_api_key=None):
    try:
        model_name = str(model_type)
        api_key = user_api_key if user_api_key else default_api_key
        client = get_gemini_client(api_key)

        template = config["decide_target_attribute_template"]
        prompt_template = PromptTemplate(input_variables=["attributes", "types_info", "head_info"], template=template)
        final_prompt = prompt_template.format(attributes=attributes, types_info=types_info, head_info=head_info)

        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0
        )
        
        json_data = extract_json(response.choices[0].message.content)
        return json_data["target"]

    except Exception as e:
        st.error(f"Detailed Error in decide_target_attribute: {e}")
        st.stop()

def decide_test_ratio(shape_info, model_type=4, user_api_key=None):
    try:
        model_name = str(model_type)
        api_key = user_api_key if user_api_key else default_api_key
        client = get_gemini_client(api_key)

        template = config["decide_test_ratio_template"]
        prompt_template = PromptTemplate(input_variables=["shape_info"], template=template)
        final_prompt = prompt_template.format(shape_info=shape_info)

        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0
        )
        
        json_data = extract_json(response.choices[0].message.content)
        return json_data["test_ratio"]

    except Exception as e:
        st.error(f"Detailed Error in decide_test_ratio: {e}")
        st.stop()

def decide_balance(shape_info, description_info, balance_info, model_type=4, user_api_key=None):
    try:
        model_name = str(model_type)
        api_key = user_api_key if user_api_key else default_api_key
        client = get_gemini_client(api_key)

        template = config["decide_balance_template"]
        prompt_template = PromptTemplate(input_variables=["shape_info", "description_info", "balance_info"], template=template)
        final_prompt = prompt_template.format(shape_info=shape_info, description_info=description_info, balance_info=balance_info)

        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0
        )
        
        json_data = extract_json(response.choices[0].message.content)
        return json_data["method"]

    except Exception as e:
        st.error(f"Detailed Error in decide_balance: {e}")
        st.stop()