import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

def process_twitter_posts(raw_file_path, processed_file_path=None):
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        enriched_posts = []
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = {**post, **metadata}
            enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)
    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = [unified_tags[tag] for tag in current_tags]
        post['tags'] = new_tags

    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4)

def extract_metadata(post):
    template = '''
    You are given a Twitter post. You need to extract the number of lines, language of the post, and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language, and tags. 
    3. Tags is an array of text tags. Extract a maximum of two tags.
    4. Language should be English or Hinglish (Hinglish means Hindi + English)
    
    Here is the actual post on which you need to perform this task:  
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post": post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse posts.")
    return res

def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    # Loop through each post and extract the tags
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])  # Add the tags to the set

    unique_tags_list = ','.join(unique_tags)

    template = '''I will give you a list of tags. You need to unify the tags with the following requirements:
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "TechTips", "Tech Advice" can all be merged into a single tag "Tech Tips". 
       Example 2: "MotivationMonday", "MondayMotivation", "Inspiration" can be mapped to "Motivation"
       Example 3: "DigitalMarketing", "OnlineMarketing", "SocialMediaMarketing" can be mapped to "Marketing"
       Example 4: "LifeHacks", "LifeTips" can be mapped to "Tips"
    2. Each tag should follow title case convention. Example: "Motivation", "Tech Tips"
    3. Output should be a JSON object, no preamble
    4. Output should have a mapping of the original tag and the unified tag. 
       For example: {{"TechTips": "Tech Tips", "Tech Advice": "Tech Tips", "MotivationMonday": "Motivation"}}
    
    Here is the list of tags: 
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": str(unique_tags_list)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse tags.")
    return res

if __name__ == "__main__":
    process_twitter_posts("data/raw_posts.json", "data/processed_posts.json")
