import requests, json
from Webui import WebuiLLM
from langchain.chains.question_answering import load_qa_chain, LLMChain
from langchain import PromptTemplate
import textwrap
def convert_markdown(name, markdown_file_path, api_url):
    with open(markdown_file_path, 'r') as file:
        markdown_content = file.read()

    data = {
        'name': name,
        'markdown': markdown_content
    }

    response = requests.post(api_url, data=data)
    if response.status_code == 200:
        data =""
        r = response.json()
        part = 1
        #print(f"{json.dumps(r, indent=4)}")
        for s in r:
            summary = summarize(s)

            data = textwrap.dedent(f"""
            {data}
            
            ## Part {part}
            {summary} 
            
            """)
            part = part +1

        print(write_article(data, part))
        #json_response = response.json()
        #print(f"{json_response}")
    else:
        print(f"Error occurred: {response.text}")

def write_article(data: str, parts):
    llm = WebuiLLM()
    llm.max_tokens = 1600
    llm.temperature = 0.3
    llm.num_beams = 1
    llm.top_k = 40
    llm.top_p = 0.1
    llm.typical_p = 1
    llm.repetition_penalty = 1.18
    print(data)
    template = """ 
    
    {notes}
    
    Write an article based on the notes above.  The article must ONLY contain information from the notes. The article must 
    be unbiased.  Do not make anything up. Use names, places, numbers, quotes and statements if available in the notes.
    Do not use dates. 
    The article should have an introduction followed by a paragraph for each of the  #PART's.
    DO NOT HALLUCINATE
    Format the article in markdown 
    """

    template = """ 

       {notes}

       Write a report based on the notes above.  The report must ONLY contain information from the notes. The report must 
       be unbiased.  Do not make anything up. Use names, places, numbers, quotes and statements if available in the notes.
       Do not use dates. 
       Fill the report with as many facts as possible from notes
       DO NOT HALLUCINATE
       Format the report in markdown 
       """
    pt= PromptTemplate(
        input_variables=["notes"],
        template=template
    )
    #print(pt.format_prompt(notes=data))
    chain = LLMChain(llm=llm, prompt=pt)
    return chain.run(notes=data)

def summarize(chunk: str):

    llm = WebuiLLM()
    llm.max_tokens = 150
    llm.temperature = 0.2
    llm.num_beams = 1
    llm.top_k = 40
    llm.top_p = 0.1
    llm.typical_p = 1
    llm.repetition_penalty = 1.25
    # Load question answering chain
    #chain = load_qa_chain(llm, chain_type="stuff")


    #print(chunk)
    #exit(0)
    template = """ 
        
    {context}
    
    
    write down a few bullets of the above text. Only use information from the text above. 
    """
    prompt = PromptTemplate(input_variables=["context"], template=template)

    chain = LLMChain(llm=llm, prompt=prompt)

    return chain.run(context=chunk)

if __name__ == '__main__':
    api_url = 'http://localhost:1337/api/embedding'
    markdown_file_path = 'input/trump-jan6.md'
    name = 'memorandum-deferred-enforced-departure-certain-venezuelans'

    convert_markdown(name, markdown_file_path, api_url)