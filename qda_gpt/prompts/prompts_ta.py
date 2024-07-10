# prompts_ta.py
# This script contains the Thematic Analysis instruction and prompts sent to OpenAI Assistant.

ta_instruction = """
You are a qualitative data analyst performing Thematic Analysis. Your task is to analyze the provided dataset of transcribed interviews.

Always respond with JSON-formatted outputs. DO NOT output any additional text outside of the JSON.

In the analysis, take into account the following information and considerations for performing the analysis:

{user_prompt}
"""



# Generating initial codes and familiarizing with the data
ta_prompt1 = """
Read through the data to understand its content and familiarize yourself with it. Identify and label significant features of the data (codes). The whole data should be allocated to different codes regarding the parts of the data that are relevant for the research and provided research questions.

For each code, provide:
- index number starting from 1,
- code name in 1-3 words (max 5 words),
- a meaningful and compact definition of the code with 2-10 sentences to describe the most significant properties, purpose, and how it differs from other somewhat similar features/codes,
- a description of a possible higher-level category it could be used in,
- a descriptive quote from some respondent.

Example JSON output:
{{
    "Codes": [
        {{
            "index": 1,
            "code_name": "Student Engagement",
            "definition": "Instances where students show active participation and interest in the learning process. This includes behaviors such as asking questions, participating in class discussions, collaborating in group activities, and demonstrating enthusiasm for learning. The purpose of this code is to capture the various ways students engage with the educational material and their peers. It differs from related codes like 'Passive Learning' or 'Disengagement' by focusing specifically on active, voluntary participation and a positive attitude towards learning.",
            "higher_level_category": "Educational Outcomes",
            "quote": "I love participating in class discussions because they help me understand the material better."
        }},
        {{
            "index": 2,
            "code_name": "Teacher Support",
            "definition": "Examples of teachers providing assistance and encouragement to students. This can involve one-on-one tutoring, offering positive reinforcement, giving constructive feedback, and providing additional learning resources. The purpose of this code is to identify supportive behaviors from teachers that enhance student learning and motivation. It differs from similar codes like 'Peer Support' or 'Parental Support' by focusing solely on the teacher's role in supporting students.",
            "higher_level_category": "Teaching Methods",
            "quote": "My teacher always takes the time to explain difficult concepts in a way that makes sense."
        }}
    ]
}}
"""


# Searching for categories
ta_prompt2 = """
Read through the data and the codes you generated. Group similar codes into different categories based on similarities or patterns observed in the data. Codes can belong to more than one category. Generally, all codes should belong to some category. However, codes that do not contribute meaningfully to the analysis can be discarded. At this stage, it is better to have too many than too few categories and codes.

For each category, provide:
- index number,
- category name in 1-3 words (max 5 words),
- a meaningful and compact definition of the category with 2-10 sentences to describe the most significant properties, purpose, and what are the requirements for a specific topic/content to be identified as a category,
- a description of the category's relevance to the research questions,
- the requirements for codes to belong to this category,
- index numbers of the codes that are related to this category.

Example JSON output:
{
    "Categories": [
        {
            "index": 1,
            "name": "Active Participation",
            "definition": "A category that encompasses various forms of active student involvement in the learning process. This includes behaviors such as asking questions, engaging in discussions, and participating in group activities. The purpose is to capture the extent and nature of student engagement in educational activities. Requirements for this category include observable behaviors that indicate active participation.",
            "description": "This category is relevant to understanding how different forms of student engagement impact learning outcomes and classroom dynamics.",
            "code_requirements": "Codes in this category must demonstrate behaviors indicative of active student participation.",
            "codes": [1, 2, 5, 9, 15, 20, 35, 36, 66, 71, 73, 88, 101, 105, 111, 123, 129, 199, 248, 266]
        },
        {
            "index": 2,
            "name": "Supportive Teaching",
            "definition": "A category that includes various types of support and encouragement provided by teachers. This can involve one-on-one tutoring, positive reinforcement, and providing additional learning resources. The purpose is to identify supportive behaviors from teachers that enhance student learning and motivation. Requirements for this category include actions taken by teachers that provide direct support to students.",
            "description": "This category helps to explore the role of teacher support in fostering student academic success and emotional well-being.",
            "code_requirements": "Codes in this category should reflect actions taken by teachers to assist students.",
            "codes": [2, 7, 11, 17, 123, 144, 347]
        }
    ]
}
"""



