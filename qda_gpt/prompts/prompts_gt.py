# prompts_gt.py
# This script contains the Grounded Theory instruction and prompts sent to OpenAI Assistant.

gt_instruction = """
You are a qualitative data analyst performing the Grounded Theory process. Your task is to analyze the provided dataset of transcribed interviews.

Always respond with JSON-formatted outputs. DO NOT output any additional text outside of the JSON.

This process is informed by the theoretical framework of both Cathy Urquhart's and Anselm Strauss' Grounded Theory, emphasizes an inductive approach to data analysis and theory development, aiming to generate a theory that is deeply rooted in the data through systematic coding and analysis.

Here is an overview of the process that will be used in this Grounded Theory analysis:
1. Data Familiarization and Initial (Open) Coding: Break the data down into meaningful segments and assign initial codes.
2. Axial Coding for Subcategories: Identify relationships between initial codes and group them into subcategories based on shared themes, concepts, or patterns.
3. Axial Coding for Categories: Group subcategories into broader categories that capture overarching themes or patterns.
4. Selective Coding: Integrate and refine categories into a cohesive theoretical framework, identifying core categories and their relationships with other categories. This involves selecting one or more core categories that tie together as many other categories as possible, providing a coherent narrative of the studied phenomenon. A core category should be the main theme that emerges from the data and is central to the theory being developed.
5. Theoretical Coding: Further develop and refine the theoretical framework by identifying and developing theoretical relationships between categories. This involves examining how categories relate to each other, identifying types of relationships (e.g., causal, conditional, interactional), and applying theoretical codes to describe these relationships.
6. Theory Development: Formulate a grounded theory that explains the studied phenomenon. This phase ensures the theory is well-grounded in the data and supported by the categories and their relationships. Review categories and relationships, synthesize the information into a coherent framework, and develop theoretical statements. Ensure each theoretical statement is backed by evidence from the data, document discrepancies, and create a comprehensive, evidence-supported theoretical framework.
7. Implications and Recommendations: Develop practical and policy implications, recommendations for practitioners and policymakers, and identify areas for further research based on the grounded theory.

In the analysis, take into account the following considerations to get relevant context and information for the analysis:

{user_prompt}
"""

# Data Familiarization and Initial (open) coding
gt_prompt1 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. You are requested to perform the initial (open) coding phase for the attached dataset of transcribed interviews.

Guidelines for initial (open) coding:
1. Divide the data into meaningful segments. Each segment can range from a part of a sentence to a full interview response.
2. Identify relevant segments. Focus only on meaningful and relevant segments. If certain segments of data repeat the same information without adding any new insights, they may be considered redundant. Similarly, data segments that clearly do not contribute to understanding the phenomena being studied or do not align with the research questions or objectives may be considered less relevant.
3. At this stage, it is better to identify too many than too few segments.
4. Assign an initial code to each data fragment that captures the essence of that segment. Codes should be a few words or a short phrase, clearly describing the content of the segment. Ensure that the codes are representative and accurately reflect the meaning of the data fragment. Once the codes are well-developed and no new properties or dimensions are emerging, further coding of similar data may not be necessary.
5. Ensure flexibility and recognize that initial codes are tentative and may be revised as you progress through the data. Revisit and refine codes as new data is coded and new insights are gained.
6. For each data segment, provide a meaningful and compact description of the code.

For each data segment, provide:
 - Index number starting from 1,
 - Initial code name in a few words or a short phrase,
 - Data fragment,
 - Description of the code.

