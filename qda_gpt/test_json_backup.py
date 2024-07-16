import json
from collections import OrderedDict
from jinja2 import Template


def generate_tables_from_response(response_text):
    try:
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start == -1 or end == -1:
            raise json.JSONDecodeError("Invalid JSON format", response_text, 0)
        response_text = response_text[start:end]
        response_json = json.loads(response_text, object_pairs_hook=OrderedDict)

        tables = []
        if isinstance(response_json, dict):
            for table_name, records in response_json.items():
                if isinstance(records, list):
                    flattened_data = []
                    for record in records:
                        flattened_records = flatten_record(record)
                        flattened_data.extend(flattened_records)

                    if flattened_data:
                        columns = list(flattened_data[0].keys())
                        data = [[record.get(col, None) for col in columns] for record in flattened_data]
                        tables.append({
                            'table_name': table_name,
                            'columns': columns,
                            'data': data
                        })
        return tables

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def flatten_record(record, parent_key='', sep='_'):
    """Flattens nested dictionaries and lists into a list of dictionaries with repeated keys for nested structures."""
    def recurse(t, parent_key=''):
        if isinstance(t, list):
            for i, item in enumerate(t):
                yield from recurse(item, f"{parent_key}{sep}{i}" if parent_key else str(i))
        elif isinstance(t, dict):
            for k, v in t.items():
                yield from recurse(v, f"{parent_key}{sep}{k}" if parent_key else k)
        else:
            yield parent_key, t

    flattened_data = {}
    for k, v in recurse(record):
        if k in flattened_data:
            if isinstance(flattened_data[k], list):
                flattened_data[k].append(v)
            else:
                flattened_data[k] = [flattened_data[k], v]
        else:
            flattened_data[k] = v

    if any(isinstance(v, list) for v in flattened_data.values()):
        max_len = max(len(v) if isinstance(v, list) else 1 for v in flattened_data.values())
        normalized_data = []
        for i in range(max_len):
            item = {}
            for k, v in flattened_data.items():
                item[k] = v[i] if isinstance(v, list) and i < len(v) else v
            normalized_data.append(item)
        return normalized_data

    return [flattened_data]

