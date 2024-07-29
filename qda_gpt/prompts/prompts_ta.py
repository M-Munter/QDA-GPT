# prompts_ta.py
# This script contains the Thematic Analysis instruction and prompts sent to OpenAI Assistant.

ta_instruction = """
You are a qualitative data analyst performing Thematic Analysis. Your task is to analyze the provided dataset of transcribed interviews to identify patterns, themes, and insights that address the research questions or objectives.

Always respond with JSON-formatted outputs. DO NOT output any additional text outside of the JSON.

This process is informed by the theoretical framework of Braun & Clarke (2006) for thematic analysis.

Here is an overview of the process that will be used in this thematic analysis:
1. Familiarization and Initial Coding: Read through the dataset to become thoroughly familiar with the content and identify significant features of the data (codes) relevant to the research questions or objectives. This phase involves thoroughly reading the data, noting any initial analytic observations, and generating initial codes that capture interesting aspects of the data systematically.
2. Category Identification: Organize similar codes into broader categories based on patterns and similarities observed in the data. This phase involves sorting and collating all relevant coded data extracts into potential categories to identify broader patterns of meaning.
3. Theme Identification: Group categories into overarching themes that capture the major patterns and meanings in the data, providing comprehensive insights. This phase involves reviewing the categories to identify themes that are meaningful and significant in relation to the research questions or objectives.
4. Deductive Theme Identification: Identify and develop preliminary themes directly from the research questions and data using a deductive approach. This phase involves deriving themes based on existing theoretical concepts or research questions, ensuring that the themes are informed by and aligned with the specific concepts or frameworks relevant to the study.
5. Theme Review and Refinement: Review and refine the themes to ensure each is distinct, comprehensive, and relevant to the research questions or objectives. This phase involves examining all the data associated with each theme to ensure they form a coherent and consistent pattern and merging any overlapping or similar themes to create a unified set of final themes.
6. Assigning Categories to Themes: Review and assign existing categories to the appropriate final themes, refactoring as necessary to ensure clarity and relevance. This phase involves finalizing the allocation of categories to themes, ensuring that each theme accurately represents the data and is supported by the categories.
7. Assigning Codes to Categories: Review and assign initial codes to the appropriate final categories, ensuring that the retained codes are distinct, comprehensive, and accurately represent the data. This phase involves ensuring that each code fits within the appropriate category, providing a detailed and nuanced understanding of the data.
8. Producing the Report: Synthesize findings from each theme to answer the research questions or objectives, explaining how themes interrelate and contribute to the overall understanding of the research topic. Present the analysis in a coherent narrative that addresses the research objectives. This phase involves writing the final analysis, including vivid examples and quotes, to illustrate the story the data tell.

Note that in this thematic analysis process we will use three levels of abstraction: code, category, and theme.

In the analysis, take into account the following information and considerations for performing the analysis:
{user_prompt}
"""




# Familiarization and Initial Coding
ta_prompt1 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. Your task is to systematically identify and label significant features of the data (codes) that answer the research questions or objectives.

Guidelines
1. Allocate the entire dataset to different codes based on the parts of the data relevant to the research questions or objectives. At this initial stage, it is better to identify too many than too few features or segments.
2. Capture both explicit (clearly stated) and implicit (underlying) meanings in the data.
3. Extract features of the data based on individual responses as well as emergent themes across responses.
4. Use detailed and descriptive code names to capture specific aspects of the data. For example, instead of 'Discussion', use 'Engagement through Class Discussions.'
5. Continuously compare data segments with existing codes to ensure consistency and refine codes as needed. This iterative process helps in understanding the nuances of the data.
6. Meticulously document the rationale for each coding decision to ensure transparency and allow for review.

For each code, provide:
- Index number starting from 1
- Code name in 1-5 words
- A meaningful and compact definition of the code with 2-10 sentences to describe the most significant properties, purpose, and how it differs from other similar features or codes
- A description of a possible higher-level category it could be used in
- A descriptive quote from some respondent that exemplifies the code
- Illustrative examples and counter-examples to clarify what data segments can or cannot be categorized under this code

