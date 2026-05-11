from ..ai_curriculum_planner import AICurriculumPlanner
import time

start_time = time.time()

user_input = {
    "topic": "Photosynthesis",
    "grade_level": "5th Grade",
    "curriculum": "Next Generation Science Standards (NGSS)",
}

planner = AICurriculumPlanner(user_input=user_input)
response = planner.mainChain()  
print("Response:", response)
end_time = time.time()
print(f"Execution Time: {end_time - start_time} seconds")   

