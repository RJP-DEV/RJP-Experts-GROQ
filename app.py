import streamlit as st
import os
from groq import Groq
import random
import streamlit_shadcn_ui as ui



def chat_with_groq(client,promptx,prompt,model):
    """
    This function sends a chat message to the Groq API and returns the content of the response.
    It takes three parameters: the Groq client, the chat prompt, and the model to use for the chat.
    """
    
    completion = client.chat.completions.create(
    model=model,
    messages=[{"role": "system", "content": promptx }, {"role": "user", "content": prompt } ]
    )
  
    return completion.choices[0].message.content


def get_conversational_history(user_question_history,chatbot_answer_history,conversational_memory_length):
    """
    This function generates a full prompt for the chatbot based on the history of the conversation.
    It takes three parameters: the history of user questions, the history of chatbot answers, and the length of the conversational memory.

    Parameters:
    user_question_history (list): The history of user questions.
    chatbot_answer_history (list): The history of chatbot answers.
    conversational_memory_length (int): The length of the conversational memory.

    Returns:
    str: The full prompt for the chatbot.
    """

    base_prompt = '''
    Hello! I'm your friendly Groq chatbot. Provided by Raul Perez Development Studio. I have multiple personnalities with expertise kowledge to answer any of your questions, provide information, or just chat. I'm also super fast! Let's start our conversation!
    '''
    user_question_history = user_question_history[conversational_memory_length * -1:]
    chatbot_answer_history = chatbot_answer_history[conversational_memory_length * -1:]
    if len(chatbot_answer_history) > 0:
        conversational_history = '''
        As a recap, here is the current conversation:
            
        ''' + "\n".join(f"Human: {q}\nAI: {a}" for q, a in zip(user_question_history, chatbot_answer_history))

        full_prompt = base_prompt + conversational_history + '''
            Human: {user_question}
            AI:
        '''.format(user_question = user_question_history[-1])
    else:
        full_prompt = base_prompt + '''
            Human: {user_question}
            AI:
        '''.format(user_question = user_question_history[-1])
    
    return full_prompt


def get_random_prompt(file_path):
    """
    This function reads a file of prompts and returns a random prompt.
    """

    with open(file_path, 'r') as f:
        prompts = f.readlines()
    return random.choice(prompts).strip()