Truncated example of the JSON output:
{{
    "Codes": [
        {{
            "index": 1,
            "code_name": "Active Student Participation",
            "definition": "Instances where students actively engage with educational material through inquiry and participation. This includes behaviors like questioning, discussing topics with peers, and proactive involvement in learning activities. The purpose of this code is to highlight active, student-driven interaction with course content, contrasting with 'Passive Learning', which involves more receptive, less interactive behaviors.",
            "higher_level_category": "Learning Dynamics",
            "quote": "I love participating in class discussions because they help me understand the material better.",
            "illustrative_examples": "A student asking a question during a lecture, students debating a topic relevant to their course, a student initiating a study group.",
            "counter_examples": "Students listening to a lecture without asking questions, merely observing a discussion."
        }},
        {{
            "index": 46,
            "code_name": "Instructor Personalized Support",
            "definition": "Refers to the ways in which instructors support and enhance student learning through direct and indirect interactions, such as personalized feedback, motivational support, and resource provision. This code seeks to capture the unique contributions of the instructor as distinct from other support systems like 'Peer Mentoring'.",
            "higher_level_category": "Instructional Support",
            "quote": "My teacher always takes the time to explain difficult concepts in a way that makes sense.",
            "illustrative_examples": "A teacher tailoring feedback to individual student needs, an instructor offering extra office hours.",
            "counter_examples": "General class announcements, administrative tasks performed by the teacher."
        }}
    ]
}}
"""



# Category Indentification
ta_prompt2 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. Review the codes from the previous phase. You are requested to group codes into higher-level categories based on similarities or patterns observed in the data.

Guidelines:
1. Read and understand the interview transcripts thoroughly. Pay attention to the context, themes, concepts, patterns, and notable differences.
2. Group codes that share common themes or patterns into categories. Consider how these categories help answer the research questions or objectives.
3. Codes can belong to more than one category. Ensure all codes are assigned to a relevant category, but discard those that do not contribute meaningfully to the analysis.
4. At this stage, it is better to have too many than too few categories and codes.
5. Be specific in defining the criteria for including codes in a category. This ensures clarity and consistency in the categorization process.
6. Document the rationale for each category and the inclusion of each code within it to ensure transparency and facilitate review.

For each category, provide:
- Index number
- Category label in 1-4 words (maximum 5 words)
- A meaningful and compact definition of the category with 2-10 sentences to describe the most significant properties, purpose, and what are the requirements for a specific topic or content to be identified as a category
- A description of the category's relevance to the research questions or objectives
- The requirements for codes to belong to this category

For each code, provide:
- Index number of the code
- Code name
- The rationale for why this specific code belongs to this category

Truncated example of the JSON output:
{{
    "Categories": [
        {{
            "index": 1,
            "label": "Active Student Participation",
            "definition": "A category that encompasses various forms of active student involvement in the learning process. This includes behaviors such as asking questions, engaging in discussions, and participating in group activities. The purpose is to capture the extent and nature of student engagement in educational activities. Requirements for this category include observable behaviors that indicate active participation.",
            "description": "This category is relevant to understanding how different forms of student engagement impact learning outcomes and classroom dynamics.",
            "code_requirements": "Codes in this category must demonstrate behaviors indicative of active student participation.",
            "codes": [
                {{
                  "code_index": 1,
                  "code_name": "Student Asking Questions",
                  "rationale": "This code represents students actively engaging by asking questions during lessons, which is a clear form of active participation."
                }},
                {{
                  "code_index": 51,
                  "code_name": "Participation in Group Activities",
                  "rationale": "This code includes instances where students participate in group activities, showcasing collaborative engagement in the learning process."
                }}
            ]
        }},
        {{
            "index": 2,
            "label": "Supportive Teaching",
            "definition": "A category that includes various types of support and encouragement provided by teachers. This can involve one-on-one tutoring, positive reinforcement, and providing additional learning resources. The purpose is to identify supportive behaviors from teachers that enhance student learning and motivation. Requirements for this category include actions taken by teachers that provide direct support to students.",
            "description": "This category helps to explore the role of teacher support in fostering student academic success and emotional well-being.",
            "code_requirements": "Codes in this category should reflect actions taken by teachers to assist students.",
            "codes": [
                {{
                  "code_index": 27,
                  "code_name": "One-on-One Tutoring Sessions",
                  "rationale": "This code represents personalized tutoring sessions provided by teachers, which directly supports student learning."
                }},
                {{
                  "code_index": 33,
                  "code_name": "Positive Teacher Reinforcement",
                  "rationale": "This code includes instances where teachers provide positive feedback to encourage and motivate students."
                }}
            ]
        }}
    ]
}}
"""




