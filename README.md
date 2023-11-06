<center><img align="center" src="./static/todo/img/todo.ico" width="90"> </center>

# Django + HTMx • [TodoApp](http://todomvc.com)
> Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

> htmx gives you access to AJAX, CSS Transitions, WebSockets and Server Sent Events directly in HTML, using attributes, so you can build modern user interfaces with the simplicity and power of hypertext

## Functionalities

##### No todos
When there are no todos, #main and #footer should be hidden.

##### New todo
New todos are entered in the input at the top of the app. The input element should be focused when the page is loaded, preferably by using the autofocus input attribute. Pressing Enter creates the todo, appends it to the todo list, and clears the input. Make sure to .trim() the input and then check that it's not empty before creating a new todo.

##### Mark all as complete
This checkbox toggles all the todos to the same state as itself. Make sure to clear the checked state after the "Clear completed" button is clicked. The "Mark all as complete" checkbox should also be updated when single todo items are checked/unchecked. Eg. When all the todos are checked it should also get checked.

##### Item

###### A todo item has three possible interactions:

 - Clicking the checkbox marks the todo as complete by updating its completed value and toggling the class completed on its parent \<li>
 - Hovering over the todo shows the remove button (.destroy)
 - Double-clicking the <label> activates editing mode, by toggling the .editing class on its \<li>



##### Editing
When editing mode is activated it will hide the other controls and bring forward an input that contains the todo title, which should be focused (.focus()). The edit should be saved on both blur and enter, and the editing class should be removed. Make sure to .trim() the input and then check that it's not empty. If it's empty the todo should instead be destroyed. If escape is pressed during the edit, the edit state should be left and any changes be discarded.

##### Counter
Displays the number of active todos in a pluralized form. Make sure the number is wrapped by a \<strong> tag. Also make sure to pluralize the item word correctly: 0 items, 1 item, 2 items. Example: 2 items left

##### Clear completed button
Removes completed todos when clicked. Should be hidden when there are no completed todos.

## Implementation

### Using webserver or development Django server

##### Get the code

Clone this repository or download it from [Github](https://github.com/ReynaldoCC/todoDjangoHtmx/archive/refs/heads/main.zip)

    git clone https://github.com/ReynaldoCC/todoDjangoHtmx.git


##### Install requirements
Create virtual environment for app requirements and activate it

    python -m venv todo -p python3
    source todo/bin/activate

For development install the development requirements

    pip install -r requirements/dev.txt

For use or production install the production requirements

    pip install -r requirements.txt

#### run the app

Run the app using Django development server

    python manange.py runserver

Using gunicorn(needs to install production requirements)

    gunicorn config.wsgi:application --bind 0.0.0.0:8000

### Using Docker

##### Get the code

Clone this repository or download it from [Github](https://github.com/ReynaldoCC/todoDjangoHtmx/archive/refs/heads/main.zip)

    git clone https://github.com/ReynaldoCC/todoDjangoHtmx.git

Using Docker you can run the app using docker as it, typing command run

    cd todoDjangoHtmx
    docker build .
    docker run -e DJANGO_SECRECT_KEY=yournewsecrectkey -p 8000:8000

Or even you can run it with docker-compose

    cd todoDjangoHtmx
    docker-compose up

## Credit

Created by [Reynaldo Cuenca Campos](http://reynaldocc.github.io)
