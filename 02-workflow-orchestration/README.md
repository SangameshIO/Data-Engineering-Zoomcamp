orchestration is making sure to use 
diffrent tools and proccess come together to produce a correct result 
example 
 like orchestrator in music band 
 drums guitar are tolls and once controlling them is orchestrator
consider tea making 
boil water 
add tea powder 
addmilk 
poure into cup 

    orchestrator understand the sequence of steps to be performed 
    and dependency between them 
    and also orchestrator helps in logging , retry 
    regularly running workflows via schedule or event 


kestra
    it is a workflow orchestrator 
    it is programming language agnostic 
    it can handle code , no code , ai workflows 
    it can also regularly run workflow or based on events as well


concepts for kestra 

kestra 
flows 
workflow container 
need 
    id : uniqueidentifier for workflow 9immutable once saved)
    namespace : name for similar or related workflows 
every workflow starts with flows 
example 
    id : myflow
    namespace : company.team


tasks 
    steps within workflows 
    each do some fundamental work 
    example : logging  a message , api request etc 
    need 
        id : identifier for step 
        type : type of step (example  : io.kestra.plugin.core.log.Log)
        message : hello world(diffrent properties according to type)
example 
    id : name 
    type : io.kestra.plugin.core.log.Log
    message : "hello sangamesh"

    id : kestra 
    type : io.kestra.plugin.core.Request 
    uri : "https.//chrome" (url or api)
there are two diffrent type of tasks 
    runnable  tasks 
        these do work like send api request or log 
    flowable tasks 
        help in orchestration logic like branching , loops 
    

inputs 
    in order to give diffrent input every time workflow runs we use workflow 
    requires 
        id : identifier for input 
        type : type of data (string , number)
        extra params 
            required : if input is mandatory for workflow 
            displayname : gui freindly name 
            defaults : default value if no input is given 
            description : helpful context 
inputs are accessed using expressions 
expressions are closed within flower brackets like this {{}}
{{inputs.inputid}}
example 
id: myworkflow
namespace: company.team

inputs:
  - id : name 
    type : STRING
    defaults : will

tasks:
  - id: hello
    type: io.kestra.plugin.core.log.Log
    message: "Hello {{inputs.name}}"

outputs 
these are results when tasks run some tasks produce output and some does nto 
these can be accessed using {{outputs.tasks_id.output_value}}
tasks_id : name of task that produce output 
output_value : name of output among all output
example : url response contains 
    uri , body , code , headers 
    choose one among these for output_values 
output can be anyahitng 
file 
rows from db query etc 


example 

make sure to use double quotes for inputs and outputs 

triggers 
when of the flows 
 types of  triggers 
    schedule triggers 
        based on cron expression 
    polling triggers 
        based on periodic checking if file is modified etc 
    realtime triggers 
        respond instantly events new file in s3 
    webhook triggers 
        when a request is made at specific endpoint 
    flow hook triggers 
        when another workflow complets 

example 
triggers
    - id : schedule
      type : io.kestra.plugin.core.trigger.schedule
      cron : "0 0 9 * *' 
depending on type of trigger there can be some other properties 

you can change the  inputs to steps by giving inputs in triggers 
and also one flow can have many triggers and diffrent input in each sschedule 
example 
id: myflow
namespace: company.team


triggers:
  - id: schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "41 6  * * *"
    inputs:
      uri : "https://kestra.docs.io"
    
  - id : evening_schedule
    type : io.kestra.plugin.core.trigger.Schedule
    cron: "42 16 * * *"
    inputs : 
        uri : "htts://kestra.io"

inputs:
  - id: uri
    type: STRING
    defaults : https://kestra.io


tasks:
  - id: make_request
    type: io.kestra.plugin.core.http.Request
    uri : "{{inputs.url}}"

  - id : log_status 
    type : io.kestra.plugin.core.log.Log
    message: "status : {{outputs.make_request.code}}"


you can add conditions that check if previous workflow or other workflow 
before running this worlflow 


expressions 
expressions can access 
inputs 
outputs 
flow : id , namespace , revision 
trigger : trigger information(mostly (id , type , cron if other present then those as well))
execution : execution metadata id , startdate , state
there are many functions already written to mainpulate and tranform data 
for example 
1+2 = 3
{{1+2}} returns 3
function to convert string to numbver 
{{"1.2" | number}} returns 1.2 
some other function 
parse json (jq can be used)
format date etc 

debug expressions 
    ui in kestra to check expression if they work fine before 
    using them in flow 
    outputs.code == 200(condition logic)


flowable  tasks 

helps in execution of flow rather than in compuation 
example 
    conditional branching
    looping same workflow again and again 

