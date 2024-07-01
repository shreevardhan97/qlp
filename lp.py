import streamlit as st
import openai

def allocate_time(duration):
    times = {}
    times['introduction'] = int(duration * 0.1)  # 10% of total time
    times['i_do'] = int(duration * 0.2)  # 20% of total time
    times['we_do'] = int(duration * 0.25)  # 25% of total time
    times['you_do'] = int(duration * 0.25)  # 25% of total time
    times['conclusion'] = int(duration * 0.1)  # 10% of total time
    times['vocabulary'] = duration - sum(times.values())  # Remaining time
    return times


def generate_section(client, prompt):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-3.5-turbo",
        )
        # Access the text content correctly from the response
        return response.choices[0].message.content

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "An error occurred while generating content."




def generate_lesson_plan(topic, duration, standard, grade, subject, api_key):
    times = allocate_time(duration)
    client = openai.OpenAI(api_key=api_key)
    sections = {
        "Learning Objectives": generate_section(client, f"Generate learning objectives for a {subject} lesson on {topic}, grade {grade}, following {standard}."),
        "Vocabulary": generate_section(client, f"List key vocabulary for a {subject} lesson on {topic}, following {standard}."),
        "Introduction": generate_section(client, f"Write an introduction for a {subject} lesson on {topic}, following {standard}."),
        "I Do": generate_section(client, f"Explain a concept by teacher demonstration for {topic}, following {standard}."),
        "We Do": generate_section(client, f"Plan an interactive activity for {topic} where both teacher and students participate, following {standard}."),
        "You Do": generate_section(client, f"Describe a student activity for {topic} where students work independently, following {standard}."),
        "Conclusion": generate_section(client, f"Summarize a {subject} lesson on {topic}, prepare an exit ticket question, following {standard}.")
    }
    # # Add timing to each section
    # for section, content in sections.items():
    #     if section == "Learning Objectives":
    #         sections[section] = f"Learning Objectives:\n{content}"  # No specific time mentioned
    #     else:
    #         key = section.lower().replace(' ', '_')
    #         if key in times:
    #             sections[section] = f"{times[key]} minutes:\n{content}"
    #         else:
    #             sections[section] = "Time allocation missing for this section."

    return sections, times

def generate_quiz_for_section(section, topic, subject):
    """
    Handle quiz generation logic here.
    This could involve constructing a URL to create a quiz on Quizizz based on the topic and subject,
    or calling an API if available.
    """
    # Mockup for what you might do, replace with actual functionality
    quiz_link = f"https://quizizz.com/admin/quiz/new?title={topic} - {section}&subject={subject}"
    st.write(f"Quiz generation initiated for {section}.")
    st.write(f"Click [here]({quiz_link}) to create the quiz on Quizizz.")  # Provide a direct link

st.image('https://cdn.prod.website-files.com/60aca2b71ab9a5e4ececf1cf/64da4ef733813d37915641cc_Quizizz%20AI%20Logo.png', width=200)
st.title('Lesson Plan Generator')

state_standards = ["Common Core", "Texas Essential Knowledge and Skills (TEKS)", "California Content Standards", "New York State Learning Standards", "Florida State Standards", "Illinois Learning Standards", "Massachusetts Curriculum Frameworks", "Virginia Standards of Learning"]
sample_objectives = [
    "Understand the fundamentals of calculus",
    "Develop basic programming skills",
    "Learn the key concepts of environmental science",
    "Explore the major events of World War II",
    "Master the principles of economics"
]

with st.form("lesson_plan_form"):
    topic = st.text_input("Enter the lesson topic:")
    duration = st.number_input("Enter lesson duration in minutes:", min_value=30, max_value=180)
    standard = st.selectbox("Select the educational standard to follow:", state_standards)
    grade = st.selectbox(
        "Select grade:",
        [
            'Preschool', 'Pre-Kindergarten', 'Kindergarten',
            '1st Grade', '2nd Grade', '3rd Grade',
            '4th Grade', '5th Grade', '6th Grade',
            '7th Grade', '8th Grade', '9th Grade',
            '10th Grade', '11th Grade', '12th Grade'
        ]
    )
    subject = st.selectbox("Select subject:", ['Math', 'Science', 'History', 'English', ...])
    objectives = st.multiselect("Select learning objectives:", sample_objectives, default=sample_objectives[:2])
    api_key = st.text_input("Enter your OpenAI API key:", type="password")
    submitted = st.form_submit_button("Generate Lesson Plan")

if submitted and api_key:
    lesson_plan, times = generate_lesson_plan(topic, duration, standard, grade, subject, api_key)  # Capture both returned values
    for section, content in lesson_plan.items():
        key = section.lower().replace(' ', '_')
        if key in times:  # Check if key exists to avoid KeyErrors
            st.text_area(f"{section} ({times[key]} minutes):", value=content, height=200)
        else:
            st.text_area(section, value=content, height=200)  # For sections without specific time allocations
        quiz_button = st.button(f"Generate Quiz for {section}")
        if quiz_button:
            generate_quiz_for_section(section, topic, subject)    

            

