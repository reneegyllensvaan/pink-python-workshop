from completed import send, channel

name = input('Enter your name: ')

print('')
print('Welcome to our chat space, type "exit" or "quit" when you want to leave.')
while True:
    message = input(name + ' > ')
    if message == 'exit' or message == 'quit':
        print('Goodbye!')
        break

    send(channel, name, message)
