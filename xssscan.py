import requests
from pprint import pprint
from bs4 import BeautifulSoup as bsoup
from urllib.parse import urljoin

def extract_all_forms(url):
    """It returns all the forms from a given url"""
    soup = bsoup(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def extract_form_details(form):
    """
    To extract all possible information from a html form
    """
    details = {}
    # extract the form action
    try:
        action = form.attrs.get("action").lower()
    except:
        action = ""
    # extract the form method e.g GET,POST etc
    method = form.attrs.get("method", "get").lower()
    # extract all the input details such as type and name
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    # store details in the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form(formDetails, url, value):
        """
        Submits a form given in `formDetails`
            formDetails is a dictionary that contain form information
            value -> this will be replaced to all text and search inputs
        It will return the HTTP response
        """
        # complete the url
        targetUrl = urljoin(url, formDetails["action"])
        # get the inputs
        inputs = formDetails["inputs"]
        data = {}
        for input in inputs:
            # replace text to search values with `value`
            if input["type"] == "text" or input["type"] == "search":
                input["value"] = value
            input_name = input.get("name")
            input_value = input.get("value")
            if input_name and input_value:
                data[input_name] = input_value

        if formDetails["method"] == "post":
            return requests.post(targetUrl, data=data)
        else:
            return requests.get(targetUrl, params=data)

def check_xss(url):
    """
    returns all xss vulnerable in a given URL
    """
    #extract forms from the url
    url="https://www."+url
    forms = extract_all_forms(url)
    xss_payload = "<script>alert('hi')</scripT>"  
    # flag value
    is_vulnerable = "0"
    # iterate over all forms
    for form in forms:
        formDetails = extract_form_details(form)
        content = submit_form(formDetails, url, xss_payload).content.decode()
        if xss_payload in content:
            return formDetails

    return is_vulnerable
    


