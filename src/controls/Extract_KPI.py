import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.document_loaders.text import TextLoader
from pydantic import BaseModel ,Field
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from dotenv import dotenv_values
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json


def extract_kpis(file_name,llm):
    base_dir = os.path.dirname(os.path.dirname(__file__))

    text_path = os.path.join(base_dir, "assets", "files", file_name, "output_text", "all_text.txt")

    loader = TextLoader(text_path, encoding='utf-8')
    all_text=loader.load()

   
    text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=2000,
    chunk_overlap=200,
    length_function=len,
    # is_separator_regex=False,
    separators=[
        "\n\n",
        "\n",
        " ",
        ".",
        ",",
        "\u200b",  # Zero-width space
        "\uff0c",  # Fullwidth comma
        "\u3001",  # Ideographic comma
        "\uff0e",  # Fullwidth full stop
        "\u3002",  # Ideographic full stop
        "",
    ],
    )
   
    meta_data={"document":file_name}
    chunks = text_splitter.create_documents([all_text[0].page_content],metadatas=[meta_data])

    class pairs(BaseModel):
        
        KPI: str = Field(description="A KPI identified within a text.")
        context: str = Field(description="An Arabic context that can be used to extract the identified KPIs from a text.")

    parser=PydanticOutputParser(pydantic_object=pairs)

    temp="\n".join([

        "قم بتقسيم النص العربي التالي إلى جمل واستخرج مؤشرات الأداء الرئيسية (KPIs) من كل جملة.", 
    "يجب أن تتضمن مؤشرات الأداء الرئيسية بيانات رقمية، أو مقاييس أداء، أو معلومات إحصائية تتعلق بالعوامل البيئية. ",
    "إذا لم تكن مؤشرات الأداء الرئيسية واردة في الجملة ،تخطي هذة الجملة'"
    

        "### text:",
        "{text}",
        "{format_instructions}",
    ])

    prompt=PromptTemplate(
        template=temp,
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    result_all=[]
    for chunk in chunks:
        message_all = prompt.format(text=chunk.page_content)
        result=llm( message_all )
        result_all.append(result.split("\n"))


    
    json_objects = []

    for block in result_all:
        for line in block:
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                json_object = json.loads(line)
                json_objects.append(json_object)

    filtered_data = [entry for entry in json_objects if entry["KPI"] is not None]
    # output_json = json.dumps(filtered_data, ensure_ascii=False, indent=2)
    # print(output_json)

    return filtered_data