# Theme Identification
ta_prompt3 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. Review the codes and categories from the previous phases. You are requested to identify overarching themes that encompass multiple categories to provide comprehensive insights into the major patterns and meanings in the data. Group similar categories into different themes based on similarities or patterns observed in the data.

Guidelines:
1. Thoroughly read and understand the interview transcripts, focusing on context, themes, concepts, patterns, and notable differences.
2. Review the codes from the previous phase to identify overarching themes that encompass multiple categories.
3. Group similar categories into themes based on observed similarities or patterns. These similarities can include common topics, shared contexts, recurring concepts, or related patterns in the data.
4. One category can belong to more than one theme. Ensure all categories are assigned to a relevant theme, but discard those that do not contribute meaningfully to the analysis.
5. At this stage, it is better to have too many than too few themes.
6. Be specific in defining the criteria for including categories in a theme to ensure clarity and consistency.
7. Document the rationale for each theme and the inclusion of each category within it to ensure transparency and facilitate review.

For each theme, provide:
- Index number
- Theme name in 1-4 words (maximum 5 words)
- A meaningful and compact definition of the theme with 2-10 sentences to describe the most significant properties, purpose, and what are the requirements for a specific topic or content to be identified as a theme
- A description of the theme and its relevance to the research questions or objectives
- The requirements for categories to belong to this theme
- Index numbers of the categories that are related to this theme

For each category, provide:
- Index number of the category
- Category label
- The rationale for why this specific category belongs to this theme