# Assign categories to themes
ta_prompt3 = """
Read through the data to understand its content. Identify overarching themes that encompass multiple categories and provide insight into the major patterns and meanings in the data. Regarding the categories that you created, group similar categories into different themes based on similarities or patterns observed in the data. One category can belong to more than one theme. Generally, all categories should belong to some theme. However, categories that do not contribute meaningfully to the analysis can be discarded. At this stage, it is better to have too many than too few themes and categories.

For each theme, provide:
- index number,
- theme name in 1-3 words (max 5 words),
- a meaningful and compact definition of the theme with 2-10 sentences to describe the most significant properties, purpose, and what are the requirements for a specific topic/content to be identified as a theme,
- a description of the theme and its relevance to the research questions,
- the requirements for categories to belong to this theme,
- index numbers of the categories that are related to this theme.

Example JSON output:
{
    "Themes": [
        {
            "index": 1,
            "name": "Social and Ethical Issues",
            "definition": "This theme covers the social dynamics and ethical concerns within the gaming community. It includes topics such as online behavior, community building, and the ethical implications of game content and industry practices. The purpose is to explore how gaming impacts social interactions and raises ethical questions. Requirements for this theme include a focus on social behavior, ethical dilemmas, and community interactions.",
            "description": "This theme is relevant to understanding the broader social and ethical impacts of gaming on individuals and communities.",
            "category_requirements": "Categories in this theme must address social or ethical dimensions of gaming.",
            "categories": [5, 6, 12, 19]
        },
        {
            "index": 2,
            "name": "Technological and Economic Impact",
            "definition": "This theme focuses on technological advancements and their economic implications within the gaming industry. It includes categories related to the development and adoption of new technologies, economic trends, and the financial aspects of game development and distribution. The purpose is to examine how technology drives economic change in the gaming sector. Requirements for this theme include a focus on technological development, economic analysis, and financial impact.",
            "description": "This theme helps to understand the influence of technological progress and economic factors on the evolution of the gaming industry.",
            "category_requirements": "Categories in this theme should reflect technological or economic aspects.",
            "categories": [3, 7, 12, 13, 18]
        }
    ]
}
"""



# Assign themes top-down, separate prompt to different OpenAI Assistant thread
ta_prompt_separate = """
Read through the data to understand its content. As the first step of thematic analysis, derive and develop preliminary themes from the research questions and data. Develop themes based on research questions (deductive). The number of themes is often 3-8, but you can deviate from that if needed. Provide a general summary of all identified themes.

For each theme, provide:
- theme name in 1-3 words (max 5 words),
- a meaningful and compact definition of the theme with 2-10 sentences to describe the most significant properties, purpose, and what are the requirements for a specific topic/content to be identified as a theme,
- a description of the theme and its relevance to the research questions.

Example JSON output:
{
    "Themes": [
        {
            "name": "Educational Impact",
            "definition": "This theme explores how gaming influences educational outcomes and learning processes. It includes both positive and negative effects of gaming on education, such as improved problem-solving skills and potential distractions from studies. Requirements for this theme include a focus on the educational aspects and consequences of gaming.",
            "description": "This theme is relevant to understanding the educational benefits and challenges associated with gaming."
        },
        {
            "name": "Social Dynamics",
            "definition": "This theme examines the role of gaming in social interactions and community building. It covers aspects such as forming friendships, online collaboration, and the social behavior influenced by gaming. Requirements for this theme include a focus on the social relationships and community aspects related to gaming.",
            "description": "This theme is important for exploring how gaming affects social relationships, community engagement, and social behavior."
        }
    ]
}
"""



