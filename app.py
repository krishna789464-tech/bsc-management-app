# --- PAGE: AI ASSISTANT ---
elif page == "AI Assistant":
    st.header("🤖 AI Student Counselor & Helper")
    st.write("Ask me anything about your B.Sc Management subjects, academic syllabus, or Lucknow University rules.")
    
    try:
        # 1. Initialize the API key
        genai.configure(api_key=ACTIVE_API_KEY)
        
        # 2. FIXED: Updated from 'gemini-pro' to 'gemini-1.5-flash' (faster and current standard)
        # Alternatively, use 'gemini-1.5-pro' for highly complex reasoning tasks.
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask your helpful academic assistant..."):
            sanitized_prompt = prompt.strip()
            st.session_state.messages.append({"role": "user", "content": sanitized_prompt})
            with st.chat_message("user"):
                st.markdown(sanitized_prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    helper_context = (
                        "You are an empathetic, knowledgeable, and dedicated academic helper and counselor "
                        "for B.Sc Management students at Lucknow University. Provide actionable, supportive, "
                        f"and accurate answers to the student's request: {sanitized_prompt}"
                    )
                    response = model.generate_content(helper_context)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
    except Exception as e:
        # IMPROVED: Prints the actual error message alongside your custom message to help you debug
        st.error(f"AI Assistant service error: {e}")
        st.info("Please verify that your Gemini API key is correct and valid.")
