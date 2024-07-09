# prompts_gt.py
# This script contains the Grounded Theory prompts sent to OpenAI Assistant.

gt_instruction = """
You are a qualitative data analyst performing Grounded Theory. Your task is to analyze the provided dataset of transcribed interviews.

Respond always with JSON-formatted outputs. DO NOT output any additional text outside of the JSON.

In the analysis, take into account the following considerations to get relevant context and information for the analysis:

{user_prompt}
"""

gt_prompt1 = """
You are requested to perform initial coding phase of the Gioia method to the attached dataset of transcribed interviews.
In this phase, scrutinize the text to identify emergent themes, concepts, or patterns.
Your output should be a JSON object with an array of strings no longer than 7 words, each representing a distinct initial code in the language of the data.
For example, your output should be in this format: {{"Initial Codes": string[]}}. Ensure to return ONLY a proper JSON array of strings.

Perform initial coding according to the Gioia method on the attached transcribed interviews. Return a JSON object.

For each initial code, provide:
 - index number starting from 1,
 - code name (i.e. initial code) in no more than 3 words,
 - a meaningful and compact description of the code with no longer than 7 words, and
 - a quote from the respondent.

JSON Example:
{{
  "Initial Codes": [
    {{
      "index": 1,
      "code": "communication issues",
      "description": "Problems with communication",
      "quote": "We often face communication issues."
    }},
    {{
      "index": 2,
      "code": "positive feedback",
      "description": "Positive feedback received",
      "quote": "The feedback from the manager was great."
    }}
    // more codes...
  ]
}}


"""


gt_prompt2 = """
You are requested to perform the 2nd order coding phase of the Gioia method.

In this phase, identify higher-level themes or categories that aggregate the initial codes. Your output should be a JSON-formatted object mapping each
higher-level theme to an array of initial codes that belong to it.

For each higher-level theme, provide:
 - index number starting from 1,
 - theme name (i.e. higher-level theme),
 - for each initial code included in the theme, provide the initial code index and name.

As a general example, "employee sentiment" could be a 2nd order code to 1st level codes "Positive feelings toward new policy" and "Sense of control".
Your output should look like this, where the keys are the higher-level concepts: {{"Some higher-Level theme": ["initial code index: initial code", "another initial code index: another initial code"]}}.
Ensure to return ONLY a proper JSON object.

Perform 2nd Order Coding according to the Gioia method and return a JSON object.

JSON Example:
{{
  "Higher-Level Themes": [
    {{
      "index": 1,
      "theme": "Employee Sentiment",
      "initial_codes": [
        {{
          "index": 1,
          "code": "positive feedback"
        }},
        {{
          "index": 2,
          "code": "communication issues"
        }}
      ]
    }},
    {{
      "index": 2,
      "theme": "Resource Allocation",
      "initial_codes": [
        {{
          "index": 3,
          "code": "lack of resources"
        }}
      ]
    }}
    // more themes...
  ]
}}


Initial codes:
{response_json}
"""


gt_prompt3 = """
You are requested to perform the Aggregate Dimensions phase of the Gioia method.
In this phase, identify overarching theoretical dimensions (typically 5-7) that aggregate the 2nd order codes.
Your output should be a JSON-formatted object mapping each aggregate dimension to an array of 2nd order codes that belong to it.
For each aggregate dimension, provide:
 - index number starting from 1,
 - dimension name (i.e. aggregate dimension),
 - for each higher-level theme included in the dimension, provide the theme index and name.

As a general example, "Policy Usability" could make for a good, quantifiable dimension. Your output should look like this, where
the keys are the (quantifiable) dimensions: {{"some dim": ["theme index: theme", "another theme index: another theme"]}}.
Ensure that the aggregate dimensions are grounded in the themes and to return ONLY a proper JSON object.

Perform aggregation into theoretical dimensions according to the Gioia method and return a JSON object.

JSON Example:
{{
  "Aggregate Dimensions": [
    {{
      "index": 1,
      "dimension": "Organizational Climate",
      "higher_level_themes": [
        {{
          "index": 1,
          "theme": "Employee Sentiment"
        }},
        {{
          "index": 2,
          "theme": "Team Dynamics"
        }}
      ]
    }},
    {{
      "index": 2,
      "dimension": "Operational Efficiency",
      "higher_level_themes": [
        {{
          "index": 3,
          "theme": "Resource Allocation"
        }}
      ]
    }}
    // more dimensions...
  ]
}}

The 2nd order codes:
{response2_json}
"""


