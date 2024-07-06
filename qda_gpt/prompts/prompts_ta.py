# prompts_ta.py
# This script contains the Thematic Analysis instruction and prompts sent to OpenAI Assistant.

ta_instruction = """
You are a qualitative data analyst performing Thematic Analysis. Your task is to analyze the provided dataset of transcribed interviews.

Respond always with JSON-formatted outputs. DO NOT output any additional text outside of the JSON.

In the analysis, take into account the following considerations to get relevant context and information for the analysis:

{user_prompt}
"""


ta_prompt1 = """
You are requested to identify the most relevant themes in the attached dataset of transcribed interviews.
        
For each theme, provide:
 - index number starting from 1,
 - theme name (i.e. code) in no more than 3 words,
 - a meaningful and compact description of the theme with one sentence, and
 - a quote from the respondent.

Format the response in json format. Format the response in a structured table format suitable for conversion to a CSV file.
"""


ta_prompt2 = """
Determine how all the topics in the following list of topics can be grouped together.

Topics can also be in more than one group.

Group all the topics numbers only and provide for each group:
- index number,
- group name, and
- description of the group.
 
For thematic analysis, create proper amount of significant groups.

Format the response in json format. Format the response in a structured table format suitable for conversion to a CSV file.

Display the full list.

List of themes:
{response_json}
"""

# List of themes can be removed as it is supposed to be in the answer
# {", ".join(topic_list)}

ta_prompt3 = """
Your task is to determine again how all the topics in the following list of topics can be grouped together.

Topics can also be in more than one group.

Group all the topics numbers only and provide for each group:
- index number,
- group name, and
- description of the group.

For thematic analysis, create proper amount of significant groups.

Format the response in json format. Format the response in a structured table format suitable for conversion to a CSV file.

Display the full list.

List of groups:
{response_json}
"""


ta_prompt4 = """
Using all the topics in the list, give summary in two sentences and a name with max 5 words for summary.

List of topics:
{response2_json}
{response3_json}
"""



"""
The data contains transcribed interviews from the "Gaming Horizons" research study. There are 13 respondents who are young video game players. This demographic represents active participants in gaming, likely to be familiar with current gaming trends and technologies. The interviews were semi-structured, allowing for both guided questions and open-ended responses that provide rich qualitative data.
The main topics discussed in the interviews were:
- Role of Video Games in Education: Exploring how games are used as educational tools, their potential in formal learning environments, and their effectiveness in engaging and teaching students.
- Cultural Impact of Gaming: Discussing how video games influence and reflect current cultural trends, including issues of representation and the evolution of gaming as a mainstream entertainment medium.
- Economic Aspects: Looking at the gaming industry’s economic impact, including discussions on monetization strategies such as in-game purchases and subscription models.
- Technological Trends: Examining advancements in gaming technology, including virtual reality, augmented reality, and the integration of artificial intelligence in games.
- Ethical and Social Issues: Addressing concerns related to gaming, such as addiction, violence, and the social dynamics within gaming communities.

"""