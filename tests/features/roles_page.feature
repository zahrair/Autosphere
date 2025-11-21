Feature: Navigate to Roles Page and perform different Functionality
 

  Scenario: Click Roles tab and verify Roles Page is displayed
    Given I am on any page
    When I click the logo to return to the Environment page 
    When I click the Roles tab from the sidebar
    Then I should be navigated to the Roles page

  Scenario: Create a new role successfully
    When I click Create Role button
    And I fill the role name as "AutomationRole"
    And I select the first Environment option
    And I select the permission scheme Administrator
    And I click the Create Role button
    Then I should see the role "AutomationRole" in the roles table

  Scenario: Delete a  role successfully
    When I open the action menu for role "AutomationRole"
    And I click delete for role "AutomationRole"
    And I confirm deleting the role
    Then the role "AutomationRole" should not be listed in the roles table

  Scenario: Edit a  role successfully
    When I open the action menu for role "user_role"
    And I click the details option for role "user_role"
    And I update the permission scheme to "Administrator"
    And I save the updated role
    Then the role "user_role" should be updated successfully
