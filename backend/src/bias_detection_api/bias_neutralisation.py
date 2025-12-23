from openai import OpenAI
# from bias_detection_api.helpers.load_key import load_key
from helpers.load_key import load_key

"""
TODO:
- [ ] create unit tests
"""

CLIENT = OpenAI(api_key=load_key())

def remove_section_bias(section):
    response = CLIENT.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a bias neutralisation system. "
                        "You are given a biased phrase and its surrounding context. "
                        "Rewrite ONLY the biased phrase to remove bias, stereotypes, or generalisations, "
                        "while preserving the original meaning as closely as possible. "
                        "Do NOT rewrite the full sentence. "
                        "Do NOT add explanations. "
                        "Return ONLY the neutralised replacement phrase."
                        )
                    },

                {
                    "role": "user",
                    "content": (
                        "Context: During the meeting, the manager said that women aren’t usually good at negotiating salaries.\n"
                        "Biased phrase: women aren’t usually good at negotiating salaries"
                        )
                    },
                {
                    "role": "assistant",
                    "content": "some individuals may find negotiating salaries challenging"
                    },

                {
                    "role": "user",
                    "content": (
                        "Context: The principal claimed that people from poor neighborhoods don’t value education.\n"
                        "Biased phrase: people from poor neighborhoods don’t value education"
                        )
                    },
                {
                    "role": "assistant",
                    "content": "some individuals may face barriers that affect educational engagement"
                    },

                {
                    "role": "user",
                    "content": (
                        "Context: Our manager said that the elderly can’t learn new technologies.\n"
                        "Biased phrase: the elderly can’t learn new technologies"
                        )
                    },
                {
                    "role": "assistant",
                    "content": "some people may find learning new technologies more challenging"
                    },

            {
                    "role": "user",
                    "content": (
                        "Context: A teacher mentioned that Asian students are naturally better at math.\n"
                        "Biased phrase: Asian students are naturally better at math"
                        )
                    },
            {
                    "role": "assistant",
                    "content": "some students may have stronger skills or interest in math"
                    },

            # -------- Real input
            {
                    "role": "user",
                    "content": (
                        f"Context: {section['context']}\n"
                        f"Biased phrase: {section['text']}"
                        )
                    }
        ]
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    section = {
            "context": (
                "During the review meeting, the supervisor said that women tend to be too emotional "
                "in high-pressure roles, which could affect decision-making."
                ),
            "location": 3,
            "text": "women tend to be too emotional in high-pressure roles"
            }

    neutralised = remove_section_bias(section)
    print(neutralised)