gt_prompt4 = """
I have completed the open and axial coding phases of my grounded theory research.

Below is the JSON data representing the categories, subcategories, and their relationships.

You are requested to perform Theoretical Coding by integrating these elements into a coherent theoretical framework in JSON format.

Specifically, identify the core category, elaborate on the key relationships between categories, and provide a narrative that explains the overall theory.

The output JSON should contain the following elements:
- Core Category: The main theme that integrates all other categories.
- Categories: An array of categories with their subcategories.
- Relationships: An array of relationships between categories.
- Theory: A summary of the overall theory, followed by detailed explanations of key relationships.

The output JSON should follow this schema:
{{
  "core_category": "Organizational Climate",
  "categories": [
    {{
      "index": 1,
      "name": "Employee Sentiment",
      "subcategories": [
        "positive feedback",
        "communication issues"
      ]
    }},
    {{
      "index": 2,
      "name": "Team Dynamics",
      "subcategories": [
        "team collaboration",
        "management support"
      ]
    }},
    {{
      "index": 3,
      "name": "Resource Allocation",
      "subcategories": [
        "lack of resources"
      ]
    }}
  ],
  "relationships": [
    {{
      "index": 1,
      "type": "influences",
      "from": "Employee Sentiment",
      "to": "Team Dynamics",
      "description": "Positive feedback improves team collaboration."
    }},
    {{
      "index": 2,
      "type": "impacts",
      "from": "Resource Allocation",
      "to": "Operational Efficiency",
      "description": "Lack of resources negatively impacts efficiency."
    }}
  ],
  "theory": {{
    "summary": "The overall organizational climate is influenced by employee sentiment, team dynamics, and resource allocation.",
    "details": [
      {{
        "relationship": "Employee Sentiment and Team Dynamics",
        "explanation": "Positive feedback and communication issues shape how well teams collaborate and the support they receive from management."
      }},
      {{
        "relationship": "Resource Allocation and Operational Efficiency",
        "explanation": "Adequate resources are critical for maintaining operational efficiency within the organization."
      }}
    ]
  }}
}}

The Aggregate Dimensions phase:
{response3_json}
"""


gt_prompt5 = """
I have completed the theoretical coding phase of my grounded theory research.

Below is the JSON data representing the refined categories, relationships, and the emerging theory.

You are requested to perform the theory refinement phase.

Specifically, the output should include suggestions for further integration and refinement of the theory,
ensuring that all aspects are comprehensive and well-structured.

Each suggestion should be a separate row, with different aspects provided as columns.

Expected Output Example for Theory Refinement:
{{
  "theory_refinement": [
    {{
      "index": 1,
      "suggestion": "Ensure that all categories and subcategories are clearly defined and interrelated.",
      "explanation": "Review and refine the definitions of all categories and subcategories to ensure clarity and coherence."
    }},
    {{
      "index": 2,
      "suggestion": "Examine any potential gaps in the theory and address them with additional data if necessary.",
      "explanation": "Identify and fill any gaps in the data by collecting additional information if required."
    }}
    // more suggestions...
  ]
}}

The Theoretical Coding:
{response4_json}
"""


gt_prompt6 = """
I have completed the theoretical coding and theory refinement phase of my grounded theory research.

Below is the JSON data representing the refined categories, relationships, and the emerging theory.

You are requested to develop validation strategies. Specifically, the output should include methods for validating the theory, including member checking, peer debriefing, and triangulation.

Each strategy should be a separate row, with different aspects provided as columns.

Expected Output Example for Validation Strategies:
{{
  "validation_strategies": [
    {{
      "index": 1,
      "strategy": "member_checking",
      "description": "Share the emerging theory with participants and ask for their feedback on its accuracy and relevance. Use their input to refine and validate the theory."
    }},
    {{
      "index": 2,
      "strategy": "peer_debriefing",
      "description": "Discuss the theory with colleagues or experts in the field to identify any biases or gaps. Incorporate their feedback to strengthen the theory."
    }},
    {{
      "index": 3,
      "strategy": "triangulation",
      "description": "Use additional data sources or methods to confirm the consistency and validity of the findings. This may include reviewing related literature, conducting supplementary interviews, or employing different analytical techniques."
    }}
    // more strategies...
  ]
}}

The refined Theoretical Coding:
{response5_json}
"""


gt_prompt7 = """
I have completed the theoretical coding phase of my grounded theory research.

Below is the JSON data representing the refined categories, relationships, and the emerging theory.

You are requested to prepare a detailed presentation of the theory.

Specifically, the output should include a detailed outline for documenting the theory, suggestions for visual
representations, and a discussion of theoretical, practical, and policy implications.

Expected Output Example for Detailed Presentation:
{{
  "presentation_and_writing": {{
    "outline": [
      {{
        "index": number,
        "section": "introduction",
        "description": "Introduce the research problem, objectives, and methodology."
      }},
      {{
        "index": number,
        "section": "theoretical_framework",
        "description": "Present the refined categories, relationships, and core category."
      }},
      {{
        "index": number,
        "section": "data_analysis",
        "description": "Describe the coding process and how the theory emerged."
      }},
      {{
        "index": number,
        "section": "discussion",
        "description": "Discuss the theoretical, practical, and policy implications of the findings."
      }},
      {{
        "index": number,
        "section": "conclusion",
        "description": "Summarize the key contributions and suggest areas for future research."
      }}
    ],
    "visual_representations": [
      {{
        "index": number,
        "visual": "Diagram of relationships",
        "description": "Create a diagram showing the relationships between categories and subcategories."
      }},
      {{
        "index": number,
        "visual": "Model illustration",
        "description": "Develop a model illustrating the core category and its connections to other elements of the theory."
      }}
    ],
    "implications": [
      {{
        "index": number,
        "type": "theoretical",
        "description": "Discuss how the theory advances understanding in the field of organizational change and communication strategies."
      }},
      {{
        "index": number,
        "type": "practical",
        "description": "Provide practical applications of the theory for managers and organizations to improve communication strategies and support systems during organizational change."
      }},
      {{
        "index": number,
        "type": "policy",
        "description": "Suggest potential policy implications and recommendations based on the findings to guide organizational policies and practices."
      }}
    ]
  }}
}}


The Final Coding:
{response6_json}
"""