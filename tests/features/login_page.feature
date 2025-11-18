Feature: Login Page Opening and UI Verification

  Scenario: Perform login with valid credentials
    Given I am on the login page
    When I enter valid login credentials
    Then I should see my username displayed on the dashboard