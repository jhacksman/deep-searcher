from deepsearcher.online_query import naive_retrieve
from deepsearcher.agent.prompt import get_vector_db_search_prompt

def test_search_functionality():
    print("Testing search functionality...")
    
    # Test naive_retrieve
    try:
        retrieval_res = naive_retrieve('test query', collection='deepsearcher')
        print('naive_retrieve test passed')
    except Exception as e:
        print(f'naive_retrieve test failed: {str(e)}')

    # Test vector DB search prompt
    try:
        collection_info = [{'collection_name': 'test', 'collection_description': 'test'}]
        prompt = get_vector_db_search_prompt('test query', collection_info)
        print('get_vector_db_search_prompt test passed')
        print(f'Generated prompt: {prompt}')
    except Exception as e:
        print(f'get_vector_db_search_prompt test failed: {str(e)}')

if __name__ == '__main__':
    test_search_functionality()
