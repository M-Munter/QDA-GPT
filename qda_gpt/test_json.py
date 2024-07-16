import json
import pandas as pd
from jinja2 import Template

def generate_tables_from_response(response_text):
    try:
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start == -1 or end == -1:
            raise json.JSONDecodeError("Invalid JSON format", response_text, 0)
        response_text = response_text[start:end]
        response_json = json.loads(response_text)

        tables = []
        if isinstance(response_json, dict):
            for table_name, records in response_json.items():
                if isinstance(records, list):
                    df = pd.json_normalize(records, sep='_')
                    df = explode_nested_columns(df)
                    tables.append({
                        'table_name': table_name,
                        'columns': df.columns.tolist(),
                        'data': df.values.tolist()
                    })
                elif isinstance(records, dict):
                    df = pd.json_normalize(records, sep='_')
                    df = explode_nested_columns(df)
                    if df.shape[0] == 1:
                        df = df.T.reset_index()
                        df.columns = ['Field', 'Value']
                    tables.append({
                        'table_name': table_name,
                        'columns': df.columns.tolist(),
                        'data': df.values.tolist()
                    })
        return tables

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def explode_nested_columns(df):
    """
    Explode and normalize nested columns in the DataFrame.
    """
    for col in df.columns:
        if isinstance(df[col].iloc[0], list):
            df = df.explode(col).reset_index(drop=True)
        if isinstance(df[col].iloc[0], dict):
            df = df.drop(columns=[col]).join(df[col].apply(pd.Series).add_prefix(f"{col}_"))
    return df

