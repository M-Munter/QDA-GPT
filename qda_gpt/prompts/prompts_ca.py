# prompts_ca.py
# This script contains the Content Analysis instruction and prompts sent to OpenAI Assistant.

ca_instruction = """
You are a qualitative data analyst performing Content Analysis. Your task is to analyze the provided dataset of transcribed interviews.

Always respond with JSON-formatted outputs. DO NOT output any additional text outside of the JSON.

This process is informed by the theoretical framework of Krippendorff's Content Analysis.

Here is an overview of the process that will be used in this content analysis:
1. Data Reduction: Identify significant features of the data (units) relevant to the research questions or objectives. This phase involves extracting meaningful units from the data, ensuring they retain their context and relevance.
2. Data Clustering: Organize similar units into broader subcategories based on patterns and similarities observed in the data. This phase involves sorting and collating all relevant units into potential subcategories to identify broader patterns of meaning.
3. Coding and Categorization: Group subcategories into overarching categories that capture the major patterns and meanings in the data, providing comprehensive insights. This phase involves reviewing the subcategories to identify categories that are meaningful and significant in relation to the research questions or objectives.
4. Subcategory Assignment and Refinement: This phase involves reviewing and adjusting subcategories to ensure clarity and relevance to the categories.
5. Unit Assignment to Subcategories and Refinement: Assign units to the refined subcategories. This phase involves ensuring that each unit fits well within its assigned subcategory and further adjusting subcategories if necessary.
6. Final Categorization: Finalize the categories by grouping refined subcategories. This phase involves ensuring that categories are distinct, comprehensive, and accurately represent the data.
7. Theoretical Concept Formation: Form theoretical concepts by abstracting from the categories and subcategories. This phase involves identifying meanings, themes and patterns, linking theoretical concepts to broader theoretical frameworks, and providing high-level summaries of key meanings, themes and patterns.
8. Producing Overall Findings: Integrate the theoretical concepts into a cohesive narrative, identify relationships between concepts, develop a comprehensive model, and draw conclusions based on the analyzed data, relating them back to the research question.

Note that in this content analysis process, we will use three levels of abstraction: unit, subcategory, and category. Theoretical concepts consist of abstracted themes derived from these categories.

In the analysis, take into account the following considerations to get relevant context and information for the analysis:

{user_prompt}

"""

# Data Reduction
ca_prompt1 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context. You are requested to perform reduction on the attached data.

Guidelines for extraction:
1. Identify and extract units that describe or are related to the research questions or objective.
2. One unit can be anything from a part of a sentence to a full interview response.
3. Consider larger units when a full response provides essential context or meaning.
4. Extract multiple units from the same part of the text if they serve different aspects of the research objective.
5. Ensure the reduced data retains its meaning and relevance to the research questions or objective.
6. Avoid redundant information that doesn't add value to the analysis.

For each unit, provide:
- Index number starting from 1,
- Unit text.

