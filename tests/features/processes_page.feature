Feature: Processes Page

  Scenario: Open the Processes section from sidebar
    When I click on the Processes sidebar option
    Then I should see the heading "Processes" on the page
  
  
  Scenario: Create a new process successfully
    When I click the Create Process button
    And I fill the process name "process5"
    And I select a machine from the dropdown
    And I upload the robo file
    And I fill the execution name "process5_exec"
    And I click the Create button for process
    Then I should see "process5" in the processes table

 