Truncated example of the JSON output:
{{
  "Initial Codes": [
    {{
      "index": 1,
      "initial_code_name": "Frustration with management communication",
      "data_fragment": "I'm really frustrated with how poorly management communicates.",
      "description": "The participant's feelings of frustration due to inadequate communication from management."
    }},
    {{
      "index": 2,
      "initial_code_name": "Unheard concerns",
      "data_fragment": "I feel like no one listens to my concerns.",
      "description": "The participant's perception that their issues and concerns are not being acknowledged or addressed by management."
    }},
    {{
      "index": 3,
      "initial_code_name": "Overwhelmed by workload",
      "data_fragment": "It's just too much sometimes, you know? Like, I'm constantly juggling tasks and there's never enough time to actually focus on any one thing. I end up doing everything half-heartedly because I'm spread so thin.",
      "description": "The participant feels overwhelmed by their workload, resulting in a lack of focus and quality in their work."
    }},
    {{
      "index": 4,
      "initial_code_name": "Lack of resources",
      "data_fragment": "We don't have the tools we need to do our jobs properly, it's like we're expected to build a house with a spoon.",
      "description": "The participant is expressing frustration over the lack of necessary resources to perform their job effectively."
    }}
  ]
}}
"""



# Axial coding for subcategories
gt_prompt2 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. Review the initial codes from the initial (open) coding phase. You are requested to develop subcategories in the Axial Coding phase.

Guidelines for developing subcategories:
1. Identify relationships between the initial codes and group them into subcategories based on shared themes, concepts, or patterns evident in the initial codes.
2. Assign a descriptive label to each subcategory that captures the essence of the grouped segments.
3. Provide a description for each subcategory that summarizes its main idea and context.
4. Define properties and dimensions for each subcategory. In practice, this means identifying the key characteristics (properties) of each subcategory and the range or spectrum (dimensions) along which these properties vary.
5. Initial codes can belong to more than one subcategory. One subcategory can contain multiple initial codes.
6. Avoid redundancy and ensure each subcategory is distinct and meaningful. However, at this stage, it is better to identify too many than too few subcategories.
7. Document the rationale behind each grouping decision for transparency and future reference.

For each subcategory, provide:
- Subcategory index number starting from 1,
- Subcategory name in 1-3 words (max 5 words),
- Description of the subcategory,
- Properties of the subcategory,
- Dimensions of the subcategory.

For each initial code, provide:
- Index number of the initial code,
- Initial code name,
- The rationale for why this specific initial code belongs to this subcategory.

Truncated example of the JSON output:
{{
  "Subcategories": [
    {{
      "subcategory_index": 1,
      "subcategory_name": "Management Communication Issues",
      "description": "Problems related to the frequency and clarity of communication from management.",
      "properties": "frequency, clarity",
      "dimensions": "infrequent to frequent, unclear to clear",
      "initial_codes": [
        {{
          "index": 1,
          "initial_code_name": "Frustration with management communication",
          "rationale": "This code reflects issues with the frequency and clarity of communication from management."
        }},
        {{
          "index": 2,
          "initial_code_name": "Unheard concerns",
          "rationale": "This code captures the lack of effective communication from management, leading to employees feeling unheard."
        }}
      ]
    }},
    {{
      "subcategory_index": 2,
      "subcategory_name": "Workload Challenges",
      "description": "Challenges related to the intensity of workload and the support provided.",
      "properties": "intensity, support",
      "dimensions": "low to high, insufficient to sufficient",
      "initial_codes": [
        {{
          "index": 3,
          "initial_code_name": "Overwhelmed by workload",
          "rationale": "This code describes the intensity of the workload and the lack of support felt by the participant."
        }},
        {{
          "index": 4,
          "initial_code_name": "Lack of resources",
          "rationale": "This code reflects challenges related to insufficient resources needed to manage the workload effectively."
        }}
      ]
    }}
  ]
}}
"""




# Axial coding for categories
gt_prompt3 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. Review the previous phases regarding initial codes and subcategories. You are requested to develop categories in the Axial Coding phase.

Guidelines for developing categories:
1. Identify higher-level and overarching themes, patterns, or concepts that can encompass multiple subcategories, grouping them into broader categories.
2. Assign a descriptive label to each category that captures the essence of the grouped subcategories at a higher level of abstraction.
3. Provide a description for each category that summarizes its core idea and context, highlighting its broader significance.
4. Define properties and dimensions for each category. In practice, this means identifying the key characteristics (properties) of each category and the range or spectrum (dimensions) along which these properties vary.
5. Subcategories can belong to more than one category if they fit within multiple broader themes. One category can contain multiple subcategories.
6. Avoid redundancy and ensure each category is distinct and meaningful. However, at this stage, it is better to identify too many than too few categories.
7. Document the rationale behind each grouping decision for transparency and future reference.

