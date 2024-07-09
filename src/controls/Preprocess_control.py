from langchain_community.document_loaders.text import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
import os





def Text_process(all_text,file_name):

    base_dir = os.path.dirname(os.path.dirname(__file__))

    text_path = os.path.join(base_dir, "assets", "files", file_name, "output_text", "all_text.txt")


    loader = TextLoader(text_path, encoding='utf-8')
    all_text=loader.load()

    # print(all_text)

    text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=500,
    chunk_overlap=50,
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

   
    MOdels_dir = os.path.join(base_dir, "assets", "models")
    model_path= os.path.join(MOdels_dir,"paraphrase_multilingual_MiniLM_model")
    encode_kwargs = {'normalize_embeddings': True}
    llm_embedding = SentenceTransformerEmbeddings(model_name=model_path,encode_kwargs=encode_kwargs)
    

    save_to_dir = os.path.join(base_dir, "assets", "files", file_name,"wiki_chroma_db")
    # vector database
    # save_to_dir = "wiki_chroma_db"
    docs_ids=list(range(len(chunks)))
    docs_ids=[str(d) for d in docs_ids]
    vector_db = Chroma.from_documents(
        chunks,
        llm_embedding,
        persist_directory=save_to_dir,
        ids=docs_ids
    )

    return vector_db
    

def retrieve_information(model,vector_db,question):

    similar_docs=vector_db.similarity_search(question,k=4)
    qna_template = "\n".join([
    "أجب عن السؤال التالي باللغة العربية باستخدام المعلومات المقدمة",
    "إذا لم تكن الإجابة واردة في السياق، فقل'لا توجد إجابة متاحة'",
    "### المعلومات",
    "{context}",
    "",
    "### السؤال:",
    "{question}",
    "",
    "### الاجابة:",
    ])


    qna_prompt=PromptTemplate(
        template=qna_template,
        input_variables=["context","question"],
        verbose=True
    )

    stuff_chain = load_qa_chain(model, chain_type="stuff", prompt=qna_prompt)
    answer=stuff_chain(
    {
        "input_documents":similar_docs,
        "question": question
    },
     return_only_outputs=False,
    )
    return answer
            

# if __name__ == "__main__":
#     pdf_path = "Enviromental_factors_egypt_arabic.pdf"
#     output_folder = 'src/asset/output_images'
#     output_txt_files_path = 'src/asset/output_text/Enviromental_factors_egypt_arabic'
#     Text_process(pdf_path, output_folder)