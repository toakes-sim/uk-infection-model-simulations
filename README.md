# uk-infection-model-simulations
The code base for running simulations of a fake infection that has taken hold of the UK. The simulations are driven by infecting patients and then monitored through patient doctor interactions.

## Pre-requisits
you will need to set up a few thing for this code to run correctly.
- Firstly, an instance of ollama ideally running on a GPU. 
- Second, an SQL schema, I used MYSQL but any should be fine with slight code adjustments.
  
### Environmental variable to be aware off
There are some environmental variables you will have to set up to make sure the code has access to what it needs.
- SQL schema connections MYSQLDATABASENAME, MYSQLUSERNAME, MYSQLPASSWORD.
- If, like me, you are running Ollama on a different machine you will need OLLAMA_IP, or simply set it to 'localhost'
- Finally the data storage location, STORAGE_LOCATION.

## Entry points
The code is set up to be triggared by two scripts, located in src/jobs
- Always make sure that set_up_entry_point.py has been run to prepopulate the surgeries and the doctors.
- The main simulation entry point is in appointment_simulation_entry_point.py, if set up has been successful this can be run as many times as you like.

## Some Runtime Context
This will vary between machines and rely on your particluar set up, but my runtime managed 10K appoinments in ~1day.
