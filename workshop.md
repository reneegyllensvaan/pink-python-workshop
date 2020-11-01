# PP AMQP/Python Workshop, Nov 2020

## Step 1. Introduction
(Read the slides and wing it)


## Step 2.
Let's start by trying out the Python interpreter REPL. First, we'll open a new
terminal window. If you followed the setup instructions using `conda`, you'll
first run `conda activate`. Next, we will start the interpreter with the
`python` command. Let's start with some basic arithmetic expressions:

_(reader's note: lines starting with `#=>` are output, lines that do not are
input we've typed)_
```python
1 + 2
#=> 3

456 + 123*1000
#=> 123456
```

Just as often, we want to work with text, rather than numbers, so we'll write
_strings_, which are sequences of characters enclosed in single or double
quotes. We can add strings to each other with `+`, this will concatenate them:
```python
'Hi there!'
#=> 'Hi there!'

'Something' + ' & ' + 'Another'
#=> 'Something & Another'
```

So other than using this language as a glorified calculator, we can save values
to names by declaring that that name should be equal to it:
```python
first_name = 'Ada'
last_name = 'Lovelace'

full_name = first_name + ' ' + last_name
full_name
#=> 'Ada Lovelace'

roughly_pi = 3.14
x = 10
x = x*roughly_pi
x
#=> 31.4
```

Program execution runs line by line, from top to bottom, unless the code we've
entered clearly forms only a part of a valid statement. This would mean a lot
of repetition to do anything significant, so what we can do is encapsulate
behavior into functions, using the `def` statement. The following code
corresponds to "Define a function with the name `greet`, that takes one
parameter, called `name`." The next block of code with increased _indentation_
(which is what we call an increment of 4 spaces at the start of a line) is the
body of the function, which states "save the string `"Hello, "`, followed by
the value of the `name` parameter to the `greeting` variable. Then, invoke the
`print` function, providing `greeting` as the value. Finally, also send
`greeting` back to whoever used this function." `print` is also a function, one
that the Python environment provides for us by default. It writes a line of
text as output, and is one of the two functions used for making interactive
terminal applications.

```python
def greet(name):
  greeting = 'Hello, ' + name + '!'
  print(greeting)
  return greeting
```

We can pull in externally defined functions using the `import` statement. These
can be defined by Python, they can be files in our project, or they can be
external modules, like the `pika` library we installed as preparation for the
workshop.
```python
# The `from` syntax is a shorthand for fetching only one name from the module
from random import random

print(random())
#=> 0.8518634904227518
```

Finally, we'll just cover three useful features: conditionals, looping, and
lists. This will be very brief and you could have a workshop dedicated to each
of these, so this is only a quick run-down.

We can use an `if` statement to only execute code if some value is not equal to
the _empty state_ for some type. For any value, `None` is empty.
```python
# We can compare two values using `==` between them
if 1 == 2:
    print('This code will never run.')

from random import random

# We can provide a fallback tht will only run if the condition is not true
if random() > 0.5:
  print('Heads!')
else
  print('Tails!')
```

We can collect multiple values into one "bucket" with a `list`.
```python
# Make a new list with 3 members
a = [10, 20, 30]

# Lists start counting at 0
a[0]
#=> 10
a[1]
#=> 20
a[2]
#=> 30

# Use the built-in `len` function to get the number of items in a list
len(a)
#=> 3
```

Lastly, we can use the `for` statement to _loop_ over a container, running some
code for very member of that container:
```python
total_sum = 0
for value in [5, 10, 20]:
  total_sum = total_sum + value

total_sum
#=> 35


people_to_greet = [
    'my darling',
    'my honey',
    'my ragtime gal',
]

for el in people_to_greet:
    greet(el)
#=> Hello, my darling!
#=> Hello, my honey!
#=> Hello, my ragtime gal!
```

Again, this workshop is not about the intricacies of program control flow, but
these are core tools for writing Python programs.

## Part 3. Network communication
To communicate with each other, we will be using the AMQP protocol. AMQP is a
protocol used widely in the industry for real-time applications -- programs
where we don't need to constantly ask a server for changes -- they will call
us. An example of a real-time system would be an email app. We don't want to
have to call out to the email server that holds our emails every 5 seconds to
check whether we have new messages, especially because in 99% of calls the
answer to this would be "no". This goes double because input and output is
usually the most performance-demanding part of many classes of programs.
Real-time systems can ping us when we get a new message, at which point we can
fetch them to our device.

This workshop is about building clients for AMQP, as a
server is both less useful (there are already several high-quality
implementations) and a significant undertaking. To say that we'll be _using_
AMQP is maybe a bit charitable -- we're going to bastardize it into an instant
messaging program, because it's fun and nobody can tell us not to.

The first step is to set up or have access to a server running on some computer
somewhere. As mentioned, I've set one up for this workshop, if you're
interested and would like help setting one up after the workshop, reach out to
me on the participants' Slack. The credentials for getting access to this
server are included in the repository for this workshop. _(reader's note: if
you are reading this after the workshop, that server is most likely
decommissioned by now)_

### The AMQP Model -- Queues
The 'Q' in AMQP is for "queue", which are the core of the protocol. A queue is
a stream of messages, roughly like a mailbox, that connected clients can send
messages to. Queues have a name, which is the identifier separate clients say
they want to send or receive to, so that client A can know they are sending
messages that will be received by client B, equivalent to the address on a
mailbox. Clients with something to say can put a letter in the mailbox with a
certain address (called _publishing_ to a queue), and then clients that want to
take letters out of that mailbox can listen for new messages, and be instantly
notified (this is called _consuming_ on a queue).


## Part 4. Let's write some code!
As mentioned, will be using the Pika library for Python to connect to our
server. The first step is to actually establish a connection to the server.
Pika requires some configuration to do this, which we have broken out into a
file, which is included in the repository. If you do not have this and are not
comfortable using `git`, you can download it from the website, either as a zip
file or just the file in question. It isn't super complicated, and there are
comments, if you are interested in what is happening behind the scenes, but the
main reason it's not included is that it's the least interesting part of our
code.

Since we're expecting to write more code now, we'll create a new file -- let's
call it `main.py` -- and put the code in it. We start by connecting to the
server using the
`make_connection` helper.
```python
import pika
from workshop_helper import make_connection

connection = make_connection()
```

Pika's model uses a "channel" between the server and our client that we "talk
to" to send and receive messages. One thing we can say to the channel is "Hey,
I want there to be a queue called 'chat' on the server. Create one if it
doesn't exist, otherwise do nothing."
```python
import pika
from workshop_helper import make_connection

connection = make_connection()

channel = connection.channel()
channel.queue_declare(queue='chat')
```

## Step 5. Publishing
Now that we have our channel, we can start to actually use it for
messaging! [pull up the `listen.py` script in a new terminal window on the
screen] We can do this in any order, but since I can pull up a view where we
can see all see our messages, we can start with sending messages. This
highlights a chicken-and-egg problem with implementing communications protocols
in general -- you need a working listener to verify that your sender is
working, but you can't really debug your listener if nobody is sending
anything.

First, let's refactor our file a bit so we declare configuration separately
from our behavior. In a real-world scenario we would be letting users of our
program configure this in a file somewhere on their computer, but in the
interest of time, we will hard-code these values.
```python
import pika
from workshop_helper import make_connection

queue_name = 'chat'

connection = make_connection()

channel = connection.channel()
channel.queue_declare(queue=queue_name)
```

### Publishing
Let's declare our sending behavior as a function called `send`. We declare this
in the same file. This is only a function call away, which we invoke on our
channel:
```python
import pika
from workshop_helper import make_connection

queue_name = 'chat'

connection = make_connection()

channel = connection.channel()
channel.queue_declare(queue=queue_name)

def send(channel, routing_key, message):
    channel.basic_publish(
        exchange='',
        routing_key=routing_key,
        body=message,
    )
```
The `routing_key` here is used by the server to determine where to route the
message we've sent. The reason this isn't just called "queue" is that the
routing key won't always refer to only a queue. There are other, different
routing strategies that our server can use. The `exchange=''` argument tells
the channel to publish to the global exchange -- we will get to these in a
moment. For now, the core takeaway is that if we provide `exchange=''`, then
the routing key will be a queue to publish the message to, the rest is magic.

To run this, we can once again take advantage of the fact that Python is an
interpreted language. We don't have to implement all the user interaction, we
can just interactively call the function from the interpreter:
```python
from workshop import channel, send, queue_name

send(channel, queue_name, 'hi there!')
send(channel, queue_name, 'testing, one, two, three')
```

Try it out with your own message and see if it appears on the screen share.

## Step 6. Consuming
Next, we want to actually be able to listen for the messages we and others send
to the queue. We do this using the `basic_consume` function. This function
takes 2 required parameters: a `queue` to consume on, and an
`on_message_callback`. _Callback_ is a programming term meaning "a variable
pointing to a function that will be called in order to handle some event", in
this case the event is the data related message we have consumed. The
non-obvious but incredibly useful aspect of this is that just like a number,
list, or string, a function is also a value that we can save to variables, can
be put in a list, can be used as an argument for another function, and can even
be constructed inside another function and then returned as a value. This is a
key pattern in functional programming languages. To be clear, Python is not a
functional programming language, but it is flexible and high-level enough to
allow us to use many of the most useful design patterns and features from
functional programming languages.

Just to demonstrate the concept, let's step back to the interpreter REPL. Start
by just trying out a `for` loop with a `range`, when we just want to run
something a certain number of times:
```python
def print_a_few_times(times):
    for _ in range(times):
        print('hi there')

# And in a repl:
print_a_few_times(5)
#=> hi there
#=> hi there
#=> hi there
#=> hi there
#=> hi there
```

Then, we make our function take a callback to run the same function on a value
multiple times. We also have to define a few functions to use as callbacks, so
that we can try our function out. Note that we do not put parentheses after
`add_two` and `duplicate`, even though they are functions -- we are interested
in them as values to pass around, and only when their name is `f`, inside the
`iteratively_apply` function, do we care about their values.
```python
def iteratively_apply(f, value, times):
    result = value
    for _ in range(times):
        result = f(result)
    return result

def add_two(value):
    return value + 2

def duplicate(value):
    return value * 2

iteratively_apply(add_two, 2, 5)
#=> 12
iteratively_apply(duplicate, 2, 5)
#=> 64
```

We can use callbacks to send a message handler as a parameter when we consume
messages. As mentioned, we'll use the `basic_consume` function. Let's take a
look at the documentation for it.  The queue will be the `queue_name` we broke
out into a variable earlier. The `on_message_callback` will then have to be
another function we declare. Let's keep it simple and just call it
`on_message`. We see from the docs that the `on_message_callback` should have a
function signature -- which means what arguments, how many, and it what order
it expects them -- is `(channel, method, properties, body)`. Let's start by
writing the `on_message` function. We can define this inside our listening
function, as we will not need it anywhere else:

```python
import pika
from workshop_helper import make_connection

queue_name = 'chat'

connection = make_connection()

channel = connection.channel()
channel.queue_bind(queue=queue_name)

def send(chan, routing_key, message):
    chan.basic_publish(
        queue=queue_name,
        routing_key=routing_key,
        body=message,
    )

def listen(chan):
    def on_message(channel, method, properties, body):
        print(' ['+ method.routing_key +']' + body)
```

This doesn't do anything by itself, so next we'll provide this as a callback
when we call `basic_consume`, which was our goal all along:
```python
import pika
from workshop_helper import make_connection

queue_name = 'chat'

connection = make_connection()

channel = connection.channel()
channel.queue_bind(queue=queue_name)

def send(chan, routing_key, message):
    chan.basic_publish(
        queue=queue_name,
        routing_key=routing_key,
        body=message,
    )

def listen(chan):
    def on_message(channel, method, properties, body):
        print(' ['+ method.routing_key +']' + body)

    chan.basic_consume(
        queue=queue_name,
        on_message_callback=on_message,
        auto_ack=True,
    )

    chan.start_consuming()
```
Finally, we `start_consuming` on the channel. This will steal program execution
-- what's known as 'blocking' -- and we will not be able to stop execution
other than by sending an interrupt signal. On most terminals and operating
systems, we do this by pressing Ctrl-C.

We can try this out by opening a second terminal window (which will generally
be useful from now on), running `conda activate` if you are using Anaconda to
manage your Python path, and then running another interpreter in a separate
window with the `python` command. Just like before, we can import and then
manually call the functions we've defined:
```python
from workshop import channel, listen

listen(channel)
```
Notice how this blocks the process; we can't write new Python expressions until
this one is done. If we switch back to our first terminal window, we can try
sending some messages. At this point, we'll notice that not everyone's message
streams look the same. Some people might be getting messages, but each message
will only go to one person! This is not a bug, but a core aspect of how an AMQP
queue works -- you take a letter out of the mailbox, and it will no longer be
in the mailbox. This is useful for some applications, but not for a chat
program.

We can manually interrupt execution with Ctrl-C here, and let's continue by
looking at _exchanges_.


## Step 7. Exchanges
So if all we can send is a letter, and we can't just read a letter at the
mailbox (we have to take it out), how should we make it so our messages get
sent to everyone? One solution would be to pick a letter, read it, and then
send it back. This has some downsides though, such as that our multiple people
listening have to read the letter one by one, first person A has to read it,
then person B, et cetera, and if we're dealing with a chat room with maybe 300
people, this would obviously cause problems down the line. Another issue is
that we would have to trust our clients to send the message back once they have
read it. This would mean a client losing their internet connection could cause
half the connected clients to also lose that message.

The way you solve this in the AMQP world is similar to how newspapers work in
the physical mail system. Instead of sending indiviual letters to one giant
mailbox, we give each client their own mailbox, with its own address. Stepping
down from the metaphor, we make every client create their own auto-generated
queue. This underpins _exchanges_. An exchange in our metaphor world would be
the newspaper office. Our clients can consume by "subscribing to the newspaper"
. When someone publishes a new edition to the newspaper, it goes to the
printers and they make a copy of it for everyone with a subscription, and then
sends it to each of their mailboxes.  This type of behavior for an AMQP
exchange is known as "fanout", one message goes in and it "fans out" to several
queues.

[SLIDE: Diagram of how fanout exchanges work]

### Using exchanges
We can convert our code to using exchanges by changing how we publish and
consume messages. To do this, we can change how we bind our channel. Instead of
binding to a queue like we've been doing so far, we can bind to an exchange
instead of a queue. The Pika way of doing this involves 3 steps:

First, we declare the exchange. A declaration in this context is a statement of
how the "world" should be. We provide an exchange name and a specification of
its settings. If no exchange with that name exists, it will be created. If one
does exist, it does nothing if its settings match the specification, and fails
with an error if it exists but is different. This is a useful pattern, as if we
try to use the same exchange with two different programs in two different ways,
we've generally made a mistake, e.g. by naming collisions between different
exchanges. We'll name our exchange `'broadcast_chat'`. The one setting we will
assert is that it should be a 'fanout' exchange, the previously described
behavior where every published message gets copied to every consumer.
```python
channel.exchange_declare(exchange='broadcast_chat', exchange_type='fanout')
```

Now that we've got some code that ensures that the newspaper office exists, the
second step is to ask for a mailbox.  We can provide an empty queue name, which
doesn't mean we won't have a queue name -- if the empty string is provided the
server will provide us with a unique, automatically generated name. To prevent
old queues from littering our server, we'll also declare it as `exclusive`,
which tells the server to delete the queue when we disconnect, as well as that
no other client is allowed to use this queue. This is fine, because it was
automatically generated anyway.
```python
channel.exchange_declare(exchange='broadcast_chat')

queue_declaration_result = channel.queue_declare(queue='', exclusive=True)
queue_name = queue_declaration_result.method.queue
```

Finally, we have an exchange and a queue, but they aren't connected in any way,
the little line between the exchange and the queues is missing.  We have a
mailbox and a newspaper office exists, but now we need to actually subscribe to
their updates. We need some way to say "this queue should receive messages from
this exchange, according to the rules of that exchange". This is called
_binding_ our queue to an exchange, which we can do with the queue_bind function.
```python
channel.exchange_declare(exchange='broadcast_chat')

queue_declaration_result = channel.queue_declare(queue='', exclusive=True)
queue_name = queue_declaration_result.method.queue

channel.queue_bind(queue=queue_name, exchange='broadcast_chat')
```

If you're feeling confused and/or not keeping up, that's fine. This is the
trickiest part of this workshop by far -- but that means everything from here
on out is pretty much smooth sailing.

The actual changes we need to make to our sending and receiving functions are
really minimal here. `listen` already uses the `queue_name` -- it needs zero
changes to work with this new model. The only change we need to make is to our
`send` function, which will now pass an `exchange` to the `basic_publish`
function, rather than a `queue`:
```python
import pika
from workshop_helper import make_connection

exchange_name = 'broadcast_chat'

connection = make_connection()

channel = connection.channel()

channel.exchange_declare(exchange='broadcast_chat', exchange_type="fanout")

queue_declaration_result = channel.queue_declare(queue='', exclusive=True)
queue_name = queue_declaration_result.method.queue

channel.queue_bind(queue=queue_name, exchange=exchange_name)

def send(chan, routing_key, message):
    chan.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        body=message,
    )

def listen(chan):
    def on_message(channel, method, properties, body):
        print(' ['+ method.routing_key +']' + body)

    chan.basic_consume(
        queue=queue_name,
        on_message_callback=on_message,
        auto_ack=True,
    )

    chan.start_consuming()
```

(this is maybe where time starts to run short? we'll see after I do a top-to
bottom trial run)
## Step 8. Making it more interactive
Now, just an importable file you have to manually call functions from isn't
much of a chat application. Now that we have our core communications foundation
set up, we can put our own spin on it. A nice format would be a file that you
can just run, and then either get to write messages or read them.

We'll start with the simplest script, which is one that just runs our `listen`
function with some set of arguments. We'll print a nice little line at startup,
so we give some feedback when the program is running, and then just print
messages as they arrive. We can name this `listen.py`:
```python
from workshop import channel, exchange_name, queue_name, listen

print('Listening on <' + exchange_name + '>, queue name ' + queue_name)

listen(channel)
```

Next, we can make our `send.py`. This is a bit more involved. What we noticed
before is that when we're using a fanout exchange the way we do currenly, we're
not really using the routing key for anything. We can decide that we use this
for user (nick)names now, as we are already using the AMQP protocol far outside
its normal parameters.

First, we'll need to prompt the user for a name. We can do this with another
built-in function, called `input`, which we can also provide with a prompt.
Let's try saving the user's name to a variable, and then greeting them:
```python
name = input('Enter your name: ')

print('Hello, ' + name)
```

So we can prompt for the user's name, now we obviously want them to be able to
write messages too. This should be done repeatedly, which we can do with a
loop:
```python
name = input('Enter your name: ')

for _ in range(5):
    message = input('> ')
    print(name + ' says: "' + message + '"')
```

Five messages is very arbitrary, we would prefer if the loop ran forever, until
we gave some instruction to exit. We can imitate this with a very long `for`
loop, but we can also do it with a `while` loop. `while` is a bit like a `for`
loop, except if instead of running over a set of elements, we run until a
condition (like in an `if` statement) is not empty. If we provide `False`, it
will never run, and if we provide `True`, it will run forever. `while True` is
a common pattern, because we can manually stop execution from inside the loop
with the `break` statement. A `while True` **must** break somewhere, otherwise
it will run forever.
```python
name = input('Enter your name: ')

print('')
print('Welcome to our chat space, type "exit" or "quit" when you want to leave.')
while True:
    message = input('> ')
    if message == 'exit' or message == 'quit':
        print('Goodbye!')
        break

    print(name + ' says: "' + message + '"')
```

Finally, we're ready to hook everything up to work together! If we just hook
our `send.py` up to actually send messages when we type, we should be ready to
talk to each other! Once again, we'll provide our user names as the routing
key, since by a happy coincidence we were printing it in the
`on_message_callback` we wrote earlier, so it sort of looks like a user name if
we squint.
```python
from workshop import send, channel

name = input('Enter your name: ')

print('')
print('Welcome to our chat space, type "exit" or "quit" when you want to leave.')
while True:
    message = input(name + ' > ')
    if message == 'exit' or message == 'quit':
        print('Goodbye!')
        break

    send(channel, name, message)
```

Let's grab our two terminal windows and start each file in one of them, and try
it out in action!


## Wrap-up
(FIXME: come up with some nice closing words here, or just wing it again. I
believe in you (me))
