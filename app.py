# import os
# import streamlit as st
# from haystack.nodes import FARMReader
# from transformers import AutoModelWithLMHead, AutoTokenizer

# st.title("Question Generation and Answering")
# st.write("Enter the context and specify the number of questions to generate.")

# new_reader = FARMReader(model_name_or_path="/content/drive/MyDrive/Colab Notebooks/Training Model")
# context = '''India, officially the Republic of India (Hindi: Bhārat Gaṇarājya),[25] is a country in South Asia. It is the seventh-largest country by area; the most populous country[26][27] and the world's most populous democracy.[28][29][30] Bounded by the Indian Ocean on the south, the Arabian Sea on the southwest, and the Bay of Bengal on the southeast, it shares land borders with Pakistan to the west;[j] China, Nepal, and Bhutan to the north; and Bangladesh and Myanmar to the east. In the Indian Ocean, India is in the vicinity of Sri Lanka and the Maldives; its Andaman and Nicobar Islands share a maritime border with Thailand, Myanmar, and Indonesia.'''


# tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
# model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")


# a = st.number_input("Enter the number of questions to generate:", min_value=1, step=1)

# def generate_questions(context, num_questions=a, max_length=64):
#   input_text = "generate question: %s </s>" % context
#   features = tokenizer([input_text], return_tensors='pt')

#   outputs = model.generate(input_ids=features['input_ids'],
#                            attention_mask=features['attention_mask'],
#                            max_length=max_length,
#                            num_return_sequences=num_questions,
#                            num_beams=10
#                            ,  # Adjust the value of num_beams for more diverse questions
#                            early_stopping=True)
#   # questions = [tokenizer.decode(output) for output in outputs]
#   questions = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

#   return questions

# generated_questions = generate_questions(context, num_questions=a)
# for question in generated_questions:
#     st.write("Question:", question)
#     res = new_reader.predict_on_texts(question, [context])
#     for answer in res['answers']:
#         st.write("Answer:", answer.answer)
# if __name__ == "__main__":
#     generate_questions_app()

import streamlit as st
from haystack.nodes import FARMReader
from transformers import AutoModelWithLMHead, AutoTokenizer
from collections import OrderedDict
def generate_questions_app():
    st.title("Question Generation and Answering")
    st.write("Enter the context and specify the number of questions to generate.")

    # context = '''Narendra Damodardas Modi is an Indian politician who has served as the 14th Prime Minister of India since May 2014. Modi was the Chief Minister of Gujarat from 2001 to 2014 and is the Member of Parliament (MP) for Varanasi. He is a member of the Bharatiya Janata Party (BJP) and of the Rashtriya Swayamsevak Sangh (RSS), a right-wing Hindu nationalist paramilitary volunteer organisation. He is the longest-serving non-Congress prime minister and the fourth longest-serving prime minister of all time.
    # Modi was born and raised in Vadnagar in northeastern Gujarat, where he completed his secondary education. He was introduced to the RSS at age eight. His account of helping his father sell tea at the Vadnagar railway station has not been reliably corroborated. At age 18, he was married to Jashodaben Modi, whom he abandoned soon after, only publicly acknowledging her four decades later when legally required to do so. Modi became a full-time worker for the RSS in Gujarat in 1971. After the state of emergency was declared by Prime Minister Indira Gandhi in 1975, he went into hiding. The RSS assigned him to the BJP in 1985 and he held several positions within the party hierarchy until 2001, rising to the rank of general secretary.[c]'''
    context = st.text_area("Enter the context:")

    new_reader = FARMReader(model_name_or_path="bert-base-uncased")

    tokenizer = AutoTokenizer.from_pretrained("Kunjesh07/t5-base-question-generation-model")
    model = AutoModelWithLMHead.from_pretrained("Kunjesh07/t5-base-question-generation-model")



    @st.cache(suppress_st_warning=True)
    def generate_questions(context, num_questions=1, max_length=64):
        input_text = "generate question: %s </s>" % context
        features = tokenizer([input_text], return_tensors='pt')

        outputs = model.generate(input_ids=features['input_ids'],
                                 attention_mask=features['attention_mask'],
                                 max_length=max_length,
                                 num_return_sequences=num_questions,
                                 num_beams=a,  # Adjust the value of num_beams for more diverse questions
                                 early_stopping=True)

        questions = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
        unique_questions = list(OrderedDict.fromkeys(questions))

        return unique_questions

    a = st.number_input("Enter the number of questions to generate:", min_value=1, step=1)
    if st.button("Submit"):
        generated_questions = generate_questions(context, num_questions=a)
        for question in generated_questions:
            st.write("Question:", question)
            res = new_reader.predict_on_texts(question, [context])
            for answer in res['answers']:
                st.write("Answer:", answer.answer)

if __name__ == "__main__":
    generate_questions_app()