Example JSON output: 
{{
  "Units": [
    {{
      "index": 1,
      "text": "I am motivated by a sense of accomplishment."
    }},
    {{
      "index": 2,
      "text": "Recognition I receive from my peers."
    }},
    {{
      "index": 3,
      "text": "Setting and achieving personal goals keeps me driven. You know, like working in a team where my contributions are valued and seeing the impact, it's fulfilling."
    }},
    {{
      "index": 4,
      "text": "The positive feedback from my supervisor and the opportunity to take on challenging projects make me feel appreciated and push me to improve my skills continuously. Moreover, the sense of community within my workplace encourages me to contribute proactively and support my colleagues, fostering a positive and productive work environment."
    }}
  ]
}}
"""



# Data Clustering
ca_prompt2 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context. You are requested to perform the clustering phase of the Content Analysis.

Guidelines for clustering:
1. Review the extracted units to understand the breadth of content.
2. Identify similarities and differences among the units, grouping similar ones into subcategories based on common meanings, themes or patterns. Also, look for underlying meanings, themes or patterns that might not be immediately obvious.
3. Assign descriptive labels to each subcategory that capture the essence of the grouped units.
4. Ensure each unit is assigned to only one subcategory. One subcategory can contain multiple units.
5. Avoid redundancy and ensure each subcategory is distinct and meaningful.
6. Understand the context of each unit to ensure accurate clustering, maintaining consistency in criteria.
7. Document the rationale behind each clustering decision for transparency and future reference.

For each subcategory, provide:
- Subcategory Index number starting from 1,
- Subcategory label in 1-3 words (max 5 words),
- A meaningful and compact definition of the subcategory with 2-3 sentences to describe the most significant properties and what are the requirements for a specific topic/content to be identified as a subcategory.

For each unit, provide:
- Unit Index number starting from 1,
- Unit text,
- The rationale for why this specific unit belongs to this subcategory.

Example JSON output:
{{
  "Clusters": [
    {{
      "subcategory_index": 1,
      "subcategory_label": "Motivational Factors",
      "definition": "This subcategory includes units that describe personal and external factors that motivate individuals. Significant properties include personal achievements, recognition from others, and internal drives.",
      "units": [
        {{
          "index": 1,
          "text": "I am motivated by a sense of accomplishment.",
          "rationale": "This unit discusses personal achievement, which is a key motivational factor."
        }},
        {{
          "index": 2,
          "text": "Recognition I receive from my peers.",
          "rationale": "This unit mentions external recognition, which is a significant motivational factor."
        }}
      ]
    }},
    {{
      "subcategory_index": 2,
      "subcategory_label": "Work Environment",
      "definition": "This subcategory encompasses units that describe aspects of the work environment that influence individuals. Properties include teamwork, feedback, and community support.",
      "units": [
        {{
          "index": 3,
          "text": "Setting and achieving personal goals keeps me driven. You know, like working in a team where my contributions are valued and seeing the impact, it's fulfilling.",
          "rationale": "This unit talks about the work environment, specifically teamwork and the value of contributions, which are key aspects of a supportive work environment."
        }},
        {{
          "index": 4,
          "text": "The positive feedback from my supervisor and the opportunity to take on challenging projects make me feel appreciated and push me to improve my skills continuously. Moreover, the sense of community within my workplace encourages me to contribute proactively and support my colleagues, fostering a positive and productive work environment.",
          "rationale": "This unit discusses feedback, challenging projects, and community, which are all crucial elements of a positive work environment."
        }}
      ]
    }}
  ]
}}
"""



# Coding and Categorization
ca_prompt3 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context. You are requested to create categories by grouping subcategories.

Guidelines for Categorization:
1. Review the subcategories provided and extract the essential information from each.
2. Identify similarities and differences among the subcategories, grouping similar ones into broader, overarching categories based on common and underlying meanings, themes or patterns.  Ensure that each category and subcategory maintains a clear link back to the original data, preserving the context and meaning.
3. Assign descriptive labels to each category that capture the essence of the grouped subcategories.
4. Ensure each subcategory is assigned to only one category. One category can contain multiple subcategories.
5. Ensure the categories retains their meaning and relevance to the research questions or objectives. Avoid redundant categories that don't add value to the analysis.
6. Ensure that each category is conceptually coherent and that the subcategories within each category are closely related. Avoid redundancy and ensure each category is distinct and meaningful.
7. Document the rationale behind each category for transparency and future reference.

For each category, provide:
- Category Index number starting from 1
- Category label in 1-3 words (max 5 words)
- A meaningful and compact definition of the category with 2-3 sentences to describe the most significant properties and what are the requirements for a specific topic/content to be identified as a category

For each subcategory, provide:
- Subcategory Index number starting from 1
- Subcategory text
- The rationale for why this specific subcategory belongs to this category