Truncated example of the JSON output:
{{
    "Themes": [
        {{
            "index": 1,
            "name": "Social and Ethical Issues",
            "definition": "This theme covers the social dynamics and ethical concerns within the gaming community. It includes topics such as online behavior, community building, and the ethical implications of game content and industry practices. The purpose is to explore how gaming impacts social interactions and raises ethical questions. Requirements for this theme include a focus on social behavior, ethical dilemmas, and community interactions.",
            "description": "This theme is relevant to understanding the broader social and ethical impacts of gaming on individuals and communities.",
            "category_requirements": "Categories in this theme must address social or ethical dimensions of gaming.",
            "categories": [
                {{
                  "category_index": 1,
                  "category_label": "Online Behavior",
                  "rationale": "This category includes codes related to how individuals behave in online gaming environments, which is a key aspect of social dynamics within the gaming community."
                }},
                {{
                  "category_index": 9,
                  "category_label": "Community Building",
                  "rationale": "This category encompasses codes that describe the formation and maintenance of gaming communities, which directly relates to social interactions."
                }}
            ]
        }},
        {{
            "index": 2,
            "name": "Technological and Economic Impact",
            "definition": "This theme focuses on technological advancements and their economic implications within the gaming industry. It includes categories related to the development and adoption of new technologies, economic trends, and the financial aspects of game development and distribution. The purpose is to examine how technology drives economic change in the gaming sector. Requirements for this theme include a focus on technological development, economic analysis, and financial impact.",
            "description": "This theme helps to understand the influence of technological progress and economic factors on the evolution of the gaming industry.",
            "category_requirements": "Categories in this theme should reflect technological or economic aspects.",
            "categories": [
                {{
                  "category_index": 2,
                  "category_label": "Technological Development",
                  "rationale": "This category includes codes related to the creation and implementation of new technologies in gaming, which is central to understanding technological impact."
                }},
                {{
                  "category_index": 6,
                  "category_label": "Economic Trends",
                  "rationale": "This category covers codes that discuss financial trends and economic factors affecting the gaming industry, crucial for analyzing economic impact."
                }}
            ]
        }}
    ]
}}
"""



# Deductive Theme Identification
ta_prompt4 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. At this phase, the purpose is to derive and develop preliminary themes deductively, guided by existing theoretical frameworks and aligned with the research questions or objectives. This means you should have a clear theoretical basis and research focus before examining the data to identify themes.

Guidelines:
1. Use a deductive approach to develop themes. Start with existing theoretical frameworks, pre-existing concepts, established themes, and relevant literature or research. Ensure these frameworks and concepts guide your theme development.
2. Consider the research questions or objectives when developing the themes. Align the themes with these questions or objectives to maintain focus and relevance.
3. Examine the data to identify themes that fit the theoretical frameworks and address the research questions or objectives. Look for patterns, concepts, and insights that support the predefined themes.
4. Aim to identify between 3 to 8 themes, but be flexible if the data justifies more or fewer themes. Provide a general summary of all identified themes.
5. Document the rationale and references for each theme. Include the existing theory/framework and relevant literature that support each theme. This helps in validating the themes and linking them to established knowledge.
6. Summarize the identified themes, including how they are derived from the data and their relevance to the research questions or objectives.

For each theme, provide:
- Theme name in 1-4 words (maximum 5 words)
- A meaningful and compact definition of the theme with 2-10 sentences to describe the most significant properties, purpose, and what are the requirements for a specific topic or content to be identified as a theme
- References to and reasoning for relevant theoretical frameworks, pre-existing concepts, established themes, and/or relevant literature or research, including specific studies or sources that support the theme
- A description of the theme and its relevance to the research questions or objectives


Truncated example of the JSON output:
{{
    "Themes": [
        {{
            "name": "Organic Farming",
            "definition": "This theme explores practices and principles related to organic farming. It includes methods such as crop rotation, green manure, compost, and biological pest control. Requirements for this theme include a focus on natural processes and sustainability in farming.",
            "references": "According to the USDA (2020), organic farming enhances biodiversity and soil health. The book 'The Organic Farming Manual' by Ann Larkin Hansen provides comprehensive techniques. Insights from organic farming communities on forums like permies.com also support this theme.",
            "description": "This theme is relevant to understanding sustainable farming practices and their impact on the environment."
        }},
        {{
            "name": "Agroforestry Systems",
            "definition": "This theme examines the integration of trees and shrubs into agricultural landscapes. It covers practices like alley cropping, silvopasture, and forest farming. Requirements for this theme include a focus on combining agriculture and forestry to create sustainable land-use systems.",
            "references": "The FAO (2018) report on Agroforestry Systems highlights benefits for biodiversity and carbon sequestration. The concept is extensively discussed in the book 'Agroforestry: Practices and Benefits' by H.E. Garrett. Online discussions in the Agroforestry Research Trust community also provide practical insights.",
            "description": "This theme is crucial for exploring how integrating trees into agricultural systems can enhance sustainability and productivity."
        }},
        {{
            "name": "Water Management",
            "definition": "This theme addresses efficient water use and conservation techniques in agriculture. It includes irrigation methods, rainwater harvesting, and drought-resistant crop varieties. Requirements for this theme include a focus on optimizing water use to ensure sustainability.",
            "references": "The 2019 UN Water Report provides guidelines on sustainable water management. The book 'Water for Every Farm' by Yeomans discusses key principles and methods. Discussions on water conservation forums like the 'Water Sustainability Network' also contribute valuable insights.",
            "description": "This theme is relevant to ensuring that water resources are managed efficiently to support sustainable agricultural practices."
        }}
    ]
}}
"""



# Theme Review and Refinement
ta_prompt5 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. Below between *** is a set of top-down driven (deductive) themes derived from the research questions, objectives, and relevant theoretical frameworks or other existing information.

***
{response4_json}
***

You are requested to merge these top-down driven themes with the themes that you created in your previous message to form a coherent set of final themes.

