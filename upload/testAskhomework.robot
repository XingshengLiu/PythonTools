*** Settings ***
Documentation    Suite description

*** Test Cases ***
Test title
    [Tags]    DEBUG
    Provided precondition
    When action
    Then check expectations

两数求和
    [Tags]    DEMO
    log    hello,RF
    ${sum}=    evaluate    12+13

*** Keywords ***
Provided precondition
    Setup system under test