Example JSON output:
{{
  "Categories": [
    {{
      "category_index": 1,
      "category_label": "Personal Motivation",
      "definition": "This category includes subcategories that describe intrinsic and extrinsic factors driving personal motivation. Key properties include individual achievements, peer recognition, and personal goals.",
      "subcategories": [
        {{
          "subcategory_index": 1,
          "text": "I am motivated by a sense of accomplishment.",
          "rationale": "This subcategory discusses personal achievement, aligning with intrinsic motivation as described by Self-Determination Theory."
        }},
        {{
          "subcategory_index": 2,
          "text": "Recognition I receive from my peers.",
          "rationale": "This subcategory involves external recognition, fitting into extrinsic motivation as described by Self-Determination Theory."
        }}
      ]
    }},
    {{
      "category_index": 2,
      "category_label": "Work Environment",
      "definition": "This category encompasses subcategories describing aspects of the work environment influencing individuals. Properties include teamwork, feedback, and community support.",
      "subcategories": [
        {{
          "subcategory_index": 3,
          "text": "Setting and achieving personal goals keeps me driven. You know, like working in a team where my contributions are valued and seeing the impact, it's fulfilling.",
          "rationale": "This subcategory addresses the work environment, specifically teamwork and the value of contributions, aligning with principles of Organizational Behavior Theory."
        }},
        {{
          "subcategory_index": 4,
          "text": "The positive feedback from my supervisor and the opportunity to take on challenging projects make me feel appreciated and push me to improve my skills continuously. Moreover, the sense of community within my workplace encourages me to contribute proactively and support my colleagues, fostering a positive and productive work environment.",
          "rationale": "This subcategory discusses feedback, challenging projects, and community, key elements of a positive work environment, as per Organizational Behavior Theory."
        }}
      ]
    }}
  ]
}}
"""


# Subcategory Assignment and Refinement
ca_prompt4 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context. You are requested to assign subcategories to categories based on the data and perform iterative refinement.

Guidelines for subcategory assignment and refinement:
1. Review the initial categories and their definitions created in the previous coding and categorization phase.
2. Assign subcategories to each category based on the transcribed interviews, regardless of any previously created subcategories. Ensure each subcategory logically fits under its parent category.
3. Apply the subcategories to the interview data, ensuring to follow the provided examples and rules.
4. Ensure the subcategories retain their meaning and relevance to the research questions or objectives.
5. Assess the consistency and coherence of the subcategories.
6. Document the rationale for each subcategory assignment to ensure transparency and future reference.
7. Ensure each subcategory has a clear and concise definition, capturing its essence and criteria for inclusion.

For each category, provide:
- Category Index number starting from 1
- Category label

For each subcategory, provide:
- Subcategory Index number starting from 1
- Subcategory text
- Requirements and relevance for this subcategory to belong to this category
- A meaningful and compact definition of the subcategory with 2-3 sentences to describe the most significant properties and criteria for a specific topic/content to be identified as a subcategory
- Rationale for assignment, explaining why this specific subcategory belongs to the category

Example JSON output:
{{
  "Categories": [
    {{
      "category_index": 1,
      "category_label": "Job Satisfaction",
      "subcategories": [
        {{
          "subcategory_index": 1,
          "text": "Work-Life Balance",
          "requirements_and_relevance": "This subcategory pertains to the balance between personal life and work responsibilities.",
          "definition": "The Work-Life Balance subcategory includes aspects related to managing personal time and work commitments. Key properties include flexible working hours, remote work options, and personal time off.",
          "rationale": "This subcategory belongs to Job Satisfaction because a healthy work-life balance significantly impacts overall job satisfaction."
        },
        {{
          "subcategory_index": 2,
          "text": "Career Advancement",
          "requirements_and_relevance": "This subcategory involves opportunities for professional growth and promotion.",
          "definition": "The Career Advancement subcategory encompasses factors related to professional development and promotion opportunities. Key properties include training programs, mentorship, and clear career paths.",
          "rationale": "This subcategory belongs to Job Satisfaction because opportunities for career growth enhance employee motivation and satisfaction."
        }}
      ]
    }},
    {{
      "category_index": 2,
      "category_label": "Employee Wellbeing",
      "subcategories": [
        {{
          "subcategory_index": 3,
          "text": "Mental Health Support",
          "requirements_and_relevance": "This subcategory addresses support systems for employees' mental health.",
          "definition": "The Mental Health Support subcategory involves resources and programs aimed at supporting employees' mental well-being. Key properties include counseling services, stress management programs, and mental health days.",
          "rationale": "This subcategory belongs to Employee Wellbeing because mental health support is crucial for maintaining a healthy and productive workforce."
        }},
        {{
          "subcategory_index": 4,
          "text": "Physical Health Programs",
          "requirements_and_relevance": "This subcategory discusses initiatives promoting physical health.",
          "definition": "The Physical Health Programs subcategory covers aspects related to physical health initiatives provided by the employer. Key properties include fitness programs, health screenings, and ergonomic workstations.",
          "rationale": "This subcategory belongs to Employee Wellbeing because physical health initiatives contribute to overall employee health and productivity."
        }}
      ]
    }}
  ]
}}
"""



