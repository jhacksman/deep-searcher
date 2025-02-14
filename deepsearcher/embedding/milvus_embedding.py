from typing import List
from deepsearcher.embedding.base import BaseEmbedding
import numpy as np

MILVUS_MODEL_DIM_MAP = {
    "BAAI/bge-large-en-v1.5": 1024,
    "BAAI/bge-base-en-v1.5": 768,
    "BAAI/bge-small-en-v1.5": 384,
    "BAAI/bge-large-zh-v1.5": 1024,
    "BAAI/bge-base-zh-v1.5": 768,
    "BAAI/bge-small-zh-v1.5": 384,
    "GPTCache/paraphrase-albert-onnx": 768,
    "default": 768,  # 'GPTCache/paraphrase-albert-onnx',
    # see https://github.com/milvus-io/milvus-model/blob/4974e2d190169618a06359bcda040eaed73c4d0f/src/pymilvus/model/dense/onnx.py#L12
}


class MilvusEmbedding(BaseEmbedding):
    def __init__(self, model_name: str=None, **kwargs) -> None:
        from pymilvus import model

        if not model_name or model_name in ["default", "GPTCache/paraphrase-albert-onnx"]:
            self.model = model.DefaultEmbeddingFunction(**kwargs)
        
        else:
            if model_name.startswith("BAAI/"):
                self.model = model.dense.SentenceTransformerEmbeddingFunction(model_name, **kwargs)
            else:
                # Only support default model and BGE series model
                raise ValueError(f"Currently unsupported model name: {model_name}")
    
    def embed_query(self, text: str) -> List[float]:
        return self.model.encode_queries([text])[0]
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode_documents(texts)
        if isinstance(embeddings[0], np.ndarray):
            return [embedding.tolist() for embedding in embeddings]
        else:
            return embeddings
    @property
    def dimension(self) -> int:
        return self.model.dim # or MILVUS_MODEL_DIM_MAP[self.model_name]
