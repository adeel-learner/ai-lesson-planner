###import section
import json
# from .utils.token_counter import TokenCounterHandler
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from app.prompts import curriculum_planner_prompts
from app.configuration.llm_service import get_llm



class AICurriculumPlanner:
    def __init__(self, user_input, llm_provider='GROQ'):
        self.user_input = user_input
        self.llm_provider = llm_provider
        # self.token_counter = TokenCounterHandler()
        self.handler = StreamingStdOutCallbackHandler()
        self.prompt = PromptTemplate(
            template=curriculum_planner_prompts.MAIN_PROMPT + "\n\n" + curriculum_planner_prompts.OBJECTIVES_PROMPT,
            input_variables=["topic", "grade_level"],
            )
        self.llm_model = get_llm(llm_provider=self.llm_provider)
    

    def mainChain(self):
        main_chain = (
                self.prompt.partial(
                    grade_level=self.user_input.get("grade_level"),
                    curriculum=self.user_input.get("curriculum")
                )
                | self.llm_model
                | StrOutputParser()
            )
        
        response = main_chain.invoke(
                {"topic": self.user_input.get("topic")}, {"callbacks": [self.handler]}
            )

        return response
    

    