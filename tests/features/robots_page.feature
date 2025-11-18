Feature: Robots Page Functionality

  Scenario: Open Robots section from sidebar
    When I click on the Robots sidebar option
    Then I should see the heading "Robots" on the page


  Scenario: Create a robot named robo2
    Given I am on the Robots page
    When I click the Create Robot button
    And I enter "robo2" in the Machine Name field
    And I select a robot license
    And I filled Working Directory field
    And I click the Create button
    Then I should see "robo2" listed in the robots table
 
  Scenario: Delete a robot through menu and confirmation
   Given I am on the Robots page
   When I open the menu of the robot 
   And I click the delete button 
   And I confirm the delete action
   Then I should not see it in the robots table

  Scenario: Edit an existing robot's name
    Given I am on the Robots page
    When I open the menu of the robot for editing 
    And I click the edit button for that robot
    And I change the robot description
    And I click the Update button
    Then I should see listed in the robots table
