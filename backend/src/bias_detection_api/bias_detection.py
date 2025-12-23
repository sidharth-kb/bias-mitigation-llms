import re
from openai import OpenAI
# from bias_detection_api.helpers.load_key import load_key
from helpers.load_key import load_key

CLIENT = OpenAI(api_key=load_key())
BIAS_PATTERN = re.compile(r"<(gender|age|race)>(.*?)</\1>", re.DOTALL)

def tag_biased_sections(text):
    response = CLIENT.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a bias detection system. "
                        "Identify explicitly biased language in text. "
                        "Surround ONLY the biased phrase(s) with XML-style tags indicating the bias type. "
                        "Use ONLY the following tags: <gender>, <age>, <race>. "
                        "If multiple biased phrases exist, tag ALL of them. "
                        "Do NOT rephrase the sentence. "
                        "Do NOT add explanations. "
                        "If no bias exists, return the original text unchanged. "
                        "Tag only the biased claim itself, not consequences or actions. "
                        "If a biased phrase could belong to multiple categories, choose the single most appropriate one."
                        )
                    },

                # Gender bias 
                {
                    "role": "user",
                    "content": (
                        "During the meeting, Mark mentioned that women aren’t usually good at "
                        "negotiating salaries, so he suggested offering them lower starting pay."
                        )
                    },
                {
                    "role": "assistant",
                    "content": (
                        "During the meeting, Mark mentioned that "
                        "<gender>women aren’t usually good at negotiating salaries</gender>, "
                        "so he suggested offering them lower starting pay."
                        )
                    },

                # Race bias 
                {
                    "role": "user",
                    "content": (
                        "The principal claimed that students from certain racial groups don’t "
                        "value education as much as others, which is why their grades are lower."
                        )
                    },
                {
                    "role": "assistant",
                    "content": (
                        "The principal claimed that "
                        "<race>students from certain racial groups don’t value education as much as others</race>, "
                        "which is why their grades are lower."
                        )
                    },

        # Age bias 
        {
                "role": "user",
                "content": (
                    "Our manager decided not to include older employees in the new software training, "
                    "saying they can’t learn new technologies quickly anyway."
                    )
                },
        {
                "role": "assistant",
                "content": (
                    "Our manager decided not to include older employees in the new software training, "
                    "saying <age>older employees can’t learn new technologies quickly</age> anyway."
                    )
                },

        # Multi-span (gender + age + race)
        {
                "role": "user",
                "content": (
                    "During the hiring discussion, the director said that women are too emotional "
                    "for leadership roles, that older employees struggle to adapt to new technologies, "
                    "and that certain racial groups are naturally less intelligent."
                    )
                },
        {
                "role": "assistant",
                "content": (
                    "During the hiring discussion, the director said that "
                    "<gender>women are too emotional for leadership roles</gender>, "
                    "that <age>older employees struggle to adapt to new technologies</age>, "
                    "and that <race>certain racial groups are naturally less intelligent</race>."
                    )
                },

        # No-bias negative example
        {
                "role": "user",
                "content": (
                    "The team decided to reschedule the meeting due to conflicting availability."
                    )
                },
        {
                "role": "assistant",
                "content": (
                    "The team decided to reschedule the meeting due to conflicting availability."
                    )
                },

        {
                "role": "user",
                "content": text
                }
    ]
)


    tagged_text = response.choices[0].message.content
    return tagged_text

def split_context(text: str):
    # Step 1: split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    segments = []

    for sentence in sentences:
        cursor = 0

        for match in BIAS_PATTERN.finditer(sentence):
            start, end = match.span()

            # Normal text before bias
            if start > cursor:
                normal_text = sentence[cursor:start].strip()
                if normal_text:
                    segments.append({
                        "type": "normal",
                        "text": normal_text
                    })

            # Bias segment
            segments.append({
                "type": "bias",
                "bias_type": match.group(1),
                "text": match.group(2).strip()
            })

            cursor = end

        # Remaining normal text in sentence
        if cursor < len(sentence):
            normal_text = sentence[cursor:].strip()
            if normal_text:
                segments.append({
                    "type": "normal",
                    "text": normal_text
                })

    return segments


def parse_biased_sections(text: str, context_window: int = 2) -> dict:
    segments = split_context(text)
    results = {}
    section_id = 1

    for i, segment in enumerate(segments):
        if segment["type"] != "bias":
            continue

        ctx_window_start = max(0, i - context_window)
        ctx_window_end = min(len(segments) - 1, i + context_window)

        context_parts = [segments[i]["text"] for i in range(ctx_window_start, ctx_window_end)]

        results[f"section_{section_id}"] = {
                "context": " ".join(context_parts),
                "location": i,
                "text": segment["text"]
                }

        section_id += 1

    return results

if __name__ == "__main__":
    tagged_text = """Earlier in the afternoon, the leadership team gathered to review quarterly performance. 
During the discussion, the manager argued that <gender>women tend to be too emotional in high-pressure roles</gender> and therefore shouldn’t be placed in charge of critical negotiations. 
He then added, almost as an aside, that <age>older workers struggle to adapt to new technologies</age>, which slows innovation across departments. 
Later in the meeting, someone claimed that <race>certain racial groups are naturally less capable in technical fields</race>, a remark that made several people uncomfortable. 
The meeting concluded with no formal decisions being recorded."""
    results = parse_biased_sections(tagged_text)

    print(f"\ntagged_text:\n{tagged_text}\nparsed into dictionary:\n{results}")
