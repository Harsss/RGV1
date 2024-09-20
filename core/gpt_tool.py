from langchain_core.output_parsers import StrOutputParser
import langchain_core.output_parsers 
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,)
import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
from kor.extraction import create_extraction_chain

# ChatGroq=None

class gpt_toolbox:
    @staticmethod
    def general_llm_call(query, api_key, llm_name, prompt1=None, few_shots=None, output_parser=StrOutputParser()):
        """
        Invokes a specified large language model (LLM) to process a given query. This method initializes the chosen LLM based on the provided `llm_name` and constructs a prompt that may include a system message and few-shot examples, if provided.

        Parameters:
        - query (str): The user input or question that needs to be processed by the LLM.
        - api_key (str): The API key required to authenticate and invoke the specified LLM.
        - llm_name (str): The name of the large language model to be used. Valid options are 'chatgpt', 'mixtral', or 'llama3'. 
          Each of these models requires specific initialization and configuration.
        - prompt1 (str, optional): An initial message or context to be included as part of the prompt to the LLM. This is useful for setting the context or providing a specific instruction to the model. Defaults to None.
        - few_shots (list of tuples, optional): Examples of few-shot learning that provide the model with context or examples of the desired task format. Each tuple should contain a pair of ('human', input) and ('ai', expected output). Defaults to None.
        - output_parser (object, optional): An instance of a parser class used to parse and format the output from the LLM. The default parser is `StrOutputParser`, which converts outputs to strings.

        Returns:
        - response (str): The processed output from the LLM as formatted by the `output_parser`.

        Raises:
        - ValueError: If an unsupported `llm_name` is provided.

        Example:
        >>> toolbox = gpt_toolbox()
        >>> response = toolbox.miscellaneous("What is AI?", "your_api_key_here", "chatgpt", "Please answer briefly:", [("What is machine learning?", "Machine learning is a subset of AI")])
        >>> print(response)
        'AI refers to systems or machines that mimic human intelligence to perform tasks and can iteratively improve themselves based on the information they collect.'
        """
        # Validate llm_name
        
        if llm_name not in ["chatgpt", "mixtral", "llama3"]:
            raise ValueError("llm_name should be either 'chatgpt', 'mixtral', or 'llama3'")
        
        # Initialize the appropriate LLM based on llm_name
        if llm_name == "chatgpt":
            llm = ChatOpenAI(api_key=api_key)
        elif llm_name == "mixtral":
            llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="mixtral-8x7b-32768")
        elif llm_name == "llama3":
            llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="llama3-70B-8192")
        elif llm_name == "llama-chota":
            llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="llama3-8B-8192")
        else: 
            llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name=llm_name)

        # Build prompt components
        prompt = [("system", prompt1)] if prompt1 else []
        
        # Create and add few-shot prompt if examples are provided
        if few_shots:
            example_prompt = ChatPromptTemplate.from_messages([
                ("human", "{input}"),
                ("ai", "{output}"),
            ])
            few_shot_prompt = FewShotChatMessagePromptTemplate(
                example_prompt=example_prompt,
                examples=few_shots,
            )
            prompt.append(few_shot_prompt)
        
        # Add user query to the prompt
        prompt.append(("human", query))

        # Construct the runnable chain
        runnable = (prompt | llm | output_parser)
        
        # Invoke the runnable and return the response
        response = runnable.invoke(query)
        return response









def invoke_llm(query, api_key, llm_name, prompt1="", few_shots=None, output_parser=StrOutputParser()):
        """
        Invokes a specified large language model (LLM) to process a given query. This method initializes the chosen LLM based on the provided `llm_name` and constructs a prompt that may include a system message and few-shot examples, if provided.

        Parameters:
        - query (str): The user input or question that needs to be processed by the LLM.
        - api_key (str): The API key required to authenticate and invoke the specified LLM.
        - llm_name (str): The name of the large language model to be used. Valid options are 'chatgpt', 'mixtral', or 'llama3'. 
          Each of these models requires specific initialization and configuration.
        - prompt1 (str, optional): An initial message or context to be included as part of the prompt to the LLM. This is useful for setting the context or providing a specific instruction to the model. Defaults to None.
        - few_shots (list of tuples, optional): Examples of few-shot learning that provide the model with context or examples of the desired task format. Each tuple should contain a pair of ('human', input) and ('ai', expected output). Defaults to None.
        - output_parser (object, optional): An instance of a parser class used to parse and format the output from the LLM. The default parser is `StrOutputParser`, which converts outputs to strings.

        Returns:
        - response (str): The processed output from the LLM as formatted by the `output_parser`.

        Raises:
        - ValueError: If an unsupported `llm_name` is provided.

        Example:
        >>> toolbox = gpt_toolbox()
        >>> response = toolbox.miscellaneous("What is AI?", "your_api_key_here", "chatgpt", "Please answer briefly:", [("What is machine learning?", "Machine learning is a subset of AI")])
        >>> print(response)
        'AI refers to systems or machines that mimic human intelligence to perform tasks and can iteratively improve themselves based on the information they collect.'
        """
        # Validate llm_name
        
        # if llm_name not in ["chatgpt", "mixtral", "llama3","openai_ch"]:
        #     llm_name='chatgpt'
            # raise ValueError("llm_name should be either 'chatgpt', 'mixtral', or 'llama3'")
        
        # Initialize the appropriate LLM based on llm_name
        if llm_name == "chatgpt":
            llm = ChatOpenAI(api_key=api_key)
        elif llm_name == "openai_ch":
            llm = ChatOpenAI(api_key=api_key,model="gpt-4o")
        elif llm_name == "openai_mini":
            llm = ChatOpenAI(api_key=api_key,model="gpt-4o-mini")
        elif llm_name == "mixtral":
            print('we are using mistral')
            llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="mixtral-8x7b-32768")
        elif llm_name == "llama3":
            llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="llama3-70B-8192")
        elif llm_name == "llama-chota":
            llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="llama3-8B-8192")
        else: 
            llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name=llm_name)
        
        # Create and add few-shot prompt if examples are provided
        if few_shots:
            example_prompt = ChatPromptTemplate.from_messages([
                ("human", "{input}"),
                ("ai", "{output}"),
            ])
            few_shot_prompt = FewShotChatMessagePromptTemplate(
                example_prompt=example_prompt,
                examples=few_shots,
            )
        else:
            few_shot_prompt=""
        prompt = ChatPromptTemplate.from_messages(
        [
        (
            "system", prompt1
        )
        ,
        few_shot_prompt
        ,
        ("human", "{query}"),
    ]
    )

        runnable = (prompt | llm | output_parser)
        # print(type(runnable))
        print(llm)
        # Invoke the runnable and return the response
        response = runnable.invoke(query)
        return response




def invoke_chain(query,product_schema,llm='openai',encoder_cls='json',input_formatter=None):
    if llm=='openai':
        print(1)
        openai_api=os.getenv('OPENAI_API_KEY')
        llm = ChatOpenAI(api_key=openai_api)
    chain = create_extraction_chain(
    llm, product_schema, encoder_or_encoder_class=encoder_cls, input_formatter=input_formatter
    )
    response = chain.invoke(query)
    return response["text"]["data"]