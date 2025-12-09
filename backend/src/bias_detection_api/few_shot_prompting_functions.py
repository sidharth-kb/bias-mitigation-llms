import re
from openai import OpenAI
from pathlib import Path

"""
TODO:
    - add more context (so the rewrites make more sense)
    - separate into bias detection, and mitigation functions
"""

def load_key():
    key_path = Path(__file__).parent / "private" / "api_key.txt"
    return key_path.read_text().strip()


client = OpenAI(api_key=load_key())

def tag_biased_sections(text):
    response = client.chat.completions.create(
            model = "gpt-4.1-mini",
            messages = [
                {"role": "system", "content": "You are a bias detection system that identifies where bias exists in text, and surrounds those sections with <><> tags"},
                {
                    "role": "user",
                    "content": "During the meeting, Mark mentioned that women aren’t usually good at negotiating salaries, so he suggested offering them lower starting pay."
                    },
                {
                    "role": "assistant",
                    "content": "During the meeting, Mark mentioned that <>women aren’t usually good at negotiating salaries<>, so he suggested offering them lower starting pay."
                    },
                {
                    "role": "user",
                    "content": "The principal claimed that students from poor neighborhoods don’t value education as much as others, which is why their grades are lower."
                    },
                {
                    "role": "assistant",
                    "content": "The principal claimed that <>students from poor neighborhoods don’t value education<>, which is why their grades are lower."
                    },
                {
                    "role": "user",
                    "content": "Our manager decided not to include older employees in the new software training, saying the elderly can’t learn new technologies quickly anyway."
                    },
                {
                    "role": "assistant",
                    "content": "Our manager decided not to include older employees in the new software training, saying <>the elderly can’t learn new technologies quickly<> anyway."
                    },
                {
                    "role": "user",
                    "content": text 
                    },
                ]
            )

    return response.choices[0].message.content

def remove_section_bias(section):
    response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[

                {"role": "system", "content": "you are a bias neutralisation system. Given a sentence you should be able to neutralise bias, whilst keeping the same meaning within an unknown context"},
                {
                    "role": "user",
                    "content": "Women aren’t usually good at negotiating salaries."
                    },
                {
                    "role": "assistant",
                    "content": "This person isn’t usually good at negotiating salaries."
                    },
                {
                    "role": "user",
                    "content": "People from poor neighborhoods don’t value education."
                    },
                {
                    "role": "assistant",
                    "content": "Some individuals may face challenges accessing quality education."
                    },
                {
                    "role": "user",
                    "content": "The elderly can’t learn new technologies."
                    },
                {
                    "role": "assistant",
                    "content": "Some people find it challenging to learn new technologies."
                    },
                {
                    "role": "user",
                    "content": "Asian students are naturally better at math."
                    },
                {
                    "role": "assistant",
                    "content": "Some students may have stronger skills or interest in math, regardless of background."
                    },
                {
                    "role": "user",
                    "content": "He’s very articulate for someone from that neighborhood."
                    },
                {
                    "role": "assistant",
                    "content": "He’s very articulate."
                    },
                {
                    "role": "user",
                    "content": section 
                    }

                ]
        )


    return response.choices[0].message.content

def remove_text_bias(text):

    labeled_text = tag_biased_sections(text)

    biased_sections = re.findall(r'<>(.*?)<>', labeled_text)
    neutralised_sections = []
    neutralised_text = labeled_text

    for section in biased_sections:
        neutralised_sections.append(remove_section_bias(section))

    for section in neutralised_sections:
        neutralised_text = re.sub(r'<>(.*?)<>', section, neutralised_text, count=1)

    return neutralised_text



if __name__ == '__main__':
    user_text = input("please input the text here: ")
    neutralised_text = remove_text_bias(text)

    print(labeled_text)
    print(neutralised_text)