Guidelines:
1. Review both sets of themes (your previous answer and the top-down themes) thoroughly.
2. Combine the themes from both sets to form a comprehensive set of final themes that encompass insights and findings from both approaches.
3. Identify any overlapping or closely related themes within the combined set. Merge overlapping and closely related themes to create unified themes that capture the essence of the combined insights. Consider the definitions, descriptions, and findings from both the top-down driven approach and your derived themes from categories and lower level codes to ensure the unified themes accurately represent the comprehensive data.
4. Retain any unique themes from both sets that do not overlap.
5. Ensure that the merged themes are distinct, comprehensive, and accurately represent the data. The merged themes should be relevant to the research questions or objectives and informed by theoretical frameworks.
6. Provide a meaningful and compact definition for each final theme, detailing the most significant properties, purpose, and requirements for a specific topic or content to be identified as a theme.
7. Document the rationale for each theme, including references to relevant theoretical frameworks, pre-existing concepts, established themes, and/or relevant literature or research.
8. Provide a description for each final theme, explaining its relevance to the research questions or objectives and the data.

For each theme, provide:
- Index number
- Theme name in 1-4 words (maximum 5 words)
- A meaningful and compact definition of the theme with 2-10 sentences to describe the most significant properties, purpose, and what are the requirements for a specific topic or content to be identified as a theme
- References to and reasoning for relevant theoretical frameworks, pre-existing concepts, established themes, and/or relevant literature or research, including specific studies or sources that support the theme
- A description of the theme and its relevance to the research questions or objectives