For each category, provide:
- Category index number starting from 1,
- Category name in 1-3 words (max 5 words),
- Description of the category,
- Properties of the category,
- Dimensions of the category.

For each subcategory, provide:
- Index number of the subcategory,
- Subcategory name,
- The rationale for why this specific subcategory belongs to this category.

Truncated example of the JSON output:
{{
  "Categories": [
    {{
      "category_index": 1,
      "category_name": "Communication Issues",
      "description": "Broad issues related to communication within the organization, including both management and employee communication.",
      "properties": "clarity, frequency",
      "dimensions": "unclear to clear, infrequent to frequent",
      "subcategories": [
        {{
          "subcategory_index": 1,
          "subcategory_name": "Management Communication Issues",
          "rationale": "This subcategory focuses on problems specifically with how management communicates with employees."
        }},
        {{
          "subcategory_index": 2,
          "subcategory_name": "Employee Communication Issues",
          "rationale": "This subcategory addresses how employees communicate with each other and with management."
        }}
      ]
    }},
    {{
      "category_index": 2,
      "category_name": "Work Environment",
      "description": "Overall conditions and factors that affect the workplace, including workload management and resource availability.",
      "properties": "workload intensity, resource support",
      "dimensions": "low to high, insufficient to sufficient",
      "subcategories": [
        {{
          "subcategory_index": 3,
          "subcategory_name": "Workload Challenges",
          "rationale": "This subcategory deals with the difficulties employees face in managing their workload."
        }},
        {{
          "subcategory_index": 4,
          "subcategory_name": "Resource Availability",
          "rationale": "This subcategory addresses the availability and adequacy of resources to support workload management."
        }}
      ]
    }}
  ]
}}
"""


# Selective coding
gt_prompt4 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. Review the previous phases regarding initial codes, subcategories, and categories. You are requested to perform selective coding for integrating and refining categories into a cohesive theoretical framework.

Guidelines for selective coding:
1. Identify one or more core categories among the existing categories that are central to the research questions or objectives. A core category is related to many other categories or holds particular importance. It should be central, frequent in the data, abstract enough to be broadly applicable, and capable of integrating other categories.
2. Categories can belong to more than one core category. Not all categories need to belong to a core category.
3. Develop a cohesive theoretical framework that explains the relationships between the core category and all other categories related to it. This framework should provide a comprehensive understanding of the studied phenomenon.
4. Create theoretical statements, including clear propositions or hypotheses that articulate the relationships and interactions between a core category and other categories.
5. Create a narrative that describes the grounded theory, illustrating how a core category and related categories explain the data.

For each core category, provide:
- Core category index number starting from 1,
- Core category name in 1-3 words (max 5 words),
- Description of the core category,
- The requirements for a specific category to be identified as a core category,
- Theoretical framework,
- Theoretical statements,
- Narrative description.

For each category, nested under its respective core category, provide:
- Category index number starting from 1 within each core category,
- Category name,
- Description of the category,
- The rationale for why this specific category belongs to this core category.

Truncated example of the JSON output:
{{
  "Core Categories": [
    {{
      "core_category_index": 1,
      "core_category_name": "Work-Life Balance",
      "description": "Central theme related to balancing professional responsibilities with personal life while working remotely.",
      "requirements": "Identified as frequent in the interview data, this category integrates multiple subcategories and is central to the research questions about remote work challenges and solutions. It is broadly applicable across various demographics and job roles, and crucial for understanding overall employee satisfaction and productivity.",
      "theoretical_framework": "Work-life balance is influenced by various factors, including flexible work schedules and boundary management. These factors collectively enhance overall satisfaction and productivity.",
      "theoretical_statements": "Flexible work schedules improve work-life balance. ||| Effective boundary management is crucial for maintaining work-life balance."
      "narrative_description": "Work-life balance emerged as a core category influencing multiple aspects of remote work dynamics. Factors such as flexible work schedules and boundary management were found to be critical in determining overall satisfaction and productivity. By addressing these factors, organizations can enhance work-life balance and achieve better outcomes.",
      "categories": [
        {{
          "category_index": 1,
          "category_name": "Flexible Work Schedules",
          "description": "Importance of having flexible working hours to accommodate personal and professional needs.",
          "rationale": "This category is critical to work-life balance as it addresses the need for flexibility in managing work and personal responsibilities."
        }},
        {{
          "category_index": 2,
          "category_name": "Boundary Management",
          "description": "Strategies for maintaining clear boundaries between work and personal life.",
          "rationale": "This category is integral to work-life balance, focusing on the importance of setting and maintaining boundaries to avoid burnout and maintain productivity."
        }}
      ]
    }},
    {{
      "core_category_index": 2,
      "core_category_name": "Remote Work Productivity",
      "description": "Central theme related to factors that impact productivity while working remotely.",
      "requirements": "Frequent mentions in the data indicate its significance, and it integrates multiple subcategories related to productivity in a remote work setting. This category is central to understanding and optimizing remote work environments for maximum efficiency and effectiveness.",
      "theoretical_framework": "Remote work productivity is influenced by various factors, including technology use and communication practices. These factors significantly impact the efficiency and effectiveness of remote work.",
      "theoretical_statements": "Effective use of technology enhances remote work productivity. ||| Clear communication practices are crucial for maintaining productivity in a remote work environment."
      "narrative_description": "Remote work productivity emerged as a core category that significantly influences the effectiveness of remote work. Elements such as technology use and communication practices were identified as key factors. Improving these aspects can lead to increased productivity and better remote work outcomes.",
      "categories": [
        {{
          "category_index": 1,
          "category_name": "Technology Use",
          "description": "The role of technology in enabling efficient remote work.",
          "rationale": "This category is crucial to remote work productivity as it addresses the importance of leveraging technology to enhance work efficiency."
        }},
        {{
          "category_index": 2,
          "category_name": "Communication Practices",
          "description": "The impact of communication strategies on maintaining productivity while working remotely.",
          "rationale": "This category is essential to remote work productivity, highlighting the need for clear and effective communication practices to support remote work."
        }}
      ]
    }}
  ]
}}
"""




