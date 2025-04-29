*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}               https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${VALID USER}        Admin
${VALID PASS}        admin123

${INVALID USER}      SaiTen
${INVALID PASS}      SaiMatKhau

*** Test Cases ***
Valid Login
    [Documentation]    Kiểm tra đăng nhập hợp lệ với OrangeHRM
    Open Login Page
    Input Username    ${VALID USER}
    Input Password    ${VALID PASS}
    Submit Credentials
    Verify Login Success

Invalid Login
    [Documentation]    Kiểm tra đăng nhập không hợp lệ với OrangeHRM
    Open Login Page
    Input Username    ${INVALID USER}
    Input Password    ${INVALID PASS}
    Submit Credentials
    Verify Login Failed

*** Keywords ***
Open Login Page
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Wait Until Element Is Visible    xpath=//input[@name='username']    10s

Input Username
    [Arguments]    ${username}
    Input Text    xpath=//input[@name='username']    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    xpath=//input[@name='password']    ${password}

Submit Credentials
    [Documentation]    Nhấn nút đăng nhập
    Click Element    xpath=//button[@type='submit']
    Sleep    2s

Verify Login Success
    [Documentation]    Kiểm tra trang Dashboard sau khi đăng nhập thành công
    Wait Until Page Contains Element    xpath=//h6[text()='Dashboard']    10s
    Page Should Contain Element    xpath=//h6[text()='Dashboard']
    Log To Console    Đăng nhập thành công

Verify Login Failed
    [Documentation]    Kiểm tra thông báo lỗi khi đăng nhập sai
    Wait Until Element Is Visible    xpath=//p[contains(text(),'Invalid')]    10s
    Page Should Contain    Invalid credentials
    Log To Console    Đăng nhập không thành công
