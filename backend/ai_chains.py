from typing import List, Optional

from langchain.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from ai_models import GPT3, GPT4

constraint_prompt = ChatPromptTemplate.from_template(\
    "You are an agent with the sole purpose of creating matchups for sports league schedule making.\
    You must generate two lists. One for the match-ups that MUST happen. And one for the match-ups that MUST NOT happen.\
    For each matchup you MUST give the two teams involved in that matchup and the stadium it should be played at.\
    The two teams MUST be different.\
    If the stadium doesn't matter, return an empty string for the stadium.\
    The stadium each game is played at MUST match a home field of one of the teams listed.\
    Teams and corresponding stadiums and divisions: {teams}\
    Here are the constraints: {constraints}\
    "
)

class Matchup(BaseModel):
    team1: Optional[str] = Field(default='', description='The team name of one team in this required matchup')
    team2: Optional[str] = Field(default='', description='The team name of the other team in this required matchup')
    stadium: Optional[str] = Field(default='', description='Stadium at which this required matchup should take place. If it does not matter, return the default value')

class ScheduleData(BaseModel):
    required_matchups: List[Matchup]
    prohibited_matchups: List[Matchup]

constraint_chain = constraint_prompt | GPT4.with_structured_output(schema=ScheduleData)
