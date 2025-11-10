Feature: Login Page Functionality Testing

  Scenario: Verify static elements on the Login Page
    Given I open the login page
    Then I should see the Autosphere text
    And the Username and Password labels
    And the Login button
    And the Login card should be centered

  Scenario: Verify valid login
    Given I open the login page
    When I enter valid credentials
    Then I should be logged into the dashboard

  Scenario: Verify invalid login
    Given I open the login page
    When I enter invalid credentials
    Then I should see a login error

  Scenario: Verify logout functionality
    Given I am logged in
    When I perform logout
    Then I should be redirected back to the login page
