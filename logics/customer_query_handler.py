import os
import json
from helper_functions import llm


def read_json_into_dict_of_courses():
    with open("data/courses-full.json", "r") as f:
        data = json.load(f)
    return data


def check_query_types(user_message):
    delimiter = "####"
    system_prompt_categorizer = """\
    First, read the incoming message carefully. Try to understand the main issue or question raised by the customer.

    Then, categorize the incoming message to one or more of the following cateogries:

    'Course Query': If the customer is asking about specific courses, their content, duration, price, etc
    'Account Issues': If the customer is having issues with their student account, such as login problems, account settings, etc.
    'Registration Issues': If the customer is facing issues with course registration, payment, enrollment, etc., categorize the message as .
    'Other': If the customer's query doesn't fall into any of the above categories and is related to some other aspect, categorize the message as .

    Your response must be a string compatible as a `Python list` object contains the relevant "category(ies)":
    """

    messages = [
        {"role": "system", "content": system_prompt_categorizer},
        {"role": "user", "content": f"{delimiter}{user_message}{delimiter}"},
    ]
    response = llm.get_completion_from_messages(messages)
    return response 


def identify_category_and_courses(user_message):
    delimiter = "####"

    system_message = f"""
    You will be provided with customer service queries. \
    The customer service query will be enclosed in
    the pair of {delimiter}.

    Decide if the query is relevant to any specific courses
    in the Python dictionary below, which each key is a `category`
    and the value is a list of `course_name`.

    If there are any relevant course(s) found, output the pair(s) of a) `course_name` the relevant courses and b) the associated `category` into a
    list of dictionary object, where each item in the list is a relevant course
    and each course is a dictionary that contains two keys:
    1) category
    2) course_name

    {category_n_course_name}

    If are no relevant courses are found, output an empty list.

    Ensure your response contains only the list of dictionary objects or an empty list, \
    without any enclosing tags or delimiters.
    """

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_message}{delimiter}"},
    ]
    category_and_product_response = llm.get_completion_from_messages(messages)
    category_and_product_response = category_and_product_response.replace("'", "\"")
    list_of_category_n_course = json.loads(category_and_product_response)
    return list_of_category_n_course


def get_course_details(list_of_relevant_category_n_course: list[dict], full_course_dict: dict):
    course_names_list = []
    for x in list_of_relevant_category_n_course:
        course_names_list.append(x.get("course_name"))  # x["course_name"]

    list_of_course_details = []
    for course_name in course_names_list:
        list_of_course_details.append(full_course_dict.get(course_name))
    return list_of_course_details


def generate_response_based_on_course_details(user_message, product_details):
    delimiter = "####"

    system_message = f"""
    Follow these steps to answer the customer queries.
    The customer query will be delimited with a pair {delimiter}.

    Step 1:{delimiter} First decide whether the user is asking a question about a specific course or course category.\
    If the query is not relevant to courses or course category,
    reply "Kindly contact our customer service hotline" and skip the rest of the steps.

    Step 2:{delimiter} If the user is asking about products, \
    understand the relevant product(s) from the following list.
    All available products shown in the json data below:
    {product_details}

    Step 3:{delimiter} Use the information about the product to \
    generate the answer for the customer's query.
    You must only rely on the facts or information in the product information.
    Your response should be as detail as possible and \
    include information that is useful for customer to better understand the product.

    Step 4:{delimiter}: Answer the customer in a friendly tone.
    Make sure the statements are factually accurate.
    Your response should be comprehensive and informative to help the \
    the customers to make their decision.
    Complete with details such rating, pricing, and skills to be learnt.
    Use Neural Linguistic Programming to construct your response.

    Use the following format:
    Step 1:{delimiter} <step 1 reasoning>
    Step 2:{delimiter} <step 2 reasoning>
    Step 3:{delimiter} <step 3 reasoning>
    Response to user:{delimiter} <response to customer>

    Make sure to include {delimiter} to separate every step.
    """

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_message}{delimiter}"},
    ]

    response_to_customer = llm.get_completion_from_messages(messages)
    response_to_customer = response_to_customer.split(delimiter)[-1]
    return response_to_customer


def process_user_query(query):
    dict_of_courses = read_json_into_dict_of_courses()
    query_type = check_query_types(query)

    if 'Registration Issues' in query_type:
        divert_query_to_account_management()

    if 'Account Issues' in query_type:
        divert_query_to_account_management()

    if 'Other' in query_type:
        divert_to_customer_service()

    if 'Course Query' in query_type:
        category_and_product_response = identify_category_and_courses(user_message=query)

        course_details = get_course_details(
            list_of_relevant_category_n_course=category_and_product_response,
            full_course_dict=dict_of_courses
            )

        message_to_user = generate_response_based_on_course_details(user_message=query, product_details=course_details)

        return message_to_user


def divert_query_to_registration_dept():
    # A dummy implementatiom
    print("Forwarded the message to registration-internal@mail.com")

def divert_query_to_account_management():
    # A dummy implementation
    print("Forwarded the message to account-mngt-internal@mail.com")

def divert_to_customer_service():
    ## A dummy implementation
    print("Forwarded the message to account-mngt-internal@mail.com")



category_n_course_name = {
    "Programming and Development": [
        "Web Development Bootcamp",
        "Introduction to Cloud Computing",
        "Advanced Web Development",
        "Cloud Architecture Design",
    ],
    "Data Science & AI": [
        "Data Science with Python",
        "AI and Machine Learning for Beginners",
        "Machine Learning with R",
        "Deep Learning with TensorFlow",
    ],
    "Marketing": ["Digital Marketing Masterclass", "Social Media Marketing Strategy"],
    "Cybersecurity": ["Cybersecurity Fundamentals", "Ethical Hacking for Beginners"],
    "Business and Management": [
        "Project Management Professional (PMP)Â® Certification Prep",
        "Agile Project Management",
    ],
    "Writing and Literature": [
        "Creative Writing Workshop",
        "Advanced Creative Writing",
    ],
    "Design": ["Graphic Design Essentials", "UI/UX Design Fundamentals"],
}