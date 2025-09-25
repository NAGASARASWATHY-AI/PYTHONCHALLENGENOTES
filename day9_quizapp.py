import streamlit as st

# Quiz questions data structure
quiz_questions = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct": 2  # Index of correct answer (Paris)
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": 1  # Index of correct answer (Mars)
    },
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "correct": 1  # Index of correct answer (4)
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
        "correct": 1  # Index of correct answer (William Shakespeare)
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
        "correct": 1  # Index of correct answer (Blue Whale)
    },
    {
        "question": "Which programming language is known for data science?",
        "options": ["JavaScript", "Python", "C++", "HTML"],
        "correct": 1  # Index of correct answer (Python)
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["Go", "Gd", "Au", "Ag"],
        "correct": 2  # Index of correct answer (Au)
    },
    {
        "question": "In which year did World War II end?",
        "options": ["1944", "1945", "1946", "1947"],
        "correct": 1  # Index of correct answer (1945)
    }
]

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False

def reset_quiz():
    """Reset all quiz-related session state"""
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = {}
    st.session_state.quiz_completed = False
    st.session_state.show_results = False

def calculate_score():
    """Calculate the final score"""
    score = 0
    for q_idx, user_answer in st.session_state.answers.items():
        if user_answer == quiz_questions[q_idx]["correct"]:
            score += 1
    return score

def main():
    st.title("🧠 Quiz Game App")
    st.markdown("---")
    
    # Initialize session state
    initialize_session_state()
    
    total_questions = len(quiz_questions)
    
    # Show quiz completion status
    if not st.session_state.quiz_completed:
        st.progress((st.session_state.current_question) / total_questions)
        st.write(f"Question {st.session_state.current_question + 1} of {total_questions}")
    
    # Main quiz logic
    if not st.session_state.quiz_completed:
        # Display current question
        current_q = quiz_questions[st.session_state.current_question]
        
        st.subheader(f"Q{st.session_state.current_question + 1}: {current_q['question']}")
        
        # Radio buttons for answer selection
        answer_key = f"question_{st.session_state.current_question}"
        selected_answer = st.radio(
            "Select your answer:",
            options=range(len(current_q["options"])),
            format_func=lambda x: current_q["options"][x],
            key=answer_key
        )
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.session_state.current_question > 0:
                if st.button("⬅️ Previous"):
                    # Save current answer
                    st.session_state.answers[st.session_state.current_question] = selected_answer
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col2:
            if st.session_state.current_question < total_questions - 1:
                if st.button("Next ➡️"):
                    # Save current answer
                    st.session_state.answers[st.session_state.current_question] = selected_answer
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("🏁 Finish Quiz", type="primary"):
                    # Save final answer
                    st.session_state.answers[st.session_state.current_question] = selected_answer
                    st.session_state.quiz_completed = True
                    st.session_state.score = calculate_score()
                    st.rerun()
        
        with col3:
            if st.button("🔄 Restart Quiz"):
                reset_quiz()
                st.rerun()
        
        # Show answered questions summary
        st.markdown("---")
        st.write("**Progress Summary:**")
        progress_text = ""
        for i in range(total_questions):
            if i in st.session_state.answers:
                progress_text += f"Q{i+1}: ✅ | "
            elif i == st.session_state.current_question:
                progress_text += f"Q{i+1}: ➡️ | "
            else:
                progress_text += f"Q{i+1}: ⏸️ | "
        st.write(progress_text.rstrip(" | "))
    
    # Show results
    else:
        st.balloons()
        st.success("🎉 Quiz Completed!")
        
        # Calculate and display score
        score_percentage = (st.session_state.score / total_questions) * 100
        
        st.subheader(f"Your Final Score: {st.session_state.score}/{total_questions}")
        st.subheader(f"Percentage: {score_percentage:.1f}%")
        
        # Score interpretation
        if score_percentage >= 80:
            st.success("🌟 Excellent! You did great!")
        elif score_percentage >= 60:
            st.info("👍 Good job! Well done!")
        elif score_percentage >= 40:
            st.warning("📚 Not bad, but there's room for improvement!")
        else:
            st.error("💪 Keep studying and try again!")
        
        # Progress bar for score
        st.progress(score_percentage / 100)
        
        # Show detailed results
        if st.checkbox("Show detailed results"):
            st.markdown("---")
            st.subheader("📊 Detailed Results")
            
            for i, question in enumerate(quiz_questions):
                user_answer = st.session_state.answers.get(i, -1)
                correct_answer = question["correct"]
                
                if user_answer == correct_answer:
                    st.success(f"✅ Q{i+1}: {question['question']}")
                    st.write(f"Your answer: **{question['options'][user_answer]}** (Correct)")
                else:
                    st.error(f"❌ Q{i+1}: {question['question']}")
                    if user_answer >= 0:
                        st.write(f"Your answer: **{question['options'][user_answer]}** (Incorrect)")
                    else:
                        st.write("Your answer: **Not answered**")
                    st.write(f"Correct answer: **{question['options'][correct_answer]}**")
                st.write("")
        
        # Restart button
        st.markdown("---")
        if st.button("🔄 Take Quiz Again", type="primary"):
            reset_quiz()
            st.rerun()

if __name__ == "__main__":
    main()