various types of flowable tasks in kestra 
if 
    then (true)
    else (otherwise)

switch 
    case 1 
    case 2 
etc 

foreach : for each value in an array 
foreachitem : run a subflow for each value in a file (better for large data(performance))
loopuntil : run until a condition is met 

parallel : helps run mutliple workflow simultaneously 
subflow : reusable flows that other flows can trigger like functions 

example for flowable tasks 


id: myflow
namespace: company.team

inputs:
  - id: uri
    type: URI
    defaults: https://kestra.io

tasks:
  - id: make_request
    type: io.kestra.plugin.core.http.Request
    uri: "{{ inputs.uri }}"

  - id: check_status
    type: io.kestra.plugin.core.flow.If
    condition: "{{ outputs.make_request.code == 200 }}"
    then:
      - id: log_success
        type: io.kestra.plugin.core.log.Log
        message: "Request successful"
    else:
      - id: log_error
        type: io.kestra.plugin.core.log.Log
        message: "Request was not successful: {{ outputs.make_request.code }}"


subflows 
id: mysubflow
namespace: company.team

inputs:
  - id: uri
    type: URI

tasks:
  - id: make_request
    type: io.kestra.plugin.core.http.Request
    uri: "{{ inputs.uri }}"

  - id: log
    type: io.kestra.plugin.core.log.Log
    message: "{{ outputs.make_request.code }}"

outputs:
  - id: data
    type: STRING
    value: "{{ outputs.make_request.code }}"

mainflow using subflow 

id: myflow
namespace: company.team

tasks:
  - id: subflow
    type: io.kestra.plugin.core.flow.Subflow
    namespace: company.team
    flowId: mysubflow
    inputs:
      uri: https://kestra.io
      
  - id: log_status_code
    type: io.kestra.plugin.core.log.Log
    message: "{{ outputs.subflow.outputs.data }}"


execution 
single run of workflow 
made of task runs 
each taskruns gets its own logging of input , output 
time it took to complete failed or succeeded 

states of execution
created : it is created not yet started 
running 
success 
failed : 

data in each execution 
visualisation veiws like : gantt chart , topology view 
outputs : 
metrics 
logs : detailed information about what happened in each execution 


replaying execution 
kestra does have version history of flow each time we sae flow new revision is created 

replay 
it is ability to run only some tasks with original execution 
it helps in debugging original flow 


secrets 
stored as env variables but base64 encoded 

example 

echo 'my_secret' | base 64 

secret_api_key = 'my_secret_base64_encoded' 

we can access it using {{secret(my_secret}}
secret function 
id: myflow
namespace: company.team

tasks:
  - id: call_api
    type: io.kestra.plugin.core.http.Request
    uri: https://api.example.com/data
    headers:
      Authorization: "Bearer {{ secret('MY_SECRET') }}"

plugins 
it helps in having common tasks easy to maage by using code built for the same 
purpose so that you dont  need to write it from scratch 
example
https.Request plugins 
slack notification plugins 


blueprints 
or catalog of flows that are already in use and are quite general 



other concepts of kestra 

variables 
to have inputs modified further like 
url/endpoint1 
url/endpoint2 

example 
variables
 myvar : hello 
 numeric_variable : 42 
 time : {{now()}}

tasks 
    - id : log 
      type : io.kestra.plugin.core.Log 
      message : "{{vars.myvar}} world {{vars.numeric_variable}} {{render(vars.time)}}"

use render to process expression before getting value frm varaible 
will work for all nested varaibles as well 

plugindefaults 
kestra:
  plugins:
    defaults:
      - type: io.kestra.plugin.aws.s3.Upload
        values:
          accessKeyId: "{{ secret('AWS_ACCESS_KEY_ID') }}"
          secretKeyId: "{{ secret('AWS_SECRET_ACCESS_KEY') }}"
          region: "us-east-1"

it is used to set common properties like debug level 
or credentails for process across workflows 



guides for kestra flows 
do not use tabs in flows use spaces 
use double quotes for string and expressions 
and | is used for multiline scripts 

if an object like array you are describing use - otherwise not 
example 
in inputs:
   - id: array01
     type : ARRAY
     defaults : 
      - brand
      - price
dont leave space between key and semicolon 


executing python script 
ways 
  script 
    less lines of code in python written in kestra workflow
  commands 
    local python sepaerate file 
    can be written in namespace 
    and used in workflow 

io.kestra.plugin.scripts.python.Commands 
script 
  io.kestra.plugin.scripts.python.Script 

in commands if you use docker then there will be no clash in dependencies 
and you can give custom image to docker to run the script 


another way to run script is by subprocess 
it acts as another process 
but if kestra is running locally it is better to use venv 