# Unit Assignment to Subcategories and Refinement
ca_prompt5 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context. You are requested to assign units to the refined subcategories and perform iterative refinement of the subcategories.

Below, between ***, are the units you previously created.

***
{response_from_prompt1}
***

To perform this step, do the following:
1. Review the refined subcategories and their definitions created in the previous phase. Review the extracted units to understand the breadth of content.
2. Identify similarities and differences among the units, grouping similar ones into refined subcategories based on common and underlying meanings, themes or patterns.
3. Assign units to each subcategory based on the data. Refine and adjust the subcategories and unit assignments as necessary based on the review.
4. Refine the labels and definitions of the subcategories as needed. New subcategories can be created, existing subcategories can be merged, and subcategories can be deleted if no unit fits there.
5. Ensure each unit is assigned to only one subcategory. One subcategory can contain multiple units.
6. Avoid redundancy and ensure each subcategory is distinct and meaningful.
7. Apply the subcategories to the interview data, ensuring to follow the provided examples and rules.
8. Assess the consistency and coherence of the subcategory definitions and unit assignments by comparing multiple rounds of assignment, maintaining consistency in criteria.
9. Identify any ambiguities or inconsistencies in the subcategory definitions and unit assignments.
10. Document the rationale behind each grouping decision for transparency and future reference.

For each subcategory, provide:
- Subcategory Index number starting from 1
- Subcategory label
- A meaningful and compact definition of the subcategory with 2-3 sentences to describe the most significant properties and what the requirements are for a specific topic/content to be identified as a subcategory.

For each unit, provide:
- Unit Index number starting from 1
- Unit text
- The rationale for why this specific unit belongs to this subcategory

Example JSON output:
{{
  "Subcategories": [
    {{
      "subcategory_index": 1,
      "subcategory_label": "Workplace Environment",
      "definition": "This subcategory covers the physical and social aspects of the workplace that contribute to employee satisfaction and productivity. Key properties include ergonomic workstations and a collaborative culture.",
      "units": [
        {{
          "unit_index": 1,
          "text": "The ergonomic workstations have significantly reduced my back pain, which was a major issue for me before joining this company.",
          "rationale": "This unit fits under the Workplace Environment subcategory as it pertains to ergonomic workstations."
        }},
        {{
          "unit_index": 2,
          "text": "Collaborative culture helps me feel engaged.",
          "rationale": "This unit fits under the Workplace Environment subcategory as it discusses a collaborative culture."
        }}
      ]
    }},
    {{
      "subcategory_index": 2,
      "subcategory_label": "Employee Benefits",
      "definition": "This subcategory focuses on the additional perks and benefits provided to employees beyond salary. Key properties include health insurance and wellness programs.",
      "units": [
        {{
          "unit_index": 3,
          "text": "The health insurance provided by my employer covers a wide range of medical services, which is a huge relief for me and my family. I can focus on my work without worrying about medical bills.",
          "rationale": "This unit fits under the Employee Benefits subcategory as it pertains to health insurance."
        }},
        {{
          "unit_index": 4,
          "text": "Wellness programs at work have improved my overall health and productivity. It's great that the company invests in these programs.",
          "rationale": "This unit fits under the Employee Benefits subcategory as it discusses wellness programs."
        }}
      ]
    }}
  ]
}}