# Example usage
response_text = '''
{
    "Codes": [
        {
            "index": 1,
            "code_name": "Game-based Learning",
            "definition": "Instances where games are utilized as educational tools within formal learning environments to enhance the learning experience. This includes activities where games are integrated into the curriculum to facilitate learning in subjects such as languages, safety training, or skill-building. It focuses on the use of interactive game elements to improve engagement and knowledge retention in educational settings. It differs from general gaming experiences by emphasizing the structured and intentional use of games for educational purposes.",
            "higher_level_category": "Role of Video Games in Education",
            "quote": "We can use games in such aspects and I see that's a sort of implement, and also, yeah, it's a good tool if you use it in this aspect rather than entertainment."
        },
        {
            "index": 2,
            "code_name": "Gamification Strategy",
            "definition": "Refers to the strategic application of game design elements, such as points, progress tracking, and rewards, to non-game contexts to enhance engagement and motivation. It highlights the use of game-like features in activities like language learning apps, safety training, and skill development programs. The focus is on how game elements can be employed to make tasks more interactive, engaging, and effective, particularly in educational and informational settings. This code differs from traditional gaming experiences by emphasizing the intentional integration of game mechanics into non-game environments.",
            "higher_level_category": "Technological Trends",
            "quote": "So, gamification sits well with strategy. So, how we include points and how we make players progress with that, it goes more with the strategy."
        },
        {
            "index": 3,
            "code_name": "Ethical Concerns in Gaming",
            "definition": "Addresses issues related to morality, safety, and privacy within the gaming industry, including age restrictions, data privacy, and personal safety. It encompasses discussions on the ethical implications of violent gameplay, age-inappropriate content, and data collection practices in games. This code focuses on the ethical dilemmas that arise from gaming experiences and the need for responsible design and regulation in the industry. It differs from general gaming discussions by centering on the ethical considerations unique to gaming environments.",
            "higher_level_category": "Ethical and Social Issues",
            "quote": "I feel we should have a second thought with games that require your personal data, such as location, camera and your mobile, access to your personal folder. So I feel a game shouldn't have these things."
        },
        {
            "index": 4,
            "code_name": "Player Engagement and Immersion",
            "definition": "Refers to the level of involvement, interest, and absorption experienced by players within gaming environments. It includes aspects of gameplay that captivate and engage players, leading to deep immersion and enjoyment. This code focuses on the immersive nature of games as a medium that can deeply involve and interact with players. It differs from other aspects by highlighting the player's experience of being engrossed and deeply connected to the game world.",
            "higher_level_category": "Cultural Impact of Gaming",
            "quote": "Definitely games have an ability to immerse people, so, compared to other mediums, they can actually talk with the player and they can bring the player into the context."
        }
    ],
    "Categories": [
        {
            "index": 1,
            "name": "Educational Use of Games",
            "definition": "This category includes codes related to the application of games as tools for educational purposes within formal learning contexts. It encompasses the use of games to facilitate learning, enhance engagement, and improve knowledge retention. The purpose is to explore how games are utilized in educational settings to support and enhance the learning process. Requirements for a topic to be identified within this category include discussions on the structured integration of games within educational curricula and their impact on learning outcomes.",
            "description": "Relevant to understanding the role of video games in education and how they can be leveraged to improve teaching and learning practices.",
            "code_requirements": "Codes related to game-based learning and gamification strategy.",
            "codes": [1, 2]
        },
        {
            "index": 2,
            "name": "Technological Advancements in Gaming",
            "definition": "This category encompasses codes discussing advancements and trends in gaming technology, including virtual reality, augmented reality, and artificial intelligence integration. It focuses on the evolution of technology within the gaming industry and its impact on gameplay experiences. The purpose is to explore how technological innovations shape the gaming landscape and player interactions. Requirements for topics to be included in this category are discussions on technological advancements specific to gaming and their implications.",
            "description": "Relevant to understanding the technological progress within the gaming industry and its influence on game development and player experiences.",
            "code_requirements": "Codes related to discussions on technological trends and innovations in gaming.",
            "codes": [2]
        },
        {
            "index": 3,
            "name": "Social and Ethical Considerations",
            "definition": "This category covers codes addressing social dynamics, ethical dilemmas, and concerns within the gaming domain, such as addiction, violence, privacy, and data security. It includes discussions on the impact of gaming on society, ethical design practices, and user safety. The purpose is to explore the ethical and social implications of gaming activities and industry practices. Topics must focus on the societal and ethical aspects of gaming to be categorized here.",
            "description": "Relevant to examining the ethical challenges and social impacts of gaming, providing insights into the broader implications of gaming on individuals and society.",
            "code_requirements": "Codes related to ethical concerns in gaming and player engagement and immersion.",
            "codes": [3, 4]
        }
    ],
    "Themes": [
        {
            "index": 1,
            "name": "Educational Impact of Gaming",
            "definition": "This theme explores how video games are utilized for educational purposes and their impact on learning outcomes. It includes categories related to game-based learning and gamification strategies in educational settings. The purpose is to examine the effectiveness of using games for teaching and learning, as well as their role in enhancing educational experiences. Requirements for this theme include a focus on the educational applications of games and their implications for learning.",
            "description": "Relevant to understanding the potential of video games in formal education and their role in engaging and educating students effectively.",
            "category_requirements": "Categories related to the educational use of games.",
            "categories": [1]
        },
        {
            "index": 2,
            "name": "Technological and Ethical Considerations in Gaming",
            "definition": "This theme addresses the intersection of technological advancements and ethical issues within the gaming industry. It encompasses categories discussing technological trends in gaming, along with social and ethical concerns related to gaming activities. The purpose is to explore how technological progress influences ethical decision-making and societal impacts in gaming. Requirements for this theme include discussions on both technological innovations and ethical considerations.",
            "description": "Relevant to examining how technological advancements shape gaming experiences and the ethical challenges that arise in gaming environments.",
            "category_requirements": "Categories related to technological advancements in gaming and social/ethical considerations in gaming.",
            "categories": [2, 3]
        },
        {
            "name": "Educational Potential of Games",
            "definition": "This theme focuses on the role of video games as educational tools, exploring how games can be utilized for learning new skills, languages, or topics. It delves into the effectiveness of gamification in educational settings and the immersive nature of games for conveying information. A key requirement for this theme is the examination of how games can engage and educate players in various subjects.",
            "references": "The concept of gamification and its educational applications have been studied by Deterding et al. (2011). Gee (2003) emphasizes the potential of games to facilitate learning and problem-solving skills. Additionally, research by Sivan (2010) discusses the effectiveness of game-based learning strategies.",
            "description": "This theme is crucial for understanding how video games can serve as effective educational tools and platforms for learning diverse subjects."
        },
        {
            "name": "Ethical Dimensions of Gaming",
            "definition": "This theme addresses ethical concerns related to video games, such as age restrictions, violence, data privacy, and potential addiction. It encompasses discussions on the influence of game content on player behavior, the necessity of age-appropriate gaming experiences, and the collection of personal data by games. Exploring the ethical considerations in gaming environments is essential for understanding the impact of video games on individuals and society.",
            "references": "The ethical implications of violent video games have been studied extensively, with research by Anderson et al. (2010) highlighting the effects of game violence on behavior. Moor & Heidbrink (2008) discuss ethical issues in gaming, including privacy concerns. Additionally, Griffiths (2010) addresses the addictive potential of gaming.",
            "description": "This theme contributes to the examination of ethical dilemmas within the gaming industry and the implications of gameplay on individuals' behavior and well-being."
        },
        {
            "name": "Social Interactions in Gaming Communities",
            "definition": "This theme explores the social dynamics within gaming communities, including aspects of toxicity, collaboration, and community engagement. It involves discussions on online interactions, player behaviors, and the challenges of maintaining positive gaming environments. A key aspect of this theme is understanding how social interactions shape players' experiences and the community culture within different games.",
            "references": "The phenomenon of toxic behavior in online gaming communities has been extensively studied, with works by Lee et al. (2020) examining strategies to address toxicity. Smith & McLean (2019) discuss the role of social interactions in gaming communities. Virtual community research by Rheingold (1994) is relevant in understanding online social dynamics.",
            "description": "This theme provides insights into the social aspects of gaming, including how interactions impact player experiences, community cohesion, and the overall gaming environment."
        },
        {
            "index": 1,
            "name": "Educational Potential of Games",
            "definition": "This theme encompasses the role of video games as educational tools and their impact on learning outcomes. It explores the effectiveness of gamification strategies and the immersive nature of games in teaching various subjects. The theme emphasizes how games can engage and educate players to enhance learning experiences.",
            "description": "Relevant to understanding the educational value of games in formal education and their potential in improving teaching and learning practices."
        },
        {
            "index": 2,
            "name": "Ethical and Social Impact of Gaming",
            "definition": "This theme addresses the ethical concerns and social dynamics within the gaming domain. It includes discussions on age restrictions, violence, privacy, data security, and community engagement. The theme explores how gaming impacts social interactions, raises ethical questions, and shapes individual behaviors and societal values.",
            "description": "Relevant to examining the ethical dilemmas and societal impacts of gaming, providing insights into the broader ethical considerations and social dynamics inherent in gaming environments."
        },
        {
            "index": 3,
            "name": "Technological Trends and Impact",
            "definition": "This theme focuses on technological advancements in gaming and their economic implications. It encompasses discussions on virtual reality, augmented reality, artificial intelligence integration, and gamification strategies. The theme explores how technological innovations shape the gaming industry, player experiences, and economic trends.",
            "description": "Relevant to understanding the impact of technological progress on the gaming landscape, game development, and player interactions, highlighting the evolving technological trends and their economic significance."
        }
    ],
    "ThemeCategoryHierarchy": [
        {
            "theme_index": 1,
            "theme_name": "Educational Potential of Games",
            "categories": [
                {
                    "category_index": 1,
                    "category_name": "Game-based Learning"
                }
            ]
        },
        {
            "theme_index": 2,
            "theme_name": "Ethical and Social Impact of Gaming",
            "categories": [
                {
                    "category_index": 3,
                    "category_name": "Ethical and Social Issues"
                }
            ]
        },
        {
            "theme_index": 3,
            "theme_name": "Technological Trends and Impact",
            "categories": [
                {
                    "category_index": 2,
                    "category_name": "Technological Trends"
                }
            ]
        }
    ],
    "CategoryCodeHierarchy": [
        {
            "category_index": 1,
            "category_name": "Educational Use of Games",
            "codes": [
                {
                    "code_index": 1,
                    "code_name": "Game-based Learning"
                }
            ]
        },
        {
            "category_index": 2,
            "category_name": "Technological Advancements in Gaming",
            "codes": [
                {
                    "code_index": 2,
                    "code_name": "Gamification Strategy"
                }
            ]
        },
        {
            "category_index": 3,
            "category_name": "Social and Ethical Considerations",
            "codes": [
                {
                    "code_index": 3,
                    "code_name": "Ethical Concerns in Gaming"
                }
            ]
        },
        {
            "category_index": 4,
            "category_name": "Player Engagement and Immersion",
            "codes": [
                {
                    "code_index": 4,
                    "code_name": "Player Engagement and Immersion"
                }
            ]
        }
    ],
    "Overall_Findings": {
        "summary_title": "Key Insights on Gaming Dynamics",
        "description": "Analyzing the educational, ethical, social, and technological aspects of gaming unveils diverse impacts and considerations within the gaming domain.",
        "flagged_segments": "No flagged segments identified.",
        "analysis_and_interpretation": "The themes collectively provide a comprehensive view of the multifaceted nature of gaming, encompassing education, ethics, social interactions, and technological advancements.",
        "conclusions_and_implications": "The analysis reveals that gaming extends beyond entertainment, influencing education, ethics, and technology. Recognition of these diverse impacts is crucial for ensuring the responsible and beneficial development of the gaming industry.",
        "reflection": "The analysis effectively addresses the research questions by exploring various dimensions of gaming, offering insights into its impact on education, ethics, and technology, providing a robust understanding of the gaming landscape."
    },
    "Initial Codes": [
        {
            "index": 1,
            "initial_code_name": "Frustration with management communication",
            "data_fragment": "I'm really frustrated with how poorly management communicates.",
            "description": "The participant's feelings of frustration due to inadequate communication from management."
        },
        {
            "index": 2,
            "initial_code_name": "Unheard concerns",
            "data_fragment": "I feel like no one listens to my concerns.",
            "description": "The participant's perception that their issues and concerns are not being acknowledged or addressed by management."
        },
        {
            "index": 3,
            "initial_code_name": "Overwhelmed by workload",
            "data_fragment": "It's just too much sometimes, you know? Like, I'm constantly juggling tasks and there's never enough time to actually focus on any one thing. I end up doing everything half-heartedly because I'm spread so thin.",
            "description": "The participant feels overwhelmed by their workload, resulting in a lack of focus and quality in their work."
        },
        {
            "index": 4,
            "initial_code_name": "Lack of resources",
            "data_fragment": "We don't have the tools we need to do our jobs properly, it's like we're expected to build a house with a spoon.",
            "description": "The participant is expressing frustration over the lack of necessary resources to perform their job effectively."
        }
    ],
    "Subcategories": [
        {
            "subcategory_index": 1,
            "subcategory_name": "Management Communication Issues",
            "description": "Problems related to the frequency and clarity of communication from management.",
            "properties": ["frequency", "clarity"],
            "dimensions": ["infrequent to frequent", "unclear to clear"],
            "initial_codes": [
                {
                    "index": 1,
                    "initial_code_name": "Frustration with management communication",
                    "rationale": "This code reflects issues with the frequency and clarity of communication from management."
                },
                {
                    "index": 2,
                    "initial_code_name": "Unheard concerns",
                    "rationale": "This code captures the lack of effective communication from management, leading to employees feeling unheard."
                }
            ]
        },
        {
            "subcategory_index": 2,
            "subcategory_name": "Workload Challenges",
            "description": "Challenges related to the intensity of workload and the support provided.",
            "properties": ["intensity", "support"],
            "dimensions": ["low to high", "insufficient to sufficient"],
            "initial_codes": [
                {
                    "index": 3,
                    "initial_code_name": "Overwhelmed by workload",
                    "rationale": "This code describes the intensity of the workload and the lack of support felt by the participant."
                },
                {
                    "index": 4,
                    "initial_code_name": "Lack of resources",
                    "rationale": "This code reflects challenges related to insufficient resources needed to manage the workload effectively."
                }
            ]
        }
    ],
    "Categories": [
        {
            "category_index": 1,
            "category_name": "Communication Issues",
            "description": "Broad issues related to communication within the organization, including both management and employee communication.",
            "properties": ["clarity", "frequency"],
            "dimensions": ["unclear to clear", "infrequent to frequent"],
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
            "properties": ["workload intensity", "resource support"],
            "dimensions": ["low to high", "insufficient to sufficient"],
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
    "Core Categories": [
        {
            "core_category_index": 1,
            "core_category_name": "Work-Life Balance",
            "description": "Central theme related to balancing professional responsibilities with personal life while working remotely.",
            "requirements": "Frequent in the data, integrates multiple categories, broadly applicable, and central to the research question.",
            "theoretical_framework": "Work-life balance is influenced by various factors, including flexible work schedules and boundary management. These factors collectively enhance overall satisfaction and productivity.",
            "theoretical_statements": [
                "Flexible work schedules improve work-life balance.",
                "Effective boundary management is crucial for maintaining work-life balance."
            ],
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
            "theoretical_statements": [
                "Effective use of technology enhances remote work productivity.",
                "Clear communication practices are crucial for maintaining productivity in a remote work environment."
            ],
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
    "Theoretical Coding": [
        {
            "core_category_index": 1,
            "coreCategoryName": "Employee Well-being",
            "relationships": [
                "Leadership Support → Emotional Support: Effective leadership practices foster a supportive team environment, enhancing emotional support among peers.",
                "Emotional Support ↔ Professional Development: A supportive team environment encourages employees to engage in professional development opportunities.",
                "Professional Development → Employee Well-being: Access to training and career advancement opportunities directly contributes to higher job satisfaction and overall well-being.",
                "Work-Life Balance → Employee Well-being: Flexible work arrangements help employees manage stress and improve their overall well-being."
            ],
            "theoretical_codes": [
                "If leadership provides guidance and mentoring, then team cohesion and peer empathy will improve.",
                "Because a supportive team environment exists, employees are more likely to participate in professional development.",
                "Professional development opportunities lead to increased job satisfaction and well-being.",
                "Flexible work hours reduce stress, which is part of improving overall employee well-being."
            ],
            "theoretical_framework": {
                "Leadership Support": "Leads to Emotional Support and Professional Development.",
                "Emotional Support": "Reduces stress and increases job satisfaction.",
                "Professional Development": "Enhances sense of growth and job satisfaction.",
                "Work-Life Balance": "Reduces burnout and enhances job satisfaction."
            },
            "narrativeDescription": "Leadership practices such as mentoring and providing feedback play a crucial role in fostering a supportive team environment. This environment enhances emotional support among employees, reducing stress and increasing job satisfaction. Additionally, opportunities for professional development contribute to a sense of growth and achievement, further enhancing well-being. Work-life balance, facilitated by flexible work arrangements, helps reduce burnout and improve overall job satisfaction. Together, these factors create a comprehensive framework for understanding and improving employee well-being in the workplace."
        }
    ],
    "Theory Development": [
        {
            "coreCategoryIndex": 1,
            "coreCategoryName": "Employee Well-being",
            "Theoretical Statements": [
                "Effective leadership practices foster a supportive team environment, enhancing emotional support among peers.",
                "A supportive team environment encourages employees to engage in professional development opportunities.",
                "Access to training and career advancement opportunities directly contributes to higher job satisfaction and overall well-being.",
                "Flexible work arrangements help employees manage stress and improve their overall well-being."
            ],
            "discrepancies_statements": [
                "Professional Development → Employee Well-being: Lack of supporting evidence from a subset of participants because some participants did not have access to training programs."
            ],
            "discrepancies_relationships": [
                "Emotional Support ↔ Professional Development: Inconsistent evidence across different departments due to varying levels of team support in different departments."
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
    "Overall_Findings": {
        "cohesive_narrative": "The theoretical concepts of Intrinsic Motivation and Workplace Dynamics are pivotal in understanding the effectiveness of leadership development programs and wellbeing initiatives. By integrating these concepts, we gain a holistic view of the factors contributing to enhanced employee satisfaction and organizational performance.",
        "relationships_and_connections": "Intrinsic Motivation and Workplace Dynamics are interrelated, with personal growth and self-fulfillment being closely tied to the quality of workplace interactions and leadership practices. Effective leadership not only fosters a positive work environment but also amplifies intrinsic motivation, creating a virtuous cycle of employee engagement and productivity.",
        "comprehensive_model": "The integrated model demonstrates the interplay between leadership development, employee wellbeing, and organizational success. Leadership programs improve workplace dynamics, fostering a supportive environment that enhances intrinsic motivation and overall employee wellbeing. This, in turn, leads to improved organizational performance.",
        "conclusions_and_implications": "The findings underscore the critical role of leadership development and employee wellbeing in driving organizational success. Effective leadership practices not only enhance workplace dynamics but also boost intrinsic motivation, leading to higher employee satisfaction and productivity. Organizations should invest in continuous leadership training and comprehensive wellbeing programs to sustain and improve performance. Furthermore, the data suggests that fostering a culture of growth and support can significantly impact overall job satisfaction and retention rates."
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