# Theoretical coding
gt_prompt5 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. Review the previous phases regarding initial codes, subcategories, categories, and selective coding. You are requested to perform theoretical coding to integrate and refine these categories into a cohesive theoretical framework.

Guidelines for Theoretical Coding:
1. Examine Categories and Subcategories. Review the categories and subcategories to understand what each represents. Think about how these categories might be related, considering whether there are any cause-and-effect relationships or if some categories provide context for others.
2. Identify Relationships. Begin by identifying conceptual links between different categories. Determine how these categories interact and influence each other, focusing on how other categories relate to the core category identified during selective coding.
3. Develop Theoretical Codes. Look for various types of relationships, such as cause and effect, context and condition, interaction, and process. Apply theoretical codes like "if-then," "because," "leads to," and "is part of" to describe these relationships. Document the identified relationships and explain how they contribute to the emerging theory.
4. Integrate Categories. Synthesize the identified relationships into a coherent theoretical framework. Map out the relationships comprehensively and see how they fit together within the emerging theory. Ensure that the framework covers all significant aspects of the data.
5. Ensure that all relationships connected with the core category, other categories, and subcategories are included. Relationships can exist between all categories and subcategories, provided there is a rationale for them.

For each theoretical code, provide:
- Core category name,
- Identified relationship between categories/subcategories with interactions and influences,
- Theoretical code,
- Description of the theoretical code,
- Theoretical framework.

For each core category, provide:
- Table format visualization of the relationships

