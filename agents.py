from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.llms import HuggingFaceEndpoint
from langchain.tools import tool
from langchain_core.prompts import PromptTemplate
import json
import re
import streamlit as st
import os

class CVAgent:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.llm = self._initialize_llm()
        self.tools = self._setup_tools()
        self.prompt = PromptTemplate(
            template="""
            You are an expert CV analysis and career advising agent. Your goal is to analyze a given CV text and provide detailed insights, including strengths, weaknesses, suggested careers, and personalized career roadmaps.
            You have access to the following tools:

            {tools}

            Use the following format for your responses:

            Question: the input question you must answer  
            Thought: you should always think about what to do  
            Action: the action to take, should be one of [{tool_names}]  
            Action Input: the input to the action  
            Observation: the result of the action  
            ... (this Thought/Action/Action Input/Observation can repeat N times)  
            Thought: I now know the final answer  
            Final Answer: the final answer should be a JSON object with keys 'strengths', 'weaknesses', 'suggested_careers', and optionally 'roadmaps'.  

            Begin!

            Question: {input}
            Thought:{agent_scratchpad}
            """,
            input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
        )
        self.agent = self._create_agent()

    def _initialize_llm(self):
        api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        if not api_token and hasattr(st, 'secrets') and "HUGGINGFACEHUB_API_TOKEN" in st.secrets:
            api_token = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
        if not api_token:
            raise ValueError("HUGGINGFACEHUB_API_TOKEN ortam değişkeni veya Streamlit secrets'ta ayarlanmamış.")

        return HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            temperature=0.1,
            max_new_tokens=500,
            huggingfacehub_api_token=api_token
        )

    def _setup_tools(self):
        @tool
        def analyze_cv_text_tool(cv_text: str) -> dict:
            try:
                analysis_prompt = f"""
                You are an expert CV analyst. Analyze the following CV text and identify key strengths, weaknesses, and suggest suitable career paths based on the content. 
                For each strength, weakness, and suggested career, provide a concise explanation.

                CV Text: {cv_text}

                Provide the analysis in the following JSON format:
                {{
                    "strengths": [...],
                    "weaknesses": [...],
                    "suggested_careers": [...]
                }}
                """

                llm_response = self.llm.invoke(analysis_prompt).strip()
                json_match = re.search(r'\{(?:[^{}]|(?R))*\}', llm_response, re.DOTALL)
                if json_match:
                    parsed_output = json.loads(json_match.group(0))
                    for key in ['strengths', 'weaknesses', 'suggested_careers']:
                        if not isinstance(parsed_output.get(key), list):
                            parsed_output[key] = []
                    return parsed_output
                else:
                    print(f"Warning: Invalid JSON format from LLM. Raw output:\n{llm_response}")
                    return self.analyzer.analyze_cv_text(cv_text)
            except Exception as e:
                print(f"Error in analyze_cv_text_tool: {e}")
                return self.analyzer.analyze_cv_text(cv_text)

        @tool
        def get_personalized_roadmap_tool(career_name: str, cv_text: str) -> dict:
            roadmap = self.analyzer.get_roadmap(career_name)
            if roadmap and 'llm_generated' not in roadmap:
                return roadmap
            try:
                roadmap_prompt = f"""
                You are an expert career advisor. Based on the following CV and the desired career path, generate a personalized roadmap.
                Desired Career: {career_name}
                CV Content: {cv_text[:2000]}

                Format:
                {{
                    "adımlar": ["..."],
                    "süre": "...",
                    "kaynaklar": ["..."]
                }}
                """

                llm_response = self.llm.invoke(roadmap_prompt).strip()
                json_match = re.search(r'\{(?:[^{}]|(?R))*\}', llm_response, re.DOTALL)
                if json_match:
                    personalized_roadmap = json.loads(json_match.group(0))
                    personalized_roadmap['llm_generated'] = True
                    return personalized_roadmap
                else:
                    return self.analyzer.get_roadmap(career_name)
            except Exception as e:
                print(f"Error generating roadmap: {e}")
                return self.analyzer.get_roadmap(career_name)

        return [analyze_cv_text_tool, get_personalized_roadmap_tool]

    def _create_agent(self):
        agent_definition = create_react_agent(self.llm, self.tools, self.prompt)
        return AgentExecutor(
            agent=agent_definition,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )

    def run(self, query: str) -> dict:
        try:
            response = self.agent.invoke({"input": query, "agent_scratchpad": ""})
            output_str = response if isinstance(response, str) else response.get("output", "")
            json_match = re.search(r'\{(?:[^{}]|(?R))*\}', output_str, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                return {
                    "error": "Agent output is not valid JSON.",
                    "strengths": [], "weaknesses": [],
                    "suggested_careers": [], "roadmaps": {}
                }
        except Exception as e:
            return {
                "error": f"Agent execution failed: {e}",
                "strengths": [], "weaknesses": [],
                "suggested_careers": [], "roadmaps": {}
            }
