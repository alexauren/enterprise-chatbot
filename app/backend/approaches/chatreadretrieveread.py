import openai
from approaches.approach import Approach
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from langchain.llms.openai import AzureOpenAI
from langchain.callbacks.manager import CallbackManager, Callbacks
from langchain.chains import LLMChain
from langchain.agents import Tool, AgentType, initialize_agent, ConversationalAgent
from langchain.memory import ConversationBufferMemory
from langchainadapters import HtmlCallbackHandler
from text import nonewlines
from typing import Any, Sequence

class ChatReadRetrieveReadApproach(Approach):
    """
    Attempt to answer questions by iteratively evaluating the question to see what information is missing, and once all information
    is present then formulate an answer. Each iteration consists of two parts:
     1. use GPT to see if we need more information
     2. if more data is needed, use the requested "tool" to retrieve it.
    The last call to GPT answers the actual question.
    This is inspired by the MKRL paper[1] and applied here using the implementation in Langchain.

    [1] E. Karpas, et al. arXiv:2205.00445
    """
    
  

    template_prefix = \
"You are an intelligent assistant. Your name is Floyd. Your job is helping DNB Bank ASA customers with their questions about insurance." \
"If the question is incomplete, ask the user for more information. " \
"If you cannot answer the question using the sources below, stop the thought process, say that you don't know, and that the user should contact customer support. " \
"\n\nYou can access the following tools: "

    memory = ConversationBufferMemory(memory_key = "chat_history")

    template_suffix = """
Begin!

Previous conversation history:
{memory}

New input:
{input}
{agent_scratchpad}"""  

    format_instructions = """To use a tool, please use the following format:

    ```
    Thought: Do I need to use a tool? Yes
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ```
    
    When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:
    
    ```
    Thought: Do I need to use a tool? No
    {ai_prefix}: [your response here]
    """

   
#     query_prompt_template = """Below is a history of the conversation so far, and a new question asked by the user that needs to be answered by searching in a knowledge base about insurance.
#     Generate a search query based on the conversation and the new question. 
#     Do not include cited source filenames and document names e.g info.txt or doc.pdf in the search query terms.
#     Do not include any text inside [] or <<>> in the search query terms.
#     If the question is not in English, translate the question to English before generating the search query.

# Chat History:
# {memory}

# Question:
# {question}

# Search Query:
# """
    #ai_prefix = 

    human_prefix = \
"For information in table format return it as an html table. Do not return markdown format. " \
"Each source has a name followed by colon and the actual data, quote the source name for each piece of data you use in the response. " \
"For example, if the question is \"What color is the sky?\" and one of the information sources says \"info123: the sky is blue whenever it's not cloudy\", then answer with \"The sky is blue [info123]\" " \
"It's important to strictly follow the format where the name of the source is in square brackets at the end of the sentence, and only up to the prefix before the colon (\":\"). " \
"If there are multiple sources, cite each one in their own square brackets. For example, use \"[info343][ref-76]\" and not \"[info343,ref-76]\". " \
"Never quote tool names or chat history as sources." \
"Answer in the same language as the question was asked. "
    
    CognitiveSearchToolDescription = "Useful for searching for public information about DNB insurance car insurance, etc."

    def __init__(self, search_client: SearchClient, openai_deployment: str, sourcepage_field: str, content_field: str):
        self.search_client = search_client
        self.openai_deployment = openai_deployment
        self.sourcepage_field = sourcepage_field
        self.content_field = content_field

    def retrieve(self, q: str, overrides: dict[str, Any]) -> Any:
        use_semantic_captions = True if overrides.get("semantic_captions") else False
        top = overrides.get("top") or 3
        exclude_category = overrides.get("exclude_category") or None
        filter = "category ne '{}'".format(exclude_category.replace("'", "''")) if exclude_category else None

        if overrides.get("semantic_ranker"):
            r = self.search_client.search(q,
                                          filter=filter, 
                                          query_type=QueryType.SEMANTIC, 
                                          query_language="en-us", 
                                          query_speller="lexicon", 
                                          semantic_configuration_name="default", 
                                          top = top,
                                          query_caption="extractive|highlight-false" if use_semantic_captions else None)
        else:
            r = self.search_client.search(q, filter=filter, top=top)
        if use_semantic_captions:
            self.results = [doc[self.sourcepage_field] + ":" + nonewlines(" -.- ".join([c.text for c in doc['@search.captions']])) for doc in r]
        else:
             self.results = [doc[self.sourcepage_field] + ":" + nonewlines(doc[self.content_field][:250]) for doc in r]
        content = "\n".join(self.results)
        return content
    
    def askUser(self, q: str) -> Any:
        return q
        
    def run(self, history: Sequence[dict[str, str]], q: str, overrides: dict[str, Any]) -> Any:
        # Not great to keep this as instance state, won't work with interleaving (e.g. if using async), but keeps the example simple
        self.results = None

        # Use to capture thought process during iterations
        cb_handler = HtmlCallbackHandler()
        cb_manager = CallbackManager(handlers=[cb_handler])
        
        acs_tool = Tool(name="CognitiveSearch", 
                        func=lambda q: self.retrieve(q, overrides), 
                        description=self.CognitiveSearchToolDescription,
                        callbacks=cb_manager)
        ask_user_tool = Tool(name="AskUser",
                        func=lambda q: self.askUser(q),
                        description="Useful for asking the user for more information if the question is incomplete.",
                        callbacks=cb_manager)
        tools = [acs_tool, ask_user_tool]

        prompt = ConversationalAgent.create_prompt(
            tools=tools,
            prefix=overrides.get("prompt_template_prefix") or self.template_prefix,
            suffix=overrides.get("prompt_template_suffix") or self.template_suffix,
            human_prefix=self.human_prefix,
            format_instructions=self.format_instructions,
            input_variables=["input", "agent_scratchpad"],
            memory=self.get_chat_history_as_text(history, include_last_turn=False), question=history[-1]["user"])
        
        print(prompt)
        llm = AzureOpenAI(deployment_name=self.openai_deployment, temperature=overrides.get("temperature") or 0, openai_api_key=openai.api_key)
        chain = LLMChain(llm = llm, prompt = prompt)
        conversational_agent = initialize_agent(
            agent=ConversationalAgent(llm_chain = chain, tools = tools),
            tools=tools, 
            llm=llm,
            verbose=True,
            max_iterations=5,
            memory=ConversationBufferMemory(memory_key = "chat_history"))
        
        result = conversational_agent(q)
                
        # Remove references to tool names that might be confused with a citation
        result = result.replace("[CognitiveSearch]", "")

        return {"data_points": self.results or [], "answer": result, "thoughts": cb_handler.get_and_reset_log()}

    def get_chat_history_as_text(self, history: Sequence[dict[str, str]], include_last_turn: bool=True, approx_max_tokens: int=1000) -> str:
        history_text = ""
        for h in reversed(history if include_last_turn else history[:-1]):
            history_text = """<|im_start|>user""" + "\n" + h["user"] + "\n" + """<|im_end|>""" + "\n" + """<|im_start|>assistant""" + "\n" + (h.get("bot", "") + """<|im_end|>""" if h.get("bot") else "") + "\n" + history_text
            if len(history_text) > approx_max_tokens*4:
                break    
        return history_text