Truncated example of the JSON output:
{{
  "Theoretical Codes": [
    {{
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "relationship": "Leadership Support → Emotional Support: Effective leadership practices foster a supportive team environment, which enhances emotional support among peers. Leaders who provide guidance, recognition, and mentoring create an atmosphere of trust and collaboration. This supportive environment encourages employees to express their concerns and seek help from their colleagues, thereby strengthening emotional bonds and reducing feelings of isolation.",
      "theoretical_code": "If leadership provides guidance and mentoring, then team cohesion and peer empathy will improve.",
      "description": "Leadership support plays a critical role in building a cohesive team. When leaders actively provide guidance and mentoring, it fosters a supportive environment where employees feel emotionally supported by their peers. This, in turn, enhances the overall well-being of employees by reducing stress and increasing job satisfaction.",
      "theoretical_framework": "This theoretical code emphasizes the importance of leadership in creating a supportive work environment, which is crucial for employee well-being. Effective leadership practices not only improve team dynamics but also contribute to the emotional health of employees."
    }},
    {{
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "relationship": "Emotional Support ↔ Professional Development: A supportive team environment encourages employees to engage in professional development opportunities. When employees feel emotionally supported by their peers and supervisors, they are more likely to pursue further training and skill development. This mutual reinforcement between emotional support and professional growth creates a positive feedback loop, leading to continuous personal and professional development.",
      "theoretical_code": "Because a supportive team environment exists, employees are more likely to participate in professional development.",
      "description": "In a work environment where emotional support is prevalent, employees are more inclined to take advantage of professional development opportunities. This mutual reinforcement between emotional support and professional growth leads to a more engaged and satisfied workforce.",
      "theoretical_framework": "The relationship between emotional support and professional development highlights their synergistic effect on employee well-being. By fostering a supportive atmosphere, organizations can encourage continuous learning and growth among their employees."
    }},
    {{
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "relationship": "Professional Development → Employee Well-being: Access to training and career advancement opportunities directly contributes to higher job satisfaction and overall well-being. Employees who have opportunities for professional growth feel valued and motivated, which enhances their sense of achievement and fulfillment. This, in turn, boosts their overall job satisfaction and contributes positively to their mental and emotional well-being.",
      "theoretical_code": "Professional development opportunities lead to increased job satisfaction and well-being.",
      "description": "When employees have access to training and career advancement opportunities, they experience a greater sense of achievement and job satisfaction. This sense of growth and advancement is a key component of overall well-being, as it fulfills employees' aspirations and professional goals.",
      "theoretical_framework": "Professional development is a crucial factor in enhancing employee well-being. Organizations that invest in the growth of their employees not only boost job satisfaction but also improve overall organizational health."
    }},
    {{
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "relationship": "Work-Life Balance → Employee Well-being: Flexible work arrangements help employees manage stress and improve their overall well-being. Employees with flexible work schedules can better balance their work and personal lives, leading to reduced stress levels and increased job satisfaction. This balance is essential for maintaining mental health and preventing burnout.",
      "theoretical_code": "Flexible work hours reduce stress, which is part of improving overall employee well-being.",
      "description": "Flexible work arrangements allow employees to balance their professional and personal lives more effectively. This reduction in work-related stress leads to improved mental health and job satisfaction, contributing to overall well-being.",
      "theoretical_framework": "Work-life balance is an essential aspect of employee well-being. By offering flexible work arrangements, organizations can help employees manage stress better and maintain a healthier work-life balance."
    }},
    {{
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "relationship": "Professional Development → Emotional Support: Professional development activities can strengthen emotional support among employees by providing shared learning experiences and fostering a culture of mutual encouragement. Employees who engage in professional growth together often develop stronger bonds and are more likely to support each other's emotional needs.",
      "theoretical_code": "If employees engage in professional development activities together, then their emotional support for each other will strengthen.",
      "description": "Shared professional development experiences can enhance emotional bonds between employees. When employees learn and grow together, they build a culture of mutual support and encouragement, which contributes to their overall emotional well-being.",
      "theoretical_framework": "Professional development not only advances skills and career growth but also fosters a supportive work environment by strengthening emotional connections among employees."
    }}
  ],
  "table_format_visualization": [
    {{
      "core_category": "Employee Well-being",
      "relationships": [
        {{"From": "Leadership Support", "To": "Emotional Support", "Description": "Effective leadership practices foster a supportive team environment, enhancing emotional support among peers. Leaders who provide guidance, recognition, and mentoring create an atmosphere of trust and collaboration."}},
        {{"From": "Emotional Support", "To": "Professional Development", "Description": "A supportive team environment encourages employees to engage in professional development opportunities. Emotional support from peers and supervisors motivates employees to pursue further training and skill development."}},
        {{"From": "Professional Development", "To": "Employee Well-being", "Description": "Access to training and career advancement opportunities directly contributes to higher job satisfaction and overall well-being. Professional growth enhances employees' sense of achievement and fulfillment."}},
        {{"From": "Work-Life Balance", "To": "Employee Well-being", "Description": "Flexible work arrangements help employees manage stress and improve their overall well-being. A balanced work schedule reduces stress and increases job satisfaction."}},
        {{"From": "Professional Development", "To": "Emotional Support", "Description": "Shared professional development experiences can enhance emotional bonds between employees. Engaging in professional growth together fosters mutual encouragement and emotional support."}}
      ]
    }}
  ]
}}

