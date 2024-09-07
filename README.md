Goals & Tasks Management App
This application is designed to help you manage goals and their associated tasks. It provides an intuitive interface for scheduling, editing, and updating goals, allowing users to track progress, handle interruptions, and manage downtime effectively.

Features
Goals Management
Add, edit, and manage goals along with associated tasks. You can schedule when each goal starts and monitor its progress.

Tasks Scheduling
Each goal can have multiple tasks associated with it. Tasks can be created, edited, and updated dynamically as per the needs of the goal.

Real-Time Updates
Track the current state of goals and tasks in real-time. The application allows for continuous updates, ensuring you have the most up-to-date information.

Downtime and Interruptions
Manage downtime or interruptions effectively by marking specific goals as paused or aborted. You can also specify the reasons for downtime.

Interactive UI
Utilize a modern, interactive UI with modals, popovers, and number inputs for editing tasks, scheduling goals, and handling interruptions.

Getting Started
Prerequisites
To run this application, you will need:

Node.js and npm installed
A compatible browser (Chrome, Firefox, etc.)
A running API endpoint for managing goals and tasks
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/goals-tasks-management-app.git
Navigate into the project directory:

bash
Copy code
cd goals-tasks-management-app
Install dependencies:

bash
Copy code
npm install
Start the application:

bash
Copy code
npm start
The app should now be running at http://localhost:3000.

Usage
Main Components
Goal Scheduler
The main view displays a timeline of goals and their tasks. You can scroll through different dates and view the progress of each goal over time.

Task Management
Each goal has tasks that can be scheduled with specific start dates. Tasks are color-coded and represent different stages like "Starting", "Running", "Finishing", etc.

Goal Menu
Each goal block contains a menu for actions like editing tasks, aborting the goal, or marking downtime. These actions can be accessed via popovers and modals.

Editing Tasks
You can edit the number of tasks associated with a goal using a number input field. The app will validate your input and ensure tasks are updated correctly.

Handling Downtime
When a goal is interrupted, you can mark it as "Down" and specify the reason for downtime (e.g., "Maintenance", "Power Failure", etc.).

Interactions
Add/Edit Goal: Use the UI to specify a goal, assign tasks, and schedule when it should start.
Abort/Stop Goal: If a goal needs to be stopped or aborted, you can trigger this action through the menu.
Handle Downtime: Manage any interruptions by marking the downtime reason and adjusting tasks as needed.
API Integration
This application interacts with an external API to store and retrieve goal and task information. The following endpoints are used:

/api/goals: Fetch and manage goals.
/api/tasks: Fetch and manage tasks associated with goals.
/api/calendar/update: Update the schedule and status of tasks for goals.
Make sure to have the API running and configured properly for the app to function correctly.

Development
Folder Structure
/src/components: Contains the main React components used in the app, such as forms, popovers, modals, and schedulers.
/src/api: Handles API calls for managing goals and tasks.
/public: Static files like HTML and CSS.
Main Files
App.js: The main entry point of the application.
SchedulerTable.js: Displays the table of scheduled goals and tasks.
IconMenu.js: Handles the menu interactions for each goal.
Customization
You can customize the app by adding new features, modifying the goals and tasks logic, or extending the UI components. To do so, work within the /src/components directory where most of the UI logic resides.

Technologies Used
React.js: For building the UI components and handling state management.
Material UI: For styling the components and providing pre-built UI elements like buttons, menus, and inputs.
Axios: For making API calls to the backend.
