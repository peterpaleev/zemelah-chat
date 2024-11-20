import os
import pandas as pd
from typing import List
from pydantic import BaseModel
from llama_index.core import Document

class ZemelahLoaderConfig(BaseModel):
    database_directory: str

def get_zemelah_documents(config: ZemelahLoaderConfig) -> List[Document]:
    """
    Load documents from CSV files in the specified directory.
    Each CSV should contain at least 'text' and 'url' columns.
    
    Args:
        config (ZemelahLoaderConfig): Configuration containing the database directory path
        
    Returns:
        List[Document]: List of Document objects created from CSV data
    """
    docs = []
    
    # Iterate through all CSV files in the directory
    for filename in os.listdir(config.database_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(config.database_directory, filename)
            
            try:
                # Read CSV file
                df = pd.read_csv(file_path)
                
                # Verify required columns exist
                if 'text' not in df.columns or 'url' not in df.columns:
                    print("Available columns:", df.columns)
                    print(f"Warning: Skipping {filename} - missing required columns (text, url)")
                    continue
                
                # Create documents from each row
                for _, row in df.iterrows():
                    # Create metadata dictionary from all columns except 'text'
                    metadata = {col: row[col] for col in df.columns if col != 'text'}
                    
                    docs.append(
                        Document(
                            text="http://" + row['text'],
                            id_=row['url'],
                            metadata=metadata
                        )
                    )
                
                print(f"Processed {filename}: Added {len(df)} documents")
                
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
