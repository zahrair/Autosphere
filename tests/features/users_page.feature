Feature: Users Page Navigation

  Scenario: Navigate to Users page from logo
    Given I am on any page
    When I click the logo to return to the Environment page
    And I open the sidebar and go to the Users page
    Then I should land on the Users page successfully
