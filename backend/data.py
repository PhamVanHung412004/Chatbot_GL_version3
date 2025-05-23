import json
from semantic_search import Sematic_search
from gen import Answer_Question_From_Documents
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator


# Lấy thư mục gốc của file hiện tại (tức là backend/)
def get_answer(use_query, model,datas, data_dict):
    try:
        # Tìm kiếm semantic
        list_index = Sematic_search(model, use_query, 3).run()
        vector_tmp = list_index[0]
        vector = [int(i) for i in vector_tmp]
        
        # Lấy các đoạn văn bản liên quan
        list_context = [data_dict[datas["text"][i]] for i in vector]
    
        # Tạo câu trả lời
        answer = Answer_Question_From_Documents(use_query, list_context).run()

        # Dịch nếu không phải tiếng Việt
        if detect(answer) != 'vi':
            answer = GoogleTranslator(source='auto', target='vi').translate(answer)

        return answer

    except ZeroDivisionError as e:
        title = str(e)
        if detect(title) != 'vi':
            title = GoogleTranslator(source='auto', target='vi').translate(title)
     
        return f"Lỗi: {title}"