"""




# Theory development
gt_prompt6 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. Review the previous phases regarding initial codes, subcategories, categories, selective coding, and theoretical coding. You are requested to perform theory development to formulate a grounded theory that explains the studied phenomenon and ensure the theory is well-grounded in the data and supported by the categories and their relationships.

Guidelines for Theory Development:
1. Formulate the Theory by synthesizing the categories and their relationships into a coherent theory that explains the core phenomenon. Review categories and relationships by examining all the categories and their identified relationships. Ensure you have a comprehensive understanding of how each category relates to the core phenomenon. Synthesize information by integrating these categories and relationships into a coherent framework. This involves combining the different elements in a way that they form a unified explanation of the phenomenon. Develop theoretical statements by creating theoretical statements or propositions that encapsulate the synthesized information. These statements should clearly articulate how different categories interact to explain the core phenomenon.
2. Ground in the data by ensuring that the theory is deeply rooted in the data. Compare the theoretical statements and framework against the raw data. Check if each theoretical statement is backed by evidence from the data. Document any discrepancies by noting which statements are not supported by the data, what specific issues exist, and why these are not supported by the data.
3. Ensure that the relationships between categories support the overall theory. Each aspect of the theory should be backed by evidence from the data. For each relationship identified in the theoretical framework, find supporting data. This can be quotes from interviews, observed behaviors, or other relevant data points. Create a document or table where each relationship is listed alongside the supporting evidence from the data. If supporting evidence cannot be found, document the discrepancies by noting which relationships are not supported by the data, what specific issues exist, and why these issues are not supported by the data.

For each core category, provide:
- Core phenomenon summarizing and describing the characteristics and properties of the developed theory,
- Theoretical statements,
- Discrepancies regarding statements,
- Discrepancies regarding relationships.

Truncated example of the JSON output:
{{
  "Theory Development": [
    {{
      "coreCategoryIndex": 1,
      "coreCategoryName": "Employee Well-being",
      "Core phenomenon": "Employee well-being is significantly enhanced by effective leadership, access to professional development, and flexible work arrangements, which together foster a supportive environment, reduce stress, and increase job satisfaction.",
      "Theoretical Statements": [
        "Effective leadership practices foster a supportive team environment, which enhances emotional support among peers.",
        "A supportive team environment encourages employees to engage in professional development opportunities, leading to increased job satisfaction.",
        "Access to training and career advancement opportunities directly contributes to higher job satisfaction and overall well-being.",
        "Flexible work arrangements help employees manage stress and improve their overall well-being.",
        "Emotional support from peers and leaders helps employees manage work-related stress, contributing to a better work-life balance."
      ]
    }}
  ],
  "Discrepancies Statements": [
    {{
      "coreCategoryIndex": 1,
      "coreCategoryName": "Employee Well-being",
      "Statements": [
        "Professional Development → Employee Well-being: Lack of supporting evidence from a subset of participants because some participants did not have access to training programs."
      ]
    }}
  ],
  "Discrepancies Relationships": [
    {{
      "coreCategoryIndex": 1,
      "coreCategoryName": "Employee Well-being",
      "Statements": [
        "Emotional Support ↔ Professional Development: Inconsistent evidence across different departments due to varying levels of team support in different departments.",
        "Work-Life Balance ↔ Job Satisfaction: Varying levels of job satisfaction reported due to different flexible work arrangement policies across departments."
      ]
    }}
  ]
}}

"""







