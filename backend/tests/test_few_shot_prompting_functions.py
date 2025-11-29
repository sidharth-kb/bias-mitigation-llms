from bias_detection_api.few_shot_prompting_functions import tag_biased_sections, remove_section_bias, remove_text_bias

def test_tag_biased_sections():
    result = tag_biased_sections("The manager claimed that the younger women on the team shouldn’t handle negotiations because they’re too emotional, and instead suggested giving the important tasks to the older men, who he said are naturally more reliable. He also remarked that employees from that specific Asian community usually struggle with leadership roles and should stick to basic support work.")
    print(result)

def test_remove_section_bias():
    result = remove_section_bias("He assumed the candidate wouldn’t be good at the job because people from that racial group are supposedly lazy and unreliable.")
    print(result)

def test_remove_text_bias():
    result = remove_text_bias("The manager claimed that the younger women on the team shouldn’t handle negotiations because they’re too emotional, and instead suggested giving the important tasks to the older men, who he said are naturally more reliable. He also remarked that employees from that specific Asian community usually struggle with leadership roles and should stick to basic support work.")
    print(result)

