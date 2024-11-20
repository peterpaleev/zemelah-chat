import os
import pandas as pd
from typing import List
from pydantic import BaseModel
from llama_index.core import Document
import json

class ZemelahLoaderConfig(BaseModel):
    database_directory: str

def get_zemelah_documents(config: ZemelahLoaderConfig) -> List[Document]:
    """
    Load documents from JSON files in the specified directory.
    Each JSON file should contain an array of objects with at least 'cleaned_text' and 'url' fields.
    
    Args:
        config (ZemelahLoaderConfig): Configuration containing the database directory path
        
    Returns:
        List[Document]: List of Document objects created from JSON data
    """
    docs = []
    
    # Iterate through all JSON files in the directory
    for filename in os.listdir(config.database_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(config.database_directory, filename)
            
            try:
                # Read JSON file
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                # Create documents from each object in the JSON array
                for item in data:
                    # Verify required fields exist
                    if 'cleaned_text' not in item or 'url' not in item:
                        print(f"Warning: Skipping item in {filename} - missing required fields (cleaned_text, url)")
                        continue
                    
                    # Create metadata dictionary from all fields except 'cleaned_text'
                    metadata = {key: value for key, value in item.items() if key != 'cleaned_text'}
                    
                    docs.append(
                        Document(
                            text=item['cleaned_text'],
                            id_=item['url'],
                            metadata=metadata
                        )
                    )
                
                print(f"Processed {filename}: Added {len(data)} documents")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue
    
    # Debug information
    print("\n=== Documents Structure ===")
    print(f"Total number of documents: {len(docs)}")
    if docs:
        print("\nSample document structure:")
        print(f"Type: {type(docs[0])}")
        print(f"Metadata: {docs[0].metadata}")
        print(f"Text preview: {docs[0].text[:100]}...")
    
    return docs