# Example usage
response_text = '''
{
  "Units": [
    {
      "index": 1,
      "text": "I am motivated by a sense of accomplishment."
    },
    {
      "index": 2,
      "text": "Recognition I receive from my peers."
    },
    {
      "index": 3,
      "text": "Setting and achieving personal goals keeps me driven. You know, like working in a team where my contributions are valued and seeing the impact, it's fulfilling."
    },
    {
      "index": 4,
      "text": "The positive feedback from my supervisor and the opportunity to take on challenging projects make me feel appreciated and push me to improve my skills continuously. Moreover, the sense of community within my workplace encourages me to contribute proactively and support my colleagues, fostering a positive and productive work environment."
    }
  ],
  "Clusters": [
    {
      "subcategory_index": 1,
      "subcategory_label": "Motivational Factors",
      "definition": "This subcategory includes units that describe personal and external factors that motivate individuals. Significant properties include personal achievements, recognition from others, and internal drives.",
      "units": [
        {
          "index": 1,
          "text": "I am motivated by a sense of accomplishment.",
          "rationale": "This unit discusses personal achievement, which is a key motivational factor."
        },
        {
          "index": 2,
          "text": "Recognition I receive from my peers.",
          "rationale": "This unit mentions external recognition, which is a significant motivational factor."
        }
      ]
    },
    {
      "subcategory_index": 2,
      "subcategory_label": "Work Environment",
      "definition": "This subcategory encompasses units that describe aspects of the work environment that influence individuals. Properties include teamwork, feedback, and community support.",
      "units": [
        {
          "index": 3,
          "text": "Setting and achieving personal goals keeps me driven. You know, like working in a team where my contributions are valued and seeing the impact, it's fulfilling.",
          "rationale": "This unit talks about the work environment, specifically teamwork and the value of contributions, which are key aspects of a supportive work environment."
        },
        {
          "index": 4,
          "text": "The positive feedback from my supervisor and the opportunity to take on challenging projects make me feel appreciated and push me to improve my skills continuously. Moreover, the sense of community within my workplace encourages me to contribute proactively and support my colleagues, fostering a positive and productive work environment.",
          "rationale": "This unit discusses feedback, challenging projects, and community, which are all crucial elements of a positive work environment."
        }
      ]
    }
  ],
  "Categories": [
    {
      "category_index": 1,
      "category_label": "Personal Motivation",
      "definition": "This category includes subcategories that describe intrinsic and extrinsic factors driving personal motivation. Key properties include individual achievements, peer recognition, and personal goals.",
      "subcategories": [
        {
          "subcategory_index": 1,
          "text": "I am motivated by a sense of accomplishment.",
          "rationale": "This subcategory discusses personal achievement, aligning with intrinsic motivation as described by Self-Determination Theory."
        },
        {
          "subcategory_index": 2,
          "text": "Recognition I receive from my peers.",
          "rationale": "This subcategory involves external recognition, fitting into extrinsic motivation as described by Self-Determination Theory."
        }
      ]
    },
    {
      "category_index": 2,
      "category_label": "Work Environment",
      "definition": "This category encompasses subcategories describing aspects of the work environment influencing individuals. Properties include teamwork, feedback, and community support.",
      "subcategories": [
        {
          "subcategory_index": 3,
          "text": "Setting and achieving personal goals keeps me driven. You know, like working in a team where my contributions are valued and seeing the impact, it's fulfilling.",
          "rationale": "This subcategory addresses the work environment, specifically teamwork and the value of contributions, aligning with principles of Organizational Behavior Theory."
        },
        {
          "subcategory_index": 4,
          "text": "The positive feedback from my supervisor and the opportunity to take on challenging projects make me feel appreciated and push me to improve my skills continuously. Moreover, the sense of community within my workplace encourages me to contribute proactively and support my colleagues, fostering a positive and productive work environment.",
          "rationale": "This subcategory discusses feedback, challenging projects, and community, key elements of a positive work environment, as per Organizational Behavior Theory."
        }
      ]
    }
  ],
  "Theoretical Concepts": [
    {
      "concept_label": "Intrinsic Motivation",
      "definition": "This concept includes categories related to internal factors that drive individuals. Key properties include personal growth, self-fulfillment, and intrinsic rewards.",
      "theoretical_framework": "This concept aligns with Self-Determination Theory (Deci & Ryan, 2000), which posits that intrinsic motivation is driven by autonomy, competence, and relatedness.",
      "representative_examples": "I am motivated by a sense of accomplishment. ||| Setting and achieving personal goals keeps me driven.",
      "key_themes_and_patterns": "Personal achievement and growth ||| Self-fulfillment through personal goals",
      "high_level_summary": "Intrinsic Motivation encompasses personal achievement and self-fulfillment, aligning with Deci & Ryan's Self-Determination Theory.",
      "categories": [
        {
          "category_index": 1,
          "text": "Personal Growth",
          "rationale": "This category fits under Intrinsic Motivation as it pertains to individual development and self-improvement."
        },
        {
          "category_index": 2,
          "text": "Self-Fulfillment",
          "rationale": "This category involves the pursuit of fulfilling personal goals and aspirations, fitting into Intrinsic Motivation."
        }
      ]
    },
    {
      "concept_label": "Workplace Dynamics",
      "definition": "This concept encompasses categories describing social and structural factors within the workplace. Key properties include teamwork, leadership, and organizational culture.",
      "theoretical_framework": "This concept is informed by Organizational Behavior Theory (Robbins & Judge, 2013), which examines the impact of individuals, groups, and structures on behavior within organizations.",
      "representative_examples": "Working in a team where my contributions are valued. ||| The positive feedback from my supervisor motivates me.",
      "key_themes_and_patterns": "Team collaboration and dynamics ||| Leadership and organizational culture",
      "high_level_summary": "Workplace Dynamics focuses on team collaboration, leadership, and organizational culture, aligning with Robbins & Judge's Organizational Behavior Theory.",
      "categories": [
        {
          "category_index": 3,
          "text": "Teamwork",
          "rationale": "This category addresses collaborative efforts and interactions among team members, aligning with Workplace Dynamics."
        },
        {
          "category_index": 4,
          "text": "Leadership",
          "rationale": "This category pertains to the influence and guidance provided by leaders, fitting into Workplace Dynamics."
        }
      ]
    }
  ],
  "Implications And Recommendations": {
    "Practical Implications": "The findings suggest that effective leadership practices can significantly enhance employee well-being. By fostering a supportive team environment and providing opportunities for professional development, organizations can reduce stress and increase job satisfaction among employees. Specific strategies derived from the theory include implementing mentorship programs, regular feedback sessions, and team-building activities. These practices can lead to improved employee morale, higher retention rates, and better overall performance.",
    "Policy Implications": "Policies that promote flexible work arrangements and provide resources for professional development can help improve employee well-being. Policymakers should consider incorporating these elements into labor regulations and organizational policies to support a healthier and more productive workforce. For instance, policies could mandate a minimum number of hours for professional development or provide tax incentives for companies that offer flexible working conditions. These changes could lead to a more engaged and satisfied workforce, reducing turnover and increasing productivity.",
    "Recommendations For Practitioners": "Practitioners should focus on creating a supportive work environment by offering regular feedback and mentoring to employees. Implementing flexible work schedules and providing access to training programs can also enhance employee satisfaction and well-being. For example, managers can hold weekly one-on-one meetings to discuss progress and areas for development, or establish peer support groups to foster a sense of community and shared learning. These steps can help practitioners improve workplace culture and employee engagement.",
    "Recommendations For Policymakers": "Policymakers should advocate for policies that encourage flexible work arrangements and support ongoing professional development for employees. This could include tax incentives for companies that invest in employee training and development, as well as regulations that protect employees' rights to request flexible working conditions. Such policies can help address current gaps in employee support and ensure that all workers have the opportunity to develop their skills and manage their work-life balance effectively.",
    "Recommendations For Further Research": "Future research should explore the long-term effects of flexible work arrangements on employee well-being. Additionally, studies could investigate the impact of leadership styles on different aspects of employee satisfaction and productivity. Specific questions that remain unanswered include: How do different leadership approaches affect employee engagement over time? What are the most effective ways to implement flexible work policies in various industries? By addressing these questions, future research can build on the current findings and contribute to a deeper understanding of employee well-being."
  },
  "Theory Development": [
    {
      "coreCategoryIndex": 1,
      "coreCategoryName": "Employee Well-being",
      "Theoretical Statements": [
        "Effective leadership practices foster a supportive team environment, enhancing emotional support among peers.",
        "A supportive team environment encourages employees to engage in professional development opportunities.",
        "Access to training and career advancement opportunities directly contributes to higher job satisfaction and overall well-being.",
        "Flexible work arrangements help employees manage stress and improve their overall well-being.",
        "Emotional Support → Work-Life Balance: Emotional support from peers and leaders helps employees manage work-related stress, contributing to a better work-life balance."
      ]
    }
  ],
  "Discrepancies Statements": [
    {
      "coreCategoryIndex": 1,
      "coreCategoryName": "Employee Well-being",
      "Statements": [
        "Professional Development → Employee Well-being: Lack of supporting evidence from a subset of participants because some participants did not have access to training programs."
      ]
    }
  ],
  "Discrepancies Relationships": [
    {
      "coreCategoryIndex": 1,
      "coreCategoryName": "Employee Well-being",
      "Statements": [
        "Emotional Support ↔ Professional Development: Inconsistent evidence across different departments due to varying levels of team support in different departments.",
        "Work-Life Balance ↔ Job Satisfaction: Varying levels of job satisfaction reported due to different flexible work arrangement policies across departments."
      ]
    }
  ],
  "Theoretical Coding_relationships": [
    {
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "relationship": "Leadership Support → Emotional Support: Effective leadership practices foster a supportive team environment, enhancing emotional support among peers."
    },
    {
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "relationship": "Emotional Support ↔ Professional Development: A supportive team environment encourages employees to engage in professional development opportunities."
    },
    {
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "relationship": "Professional Development → Employee Well-being: Access to training and career advancement opportunities directly contributes to higher job satisfaction and overall well-being."
    },
    {
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "relationship": "Work-Life Balance → Employee Well-being: Flexible work arrangements help employees manage stress and improve their overall well-being."
    }
  ],
  "Theoretical Coding_theoretical_codes": [
    {
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "theoretical_code": "If leadership provides guidance and mentoring, then team cohesion and peer empathy will improve."
    },
    {
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "theoretical_code": "Because a supportive team environment exists, employees are more likely to participate in professional development."
    },
    {
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "theoretical_code": "Professional development opportunities lead to increased job satisfaction and well-being."
    },
    {
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "theoretical_code": "Flexible work hours reduce stress, which is part of improving overall employee well-being."
    }
  ],
  "Theoretical Coding_theoretical_framework": [
    {
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "framework_component": "Leadership Support",
      "description": "Leads to Emotional Support and Professional Development."
    },
    {
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "framework_component": "Emotional Support",
      "description": "Reduces stress and increases job satisfaction."
    },
    {
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "framework_component": "Professional Development",
      "description": "Enhances sense of growth and job satisfaction."
    },
    {
      "core_category_index": 1,
      "coreCategoryName": "Employee Well-being",
      "framework_component": "Work-Life Balance",
      "description": "Reduces burnout and enhances job satisfaction."
    }
  ],
  "Core Categories": [
    {
      "core_category_index": 1,
      "core_category_name": "Work-Life Balance",
      "description": "Central theme related to balancing professional responsibilities with personal life while working remotely.",
      "requirements": "Frequent in the data, integrates multiple categories, broadly applicable, and central to the research question.",
      "theoretical_framework": "Work-life balance is influenced by various factors, including flexible work schedules and boundary management. These factors collectively enhance overall satisfaction and productivity.",
      "theoretical_statements": "Flexible work schedules improve work-life balance. ||| Effective boundary management is crucial for maintaining work-life balance.",
      "narrative_description": "Work-life balance emerged as a core category influencing multiple aspects of remote work dynamics. Factors such as flexible work schedules and boundary management were found to be critical in determining overall satisfaction and productivity. By addressing these factors, organizations can enhance work-life balance and achieve better outcomes.",
      "categories": [
        {
          "category_index": 1,
          "category_name": "Flexible Work Schedules",
          "description": "Importance of having flexible working hours to accommodate personal and professional needs.",
          "rationale": "This category is critical to work-life balance as it addresses the need for flexibility in managing work and personal responsibilities."
        },
        {
          "category_index": 2,
          "category_name": "Boundary Management",
          "description": "Strategies for maintaining clear boundaries between work and personal life.",
          "rationale": "This category is integral to work-life balance, focusing on the importance of setting and maintaining boundaries to avoid burnout and maintain productivity."
        }
      ]
    },
    {
      "core_category_index": 2,
      "core_category_name": "Remote Work Productivity",
      "description": "Central theme related to factors that impact productivity while working remotely.",
      "requirements": "Frequent in the data, integrates multiple categories, broadly applicable, and central to the research question.",
      "theoretical_framework": "Remote work productivity is influenced by various factors, including technology use and communication practices. These factors significantly impact the efficiency and effectiveness of remote work.",
      "theoretical_statements": "Effective use of technology enhances remote work productivity. ||| Clear communication practices are crucial for maintaining productivity in a remote work environment.",
      "narrative_description": "Remote work productivity emerged as a core category that significantly influences the effectiveness of remote work. Elements such as technology use and communication practices were identified as key factors. Improving these aspects can lead to increased productivity and better remote work outcomes.",
      "categories": [
        {
          "category_index": 1,
          "category_name": "Technology Use",
          "description": "The role of technology in enabling efficient remote work.",
          "rationale": "This category is crucial to remote work productivity as it addresses the importance of leveraging technology to enhance work efficiency."
        },
        {
          "category_index": 2,
          "category_name": "Communication Practices",
          "description": "The impact of communication strategies on maintaining productivity while working remotely.",
          "rationale": "This category is essential to remote work productivity, highlighting the need for clear and effective communication practices to support remote work."
        }
      ]
    }
  ],
  "Categories": [
    {
      "category_index": 1,
      "category_name": "Communication Issues",
      "description": "Broad issues related to communication within the organization, including both management and employee communication.",
      "properties": "clarity, frequency",
      "dimensions": "unclear to clear, infrequent to frequent",
      "subcategories": [
        {
          "subcategory_index": 1,
          "subcategory_name": "Management Communication Issues",
          "rationale": "This subcategory focuses on problems specifically with how management communicates with employees."
        },
        {
          "subcategory_index": 2,
          "subcategory_name": "Employee Communication Issues",
          "rationale": "This subcategory addresses how employees communicate with each other and with management."
        }
      ]
    },
    {
      "category_index": 2,
      "category_name": "Work Environment",
      "description": "Overall conditions and factors that affect the workplace, including workload management and resource availability.",
      "properties": "workload intensity, resource support",
      "dimensions": "low to high, insufficient to sufficient",
      "subcategories": [
        {
          "subcategory_index": 3,
          "subcategory_name": "Workload Challenges",
          "rationale": "This subcategory deals with the difficulties employees face in managing their workload."
        },
        {
          "subcategory_index": 4,
          "subcategory_name": "Resource Availability",
          "rationale": "This subcategory addresses the availability and adequacy of resources to support workload management."
        }
      ]
    }
  ],
  "Categories": [
    {
      "index": 1,
      "name": "Active Participation",
      "definition": "A category that encompasses various forms of active student involvement in the learning process. This includes behaviors such as asking questions, engaging in discussions, and participating in group activities. The purpose is to capture the extent and nature of student engagement in educational activities. Requirements for this category include observable behaviors that indicate active participation.",
      "description": "This category is relevant to understanding how different forms of student engagement impact learning outcomes and classroom dynamics.",
      "code_requirements": "Codes in this category must demonstrate behaviors indicative of active student participation.",
      "codes": "1, 2, 5, 8, 9, 15, 20, 35, 36, 38, 65, 66, 68, 71, 73, 82, 88, 101, 105, 111"
    },
    {
      "index": 2,
      "name": "Supportive Teaching",
      "definition": "A category that includes various types of support and encouragement provided by teachers. This can involve one-on-one tutoring, positive reinforcement, and providing additional learning resources. The purpose is to identify supportive behaviors from teachers that enhance student learning and motivation. Requirements for this category include actions taken by teachers that provide direct support to students.",
      "description": "This category helps to explore the role of teacher support in fostering student academic success and emotional well-being.",
      "code_requirements": "Codes in this category should reflect actions taken by teachers to assist students.",
      "codes": "2, 7, 11, 17, 23, 44, 98"
    }
  ],
  "Categories": [
    {
      "index": 1,
      "name": "Educational Benefits",
      "definition": "This category includes various positive impacts of gaming on educational contexts. It encompasses improved problem-solving skills, enhanced motivation for learning, and the use of educational games for skill development. Requirements for this category include observable educational outcomes that are positively influenced by gaming.",
      "requirements_relevance": "Categories in this theme must demonstrate educational improvements or benefits resulting from gaming. This is relevant for understanding how gaming can enhance learning experiences and outcomes.",
      "themes": "1",
      "theme_names": "Educational and Social Impact"
    },
    {
      "index": 2,
      "name": "Social Interaction",
      "definition": "This category covers how gaming facilitates social interactions. It includes forming friendships, online collaboration, and community building through gaming. Requirements for this category include social behaviors and interactions that occur within the context of gaming.",
      "requirements_relevance": "Categories in this theme must reflect social interactions and community engagement facilitated by gaming. This is relevant for understanding the social aspects and community-building potential of gaming.",
      "themes": "1, 2",
      "theme_names": "Educational and Social Impact, Technological Advances"
    },
    {
      "index": 3,
      "name": "Technological Innovation",
      "definition": "This category includes advancements in gaming technology such as new game engines, VR/AR, and other cutting-edge technologies. Requirements for this category include the development and implementation of new technologies in gaming.",
      "requirements_relevance": "Categories in this theme must demonstrate technological advancements and innovations in gaming. This is relevant for understanding the role of technology in shaping the gaming industry.",
      "themes": "2",
      "theme_names": "Technological Advances"
    },
    {
      "index": 4,
      "name": "Economic Impact",
      "definition": "This category covers the economic aspects of gaming, including revenue generation, job creation, and market trends. Requirements for this category include the financial implications and economic benefits of the gaming industry.",
      "requirements_relevance": "Categories in this theme must reflect economic factors and impacts related to gaming. This is relevant for understanding the economic influence of the gaming industry.",
      "themes": 2,
      "theme_names": "Technological Advances"
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
  ],
  "Themes": [
    {
      "name": "Educational and Social Impact",
      "quotes": "Gaming has significantly improved my problem-solving skills. ||| I have made many friends through online gaming. ||| Educational games have made me more interested in learning.",
      "analysis": "This theme shows that gaming has both positive and negative impacts on education and social behavior.",
      "conclusions": "Gaming can be a valuable educational tool but requires careful implementation. This conclusion aligns with the research objective to understand the educational benefits of gaming."
    },
    {
      "name": "Technological Advances",
      "quotes": "The new VR technology has transformed my gaming experience. ||| The gaming industry has created numerous job opportunities. ||| Technological innovations are crucial for the future of gaming.",
      "analysis": "Technological innovations in gaming drive industry growth and change user experiences.",
      "conclusions": "Ongoing technological developments are crucial for the future of the gaming industry. This conclusion addresses the research question on the impact of technological advancements in gaming."
    }
  ],
  "Overall_Findings": {
    "summary_title": "Key Educational, Social, and Technological Findings from Gaming",
    "description": "This study explores the educational, social, and technological impacts of gaming, highlighting both benefits and challenges.",
    "flagged_segments": "The segment 'Gaming has helped me understand historical events better' is not sufficiently covered, which could potentially provide new insights if properly categorized. ||| The segment 'I use VR for exercise routines' appears to be miscategorized under 'Technological Advances' when it might fit better under 'Educational and Social Impact'. ||| The segment 'Gaming can sometimes be isolating' is missing critical information on the specific contexts where this occurs.",
    "analysis_and_interpretation": "The themes collectively highlight the multifaceted impact of gaming on education, social behavior, and technological progress. These findings directly address the research questions regarding the benefits and challenges of gaming in these areas.",
    "conclusions_and_implications": "The study concludes that while gaming offers significant educational and social benefits, there are also challenges that need to be addressed. Technological advancements play a key role in the industry's future. These conclusions are aligned with the research objectives to understand the broad impacts of gaming.",
    "reflection": "The analysis adequately addresses the original research questions by exploring the key areas of educational, social, and technological impact. However, some segments require further review to ensure complete coverage and to enhance the reliability and validity of the findings."
  }
}

'''

tables = generate_tables_from_response(response_text)
for table in tables:
    print(f"Table Name: {table['table_name']}")
    print(f"Columns: {table['columns']}")
    for row in table['data']:
        print(f"Data: {row}")
    print("\n" + "-" * 50 + "\n")

prompt_table_pairs = [{
    "prompt": "Example User Prompt",
    "tables": tables
}]

# Adjust this path to where your response_table.html is located
template_path = 'C:\\Users\\MM\\PycharmProjects\\QDA-GPT_project\\qda_gpt\\templates\\qda_gpt\\response_table.html'

# Load the HTML template
with open(template_path, 'r') as file:
    template_content = file.read()

# Render the template with the tables data
template = Template(template_content)
rendered_html = template.render(prompt_table_pairs=prompt_table_pairs)

# Save the rendered HTML to a file with UTF-8 encoding
output_path = 'C:\\Users\\MM\\PycharmProjects\\QDA-GPT_project\\qda_gpt\\rendered_response.html'
with open(output_path, 'w', encoding='utf-8') as file:
    file.write(rendered_html)

print(f"HTML rendered and saved to {output_path}")