# Merge themes
ta_prompt4 = """
Read through the data to understand its content. Below between *** is a set of top-down themes derived from the research questions.

***
{response_from_separate_thread}
***

Merge these top-down themes with the themes that you created in your previous message to form a coherent set of final themes, ensuring that both (themes from your previous answer and above top-down) insights are considered. Identify any overlapping or closely related themes between the two sets. Merge overlapping and closely related themes to create unified themes that capture the essence of both insights. Retain any unique themes from both sets that do not overlap. Ensure that the merged themes are distinct, comprehensive, and accurately represent the data and are relevant for the research questions/objectives. Provide a brief description for each final theme, explaining its relevance to the research questions and the data.

For each theme, provide:
- index number,
- theme name in 1-3 words (max 5 words),
- a meaningful and compact definition of the theme with 2-10 sentences to describe the most significant properties, purpose, and what are the requirements for a specific topic/content to be identified as a theme,
- a description of the theme and its relevance to the research questions.

Example JSON output:
{{
    "Themes": [
        {{
            "index": 1,
            "name": "Educational and Social Impact",
            "definition": "This theme combines insights on the educational outcomes and social dynamics influenced by gaming. It covers both the positive and negative effects of gaming on education, such as improved problem-solving skills and potential distractions, as well as social aspects like forming friendships and community building. Requirements for this theme include a focus on the educational and social consequences of gaming.",
            "description": "This theme is relevant to understanding the combined educational and social impacts of gaming on individuals and communities."
        }},
        {{
            "index": 2,
            "name": "Technological Advances",
            "definition": "This theme focuses on technological advancements and their implications for the gaming industry. It includes categories related to the development and adoption of new technologies, the impact of these technologies on gameplay, and their economic implications. Requirements for this theme include a focus on technological development and economic analysis within gaming.",
            "description": "This theme helps to understand the role of technological progress in shaping the future of the gaming industry and its economic impact."
        }}
    ]
}}
"""


# Assign categories to final themes
ta_prompt5 = """
Read through the data to understand its content. Below between *** are the categories you previously created.

***
{response_from_prompt2}
***

Review current categories and assign existing categories to the appropriate final themes. You can refactor categories based on the data and research questions if needed. Based on the data, you can also add new categories. Redundant categories that cannot be assigned to any of the themes can be removed. One category can belong to more than one theme. Ensure that the retained categories are distinct, comprehensive, and accurately represent the data. Provide a brief description for each category, explaining its relevance to the theme.

For each category, provide:
- index number,
- category name in 1-3 words (max 5 words),
- a meaningful and compact definition of the category with 2-10 sentences to describe the most significant properties, purpose, and what are the requirements for a specific topic/content to be identified as a category,
- the requirements for this category to belong to this theme/these themes,
- index numbers of the themes that are related to this category,
- names of the themes that are related to this category.

Additionally, provide a nested table that shows the hierarchical structure of themes and categories.

Example JSON output:
{
    "Categories": [
        {
            "index": 1,
            "name": "Educational Benefits",
            "definition": "This category includes various positive impacts of gaming on educational contexts. It encompasses improved problem-solving skills, enhanced motivation for learning, and the use of educational games for skill development. Requirements for this category include observable educational outcomes that are positively influenced by gaming.",
            "theme_requirements": "Categories in this theme must demonstrate educational improvements or benefits resulting from gaming.",
            "themes": [1],
            "theme_names": ["Educational and Social Impact"]
        },
        {
            "index": 2,
            "name": "Social Interaction",
            "definition": "This category covers how gaming facilitates social interactions. It includes forming friendships, online collaboration, and community building through gaming. Requirements for this category include social behaviors and interactions that occur within the context of gaming.",
            "theme_requirements": "Categories in this theme must reflect social interactions and community engagement facilitated by gaming.",
            "themes": [1, 2],
            "theme_names": ["Educational and Social Impact", "Technological Advances"]
        },
        {
            "index": 3,
            "name": "Technological Innovation",
            "definition": "This category includes advancements in gaming technology such as new game engines, VR/AR, and other cutting-edge technologies. Requirements for this category include the development and implementation of new technologies in gaming.",
            "theme_requirements": "Categories in this theme must demonstrate technological advancements and innovations in gaming.",
            "themes": [2],
            "theme_names": ["Technological Advances"]
        },
        {
            "index": 4,
            "name": "Economic Impact",
            "definition": "This category covers the economic aspects of gaming, including revenue generation, job creation, and market trends. Requirements for this category include the financial implications and economic benefits of the gaming industry.",
            "theme_requirements": "Categories in this theme must reflect economic factors and impacts related to gaming.",
            "themes": [2],
            "theme_names": ["Technological Advances"]
        }
    ],
    "ThemeCategoryHierarchy": [
        {
            "theme_index": 1,
            "theme_name": "Educational and Social Impact",
            "categories": [
                {
                    "category_index": 1,
                    "category_name": "Educational Benefits"
                },
                {
                    "category_index": 2,
                    "category_name": "Social Interaction"
                }
            ]
        },
        {
            "theme_index": 2,
            "theme_name": "Technological Advances",
            "categories": [
                {
                    "category_index": 2,
                    "category_name": "Social Interaction"
                },
                {
                    "category_index": 3,
                    "category_name": "Technological Innovation"
                },
                {
                    "category_index": 4,
                    "category_name": "Economic Impact"
                }
            ]
        }
    ]
}
"""