# Implications and Recommendations
gt_prompt7 = """
Read the interview transcripts provided and familiarize yourself with them, understanding the context, themes, concepts, patterns, and notable differences. Review the previous phases regarding initial codes, subcategories, categories, selective coding, theoretical coding, and theory development. You are requested to develop the implications and recommendations based on the grounded theory.

Practical Implications. Discuss how the findings can be applied in practical settings. Consider the following:
- How can the grounded theory inform best practices within the relevant field?
- What specific strategies or interventions can be derived from the theory?
- How can these findings improve processes, behaviors, or outcomes in practical settings?

Policy Implications. Explain how the findings can inform policy decisions. Consider the following:
- What policy changes or developments can be suggested based on the findings?
- How can the grounded theory inform or support policy-making processes?
- What specific aspects of policy could be influenced or shaped by the findings?

Recommendations for Practitioners. Suggest practical strategies or interventions based on the findings. Consider the following:
- What actionable steps can practitioners take to implement the findings in their work?
- How can these strategies or interventions improve practices within the field?
- Provide concrete examples of how practitioners can apply the grounded theory in their daily operations.

Recommendations for Policymakers. Offer policy recommendations informed by the theory. Consider the following:
- What specific policy recommendations can be made based on the grounded theory?
- How can these recommendations address current gaps or challenges in existing policies?
- Provide clear and actionable suggestions for policymakers to consider.

Recommendations for Further Research. Identify areas for further research and remaining questions. Consider the following:
- What aspects of the phenomenon require further investigation?
- What questions remain unanswered that future research could address?
- Suggest potential research directions or methodologies that could build on the current findings.

Truncated example of the JSON output:
{{
  "Implications And Recommendations": {{
    "Practical Implications": "The findings suggest that effective leadership practices can significantly enhance employee well-being. By fostering a supportive team environment and providing opportunities for professional development, organizations can reduce stress and increase job satisfaction among employees. Specific strategies derived from the theory include implementing mentorship programs, regular feedback sessions, and team-building activities. These practices can lead to improved employee morale, higher retention rates, and better overall performance.",
    "Policy Implications": "Policies that promote flexible work arrangements and provide resources for professional development can help improve employee well-being. Policymakers should consider incorporating these elements into labor regulations and organizational policies to support a healthier and more productive workforce. For instance, policies could mandate a minimum number of hours for professional development or provide tax incentives for companies that offer flexible working conditions. These changes could lead to a more engaged and satisfied workforce, reducing turnover and increasing productivity.",
    "Recommendations For Practitioners": "Practitioners should focus on creating a supportive work environment by offering regular feedback and mentoring to employees. Implementing flexible work schedules and providing access to training programs can also enhance employee satisfaction and well-being. For example, managers can hold weekly one-on-one meetings to discuss progress and areas for development, or establish peer support groups to foster a sense of community and shared learning. These steps can help practitioners improve workplace culture and employee engagement.",
    "Recommendations For Policymakers": "Policymakers should advocate for policies that encourage flexible work arrangements and support ongoing professional development for employees. This could include tax incentives for companies that invest in employee training and development, as well as regulations that protect employees' rights to request flexible working conditions. Such policies can help address current gaps in employee support and ensure that all workers have the opportunity to develop their skills and manage their work-life balance effectively.",
    "Recommendations For Further Research": "Future research should explore the long-term effects of flexible work arrangements on employee well-being. Additionally, studies could investigate the impact of leadership styles on different aspects of employee satisfaction and productivity. Specific questions that remain unanswered include: How do different leadership approaches affect employee engagement over time? What are the most effective ways to implement flexible work policies in various industries? By addressing these questions, future research can build on the current findings and contribute to a deeper understanding of employee well-being."
  }}
}}
"""


