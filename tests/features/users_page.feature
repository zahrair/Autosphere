Feature: Users Page Navigation

  Scenario: Navigate to Users page from logo
    Given I am on any page
    When I click the logo to return to the Environment page
    And I open the sidebar and go to the Users page
    Then I should land on the Users page successfully
  

  Scenario: Create a new user successfully
    Given I am on the Users page
    When I click Add User button
    And I fill in all user fields
    And I select the first role from dropdown
    And I select the first license from dropdown
    And I click Create User

  Scenario: Delete an existing user successfully
    When I open the action menu for "User Twelve"
    And I click delete for "User Twelve"
    And I confirm user deletion
    Then the user "User Twelve" should not be listed

  Scenario: Edit an existing user successfully
    When I open the action menu for "User Test"
    When I click the edit button
    And I update the user's name to "User Test Updated"
    And I update the user's password to "newPass123"
    And I save the updated user
    Then I should see the updated name "User Test Updated" in the users list

    