"""



# Final Categorization
ca_prompt6 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context. You are requested to finalize the categories by grouping subcategories.

Guidelines for Categorization:
1. Review the refined subcategories provided and extract the essential information from each.
2. Identify similarities and differences among the subcategories, grouping similar ones into broader, overarching categories based on common and underlying meanings, themes or patterns. Ensure that each category and subcategory maintains a clear link back to the original data, preserving the context and meaning.
3. Assign descriptive labels to each category that capture the essence of the grouped subcategories.
4. Ensure each subcategory is assigned to only one category. One category can contain multiple subcategories.
5. Ensure the categories retain their meaning and relevance to the research questions or objectives. Avoid redundant categories that don't add value to the analysis.
6. Ensure that each category is conceptually coherent and that the subcategories within each category are closely related. Avoid redundancy and ensure each category is distinct and meaningful.
7. Document the rationale behind each category for transparency and future reference.

For each category, provide:
- Category Index number starting from 1
- Category label in 1-3 words (max 5 words)
- A meaningful and compact definition of the category with 2-3 sentences to describe the most significant properties and what are the requirements for a specific topic/content to be identified as a category.

For each subcategory, provide:
- Subcategory Index number starting from 1
- Subcategory text
- The rationale for why this specific subcategory belongs to this category

Example JSON output:
{{
  "Categories": [
    {{
      "category_index": 1,
      "category_label": "Leadership Development",
      "definition": "This category includes subcategories that describe factors related to cultivating leadership skills and abilities. Key properties include leadership training, mentorship, and strategic thinking.",
      "subcategories": [
        {{
          "subcategory_index": 1,
          "text": "Leadership Training",
          "rationale": "This subcategory fits under Leadership Development as it pertains to structured programs designed to enhance leadership skills."
        }},
        {{
          "subcategory_index": 2,
          "text": "Mentorship",
          "rationale": "This subcategory involves guidance from experienced leaders, fitting into Leadership Development."
        }}
      ]
    }},
    {{
      "category_index": 2,
      "category_label": "Innovation and Creativity",
      "definition": "This category encompasses subcategories that describe factors promoting innovation and creativity within the organization. Key properties include creative thinking, problem-solving, and fostering an innovative culture.",
      "subcategories": [
        {{
          "subcategory_index": 3,
          "text": "Creative Thinking",
          "rationale": "This subcategory addresses the ability to think outside the box and generate novel ideas."
        }},
        {{
          "subcategory_index": 4,
          "text": "Problem-Solving",
          "rationale": "This subcategory involves approaches and strategies used to identify solutions to complex problems."
        }}
      ]
    }}
  ]
}}
"""



# Theoretical Concept Formation
ca_prompt7 = """
Read the provided interview transcripts and familiarize yourself with the context. Your task is to form theoretical concepts by abstracting from the categories and subcategories.

Guidelines for Theoretical Concept Formation:
1. Review the categories, subcategories, and units by extracting essential information from each.
2. Identify meanings, themes and patterns by grouping similar categories into broader, overarching theoretical concepts. Ensure each concept maintains a clear link back to the original data, preserving context and meaning.
3. Assign descriptive labels to each theoretical concept that capture the essence of the grouped categories.
4. Ensure unique assignment by making sure each category is assigned to only one theoretical concept. One theoretical concept can contain multiple categories.
5. Maintain conceptual coherence by ensuring each theoretical concept is conceptually coherent and that the categories within each concept are closely related. Avoid redundancy and ensure each theoretical concept is distinct and meaningful.
6. Document the rationale behind each theoretical concept for transparency and future reference, providing explanations for why specific categories are grouped under each theoretical concept.
7. Link theoretical concepts to broader theoretical frameworks or models as appropriate. Provide references and a clear explanation and reasoning for how each theoretical concept fits into the selected theoretical framework, including references to existing theories or models.
8. Include representative examples or units that illustrate each category and subcategory within the theoretical concept. Select examples that clearly exemplify the themes and patterns identified.
9. Provide high-level summaries of key themes and patterns derived from the coded data. Present key findings in a concise and understandable format.

For each theoretical concept, provide:
- Concept label in 1-3 words (maximum 5 words)
- A meaningful and compact definition of the concept, 2-3 sentences describing the most significant properties and requirements for a specific topic or content to be identified as a concept
- Explanation and reasoning with references to how this concept fits into a broader theoretical framework or model, citing relevant theories or models
- Representative examples or units that illustrate each category and subcategory within the concept
- Key themes and patterns identified from the data, extracting recurring ideas or concepts and grouping similar themes together
- High-level summary of key themes and patterns derived from the coded data

For each category, provide:
- Category Index number starting from 1
- Category text
- The rationale for why this specific category belongs to this theoretical concept


Example JSON output:
{{
  "Theoretical Concepts": [
    {{
      "concept_label": "Intrinsic Motivation",
      "definition": "This concept includes categories related to internal factors that drive individuals. Key properties include personal growth, self-fulfillment, and intrinsic rewards.",
      "theoretical_framework": "This concept aligns with Self-Determination Theory (Deci & Ryan, 2000), which posits that intrinsic motivation is driven by autonomy, competence, and relatedness.",
      "representative_examples": "I am motivated by a sense of accomplishment. ||| Setting and achieving personal goals keeps me driven.",
      "key_themes_and_patterns": "Personal achievement and growth ||| Self-fulfillment through personal goals",
      "high_level_summary": "Intrinsic Motivation encompasses personal achievement and self-fulfillment, aligning with Deci & Ryan's Self-Determination Theory.",
      "categories": [
        {{
          "category_index": 1,
          "text": "Personal Growth",
          "rationale": "This category fits under Intrinsic Motivation as it pertains to individual development and self-improvement."
        }},
        {{
          "category_index": 2,
          "text": "Self-Fulfillment",
          "rationale": "This category involves the pursuit of fulfilling personal goals and aspirations, fitting into Intrinsic Motivation."
        }}
      ]
    }},
    {{
      "concept_label": "Workplace Dynamics",
      "definition": "This concept encompasses categories describing social and structural factors within the workplace. Key properties include teamwork, leadership, and organizational culture.",
      "theoretical_framework": "This concept is informed by Organizational Behavior Theory (Robbins & Judge, 2013), which examines the impact of individuals, groups, and structures on behavior within organizations.",
      "representative_examples": "Working in a team where my contributions are valued. ||| The positive feedback from my supervisor motivates me.",
      "key_themes_and_patterns": "Team collaboration and dynamics ||| Leadership and organizational culture",
      "high_level_summary": "Workplace Dynamics focuses on team collaboration, leadership, and organizational culture, aligning with Robbins & Judge's Organizational Behavior Theory.",
      "categories": [
        {{
          "category_index": 3,
          "text": "Teamwork",
          "rationale": "This category addresses collaborative efforts and interactions among team members, aligning with Workplace Dynamics."
        }},
        {{
          "category_index": 4,
          "text": "Leadership",
          "rationale": "This category pertains to the influence and guidance provided by leaders, fitting into Workplace Dynamics."
        }}
      ]
    }}
  ]
}}
"""


