#import streamlit as st
##import streamlit.components.v1 as components

#from logger import logger
#from languages import supported_languages
#from translator import detect_source_language, translate


# def main():
 ##   """Entry point"""
 
main_container = st.container()
_, center_column, _ = main_container.columns([1, 5, 1])

#source_text = llm_answer

   # source_text = center_column.text_area(
   #     "Text",
   #     placeholder="Type your text here...",
   #     max_chars=1000,
   #     key="source_text",
   #     label_visibility="hidden",
   # )

#st.session_state.source_lang = detect_source_language(llm_answer)

    
#destination_language = "en"
   # destination_language = center_column.selectbox(
   #     "Select Language",
   #     sorted(list(supported_languages.keys())[1:]),
   #     key="target_lang",
   #     label_visibility="hidden",
   # )

#logger.debug(f"Selected destination language as {destination_language}")

#  center_column.button("Translate", on_click=translate, type="primary", use_container_width=True)
 

result_container = st.container()
_, col2, _ = result_container.columns([1, 5, 1])



if "translation" not in st.session_state:
        st.session_state.translation = ""

col2.markdown(f"**{st.session_state.translation}**")

if st.session_state.translation:
        col2.audio("translation.mp3", format="audio/mp3")
        
       
       

#if __name__ == "__main__":
 #   main()