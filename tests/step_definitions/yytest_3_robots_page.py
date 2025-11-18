from pytest_bdd import scenarios, given, when, then
from tests.pages.robots_page import RobotsPage

scenarios('../features/robots_page.feature')


@when("I click on the Robots sidebar option")
def click_sidebar_robots(page):
    robots = RobotsPage(page)
    robots.open_robots_section()

@then('I should see the heading "Robots" on the page')
def verify_heading(page):
    robots = RobotsPage(page)
    robots.verify_robots_heading()


@given("I am on the Robots page")
def open_robots_page(page):
    robots = RobotsPage(page)
    robots.open_robots_section()
    robots.verify_robots_heading()

@when("I click the Create Robot button")
def click_create(page):
    RobotsPage(page).click_create_robot()

@when('I enter "robo2" in the Machine Name field')
def fill_machine_name(page):
    RobotsPage(page).fill_machine_name("robo2")

@when("I select a robot license")
def select_license(page):
    RobotsPage(page).select_robot_license()

@when('I filled Working Directory field')
def fill_directory(page):
    RobotsPage(page).fill_working_directory("D:\\Autosphere")

@when("I click the Create button")
def click_submit(page):
    RobotsPage(page).submit_robot_creation()

@then('I should see "robo2" listed in the robots table')
def verify_robot(page):
    RobotsPage(page).verify_robot_present("robo2")
    
@given("I am on the Robots page")
def open_robots_page(page):
    robots = RobotsPage(page)
    robots.open_robots_section()
    robots.verify_robots_heading()

@when('I open the menu of the robot')
def open_robot_menu(page):
    RobotsPage(page).open_robot_menu("robo2")

@when('I click the delete button')
def click_delete_button(page):
    RobotsPage(page).click_delete_button("robo2")

@when('I confirm the delete action')
def confirm_delete_action(page):
    RobotsPage(page).confirm_delete_action()

@then('I should not see it in the robots table')
def verify_robot_not_present(page):
    RobotsPage(page).verify_robot_not_present("robo2")
    
    
@when('I open the menu of the robot for editing')
def open_robot_menu(page):
    RobotsPage(page).open_robot_menu("robo3")

@when("I click the edit button for that robot")
def click_edit_button(page):
    RobotsPage(page).click_edit_button()

@when('I change the robot description')
def change_robot_description(page):
    description_text = "Updated description for robo3" 
    RobotsPage(page).edit_robot_description(description_text)    

@when("I click the Update button")
def click_update_button(page):
    RobotsPage(page).submit_robot_edit()

@then('I should see listed in the robots table')
def verify_updated_name(page):
    RobotsPage(page).verify_robot_present("robo3")