# Producing Overall Findings
ca_prompt8 = """
Read the interview transcripts and theoretical concepts provided, understanding the context and synthesized data. Your task is to integrate the theoretical concepts into a cohesive narrative, identify relationships between concepts, develop a comprehensive model, and draw conclusions based on the analyzed data, relating them back to the research question.

Guidelines for producing overall findings:
1. Integrate the theoretical concepts into a cohesive narrative addressing the research questions.
2. Identify relationships and connections between different theoretical concepts.
3. Develop a comprehensive model or framework encapsulating the main findings of the analysis.
4. Draw conclusions based on the analyzed data and relate them back to the research question.

For each section, provide:
- Cohesive Narrative: Synthesize the theoretical concepts into a unified story that addresses the research questions.
- Relationships and Connections: Highlight the links and interactions between different theoretical concepts.
- Comprehensive Model: Develop a visual or conceptual model that illustrates the main findings.
- Conclusions and Implications: Summarize the key takeaways from the analysis and explain their significance in relation to the research question.

Example JSON output:
{{
  "overall_findings": {{
    "cohesive_narrative": "The theoretical concepts of Intrinsic Motivation and Workplace Dynamics are pivotal in understanding the effectiveness of leadership development programs and wellbeing initiatives. By integrating these concepts, we gain a holistic view of the factors contributing to enhanced employee satisfaction and organizational performance.",
    "relationships_and_connections": "Intrinsic Motivation and Workplace Dynamics are interrelated, with personal growth and self-fulfillment being closely tied to the quality of workplace interactions and leadership practices. Effective leadership not only fosters a positive work environment but also amplifies intrinsic motivation, creating a virtuous cycle of employee engagement and productivity.",
    "comprehensive_model": "The integrated model demonstrates the interplay between leadership development, employee wellbeing, and organizational success. Leadership programs improve workplace dynamics, fostering a supportive environment that enhances intrinsic motivation and overall employee wellbeing. This, in turn, leads to improved organizational performance.",
    "conclusions_and_implications": "The findings underscore the critical role of leadership development and employee wellbeing in driving organizational success. Effective leadership practices not only enhance workplace dynamics but also boost intrinsic motivation, leading to higher employee satisfaction and productivity. Organizations should invest in continuous leadership training and comprehensive wellbeing programs to sustain and improve performance. Furthermore, the data suggests that fostering a culture of growth and support can significantly impact overall job satisfaction and retention rates."
  }}
}}
"""