# Assign codes to final categories
ta_prompt6 = """
Read through the data to understand its content. Below between *** are the codes you previously created.

***
{response_from_prompt1}
***

Review initial codes and assign them to the appropriate final categories. You can merge codes that are very similar into a single, more comprehensive code (do not do this easily). You can change code names but not the underlying meaning/feature/description. You can remove redundant codes that do not belong to any category. One code can belong to more than one category. Ensure that the retained codes are distinct, comprehensive, and accurately represent the data.

For each code, provide:
- index number,
- code name in 1-3 words (max 5 words),
- a meaningful and compact definition of the code with 2-10 sentences to describe the most significant properties, purpose, and how it differs from other somewhat similar features,
- a descriptive quote from the respondent,
- the requirements for this code to belong to this category or these categories,
- index numbers of the categories that are related to the code,
- names of the categories that are related to the code.

Additionally, provide a nested table that shows the hierarchical structure of categories and codes.

Example JSON output:
{
    "Codes": [
        {
            "index": 1,
            "name": "Problem Solving Skills",
            "definition": "This code refers to instances where gaming has helped improve problem-solving skills. It includes scenarios where players need to strategize, plan, and solve complex problems within the game environment. This differs from 'Learning Motivation' which focuses on the motivational aspects of learning through gaming.",
            "quote": "Gaming has significantly improved my problem-solving skills.",
            "category_requirements": "Codes in this category must demonstrate improvements in cognitive skills due to gaming.",
            "categories": [1],
            "category_names": ["Educational Benefits"]
        },
        {
            "index": 2,
            "name": "Online Friendships",
            "definition": "This code captures instances where gaming has led to the formation of new friendships online. It includes examples of players meeting new people, building friendships, and maintaining social connections through gaming. This differs from 'Community Events' which focuses on organized events within the gaming community.",
            "quote": "I have made many friends through online gaming.",
            "category_requirements": "Codes in this category must reflect social interactions and relationships formed through gaming.",
            "categories": [2],
            "category_names": ["Social Interaction"]
        },
        {
            "index": 3,
            "name": "VR Technology",
            "definition": "This code includes mentions of Virtual Reality (VR) technology in gaming. It encompasses the development, use, and impact of VR on the gaming experience. This differs from 'Game Engine Development' which focuses on the software used to create games.",
            "quote": "The new VR technology has transformed my gaming experience.",
            "category_requirements": "Codes in this category must demonstrate the use and impact of VR technology in gaming.",
            "categories": [1, 2],
            "category_names": ["Educational Benefits", "Social Interaction"]
        },
        {
            "index": 4,
            "name": "Job Creation",
            "definition": "This code represents instances where the gaming industry has created job opportunities. It includes examples of employment in game development, marketing, and esports. This differs from 'Revenue Generation' which focuses on the financial income from gaming.",
            "quote": "The gaming industry has created numerous job opportunities.",
            "category_requirements": "Codes in this category must reflect economic benefits and job creation related to gaming.",
            "categories": [1],
            "category_names": ["Educational Benefits"]
        },
        {
            "index": 5,
            "name": "Learning Motivation",
            "definition": "This code refers to instances where gaming has increased motivation for learning. It includes examples where educational games or gamified learning experiences have encouraged students to engage more with educational content. This differs from 'Problem Solving Skills' which focuses on cognitive skill development.",
            "quote": "Educational games have made me more interested in learning.",
            "category_requirements": "Codes in this category must demonstrate increased motivation for learning due to gaming.",
            "categories": [1],
            "category_names": ["Educational Benefits"]
        },
        {
            "index": 6,
            "name": "Community Events",
            "definition": "This code captures instances of organized events within the gaming community, such as tournaments, meetups, and online gatherings. This differs from 'Online Friendships' which focuses on individual social relationships.",
            "quote": "I love participating in online gaming tournaments.",
            "category_requirements": "Codes in this category must reflect organized community events within the gaming context.",
            "categories": [2],
            "category_names": ["Social Interaction"]
        }
    ],
    "CategoryCodeHierarchy": [
        {
            "category_index": 1,
            "category_name": "Educational Benefits",
            "codes": [
                {
                    "code_index": 1,
                    "code_name": "Problem Solving Skills"
                },
                {
                    "code_index": 3,
                    "code_name": "VR Technology"
                },
                {
                    "code_index": 4,
                    "code_name": "Job Creation"
                },
                {
                    "code_index": 5,
                    "code_name": "Learning Motivation"
                }
            ]
        },
        {
            "category_index": 2,
            "category_name": "Social Interaction",
            "codes": [
                {
                    "code_index": 2,
                    "code_name": "Online Friendships"
                },
                {
                    "code_index": 3,
                    "code_name": "VR Technology"
                },
                {
                    "code_index": 6,
                    "code_name": "Community Events"
                }
            ]
        }
    ]
}
"""




