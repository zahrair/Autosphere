from pytest_bdd import scenarios, given, when, then
from tests.pages.processes_page import ProcessesPage

scenarios('../features/processes_page.feature')


@when("I click on the Processes sidebar option")
def click_sidebar_processes(page):
    processes = ProcessesPage(page)
    processes.open_processes_section()


@then('I should see the heading "Processes" on the page')
def verify_processes_heading(page):
    processes = ProcessesPage(page)
    processes.verify_processes_heading()



@when("I click the Create Process button")
def click_create(page):
    ProcessesPage(page).click_create_process()


@when('I fill the process name "process5"')
def fill_name(page):
    ProcessesPage(page).fill_process_name("process5")


@when("I select a machine from the dropdown")
def select_machine(page):
    ProcessesPage(page).select_machine()


@when("I upload the robo file")
def upload_file(page):
    ProcessesPage(page).upload_robo_file()


@when('I fill the execution name "process5_exec"')
def fill_execution(page):
    ProcessesPage(page).fill_execution_name("AddQueueItem")


@when("I click the Create button for process")
def submit(page):
    ProcessesPage(page).submit_process()


@then('I should see "process5" in the processes table')
def verify(page):
    ProcessesPage(page).verify_process_present("process5")
    
@given("I am on the Process page")
def open_robots_page(page):
    process = ProcessesPage(page)
    process.open_processes_section()
    process.verify_processes_heading()

@when('I open the menu of the process')
def open_robot_menu(page):
    ProcessesPage(page).open_robot_menu("process5")


    
    