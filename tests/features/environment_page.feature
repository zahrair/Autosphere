Feature: Environment Page Verification
  Verify that after login, user can open the environment and see correct username

  Scenario: Open Zahra environment and verify username
    When I open my environment card
    Then I should see my username "zahra" displayed on the page
