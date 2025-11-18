Feature: Navigate to Roles Page and perform different Functionality
 

  Scenario: Click Roles tab and verify Roles Page is displayed
    Given I am on any page
    When I click the logo to return to the Environment page 
    When I click the Roles tab from the sidebar
    Then I should be navigated to the Roles page