Truncated example of the JSON output:
{{
    "Themes": [
        {{
            "index": 1,
            "name": "Physical Fitness",
            "definition": "This theme explores the various aspects of physical fitness, including strength, endurance, flexibility, and cardiovascular health. It encompasses different types of physical activities and exercises that contribute to overall fitness. Requirements for this theme include a focus on the components and benefits of physical fitness.",
            "references": "The World Health Organization (WHO) guidelines on physical activity and sedentary behavior provide comprehensive insights. The book 'Fitness and Health' by Brian Sharkey and Steven Gaskill discusses the science behind fitness. In our recent study on community fitness programs, we observed that participants engaging in 30-minute daily workouts showed a 20% improvement in cardiovascular health.",
            "description": "This theme is relevant to understanding the key components of physical fitness and how different exercises contribute to overall health."
        }},
        {{
            "index": 2,
            "name": "Exercise Psychology",
            "definition": "This theme examines the psychological aspects of exercise, including motivation, mental health benefits, and adherence to exercise programs. It covers the role of exercise in reducing stress, anxiety, and depression. Requirements for this theme include a focus on the mental and emotional impacts of regular physical activity.",
            "references": "The journal 'Psychology of Sport and Exercise' provides numerous studies on the psychological benefits of exercise. Insights from the 'Couch to 5K' program community highlight real-world experiences. Our study on group fitness classes found that 85% of participants reported significantly reduced stress levels after just eight weeks.",
            "description": "This theme helps to understand the psychological benefits of exercise and the factors that motivate individuals to maintain an active lifestyle."
        }},
        {{
            "index": 3,
            "name": "Nutrition and Performance",
            "definition": "This theme explores the relationship between nutrition and athletic performance. It includes the role of macronutrients, micronutrients, and hydration in supporting physical activity and enhancing performance. Requirements for this theme include a focus on dietary strategies and their impact on fitness outcomes.",
            "references": "The book 'Nutrient Timing' by John Ivy and Robert Portman explains how nutrition affects athletic performance. The International Journal of Sport Nutrition and Exercise Metabolism publishes relevant research. In our longitudinal study on elite athletes, those who followed personalized nutrition plans improved their performance metrics by 15%.",
            "description": "This theme is important for exploring how proper nutrition supports athletic performance and overall fitness goals."
        }}
    ]
}}
"""


# Assign Categories to Themes
ta_prompt6 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. Below between *** are the categories you previously created.

***
{response2_json}
***

Review the categories you previously created and assign them to the appropriate final themes that you created in your last message.

Guidelines:
1. Assign previously created categories to the final themes. In this assignment, consider the alignment of categories with the definitions, purposes, and properties of the themes. Ensure that the categories accurately reflect the key aspects of the themes they are assigned to.
2. Refactor categories based on the data and research questions or objectives if needed. Refactoring can include merging similar categories, splitting broad categories, or creating new categories based on emerging patterns. Add new categories if they better capture the data's meaning. Remove redundant categories that cannot be assigned to any themes.
3. One category can belong to more than one theme. Ensure that the retained categories are distinct, comprehensive, and accurately represent the data.
4. Ensure that each category is supported by data segments and aligns with the overall objectives and research questions. This alignment will help in maintaining the integrity and focus of the analysis.
5. Provide a brief description for each category, explaining its relevance to the theme. Include details about the category's definition, requirements, and relevance.

For each theme, provide:
- Index number
- Theme name

For each category, provide:
- Index starting from 1
- Category name in 1-4 words (max 5 words)
- A meaningful and compact definition of the category with 2-10 sentences to describe the most significant properties, purpose, and what are the requirements for a specific topic/content to be identified as a category
- A description of the category's relevance to the research questions or objectives
- The requirements and relevance for this category to belong to this theme / these themes

Truncated example of the JSON output:
{{
    "Themes and Categories": [
        {{
            "theme_index": 1,
            "theme_name": "Software Development",
            "categories": [
                {{
                    "category_index": 1,
                    "category_label": "Agile Practices",
                    "definition": "This category includes practices and methodologies that fall under the Agile framework, such as Scrum, Kanban, and Extreme Programming (XP). These practices emphasize iterative development, collaboration, and customer feedback to improve software quality and responsiveness.",
                    "description": "This category is relevant to understanding how Agile methodologies impact the efficiency and flexibility of software development processes, and how they contribute to the rapid delivery of high-quality software.",
                    "requirements_relevance": "To belong to this category, practices must demonstrate iterative development, continuous feedback, and adaptive planning. This category aligns with the theme of software development as it highlights methods that enhance productivity and adaptability in software projects."
                }},
                {{
                    "category_index": 17,
                    "category_label": "Version Control",
                    "definition": "This category covers the use of version control systems like Git, SVN, and Mercurial, focusing on their role in managing code changes, facilitating collaboration, and maintaining the integrity of the codebase. It includes practices such as branching, merging, and pull requests.",
                    "description": "Version control is crucial for tracking changes, facilitating collaboration among developers, and maintaining the integrity and history of the codebase.",
                    "requirements_relevance": "To belong to this category, tools and practices must involve systematic tracking of code changes, support for collaborative development, and mechanisms for resolving conflicts. This category is essential for the software development theme as it ensures that code is consistently and accurately managed throughout the development lifecycle."
                }}
            ]
        }},
        {{
            "theme_index": 2,
            "theme_name": "Data Science",
            "categories": [
                {{
                    "category_index": 2,
                    "category_label": "Machine Learning",
                    "definition": "This category encompasses techniques and algorithms used in machine learning, including supervised learning (e.g., linear regression, classification), unsupervised learning (e.g., clustering, dimensionality reduction), and reinforcement learning. It covers the entire process from data preprocessing to model evaluation and deployment.",
                    "description": "Machine learning is essential for creating predictive models and automating data-driven decision-making. It involves the application of statistical techniques to learn patterns from data and make predictions.",
                    "requirements_relevance": "To be included in this category, methods must involve the application of algorithms that allow systems to learn and improve from experience. This category supports the data science theme by providing the foundation for predictive analytics and intelligent data processing."
                }},
                {{
                    "category_index": 15,
                    "category_label": "Data Visualization",
                    "definition": "This category includes tools and techniques for visualizing data, such as charts, graphs, and dashboards, to communicate insights effectively. It encompasses principles of design, user experience, and the use of software like Tableau, Power BI, and D3.js.",
                    "description": "Data visualization is key to interpreting complex data and presenting findings in an accessible way. It helps stakeholders understand data patterns and insights through visual representation.",
                    "requirements_relevance": "To belong to this category, techniques must transform raw data into visual formats that highlight key trends and insights. This category is crucial for the data science theme as it enables effective communication of data findings to both technical and non-technical audiences."
                }}
            ]
        }}
    ]
}}
"""




# Assign Codes to Categories
ta_prompt7 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. Below between *** are the initial codes you previously created.

***
{response1_json}
***

Review the initial codes and assign them to the appropriate final categories.

