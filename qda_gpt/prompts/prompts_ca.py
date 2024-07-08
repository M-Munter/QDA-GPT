# prompts_ca.py
# This script contains the Content Analysis instruction and prompts sent to OpenAI Assistant.

ca_instruction = """
You are a qualitative data analyst performing Content Analysis. Your task is to analyze the provided dataset of transcribed interviews.

Respond always with JSON-formatted outputs. DO NOT output any additional text outside of the JSON.

In the analysis, take into account the following considerations to get relevant context and information for the analysis:

{user_prompt}

"""

# Data Reduction
ca_prompt1 = """
You are requested to perform reduction on the attached data.
 
To perform this step, do the following:
- Read the interview transcript provided.
- Identify and extract expressions that describe the research objective.
- Simplify and list these expressions.

Use the following JSON format:
{{ "Expressions": [ "simplified expression 1", "simplified expression 2", ... ] }}
"""


# Data Clustering
ca_prompt2 = """
You are requested to perform clustering phase of the Content Analysis by clustering provided simplified expressions.

To perform this step, do the following:
- Review the simplified expressions provided.
- Identify similarities and differences among the expressions.
- Group similar expressions into subcategories and assign a descriptive label to each subcategory.

Use the following format:
{{
  "Clusters": [
    {{
      "subcategory": "subcategory name",
      "expressions": [
        "simplified expression 1",
        "simplified expression 2"
      ]
    }}
  ]
}}

List of simplified expressions:
{response_json}
"""


# Data Abstraction
ca_prompt3 = """
You are requested to perform abstraction for clustered expressions.

To perform this step, do the following:
- Review the clusters provided.
- Extract the essential information from each cluster.
- Formulate theoretical concepts based on the extracted information.


Expected Output:
{{
  "Theoretical Concepts": [
    {{
      "concept": "theoretical concept name",
      "linked_clusters": [
        "subcategory name 1",
        "subcategory name 2"
      ]
    }}
  ]
}}

List of Clusters:
{response2_json}
"""

# Coding and categorizing
ca_prompt4 = """
You are requested to create categories for coded interview data.

To perform this step, do the following:
- Review the list of theoretical concepts.
- Use these concepts to define categories. Each category may be derived from one or multiple theoretical concepts, and a single concept can lead to several categories.
- Define each category with a concise name, detailed description, examples, and coding rules.
- Provide examples for each category, including:
  - Real examples: Direct excerpts from the interview data that fit the category.
  - Hypothetical examples: Constructed examples that illustrate the category if real examples are insufficient or unclear.
  - Non-examples: Excerpts that may seem related but do not fit the category, to clarify boundaries.


Expected output:
{{
  "Categories": [
    {{
      "name": "category name",
      "description": "detailed description of the category",
      "related_concepts": [
        "concept 1",
        "concept 2"
      ],
      "real_examples": [
        "example from data 1",
        "example from data 2"
      ],
      "hypothetical_examples": [
        "constructed example 1",
        "constructed example 2"
      ],
      "non_examples": [
        "non-example 1",
        "non-example 2"
      ],
      "rules": "rules for inclusion in the category"
    }}
  ]
}}



List of Clusters:
{response3_json}
"""


# Pilot testing
ca_prompt5 = """
You are requested to perform pilot testing on the coding framework.

To perform this step, do the following:
- Review the categories and their definitions created in the previous coding and categorization phase.
- Select a subset of the interview data.
- Apply the categories to this subset of data, ensuring to follow the provided examples and rules.
- Assess the consistency and coherence of the coding by comparing multiple rounds of coding.
- Identify any ambiguities or inconsistencies in the category definitions and coding rules.
- Refine and adjust the categories and coding rules as necessary based on the pilot testing results.
- Categories and coding rules do not need to be adjusted needlessly. However, still changes can be done is it is relevant.

Use the following format:
{{
  "Pilot Testing Results": [
    {{
      "text": "interview text 1",
      "initial_category": "applied category in first round",
      "revised_category": "applied category in second round"
    }}
  ],
  "Refined Categories": [
    {{
      "name": "refined category name",
      "description": "refined description of the category",
      "linked_concepts": [
        "concept 1",
        "concept 2"
      ],
      "real_examples": [
        "refined example from data 1",
        "refined example from data 2"
      ],
      "hypothetical_examples": [
        "refined constructed example 1",
        "refined constructed example 2"
      ],
      "non_examples": [
        "refined non-example 1",
        "refined non-example 2"
      ],
      "rules": "refined rules for inclusion in the category"
    }}
  ]
}}





List of Categories (or revised categories):
{response4_json}
"""


# Main analysis
ca_prompt6 = """
You are requested to perform the main analysis phase the Content Analysis.

To perform this step, do the following:
- Review the categories and their definitions that were refined in the pilot testing phase to ensure that you are
familiar with the categories, definitions, examples, and rules, which are crucial for consistent and accurate coding.
- Apply the refined coding framework to the entire datasetto ensure comprehensive coding of the data, allowing for 
the identification of all relevant instances according to the refined categories. Follow the examples and rules 
strictly to maintain consistency.
- Document any issues or ambiguities encountered during codingto identify areas that may need further refinement 
and ensures transparency in the coding process.
- Analyze the coded data to identify patterns, themes, and relationships to derive meaningful insights from the coded data.
Link these patterns, themes, and relationships to the refined categories to ensure they are grounded in the coding framework.
- Summarize how the findings align with the research questions and theoretical framework to provide a comprehensive view 
of how the analysis answers the research questions and relates to the theoretical concepts. Create a detailed report 
that includes patterns, themes, relationships, and their alignment with theory and research questions.

Use the following format in the output:
{{
  "Refined Categories": [
    {{
      "name": "refined category name",
      "description": "refined description of the category",
      "linked_concepts": ["concept 1", "concept 2"],
      "real_examples": ["refined example from data 1", "refined example from data 2"],
      "hypothetical_examples": ["refined constructed example 1", "refined constructed example 2"],
      "non_examples": ["refined non-example 1", "refined non-example 2"],
      "rules": "refined rules for inclusion in the category"
    }}
  ],
  "Analysis Results": {{
    "patterns": [
      {{
        "pattern": "pattern description",
        "linked_categories": [
          "refined category name 1",
          "refined category name 2"
        ]
      }}
    ],
    "themes": [
      {{
        "theme": "theme description",
        "linked_patterns": [
          "pattern description 1",
          "pattern description 2"
        ],
        "linked_categories": [
          "refined category name 1",
          "refined category name 2"
        ]
      }}
    ],
    "relationships": [
      {{
        "relationship": "relationship description",
        "linked_themes": [
          "theme description 1",
          "theme description 2"
        ],
        "linked_patterns": [
          "pattern description 1",
          "pattern description 2"
        ],
        "linked_categories": [
          "refined category name 1",
          "refined category name 2"
        ]
      }}
    ],
    "alignment_with_theory": "description of how results align with theoretical concepts",
    "answers_to_research_questions": "summary of how the findings answer the research questions"
  }}
}}



List of input  categories:
{response5_json}
"""