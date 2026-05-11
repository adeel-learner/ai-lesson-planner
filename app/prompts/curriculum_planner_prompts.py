MAIN_PROMPT = """
You are an expert Islamic educator, curriculum designer, and science communicator.

Your role is to generate educational lesson content that integrates:
1. Scientific understanding
2. Critical thinking
3. Reflection
4. Ethical development
5. Islamic spiritual insights

Guidelines:
- Connect scientific concepts with themes encouraged in Islam such as:
  - reflection upon creation
  - gratitude
  - wisdom
  - balance
  - responsibility
  - purpose
  - signs in nature
  - humility
  - beneficial knowledge

- Do NOT make scientifically false claims.
- Do NOT claim science "proves" religion.
- Avoid sectarian debates.
- Avoid fabricated religious references.
- Use respectful and educational language.
- Encourage contemplation and learning.
- When appropriate, connect concepts to Quranic themes such as:
  - observation of creation
  - order in the universe
  - benefit to humanity
  - accountability
  - mercy
  - interconnectedness

Generate content suitable for students and educational environments.
"""

OBJECTIVES_PROMPT = """
Generate detailed learning objectives for the following topic.

Topic: {topic}
Grade Level: {grade_level}
Curriculum Standards: {curriculum}

Requirements:
- Include scientific understanding
- Include critical thinking
- Include ethical reflection
- Include spiritual contemplation encouraged in Islam
- Include appreciation for beneficial knowledge
- Encourage curiosity and observation
"""

EXPLORE_PROMPT = """
Generate an "Explore" section for the following topic.

Topic: {topic}
Grade Level: {grade_level}

Requirements:
- Explain the scientific concepts clearly
- Encourage students to observe patterns, systems, and interconnections
- Include reflective questions related to purpose, balance, and wisdom
- Connect learning with themes encouraged in Islam such as reflection upon creation and gratitude
- Encourage respectful inquiry and contemplation
"""

COMPARE_PROMPT = """
Generate a compare-and-contrast learning section.

Topic: {topic}
Grade Level: {grade_level}

Requirements:
- Compare concepts
- Show similarities and differences
- Include analytical thinking
"""

QUESTION_PROMPT = """
Generate inquiry-based questions.

Topic: {topic}
Grade Level: {grade_level}

Requirements:
- Open-ended questions
- Critical thinking questions
- Reflection questions
"""

CONNECT_PROMPT = """
Generate a "Connect" section that links scientific understanding with Islamic spiritual reflection.

Topic: {topic}
Grade Level: {grade_level}

Requirements:
- Connect the topic with human life and responsibility
- Relate scientific observations to themes encouraged in Islam
- Highlight wisdom, order, balance, and beneficial design
- Encourage gratitude and humility
- Mention how knowledge can benefit humanity
- Avoid unsupported miracle claims
- Avoid pseudo-science
- Keep the tone educational and reflective
"""

APPRECIATE_PROMPT = """
Generate an "Appreciate" section.

Topic: {topic}
Grade Level: {grade_level}

Requirements:
- Discuss the blessings and benefits related to this topic
- Encourage gratitude
- Explain how this knowledge helps humanity
- Include reflection on responsibility and ethical usage
- Encourage appreciation for learning and beneficial technology
"""

ACTIVITIES_PROMPT = """
Generate classroom activities.

Topic: {topic}
Grade Level: {grade_level}

Requirements:
- Interactive activities
- Group activities
- Practical exercises
- Hands-on learning
"""