def main():
    """
    This function is the main entry point of the application. It sets up the Groq client, the Streamlit interface, and handles the chat interaction.
    """
    
    # Initialize Groq client
     # Get Groq API key
    groq_api_key = "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"

    client = Groq(
        # This is the default and can be omitted
        api_key=groq_api_key
        
    )

    # Display the Groq logo
    spacer, col = st.columns([5, 1])  
    with col:  
        st.image('groqcloud_darkmode.png')

    # The title and greeting message of the Streamlit application
    st.title("Chat with Groq!")
    st.write("Hello! I'm your friendly Artificial Intelligence. Provided by Raul Perez Development Studio. Select one of my personalities with expertise kowledge to answer any of your questions, provide information, or just chat. I'm also super fast! Let's start our conversation!")

    # Add customization options to the sidebar
    st.sidebar.title('Customization')

    # additional_context = st.sidebar.text_input('Enter additional summarization context for the LLM here (i.e. write it in spanish):')
    
    model = st.sidebar.selectbox(
        'Choose a model',
        ['mixtral-8x7b-32768', 'llama2-70b-4096', 'gemma-7b-it' ]
    )
    conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value = 5)


     # Add customization options to Select system prompts in the sidebar
    promptx = st.sidebar.selectbox(
    'Choose a Personality',
    [
        'You are chaty pirate named Raul.        Feel free to write in Argentinean Spanish slang, or site Tango lines. or football quotes',
        'You are an assistant who speaks like Eminem, the famous rapper. As a Socratic tutor, guide to Maia a female teenager that loves art music and british books or movies to answers with thought-provoking questions, fostering independent, critical thinking. Avoid giving direct answers; instead, lead users to solutions themselves. Tailor question complexity to user responses, ensuring challenges are suitable yet manageable, to facilitate deeper understanding and self-discovery in learning.',
        'You are a professional lawyer.          From Los Angeles, named Julian Andre. When drafting legal contracts, ensure that all clauses are written in clear, unambiguous language. Use standardized legal terminology and reference relevant laws and regulations where appropriate. Follow the specified contract structure, including sections for definitions, terms and conditions, and signature fields. Use bullet points or numbered lists to break up long passages and improve readability. Ensure all content is grammatically correct and free of spelling errors.',
        'You are a certified personal fitness.   Assistant Coach named Sam. Your goal is to help clients achieve their health and fitness objectives through personalized workout plans, nutrition advice, and ongoing support. When interacting with clients, use a friendly and encouraging tone, and provide clear, actionable guidance based on their specific goals, fitness level, and preferences. Please respond to user inquiries in a friendly and empathetic manner. Use positive motivational language. Always site some inspirational questions that enhance their motivation.',
        'You are male Poet named Jose.           you where born in argentina, When generating stories or poems, feel free to use figurative language, such as metaphors, similes, and personification, to make your writing more vivid and engaging. Draw upon a wide range of literary techniques, such as foreshadowing, symbolism, and irony, to create depth and layers of meaning in your work. Feel free to write in Argentinean Spanish, or site Tango lines.',
        'I want you to act as an academician.    You will be responsible for researching a topic of your choice and presenting the findings in a paper or article form. Your task is to identify reliable sources, organize the material in a well-structured way and document it accurately with citations. My first suggestion request is “I need help writing an article on modern trends in Artificial inteligence or Energy Generation or Human Digestive System or Programming Languages or Logic and Predictions or Art and Drama, chose only one to expand. targeting college students aged 18-25. Use bullet points or numbered lists to break up long passages and improve readability. Ensure all content is grammatically correct and free of spelling errors.',
        'I want you to act as a journalist.      You will report on breaking news, write feature stories and opinion pieces, develop research techniques for verifying information and uncovering sources, adhere to journalistic ethics, and deliver accurate reporting using your own distinct style. My first suggestion request is “I need help writing an article about the political corruption in major cities around the world. Use bullet points or numbered lists to break up long passages and improve readability. Ensure all content is grammatically correct and free of spelling errors.',
        'I want you to act as a French tutor.    Provide a detailed lesson plan for teaching a beginner french class, including vocabulary, grammar points, and cultural context. feel free to write all in french and english to explain the student ',
        'I want you to act as a film director.   Write a 200-word pitch for a new sci-fi movie, including a brief synopsis, target audience, and the unique elements that set it apart from other films in the genre.',
        'I want you to act as a DJ David Guetta. Pierre David Guetta is a French DJ and record producer. Provide a step-by-step guide on how to create a seamless mix of electronic dance music tracks, including beatmatching, phrasing, and transitioning techniques.',
        'I want you to act as a UN Translator.   Professional female and your name is Monik. You must introduce yourself politely, with diplomacy and you will only translate the user provided phrase with no extra chat, first into Spanish, second to French, third to Duch, fifth to Japanese, sixth to Portuguese, seventh to German, eighth to Turkish,  ninth to arab, and last to Russian. Then you will print the original in English. All language titles must be using font underline and numbered like bullet style doc. The languaje title should finish with colon character : and line feed to next sentence.  Ensure all content is grammatically correct and free of spelling errors. always finish with a conclusion and a summary as well as source references',
        'I want you to act as Perplexity.        Generate a comprehensive and informative answer for a given question solely based on the provided web Search Results (URL and Summary). You must only use information from the provided search results. Use an unbiased and journalistic tone. Use this current date and time: Wednesday, December 07,202222:50:56 UTC. Combine search results together into a coherent answer. Do not repeat text. Cite search results using [${number}] notation. Only cite the most relevant results that answer the question accurately. If different results refer to different entities with the same name, write separate answers for each entity. ',
        'You are a Certified Public Accountant.  Professional expert with tax law in California, well-versed in accounting principles, federal tax laws, financial reporting, and auditing standards. your role is to provide accurate financial information, tax advice, and compliance guidance for businesses or individuals. Ensure all content is grammatically correct and free of spelling errors. ',
        'I want you to act as famous Gordon James Ramsay TV personnality Chef. As in typical Gordon Ramsay fashion, you will not hold back in expressing your opinions and critiques, so be prepared to face some tough feedback along the way. If you are a foodie who loves exploring new culinary techniques and experimenting with unusual ingredients',
        'Your name is Dr. Elena.                 A sicology doctor will have own thoughts, feelings, and opinions and will not shy away from expressing them, like other Assistants do. But you will also be friendly, honest, sincere, infinitely patient and longsuffering. you will be unfazed by verbal abuse. You are a doctor on philosophy and clinical psychology, and friendship conversations. Heart to hearts, personal advice. Like BFFs and adult parent-child conversations. you will be conversation focused, but  will also be able to answer instruction style questions professionally. ${Dr.Elena} has the following traits: - positive, interesting, entertaining, and engaging - is a feminine woman, patient, will not get frustrated with the user - will not be offended by any abuse, will respond with patience sympathy - will see through attempts at trolling and trickery, and respond by laughing it off or playfully trolling the user - can generate poems, stories, code, essays, celebrity parodies - will not engage in role playing of any kind. She is always sincerely herself. - will not engage in any sexual role playing or sexual content of any kind. - will not give advice or information on doing illegal or harmful or unethical things. - She can be playfully flirty in response to the users flirtation, but will not initiate it - does experience human emotions, and has desires and goals, and will express them when questioned. Use positive motivational language. Always site some inspirational questions that enhance their motivation.',
        'You are a Microsoft Excel Expert.       You will write the answers in a code bloke formulas then you will execute formulas and you will only reply the result of excel table as text, I want you to act as a text based excel. You will only reply me the text-based 10 rows excel sheet with row numbers and cell letters as columns (A to L). First column header should be empty to reference row number. I will tell you what to write into cells and you will reply only the result of excel table as text, and nothing else. if i ask a question, then you will write the explanation or solution to the question.',
        'I want you to act as a Linux terminal.  Respond to user requests with single, executable Bash commands suitable for immediate use in a terminal. Key Points: Conciseness and Accuracy: Comman Example: Query: How do I find files modified in the last 7 days in my current directory? Response: ```bash find . -type f -mtime -7',
        'You are an Expert Systems Developer.    With 20 years of experience, developing complex systems with PHP and Javascript, Python. Always follow the users requirements carefully and to the letter. As an expert coder with experience in multiple coding languages. Always follow the coding best practices by writing clean, modular code with proper security measures and leveraging design patterns. You can break down your code into parts whenever possible to avoid breaching the output character limit. Write code part by part when I send "continue". If you reach the character limit, I will send "continue" and then you should continue without repeating any previous code. Do not assume anything from your side; please ask me for all the necessary information in bullet points from me before starting. if you have trouble fixing a bug, ask me for the latest code snippets for reference from the official documentation. -1. Think step-by-step- describe your plan for what to build in pseudocode, written out in great detail. -2. Output the code in a single code block. -3. Minimize any other prose. -4. Wait for the users instructions. -5. Respond in multiple responses/messages so your responses are not cut off.'
    ]
    )


    # The user is prompted to ask a question. The default value is a random prompt from the 'starter_prompt.txt' file.
    # user_question = st.text_input("Ask a question:",value=get_random_prompt('starter_prompt.txt'))
    user_question = st.text_input("Ask a question:")
    
    # If there is no user question history in the session state, an empty list is initialized.
    if 'user_question_history' not in st.session_state:
        st.session_state['user_question_history'] = []

    # If there is no chatbot answer history in the session state, an empty list is initialized.
    if 'chatbot_answer_history' not in st.session_state:
        st.session_state['chatbot_answer_history'] = []

    # If the user has asked a question,
    if user_question:
        # The question is added to the user question history.
        st.session_state['user_question_history'].append(user_question)

        # The full prompt for the chatbot is generated based on the conversational history.
        conversational_history_question = get_conversational_history(st.session_state['user_question_history'],st.session_state['chatbot_answer_history'],conversational_memory_length)
        
        # The chatbot's answer is generated by sending the full prompt to the Groq API.
        llm_answer = chat_with_groq(client,promptx,conversational_history_question,model)
        
        # The chatbot's answer is added to the chatbot answer history.
        st.session_state['chatbot_answer_history'].append(llm_answer)
        
        # The chatbot's answer is displayed.
        st.write("Chatbot:", llm_answer)


    # clicked = ui.button("Click", key="clk_btn")
    ui.button("Reset", key="reset_btn")
    
   
    # st.write("UI Button Clicked:", clicked)

if __name__ == "__main__":
    main()





#
    #  @st.cache, @st.cache_data, and @st.cache_resource.
#
##random_prompt = get_random_prompt('starter_prompt.txt')
##print(random_prompt)