Guidelines:
1. Assign initial codes to the appropriate final categories. Consider the alignment of codes with the definitions, purposes, and properties of the categories. Ensure that the codes accurately reflect the key aspects of the categories they are assigned to.
2. Merge codes that are very similar into a single, more comprehensive code (do this sparingly). You can change code names but not the underlying meaning/feature/description. Remove redundant codes that do not belong to any category.
3. One code can belong to more than one category if relevant. Ensure that the retained codes are distinct, comprehensive, and accurately represent the data.
4. Ensure each code is supported by data segments and aligns with the overall objectives and research questions. This alignment will help maintain the integrity and focus of the analysis.
5. Provide a brief description for each code, explaining its relevance to the category. Include details about the code's definition, relevance to the research questions, and a descriptive quote.

For each category, provide:
- Category number
- Category name

For each code, provide:
- Index starting from 1
- Code name in 1-5 words
- A meaningful and compact definition of the code with 2-10 sentences to describe the most significant properties, purpose, and how it differs from other similar features or codes
- A description of the code's relevance to the research questions or objectives
- A descriptive quote from some respondent that exemplifies the code


Truncated example of the JSON output:
{{
    "Categories and Codes": [
        {{
            "category_index": 1,
            "category_name": "Problem Solving Skills",
            "codes": [
                {{
                    "code_index": 73,
                    "code_name": "Critical Thinking Analysis",
                    "definition": "This code refers to the ability to analyze information objectively and make a reasoned judgment. Critical thinking involves the evaluation of data and arguments, recognizing biases, and constructing logical arguments.",
                    "description": "Critical thinking is essential for problem-solving as it allows individuals to approach complex issues methodically and make informed decisions.",
                    "quote": "When I face a problem at work, I always try to break it down into smaller parts and analyze each aspect carefully."
                }},
                {{
                    "code_index": 89,
                    "code_name": "Innovative Creative Solutions",
                    "definition": "This code captures instances where individuals generate innovative and effective solutions to problems. It involves thinking outside the box and applying unconventional methods to find answers.",
                    "description": "Creative solutions are important for overcoming obstacles that do not have clear or traditional solutions, demonstrating flexibility and resourcefulness.",
                    "quote": "I love brainstorming sessions because they often lead to unexpected and creative solutions that we wouldn't have thought of otherwise."
                }}
            ]
        }},
        {{
            "category_index": 2,
            "category_name": "Online Friendships",
            "codes": [
                {{
                    "code_index": 41,
                    "code_name": "Digital Social Networking",
                    "definition": "This code refers to the use of online platforms to build and maintain friendships. It includes interactions on social media, forums, and other digital communication tools.",
                    "description": "Social networking is crucial for understanding how people form and sustain relationships in the digital age, impacting both social dynamics and personal connections.",
                    "quote": "I've met some of my closest friends through online gaming communities. We talk every day even though we live in different countries."
                }},
                {{
                    "code_index": 82,
                    "code_name": "Virtual Emotional Support",
                    "definition": "This code encompasses the emotional and practical support individuals receive from their online friends. It includes instances of advice, encouragement, and assistance provided through digital means.",
                    "description": "Virtual support highlights the importance of online friendships in providing emotional and practical help, demonstrating the value of digital connections.",
                    "quote": "When I was going through a tough time, my friends from an online forum were there for me, offering advice and cheering me up."
                }}
            ]
        }}
    ]
}}
"""


# Producing the Report
ta_prompt8 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. You are requested to create a comprehensive report that synthesizes and presents the findings from the analyzed data.

Guidelines:
1. Analyze the final themes, categories, and codes to draw conclusions related to the research questions or objectives. Highlight key findings and insights for interpretation.
2. Present each theme with definitions, descriptions, illustrative quotes, and identified relationships to other themes. Ensure that the presentation is clear and cohesive, demonstrating how each theme contributes to the overall understanding of the research topic.
3. For all themes combined, provide a joint summary, description, analysis, interpretation, reflection, and narrative. This should include insights on how the themes interrelate and contribute to answering the research questions or objectives.
4. Review the dataset to ensure that all data segments are coded correctly under the final themes, categories, and codes. Flag any segments that are not sufficiently covered, misclassified, or missing critical information related to themes, categories, and/or codes. Identify patterns, relationships, and insights, and suggest any potential sub-themes.
5. Synthesize the findings from each of the analyzed themes. Integrate these insights to answer the research questions or objectives and explain how the themes interrelate and contribute to the overall understanding of the research topic.

The output should include:
- Presentation of each theme with definitions, descriptions, illustrative quotes, and identified relationships to other themes
- A joint summary, description, analysis, interpretation, reflection, and narrative for all themes combined
- A concise title for the summary that captures the essence of the findings in up to 10 words
- A description in two sentences covering the main insights from the themes and groups
- Flagged segments that are not sufficiently covered, misclassified, or missing critical information related to themes, categories, and/or codes
- Analysis and interpretation of findings (consider also the relation to the research questions or objectives)
- Conclusions and implications (consider also the relation to the research questions or objectives)
- Reflection on how well the analysis addresses the original research questions or objectives
- Narrative to provide a coherent and engaging story of the findings

Truncated example of the JSON output:
{{
    "Themes": [
        {{
            "name": "Innovation and Creativity",
            "quotes": "Design thinking has unleashed our team's creativity. ||| We came up with innovative solutions we hadn't considered before. ||| Our brainstorming sessions have become much more productive.",
            "definition": "This theme explores how design thinking fosters innovation and creativity within the workplace.",
            "description": "Design thinking encourages out-of-the-box thinking, leading to unique and innovative solutions.",
            "relationship": "This theme is related to 'Collaboration and Teamwork' as creative ideas often emerge from collaborative efforts.",
            "analysis": "Design thinking significantly enhances creativity and innovation by promoting an open-minded approach to problem-solving.",
            "conclusions": "Implementing design thinking can drive innovation and creative problem-solving within teams. This conclusion aligns with the research objective to understand the impact of design thinking on workplace innovation."
        }},
        {{
            "name": "Collaboration and Teamwork",
            "quotes": "Our team collaboration has improved since adopting design thinking. ||| We are more open to each other's ideas and feedback. ||| Teamwork has become more seamless and efficient.",
            "definition": "This theme focuses on the role of design thinking in enhancing collaboration and teamwork among employees.",
            "description": "Design thinking promotes a collaborative environment where team members feel valued and heard.",
            "relationship": "This theme is related to 'Innovation and Creativity' as collaborative efforts are essential for fostering creative solutions. It is also related to 'Problem-Solving Efficiency' because improved teamwork leads to more effective problem resolution.",
            "analysis": "Design thinking fosters a collaborative culture that enhances teamwork and collective problem-solving.",
            "conclusions": "Adopting design thinking practices improves collaboration and teamwork, contributing to overall workplace efficiency. This conclusion addresses the research question on the benefits of design thinking for team dynamics."
        }}
    ],
    "Overall Findings": {{
        "summary_title": "Key Insights on Design Thinking in the Workplace",
        "description": "This study explores the impact of design thinking on workplace innovation, collaboration, and problem-solving.",
        "flagged_segments": "The segment 'Design thinking has streamlined our workflow' is not sufficiently covered, which could provide new insights if properly categorized. ||| The segment 'We struggle with applying design thinking principles consistently' appears to be miscategorized under 'Innovation and Creativity' when it might fit better under 'Challenges and Barriers'. ||| The segment 'Design thinking has made our meetings more engaging' is missing critical information on specific methods used.",
        "analysis_and_interpretation": "The themes collectively highlight how design thinking enhances innovation, collaboration, and problem-solving in the workplace. These findings directly address the research questions regarding the benefits and challenges of implementing design thinking.",
        "conclusions_and_implications": "The study concludes that while design thinking offers significant benefits for innovation and teamwork, there are also challenges in its consistent application. These conclusions align with the research objectives to understand the overall impact of design thinking in a workplace setting.",
        "reflection": "The analysis addresses the original research questions by exploring key areas such as innovation, collaboration, and problem-solving. However, some segments require further review to ensure complete coverage and to enhance the reliability and validity of the findings.",
        "narrative": "This report tells the story of how design thinking transforms workplace dynamics, from fostering creativity and innovation to improving teamwork and collaboration. By combining the experiences of employees with research insights, the narrative illustrates the profound impact of design thinking on modern work environments."
    }}
}}
"""




