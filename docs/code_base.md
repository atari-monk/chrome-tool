# Code Base Overview

## Chrome scripts

### Chrome Profiles

-   json config

    -   defines chrome profile path template
    -   defines computers

-   get_chrome_profile
    -   loads config
    -   checks profile exists
    -   returns profile data

### Chrome Automation

-   open_chrome_with_profile
    -   checks valid url
    -   gets chrome profile
    -   sets chrome options
    -   lunches browser
    -   returns driver

## Utils

### Json Utils

-   convert_paths_to_json_safe
    -   converts paths in json string to forward slash /
-   append_json_strings_to_array
    -   appends json string or list of them to file

## Chatgpt Automation

### Chatgpt Automation

-   send_prompt

    -   sends prompt as a one line string

-   send_multiline_prompt

    -   sends prompt by typing each line stacking them with shift + enter

-   save_response

    -   saves last chatgpt response in markdown file

-   save_code_block
    -   appends last chatgpt response, that is code block, to json/md/txt file

### Chatgpt CLI

-   open_chatgpt_session

    -   opens chatgpt, waits x seconds

-   send_chatgpt_prompt

    -   sends prompt with multiline method, waits x seconds

-   save_chatgpt_code_block
    -   saves last response code block, waits x seconds

## Archive

-   TaskPrompt
    -   fetches task form api
    -   generates prompt
-   CodeAgent
    -   use ChatGPTAgent
    -   sends TaskPrompt prompt

## Agents

-   ChatGPTAgent
    -   class with ability to:
        -   send_prompt
        -   save_code
-   CodeBaseAgent
    -   agent with ability to process path with py code and produce metadata about it

## TDD Tool

-   tdd_pipe
    - script to simulate tdd process with chatgpt
    - implementing interface, unit test for feature, empty implementation
    - checks syntax and typing up to 2 times
    - runs tests to fail all of them as first step of tdd
    - failed subproject
    - to complex
    - to little gain! relative to efort
    - planning is needed and much modest time and features needed to be planned to reach implementations that are gaining something much faster and in managable increments of 1 hr 

    TDD Pipe flow: //(part)
    ```plaintext
    Element1 //defines what to implement
    //Interface, Class, UnitTest
    //1-implementation, 2-syntax validation, 3-strict types validation
    I1->I2->I3
    C1->C2->C3
    T1->T2->T3
    //run unit tests
    UT
    UT_Feedback (all test should fail in tdd initial state)
    ```