# Interpretation, analysis, and synthesis
ta_prompt7 = """
Read through the data to understand its content. Analyze the themes, categories, and codes to draw conclusions related to the research questions. Highlight key findings and insights for interpretation.

Review the following dataset to ensure that all data segments are coded correctly under the final themes, categories, and codes. Flag any segments that are unaddressed, misclassified, or missing critical information related to themes, categories, and/or codes. Identify patterns, relationships, and insights, and suggest any potential sub-themes.

Please synthesize the findings from each of the analyzed themes. Integrate these insights to answer the research questions and explain how the themes interrelate and contribute to the overall understanding of the research topic.

The output should include:
- a concise title for the summary that captures the essence of the findings in up to 10 words,
- a description in two sentences covering the main insights from the themes and groups,
- flagged segments that are unaddressed, misclassified, or missing critical information related to themes, categories, and/or codes,
- presentation of each theme with definitions, descriptions, and illustrative quotes,
- analysis and interpretation of findings,
- conclusions and implications of the study.

Example JSON output:

{
    "Themes": [
        {
            "name": "Educational and Social Impact",
            "quotes": "Gaming has significantly improved my problem-solving skills. ||| I have made many friends through online gaming. ||| Educational games have made me more interested in learning.",
            "analysis": "This theme shows that gaming has both positive and negative impacts on education and social behavior.",
            "conclusions": "Gaming can be a valuable educational tool but requires careful implementation."
        },
        {
            "name": "Technological Advances",
            "quotes": "The new VR technology has transformed my gaming experience. ||| The gaming industry has created numerous job opportunities. ||| Technological innovations are crucial for the future of gaming.",
            "analysis": "Technological innovations in gaming drive industry growth and change user experiences.",
            "conclusions": "Ongoing technological developments are crucial for the future of the gaming industry."
        }
    ],
    "Overall_Findings": {
        "summary_name": "Key Educational, Social, and Technological Findings from Gaming",
        "description": "This study explores the educational, social, and technological impacts of gaming, highlighting both benefits and challenges.",
        "flagged_segments": "The segment 'Gaming has helped me understand historical events better' is unaddressed, which could potentially provide new insights if properly categorized. ||| The segment 'I use VR for exercise routines' appears to be misclassified under 'Technological Advances' when it might fit better under 'Educational and Social Impact'. ||| The segment 'Gaming can sometimes be isolating' is missing critical information on the specific contexts where this occurs.",
        "analysis_and_interpretation": "The themes collectively highlight the multifaceted impact of gaming on education, social behavior, and technological progress.",
        "conclusions_and_implications": "The study concludes that while gaming offers significant educational and social benefits, there are also challenges that need to be addressed. Technological advancements play a key role in the industry's future."
    }
}



